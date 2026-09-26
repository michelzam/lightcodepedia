"""A Databricks warehouse behind a same-origin proxy, stubbed: POST answers
PENDING with a statement id, the first GET answers SUCCEEDED with the rows
from the table, and every request records the Authorization it carried."""
import json
import re
from behave import given, when, then
from playwright.sync_api import expect


@given('a Databricks warehouse behind "{host}" that answers after one poll with the rows')
def step_warehouse(context, host):
    heads = context.table.headings
    rows = [[r[h] for h in heads] for r in context.table]
    cols = [{"name": h, "type_name": "DOUBLE" if h.endswith("kusd") else "STRING"} for h in heads]
    context.dbx_calls = []
    context.dbx_refuse = False

    def statements(route, req):
        context.dbx_calls.append({"method": req.method, "url": req.url,
                                  "auth": req.headers.get("authorization", ""),
                                  "body": req.post_data})
        if context.dbx_refuse:
            route.fulfill(status=403, json={"message": "Invalid access token."})
            return
        if req.method == "POST":
            route.fulfill(json={"statement_id": "st-1", "status": {"state": "PENDING"}})
        else:
            route.fulfill(json={"statement_id": "st-1", "status": {"state": "SUCCEEDED"},
                                "manifest": {"schema": {"columns": cols}},
                                "result": {"data_array": rows}})

    context.page.route(re.compile(r".*" + re.escape(host) + r"/api/2\.0/sql/statements.*"), statements)


@given('a Databricks token "{tok}" on this device')
def step_token(context, tok):
    context.page.add_init_script("localStorage.setItem('lc_key_dbx', %s);" % json.dumps(tok))


@given("the warehouse refuses the token")
def step_refuse(context):
    context.dbx_refuse = True


@then('the grid "{gid}" shows {n:d} rows')
def step_grid_rows(context, gid, n):
    rows = context.page.locator('[data-lc-id="%s"] .ag-center-cols-container .ag-row, [data-lc-id="%s"] .lc-dg-table tbody tr' % (gid, gid))
    expect(rows).to_have_count(n, timeout=15_000)


@then('the bar of "{did}" reads "{text}"')
def step_bar_reads(context, did, text):
    expect(context.page.locator('[data-lc-dbx="%s"] .lc-dbx-status' % did)).to_contain_text(text, timeout=15_000)


@then('the bar of "{did}" asks for a token')
def step_bar_asks(context, did):
    bar = context.page.locator('[data-lc-dbx="%s"]' % did)
    expect(bar.locator(".lc-dbx-status")).to_contain_text("token", timeout=15_000)
    expect(bar.locator(".lc-dbx-token")).to_be_visible()


@when('I paste the Databricks token "{tok}" in the bar of "{did}"')
def step_paste(context, tok, did):
    bar = context.page.locator('[data-lc-dbx="%s"]' % did)
    bar.locator(".lc-dbx-token").fill(tok)
    bar.locator(".lc-dbx-save").click()


@then('the warehouse was asked with the token "{tok}" for "{wh}"')
def step_asked(context, tok, wh):
    context.page.wait_for_timeout(300)
    posts = [c for c in context.dbx_calls if c["method"] == "POST"]
    assert posts, "no statement was posted: %r" % context.dbx_calls
    body = json.loads(posts[-1]["body"])
    assert body["warehouse_id"] == wh, body
    assert "SELECT region" in body["statement"], body
    for c in context.dbx_calls:
        assert c["auth"] == "Bearer " + tok, "a call carried %r" % c["auth"]
    assert any(c["method"] == "GET" for c in context.dbx_calls), "the PENDING answer was never polled"


@then("the warehouse was not asked")
def step_not_asked(context):
    context.page.wait_for_timeout(500)
    assert not context.dbx_calls, context.dbx_calls


@then("the number columns arrived as numbers")
def step_numbers(context):
    kinds = context.page.evaluate("() => (window.lcDatasets.arr || []).map(r => typeof r.arr_kusd)")
    assert kinds == ["number", "number", "number"], kinds
