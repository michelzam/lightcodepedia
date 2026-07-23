import re
from behave import when, then
from playwright.sync_api import expect


@when('I open the runner page on "{src}"')
def step_open_runner(context, src):
    context.page.goto(context.base_url + "/run#src=" + src, wait_until="domcontentloaded")


@when("I wait for the runner to render")
def step_wait_render(context):
    # the status note hides when the render pipeline completes
    context.page.wait_for_selector(".lc-runner .lc-run-status", state="hidden", timeout=20_000)
    context.page.wait_for_timeout(400)


@then('the runner shows a heading "{text}"')
def step_heading(context, text):
    expect(context.page.locator("#lc-run h1", has_text=text)).to_be_visible()


@then("the runner shows bold text")
def step_bold(context):
    expect(context.page.locator("#lc-run strong").first).to_be_visible()


@then('the runner contains a "{sel}" element')
def step_contains(context, sel):
    expect(context.page.locator("#lc-run " + sel).first).to_be_visible(timeout=10_000)


@then('the rendered block mentions "{text}"')
def step_block_text(context, text):
    assert text in context.page.locator("#lc-run .lc-block").first.inner_text()


@then("the runner reports it could not load")
def step_error(context):
    # the status is visible immediately ("Loading…"); wait for the fetch to
    # actually 404 and the message to change — on a deployed CDN the round-trip
    # is not instant, so asserting on visibility alone races (was flaky red)
    status = context.page.locator(".lc-runner .lc-run-status")
    expect(status).to_contain_text(
        re.compile("could not load|is private", re.I), timeout=15_000
    )


@then("a rendered component carries an editable source snapshot")
def step_rt_snapshot(context):
    # the runner auto-ids fences and snapshots them pre-upgrade, so xray edits
    # the verbatim markdown source (backticks intact), not the rendered text
    got = context.page.evaluate(
        """() => {
          var el = document.querySelector('#lc-run [data-lc-id]');
          if (!el) return { ok: false, why: 'no data-lc-id wrapper' };
          var snap = window.lcSourceOf && window.lcSourceOf(el.getAttribute('data-lc-id'));
          return { ok: !!snap && snap.indexOf('Lucky') >= 0, why: (snap || '').slice(0, 60) };
        }"""
    )
    assert got["ok"], got["why"]


@then("footnote refs and their definitions render, none left raw")
def step_rt_footnotes(context):
    # marked has no footnote syntax; the client pipeline (lcClientFootnotes)
    # must emit the kramdown shape — datagrid.md has 3 live refs, one nested
    # inside another definition's body
    got = context.page.evaluate(
        """() => ({
          sups: document.querySelectorAll('#lc-run sup[id^=fnref] a.footnote').length,
          notes: document.querySelectorAll('#lc-run div.footnotes li[id^=fn]').length,
          raw: document.getElementById('lc-run').innerText.match(/\\[\\^[^\\]]+\\]:/g) || []
        })"""
    )
    assert got["sups"] >= 3 and got["notes"] >= 3 and not got["raw"], got


# ── the ownership bar (course/ ↔ my/ convention on benches) ────────────

import base64

BENCH_REPO = "zam-academy/build-ai-x-stu"
BENCH_MD = "# Exercise 1\n\nSolve it your way.\n\n[Back to the bench](../index.md)\n"


def _bench_route(context):
    st = context.bench_stub

    def envelope():
        return {"content": base64.b64encode(BENCH_MD.encode()).decode(),
                "encoding": "base64", "sha": st["orig_sha"]}

    def handler(route):
        req = route.request
        url, method = req.url, req.method
        raw = "raw" in (req.headers.get("accept") or "")
        if "/contents/index.md" in url and method == "GET":
            route.fulfill(status=200, content_type="text/plain",
                          body="# Bench\n\n[Exercise 1](course/ex1.md)\n")
            return
        if "/contents/course/ex1.md" in url and method == "GET":
            if raw:
                route.fulfill(status=200, content_type="text/plain", body=BENCH_MD)
            else:
                route.fulfill(status=200, json=envelope())
            return
        if "/contents/my/ex1.md" in url and method == "PUT":
            st["puts"].append(url)
            st["mine"] = True
            route.fulfill(status=201, json={"content": {"sha": "copy"}})
            return
        if "/contents/my/ex1.md" in url and method == "GET":
            if not st.get("mine"):
                route.fulfill(status=404, json={"message": "Not Found"})
            elif raw:
                route.fulfill(status=200, content_type="text/plain", body=BENCH_MD)
            else:
                route.fulfill(status=200, json=envelope())
            return
        # a bench page carrying a BARE {: .folder } — no path, no open knob
        if "/contents/shelf.md" in url and method == "GET":
            route.fulfill(status=200, content_type="text/plain",
                          body="# Shelf\n\n[in this folder](#)\n{: .folder }\n")
            return
        # the current-folder listing a bare {: .folder } enumerates (bench root)
        if url.split("?")[0].endswith("/contents/") and method == "GET":
            route.fulfill(status=200, json=[
                {"name": "lesson_a.md", "path": "lesson_a.md", "type": "file"},
                {"name": "index.md", "path": "index.md", "type": "file"},
            ])
            return
        if "/contents/menu.md" in url and method == "GET":
            if st.get("menu"):
                route.fulfill(status=200, content_type="text/plain",
                              body="[🛠 My bench](index.md) [🎓 Course](/courses/join)")
            else:
                route.fulfill(status=404, json={"message": "Not Found"})
            return
        route.fulfill(status=404, json={"message": "stub"})

    context.page.route("https://api.github.com/**", handler)


@given("a stubbed bench with a course page")
def step_stub_bench(context):
    context.bench_stub = {"orig_sha": "sha-orig", "puts": []}


@given("my copy exists from an older original")
def step_stub_stale_copy(context):
    context.bench_stub["mine"] = True
    context.bench_seed_old_sha = True


@when('I open the bench page "{path}"')
def step_open_bench_page(context, path):
    _bench_route(context)
    context.page.add_init_script("localStorage.setItem('lc_ed_pat','ghp_stu');")
    if getattr(context, "bench_seed_old_sha", False):
        context.page.add_init_script(
            "localStorage.setItem('lc_orig_sha:%s/my/ex1.md','sha-old');" % BENCH_REPO)
    context.page.goto(context.base_url + "/run#src=gh:" + BENCH_REPO + "/" + path,
                      wait_until="domcontentloaded")
    context.page.wait_for_selector(".lc-runner .lc-run-status", state="hidden", timeout=20_000)


@then('the runner bar names the source "{text}"')
def step_bar_names(context, text):
    expect(context.page.locator(".lc-run-bar")).to_contain_text(text, timeout=8000)


@then("the runner page title is hidden")
def step_title_hidden(context):
    expect(context.page.locator("h1", has_text="Runner").first).to_be_hidden()


@given("the bench ships a menu")
def step_bench_has_menu(context):
    context.bench_stub["menu"] = True


@then("the topbar switches to bench mode")
def step_topbar_bench_mode(context):
    expect(context.page.locator("#lc-topbar")).to_have_class(
        __import__("re").compile(r"\blc-bench-mode\b"), timeout=8000)
    expect(context.page.locator("#lc-topbar .lc-brand")).to_contain_text("Build Ai X Stu")
    # the full repo name lives in the brand tooltip; the rendered file in the bar
    assert BENCH_REPO in (context.page.locator("#lc-topbar .lc-brand").get_attribute("title") or "")
    # 🏠 home is always in reach, pointing at the bench README
    expect(context.page.locator("#lc-topbar .lc-bench-home")).to_be_visible()
    expect(context.page.locator("#lc-topbar .lc-bench-file")).to_contain_text("ex1.md")


@then("the topbar menu comes from the bench")
def step_topbar_bench_menu(context):
    link = context.page.locator("#lc-topbar .lc-links a", has_text="My bench")
    expect(link).to_be_visible(timeout=8000)
    href = link.get_attribute("href") or ""
    assert "run.html#src=gh:" + BENCH_REPO + "/index.md" in href, href


@then('the shelf lists a card opening gh path "{path}"')
def step_shelf_card(context, path):
    # a bare {: .folder } inside a render defaults to the CURRENT folder and
    # auto-uses runner mode — so a card links into the runner for that repo file
    a = context.page.locator(
        '#lc-run .lc-cards a[href*="run.html#src=gh:%s/%s"]' % (BENCH_REPO, path))
    expect(a.first).to_be_visible(timeout=10_000)


@then('the page editor is editing "{path}"')
def step_editor_targets(context, path):
    # the rich editor drawer bound to the runner-rendered source: the filename
    # header names the gh path (no docs/ prefix — it lives outside docs/)
    expect(context.page.locator("#ed-filename")).to_contain_text(path, timeout=10_000)


@then('the link "{text}" opens gh path "{path}"')
def step_link_heals(context, text, path):
    a = context.page.locator("#lc-run a", has_text=text).first
    expect(a).to_be_visible(timeout=8000)
    href = a.get_attribute("href") or ""
    assert "run.html#src=gh:" + BENCH_REPO + "/" + path in href, href
