import json

from behave import given, then, when
from playwright.sync_api import expect

T = 20_000


@given("the AI answers as Rey and Chuck, Rey wrong the first time")
def step_stub_crew_ai(context):
    """Rey (the reader) says PAY first, then VISIT once Chuck's words come back;
    Chuck (the checker) disagrees with PAY and agrees with VISIT."""
    context.crew_asks = []

    def answer(route):
        body = json.loads(route.request.post_data or "{}")
        system = body["messages"][0]["content"]
        user = body["messages"][1]["content"]
        context.crew_asks.append({"system": system, "user": user})
        if "AGREE or DISAGREE" in system:
            text = "DISAGREE — no visit is booked for Biscuit" if "The verdict: PAY" in user else "AGREE — a visit first"
        else:
            text = "VERDICT: VISIT" if "disagreed" in user else "VERDICT: PAY"
        route.fulfill(status=200, content_type="application/json",
                      body=json.dumps({"choices": [{"message": {"content": text}}]}))
    context.page.route("**/chat/completions*", answer)


def _crew(context, cid):
    return context.page.locator(".lc-crew[data-lc-id='" + cid + "']")


@when('I press ▶ Run on the crew "{cid}"')
def step_run_crew(context, cid):
    btn = _crew(context, cid).locator(".lc-crew-run")
    expect(btn).to_be_enabled(timeout=T)
    btn.click()


@then('the crew "{cid}" is done')
def step_crew_done(context, cid):
    expect(_crew(context, cid)).to_have_attribute("data-state", "done", timeout=T)


def _rows(context, ds):
    return context.page.evaluate("id => (window.lcDatasets || {})[id] || []", ds)


@then('the crew "{cid}" sorted "{family}" as "{lane}" in {tries:d} tries')
def step_crew_sorted(context, cid, family, lane, tries):
    rows = [r for r in _rows(context, cid + ".sorted") if r.get("family") == family]
    assert rows, "no lane for %s in %r" % (family, _rows(context, cid + ".sorted"))
    assert rows[0]["lane"] == lane and int(rows[0]["tries"]) == tries, rows[0]


@then('the crew "{cid}" asked the AI {n:d} times')
def step_crew_asks(context, cid, n):
    got = int(_crew(context, cid).get_attribute("data-asks") or 0)
    assert got == n, "%d AI asks, expected %d" % (got, n)


@then('the crew\'s log shows "{who}" saying "{text}"')
def step_crew_log(context, who, text):
    rows = _rows(context, "desk.log")
    assert any(r.get("who") == who and text in str(r.get("out")) for r in rows), rows


@then("Rey's second ask carried Chuck's words")
def step_second_ask(context):
    reads = [a for a in context.crew_asks if "AGREE or DISAGREE" not in a["system"]]
    assert len(reads) == 2, reads
    assert "no visit is booked" in reads[1]["user"], reads[1]["user"]


