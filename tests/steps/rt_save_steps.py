import base64
import json

from behave import given, when, then
from playwright.sync_api import expect

# The two-repo contract (save="my/…"): the page renders from the AUTHOR's
# repo (acme/demo, stubbed by the shared contents-API step), the learner's
# work reads/writes THEIR bench (stub/bench). These steps stub the bench
# side and record every write, so the scenarios can assert not just that a
# save happened, but WHICH repo received it — the whole point of the design.

BENCH = "stub/bench"


def _stub_bench(context, files):
    """Route the bench repo's contents API: GET serves `files`, PUT records."""
    context.bench_commits = []
    context.author_commits = []

    def bench(route, req):
        path = req.url.split("/contents/", 1)[1].split("?")[0]
        if req.method == "GET":
            if path in files:
                route.fulfill(json={
                    "content": base64.b64encode(files[path].encode()).decode(),
                    "sha": "bench-sha-1",
                })
            else:
                route.fulfill(status=404, json={"message": "Not Found"})
        elif req.method == "PUT":
            body = json.loads(req.post_data)
            context.bench_commits.append({
                "path": path,
                "text": base64.b64decode(body.get("content", "")).decode(),
            })
            route.fulfill(json={"content": {"sha": "bench-sha-2"}})
        else:
            route.continue_()

    def author_put(route, req):
        # the author's repo must never see a write from a learner page.
        # GETs fall back to the earlier stub that serves the page document —
        # continue_() would go to the real network instead.
        if req.method == "PUT":
            context.author_commits.append(req.url)
            route.fulfill(status=403, json={"message": "forbidden"})
        else:
            route.fallback()

    context.page.route("https://api.github.com/repos/" + BENCH + "/contents/**", bench)
    context.page.route("https://api.github.com/repos/acme/demo-vault/contents/**", author_put)
    context.page.add_init_script(
        "localStorage.setItem('lc_ed_pat', 'ghp_stub');"
        "localStorage.setItem('lc_ed_repo', '" + BENCH + "');"
    )


@given('a connected bench whose "{path}" does not exist yet')
def step_bench_empty(context, path):
    _stub_bench(context, {})


@given('a connected bench whose "{path}" holds "{text}"')
def step_bench_with(context, path, text):
    _stub_bench(context, {path: text.replace("\\n", "\n")})


@then("the pad shows the author's starter")
def step_pad_starter(context):
    ta = context.page.locator(".lc-mdpad-in").first
    expect(ta).to_be_visible(timeout=15_000)
    expect(ta).to_have_value("# Starter résumé — replace me", timeout=10_000)


@then('the pad shows "{text}"')
def step_pad_shows(context, text):
    expect(context.page.locator(".lc-mdpad-in").first).to_have_value(
        text, timeout=10_000
    )


@then("the pad's save button is disabled with a join hint")
def step_pad_save_disabled(context):
    btn = context.page.locator(".lc-mdpad-save").first
    expect(btn).to_be_visible(timeout=10_000)
    expect(btn).to_be_disabled()
    assert "join" in (btn.get_attribute("title") or "").lower(), \
        "disabled without saying why: %r" % btn.get_attribute("title")


@then("the pad is marked as the reader's own")
def step_pad_mine(context):
    expect(context.page.locator(".lc-mdpad[data-lc-mine='1']").first) \
        .to_be_visible(timeout=10_000)
    expect(context.page.locator(".lc-mdpad-mine").first).to_be_visible()


@then("the pad is not marked as the reader's own")
def step_pad_not_mine(context):
    context.page.wait_for_timeout(800)   # give a (wrong) override time to land
    assert context.page.locator(".lc-mdpad[data-lc-mine='1']").count() == 0


@when('I type "{text}" into the pad and save')
def step_type_and_save(context, text):
    ta = context.page.locator(".lc-mdpad-in").first
    ta.wait_for(state="visible", timeout=15_000)
    ta.fill(text)
    btn = context.page.locator(".lc-mdpad-save").first
    expect(btn).to_be_enabled(timeout=10_000)
    btn.click()
    context.page.wait_for_timeout(800)


@when("I press the pad's start-over button")
def step_pad_reset(context):
    btn = context.page.locator(".lc-mdpad-reset").first
    btn.wait_for(state="visible", timeout=15_000)
    btn.click()
    context.page.wait_for_timeout(400)


@then('the bench received a commit to "{path}" containing "{text}"')
def step_bench_commit(context, path, text):
    hits = [c for c in context.bench_commits if c["path"] == path]
    assert hits, "no commit to %s — bench saw: %r" % (
        path, [c["path"] for c in context.bench_commits])
    assert text in hits[-1]["text"], hits[-1]["text"][:400]


@then("the bench received no commit")
def step_bench_no_commit(context):
    assert not context.bench_commits, context.bench_commits


@then("the author's repo received no commit")
def step_author_untouched(context):
    assert not context.author_commits, context.author_commits


@then('the dogs grid shows "{text}"')
def step_grid_shows(context, text):
    cell = context.page.locator(".lc-datagrid .ag-cell", has_text=text).first
    expect(cell).to_be_visible(timeout=20_000)


@then("the grid is marked as the reader's own")
def step_grid_mine(context):
    expect(context.page.locator(".lc-datagrid[data-lc-mine='1']").first) \
        .to_be_visible(timeout=10_000)
    expect(context.page.locator(".lc-dg-mine").first).to_be_visible()


@when("I press the grid's keep button")
def step_grid_keep(context):
    btn = context.page.locator(".lc-dg-save").first
    btn.wait_for(state="visible", timeout=20_000)
    expect(btn).to_be_enabled(timeout=10_000)
    btn.click()
    context.page.wait_for_timeout(800)


@when('the dataset "{name}" is repaired elsewhere')
def step_repair_dataset(context, name):
    # a repair arriving from ANYWHERE upstream — an edit, a query recompute,
    # a saved copy landing. The derived view must follow it either way.
    context.page.wait_for_selector(".lc-datagrid .ag-cell", timeout=20_000)
    context.page.evaluate(
        """(id) => {
             const rows = (window.lcDatasets[id] || []).map(
               r => Object.assign({}, r, { campus: 'Milwaukee' }));
             window.lcSetDataset(id, rows);
           }""",
        name,
    )
    context.page.wait_for_timeout(700)


@then('no grid cell still shows "{text}"')
def step_no_stale_cell(context, text):
    stale = context.page.evaluate(
        """(t) => Array.from(document.querySelectorAll('.lc-datagrid .ag-cell'))
                   .filter(c => (c.textContent || '').trim() === t).length""",
        text,
    )
    assert stale == 0, "%d cell(s) still showing the stale value %r" % (stale, text)


@then('the dataset "{name}" now reads "{text}"')
def step_dataset_reads(context, name, text):
    got = context.page.evaluate(
        "(id) => JSON.stringify(window.lcDatasets[id] || [])", name
    )
    assert text in got, "dataset %s does not carry %r: %s" % (name, text, got[:300])


@given('a learner connected to bench "{bench}" reading the class hub "{other}"')
def step_bench_vs_connected(context, bench, other):
    # the Canvas shape: ONE hub url framed for the whole class, each
    # learner connected to their own bench. Both repos record their
    # writes, so the assertion can say where the work actually landed.
    import base64 as _b64
    import json as _json
    context.bench_commits = []
    context.other_commits = []

    def record(bucket):
        def handler(route, req):
            path = req.url.split("/contents/", 1)[1].split("?")[0]
            if req.method == "PUT":
                body = _json.loads(req.post_data)
                bucket.append({
                    "path": path,
                    "text": _b64.b64decode(body.get("content", "")).decode(),
                })
                route.fulfill(json={"content": {"sha": "sha-x"}})
            elif req.method == "GET" and "/contents/my/" in req.url:
                route.fulfill(status=404, json={"message": "Not Found"})
            else:
                route.fallback()   # the earlier stub serves the document
        return handler

    context.page.route("https://api.github.com/repos/" + bench + "/contents/**",
                       record(context.bench_commits))
    context.page.route("https://api.github.com/repos/" + other + "/contents/**",
                       record(context.other_commits))
    context.page.add_init_script(
        "localStorage.setItem('lc_ed_pat', 'ghp_stub');"
        "localStorage.setItem('lc_ed_repo', '" + bench + "');"
    )


@then('the repo "{repo}" received no commit')
def step_other_untouched(context, repo):
    assert not context.other_commits, context.other_commits


@when("I open a cell editor in the dogs grid")
def step_open_cell_editor(context):
    cell = context.page.locator(".lc-datagrid .ag-cell").first
    cell.wait_for(state="visible", timeout=20_000)
    cell.dblclick()
    context.page.wait_for_selector('.lc-datagrid input[type="text"]', timeout=10_000)


@then("the cell editor refuses autofill")
def step_editor_refuses_autofill(context):
    attrs = context.page.evaluate(
        """() => {
          const i = document.querySelector('.lc-datagrid input[type=\"text\"]');
          return i && { ac: i.getAttribute('autocomplete'),
                        name: i.getAttribute('name'),
                        lp: i.getAttribute('data-lpignore') };
        }"""
    )
    assert attrs, "no editor input found"
    assert attrs["ac"] == "off" and attrs["name"] == "lc-cell" and attrs["lp"] == "true", attrs
