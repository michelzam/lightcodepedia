import re
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
                "message": body.get("message", ""),
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
    # trailing newline: a file ends with one, the pad does not add one, and
    # it is not a difference the learner can see — compare what is readable
    loc = context.page.locator(".lc-mdpad-in").first
    expect(loc).not_to_have_value("", timeout=10_000)
    got = (loc.input_value() or "").strip()
    assert got == text.strip(), "pad holds %r, expected %r" % (got, text)


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


@given('the bench remembers two earlier versions of "{path}"')
def step_bench_history(context, path):
    # the commit list and the by-ref reads that back it — the shape the
    # GitHub API answers with, so the panel exercises the real contract
    # a version's content follows the FILE's kind — prose for a pad, rows
    # for a grid — so each component's diff reads real data of its own shape
    if path.endswith((".yaml", ".yml", ".json")):
        VERSIONS = {"sha-old": "- name: Rex\n  campus: Milwauke\n",
                    "sha-mid": "- name: Rex\n  campus: MKE\n"}
    else:
        VERSIONS = {"sha-old": "# Draft one\n", "sha-mid": "# Draft two\n"}

    def commits(route, req):
        route.fulfill(json=[
            {"sha": "sha-mid",
             "commit": {"author": {"date": "2026-08-02T09:00:00Z"},
                        "message": "\u270d\ufe0f cv"}},
            {"sha": "sha-old",
             "commit": {"author": {"date": "2026-08-01T09:00:00Z"},
                        "message": "\u270d\ufe0f cv"}},
        ])

    def at_ref(route, req):
        for sha, text in VERSIONS.items():
            if "ref=" + sha in req.url:
                route.fulfill(status=200, content_type="text/plain", body=text)
                return
        route.fallback()

    context.page.route("https://api.github.com/repos/" + BENCH + "/commits*", commits)
    # REGEX, not a glob. Playwright compiles "contents/**?ref=*" down to
    # "contents/([^/]*).ref=([^/]*)" — the ** collapses to single-star,
    # no-slash semantics once a ? follows it, so it could never match a path
    # with a folder in it. This route silently never fired: the plain
    # contents/** stub answered instead, with the CURRENT file's JSON
    # envelope, and three scenarios have been failing on that ever since —
    # the pad "restored" a version by displaying {"content": "…"} verbatim,
    # and the grid diffed its live rows against that same envelope, so every
    # row read as added and no was/now pair could exist. The engine was
    # right throughout: readAt asks for ?ref= with Accept: raw, which is
    # exactly what GitHub answers with.
    context.page.route(
        re.compile(r"https://api\.github\.com/repos/" + re.escape(BENCH)
                   + r"/contents/.*[?&]ref="),
        at_ref)


@when("I open the pad's version list")
def step_open_versions(context):
    btn = context.page.locator(".lc-mdpad-bar .lc-ver-btn").first
    expect(btn).to_be_visible(timeout=15_000)
    btn.click()
    context.page.wait_for_selector(".lc-ver-panel li", timeout=10_000)


@then("the list shows {n:d} saved versions")
def step_version_count(context, n):
    expect(context.page.locator(".lc-ver-panel li")).to_have_count(n, timeout=10_000)


@when("I compare the oldest version")
def step_compare_oldest(context):
    context.page.locator(".lc-ver-panel li").last.locator(
        "button", has_text="compare").click()
    context.page.wait_for_timeout(700)


@then("the difference is shown line by line")
def step_diff_shown(context):
    box = context.page.locator(".lc-ver-diff")
    expect(box).to_be_visible(timeout=10_000)
    assert box.locator(".del").count() > 0, "no removed line marked"
    assert box.locator(".add").count() > 0, "no added line marked"


@when("I bring back the oldest version")
def step_bring_back(context):
    context.page.locator(".lc-ver-panel li").last.locator(
        "button", has_text="bring back").click()
    context.page.wait_for_timeout(800)


@when("I open the grid's version list")
def step_open_grid_versions(context):
    btn = context.page.locator(".lc-dg-savebar .lc-ver-btn").first
    expect(btn).to_be_visible(timeout=20_000)
    btn.click()
    context.page.wait_for_selector(".lc-ver-panel li", timeout=10_000)


@when('I type "{text}" into a grid cell without leaving it')
def step_type_cell_open(context, text):
    # deliberately NO Enter, NO Tab, no click elsewhere — the editor stays
    # open, which is the state that used to lose the change
    cell = context.page.locator(".lc-datagrid .ag-cell").nth(1)
    cell.wait_for(state="visible", timeout=20_000)
    cell.dblclick()
    inp = context.page.locator('.lc-datagrid input[type="text"]').first
    inp.wait_for(state="visible", timeout=10_000)
    inp.fill(text)


@then("the difference is a grid showing only the changed rows")
def step_diff_is_grid(context):
    box = context.page.locator(".lc-ver-diff")
    expect(box).to_be_visible(timeout=15_000)
    grid = box.locator(".lc-datagrid")
    expect(grid).to_be_visible(timeout=15_000)
    cells = box.locator(".ag-cell")
    expect(cells.first).to_be_visible(timeout=15_000)
    txt = box.inner_text()
    assert "was" in txt and "now" in txt, "no was/now pair in the difference: %s" % txt[:200]


@then('the bench received {n:d} commits to "{path}"')
def step_commit_count(context, n, path):
    hits = [c for c in context.bench_commits if c["path"] == path]
    assert len(hits) == n, "expected %d commit(s) to %s, saw %d: %r" % (
        n, path, len(hits), [c["text"][:30] for c in hits])
    context.lc_hits = hits


@then("the first of them is the lesson's starter")
def step_first_is_starter(context):
    first = context.lc_hits[0]
    assert "Starter" in first["text"] or "starter" in first["text"], \
        "the first commit is not the author's seed: %r" % first["text"][:80]
    assert first.get("message", "").startswith("\U0001f4c4 starter"), \
        "the starter commit is not labelled as one: %r" % first.get("message")


@then('the last of them holds "{text}"')
def step_last_holds(context, text):
    assert text in context.lc_hits[-1]["text"], context.lc_hits[-1]["text"][:120]


@given('the bench remembers a starter and a change for "{path}"')
def step_history_with_starter(context, path):
    def commits(route, req):
        route.fulfill(json=[
            {"sha": "sha-mine",
             "commit": {"author": {"date": "2026-08-02T09:00:00Z"},
                        "message": "\u270d\ufe0f cv"}},
            {"sha": "sha-seed",
             "commit": {"author": {"date": "2026-08-01T09:00:00Z"},
                        "message": "\U0001f4c4 starter — before my first change"}},
        ])
    context.page.route("https://api.github.com/repos/" + BENCH + "/commits*", commits)


@then("the oldest version is labelled as the lesson's starter")
def step_starter_labelled(context):
    last = context.page.locator(".lc-ver-panel li").last
    expect(last).to_contain_text("starter", timeout=10_000)
    assert "starter" in (last.get_attribute("class") or ""), \
        "the starter row is not marked apart from the learner's own versions"


@then("the changed value is marked red where it was and green where it is")
def step_values_coloured(context):
    box = context.page.locator(".lc-ver-diff")
    expect(box.locator(".ag-cell.lc-dg-was").first).to_be_visible(timeout=15_000)
    expect(box.locator(".ag-cell.lc-dg-now").first).to_be_visible(timeout=10_000)


@then("the slot shows the lesson's seed")
def step_slot_seed(context):
    slot = context.page.locator(".lc-bench-slot").first
    expect(slot).to_contain_text("Wire me", timeout=15_000)


@then('the slot shows "{text}"')
def step_slot_shows(context, text):
    expect(context.page.locator(".lc-bench-slot").first).to_contain_text(
        text, timeout=15_000)


@then('the slot commits to "{path}"')
def step_slot_target(context, path):
    # the whole trick: the region is its OWN source, so the editor's
    # closest() lands on the bench instead of the read-only lesson
    slot = context.page.locator(".lc-bench-slot").first
    expect(slot).to_have_attribute("data-lc-src-path", path, timeout=10_000)
    repo = slot.get_attribute("data-lc-src-repo")
    assert repo == BENCH, "the slot points at %r, not the learner's bench" % repo


@then("the slot is marked as the reader's own")
def step_slot_mine(context):
    expect(context.page.locator(".lc-bench-slot[data-lc-mine='1']").first
           ).to_be_visible(timeout=15_000)


@given('the signed-in learner is "{login}"')
def step_signed_in(context, login):
    """The topbar caches the account; the bench stripe reads it from there."""
    context.page.add_init_script(
        "localStorage.setItem('lc_gh_user', JSON.stringify(%s))"
        % json.dumps({"login": login, "avatar_url": ""})
    )


@then('the slot\'s stripe names "{who}"')
def step_stripe_who(context, who):
    expect(context.page.locator(".lc-bench-head .lc-bench-who").first).to_have_text(
        who, timeout=15_000
    )


@then("the slot's stripe says it is still the lesson's copy")
def step_stripe_seed(context):
    expect(context.page.locator(".lc-bench-head .lc-bench-seed").first).to_be_visible(
        timeout=15_000
    )


@then('the slot is in the "{state}" state')
def step_slot_state(context, state):
    slot = context.page.locator(".lc-bench-slot").first
    expect(slot).to_have_attribute("data-state", state, timeout=15_000)


@when("the lesson's check on the slot passes")
def step_marker_passes(context):
    """The runner's own path: a settled status announces itself on the bus."""
    context.page.evaluate(
        """() => { const f = document.querySelector('.lc-feature[data-grades]');
                   f.setAttribute('data-status', 'passing');
                   document.dispatchEvent(new CustomEvent('lc-model-changed')); }"""
    )
    context.page.wait_for_timeout(400)


@then('the slot offers "{label}"')
def step_slot_save_button(context, label):
    b = context.page.locator(".lc-bench-save").first
    expect(b).to_be_visible(timeout=15_000)
    expect(b).to_contain_text(label.replace("💾 ", ""))


@when("I open the slot's menu")
def step_open_slot_menu(context):
    btn = context.page.locator(".lc-bench-more").first
    btn.wait_for(state="visible", timeout=15_000)
    btn.click()
    context.page.wait_for_selector(".lc-bench-menu", timeout=5_000)


@then('"{label}" is offered')
def step_menu_enabled(context, label):
    b = context.page.locator(".lc-bench-menu button", has_text=label).first
    expect(b).to_be_enabled(timeout=5_000)


@then('"{label}" is greyed out')
def step_menu_disabled(context, label):
    b = context.page.locator(".lc-bench-menu button", has_text=label).first
    expect(b).to_be_disabled(timeout=5_000)
