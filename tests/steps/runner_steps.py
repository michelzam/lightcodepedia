import re
from behave import given, when, then
from playwright.sync_api import expect


@when('I open the runner page on "{src}"')
def step_open_runner(context, src):
    context.page.goto(context.base_url + "/run#src=" + src, wait_until="domcontentloaded")


@when("I open the frame host page scrolled past the lesson's top")
def step_open_frame_host(context):
    context.page.goto(context.base_url + "/run_samples/host.html",
                      wait_until="domcontentloaded")
    frame = context.page.frame_locator("#lesson")
    frame.locator('a:has-text("Back to this page")').wait_for(timeout=15_000)
    # the reader is deep in the lesson: the frame's top is well above the fold
    context.page.evaluate("window.scrollTo(0, 1800)")
    context.page.wait_for_timeout(200)


@when('I click the framed runner link "{label}"')
def step_click_framed_link(context, label):
    context.page.frame_locator("#lesson").locator(
        'a:has-text("%s")' % label).click()


@then("the host page is scrolled back to the lesson's top")
def step_host_at_frame_top(context):
    # the frame sits at y=1200 (the filler above it); smooth scroll settles there
    context.page.wait_for_function(
        "() => window.scrollY <= 1250", timeout=5_000)


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


@then("a rendered diagram replaces the dot source")
def step_dot_rendered(context):
    from playwright.sync_api import expect
    svg = context.page.locator(".lc-dot-diagram svg").first
    expect(svg).to_be_visible(timeout=20_000)
    assert context.page.locator("code.language-dot").count() == 0, \
        "the DOT source is still on the page, unrendered"


@then("the diagram is no wider than the page")
def step_diagram_fits(context):
    m = context.page.evaluate(
        """() => {
             const box = document.querySelector('.lc-dot-diagram');
             const svg = box && box.querySelector('svg');
             if (!svg) return null;
             return { svg: svg.getBoundingClientRect().width,
                      box: box.clientWidth,
                      scroll: box.scrollWidth };
           }"""
    )
    assert m, "no diagram found"
    assert m["svg"] <= m["box"] + 1, (
        "diagram %spx wide inside a %spx column — the reader must scroll"
        % (round(m["svg"]), round(m["box"])))


# ── one render, one set of positional names ────────────────────────────────
# run_1 on this page is a DIFFERENT block from run_1 on the last one. The
# registry that feeds the ⚙️ editor is keyed by that name, so it has to be
# emptied when a render starts or the editor opens the previous page's markup.

@when('I move to the runner source "{src}"')
def step_move_runner_source(context, src):
    """Change the hash — NO reload. That is the whole point: a reload would
    give the page a fresh JS context and hide the bug. The runner re-renders on
    hashchange, in the same context, which is exactly how a reader walks from a
    module's index into its first lesson."""
    context.page.evaluate("s => { location.hash = '#src=' + s; }", src)
    context.page.wait_for_timeout(600)


@then('the block editor on the rendered fence shows "{text}"')
def step_editor_shows(context, text):
    from playwright.sync_api import expect as _expect

    block = context.page.locator("#lc-run [data-lc-id]").first
    block.wait_for(state="visible", timeout=20_000)
    block.scroll_into_view_if_needed()
    block.evaluate(
        "el => el.dispatchEvent(new PointerEvent('pointermove',"
        " {altKey: true, bubbles: true, cancelable: true}))"
    )
    gear = context.page.locator("#lcx-gear")
    gear.wait_for(state="visible", timeout=5_000)
    gear.click(force=True)
    content = context.page.locator("#lcx-content")
    _expect(content).to_be_visible(timeout=5_000)
    got = content.input_value()
    assert text in got, (
        "the ⚙️ opened on %r — it is showing another block's source, "
        "not this page's" % got[:160]
    )


@then('no snapshot still carries "{text}"')
def step_no_stale_snapshot(context, text):
    stale = context.page.evaluate(
        """(needle) => {
          var out = [];
          document.querySelectorAll('#lc-run [id]').forEach(function (el) {
            var s = window.lcSourceOf && window.lcSourceOf(el.id);
            if (s && s.indexOf(needle) >= 0) out.push(el.id);
          });
          return out;
        }""",
        text,
    )
    assert not stale, "ids still holding the previous page's source: %r" % stale


@when('I click the runner link "{label}"')
def step_click_runner_link(context, label):
    context.page.click('a:has-text("%s")' % label)
    # the here-link scrolls smoothly — let the gesture finish before asserting
    context.page.wait_for_function("() => window.scrollY === 0", timeout=5_000)


@when('I open the framed bench page "{path}"')
def step_open_framed_bench_page(context, path):
    # same bench, but inside a teacher's frame (?crumb=…, the LMS view)
    _bench_route(context)
    context.page.add_init_script("localStorage.setItem('lc_ed_pat','ghp_stu');")
    context.page.goto(context.base_url + "/run.html?crumb=BUILD#src=gh:"
                      + BENCH_REPO + "/" + path, wait_until="domcontentloaded")


@then("the pill's Edit door is grayed with a reason")
def step_edit_grayed(context):
    context.page.wait_for_function(
        "() => { const b = document.getElementById('lc-bl-edit-btn');"
        "        return b && b.disabled; }", timeout=8_000)
    title = context.page.locator("#lc-bl-edit-btn").get_attribute("title") or ""
    assert "bench" in title, "no reason on the grayed door: %r" % title


@then("pressing Alt+E does not open the editor")
def step_alt_e_noop(context):
    context.page.keyboard.press("Alt+KeyE")
    context.page.wait_for_timeout(600)
    mode = context.page.evaluate("window.lcMode ? window.lcMode.current() : 'read'")
    assert mode != "edit", "the hotkey opened the editor on a course page"


@then("the pill's Edit door is open")
def step_edit_open(context):
    # bench mode stamps after the render; only then is "not disabled" a verdict
    # rather than the initial state — and the delayed syncs get their say too
    context.page.wait_for_function(
        "() => document.querySelector('#lc-topbar.lc-bench-mode')", timeout=15_000)
    context.page.wait_for_timeout(2200)
    assert not context.page.evaluate(
        "document.getElementById('lc-bl-edit-btn').disabled"), \
        "the learner's own page lost its Edit door"


@when("I scroll the runner to the bottom")
def step_scroll_bottom(context):
    context.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    context.page.wait_for_timeout(200)
    context.rt_scroll = context.page.evaluate("window.scrollY")
    assert context.rt_scroll > 200, f"page is not tall enough to test: {context.rt_scroll}"


@when('the runner navigates to "{src}"')
def step_rt_navigate(context, src):
    """Exactly what a healed card link does: swap the src in the hash."""
    context.page.evaluate("s => { location.hash = 'src=' + s; }", src)
    context.page.wait_for_timeout(1500)


@then("the runner is scrolled to the top")
def step_rt_at_top(context):
    y = context.page.evaluate("window.scrollY")
    assert y == 0, f"landed at {y}px down a page the reader has never seen"


@then("the runner is still scrolled down")
def step_rt_kept_place(context):
    y = context.page.evaluate("window.scrollY")
    assert y > 0, "a re-render threw the reader back to the top"


@then('the embedded runner shows a heading "{text}"')
def step_embedded_heading(context, text):
    """The nested render lives in its own .lc-runner, without the #lc-run id
    the page-level one owns."""
    inner = context.page.locator(".lc-runner .lc-run:not(#lc-run)").first
    expect(inner).to_contain_text(text, timeout=20_000)


@given("a course key that GitHub rejects")
def step_stale_key(context):
    """An expired or revoked PAT: every GitHub call answers 401."""
    context.page.add_init_script(
        "localStorage.setItem('lc_ed_pat','ghp_stale');"
        "localStorage.setItem('lc_ed_repo','acme/demo-vault');")
    context.page.route(
        "https://api.github.com/**",
        lambda r: r.fulfill(status=401, content_type="application/json",
                            body='{"message": "Bad credentials"}'))


@then("the runner says the key itself is the problem")
def step_key_named(context):
    status = context.page.locator(".lc-runner .lc-run-status")
    expect(status).to_contain_text(re.compile("key", re.I), timeout=20_000)


@then("the runner never shows a bare HTTP status")
def step_no_bare_status(context):
    txt = context.page.locator(".lc-runner .lc-run-status").inner_text()
    assert "Could not load" not in txt, txt


@then("the sign-in door is offered")
def step_signin_door(context):
    pill = context.page.locator("#lc-start-pill")
    expect(pill).to_be_visible(timeout=10_000)


@then("the runner says the course is private")
def step_private_said(context):
    status = context.page.locator(".lc-runner .lc-run-status")
    expect(status).to_contain_text(re.compile("private", re.I), timeout=20_000)


@then("the runner offers a way to make a key")
def step_key_ladder(context):
    link = context.page.locator('.lc-run-status a[href*="github.com/settings/tokens"]')
    expect(link).to_have_count(1, timeout=10_000)


@then("the runner names the Get started door")
def step_names_door(context):
    txt = context.page.locator(".lc-runner .lc-run-status").inner_text()
    assert "Get started" in txt, txt


@given("a private vault that answers a stranger with 404")
def step_private_vault(context):
    """GitHub hides a private repo from an anonymous caller behind 404 —
    the same answer as "no such repo", which is why the message has to be
    about the missing key rather than about the status."""
    context.page.route(
        "https://api.github.com/**",
        lambda r: r.fulfill(status=404, content_type="application/json",
                            body='{"message": "Not Found"}'))


@when('I open the "{title}" accordion')
def step_open_accordion(context, title):
    context.page.evaluate(
        """(t) => { const d = [...document.querySelectorAll('details')]
             .find(x => ((x.querySelector('summary')||{}).textContent||'').includes(t));
           if (d) d.open = true; }""", title)
    # the body renders on FIRST open (marked + a full component scan), so wait
    # for something to appear rather than guessing a delay
    try:
        context.page.wait_for_selector("details .lc-ac-body *", timeout=15_000)
    except Exception:
        pass
    context.page.wait_for_timeout(1500)


@then("the accordion holds two blocks side by side")
def step_two_blocks(context):
    geo = context.page.evaluate("""() => {
      const b = document.querySelector('details .lc-blocks');
      if (!b) return null;
      const cols = getComputedStyle(b).gridTemplateColumns.split(' ').length;
      /* the page carries other panels (the runner's own ⚙️ Connect); what must
         not exist is a panel named after a heading INSIDE the nested fence */
      const stolen = [...document.querySelectorAll('details > summary')]
        .filter(s => /Name|In motion/.test(s.textContent || '')).length;
      return { cards: b.children.length, cols: cols, stolen: stolen };
    }""")
    if not geo:
        dump = context.page.evaluate(
            """() => ({ details: document.querySelectorAll('details').length,
                        summaries: [...document.querySelectorAll('summary')].map(s => s.textContent.trim()),
                        body: (document.querySelector('details .lc-ac-body') || {}).innerHTML,
                        run: ((document.querySelector('#lc-run') || {}).innerHTML || '').slice(0, 220),
                        status: ((document.querySelector('.lc-run-status') || {}).textContent || '') })""")
        raise AssertionError("the nested block never rendered: %r" % dump)
    assert geo["cards"] == 2 and geo["cols"] == 2, geo
    assert geo["stolen"] == 0, "the nested headings became panels of their own: %r" % geo


@then("the clip is a video element that loops and starts muted")
def step_native_clip(context):
    v = context.page.evaluate("""() => { const v = document.querySelector('video.lc-video-file');
      return v ? { loop: v.loop, muted: v.muted, autoplay: v.autoplay,
                   iframes: document.querySelectorAll('iframe.lc-video').length } : null; }""")
    assert v, "the clip became an iframe (or nothing) instead of a video"
    assert v["loop"] and v["muted"] and v["autoplay"], v
    assert v["iframes"] == 0, v


@given('the GitHub contents API counts every read of "{name}"')
def step_count_media(context, name):
    context.media_reads = []

    def serve(route):
        context.media_reads.append(route.request.url)
        # a 1×1 gif standing in for a clip: the point is HOW MANY times it is read
        route.fulfill(status=200, content_type="application/vnd.github.v3.raw",
                      body=b"\x00\x00\x00\x18ftypmp42")

    # every shape the contents API takes for a file inside a folder
    context.page.route("**/contents/**" + name + "**", serve)


@then("both clips share one download")
def step_one_download(context):
    context.page.wait_for_timeout(1500)
    reads = getattr(context, "media_reads", [])
    srcs = context.page.evaluate(
        "() => [...document.querySelectorAll('video.lc-video-file')].map(v => v.src)")
    assert len(srcs) == 2, "expected two clips, got %r" % srcs
    assert len(reads) == 1, "the file was downloaded %d times" % len(reads)
    assert srcs[0] == srcs[1], "each clip made its own blob: %r" % srcs


@then("the embedded runner is inside a border of its own")
def step_embed_border(context):
    """An injected file must LOOK injected. Without an edge, a lesson and the
    app it embeds run together again — the blurry mixture the seam went after
    (Michel, 2026-08-14). The page-level runner IS the page and keeps none."""
    got = context.page.evaluate(
        """() => {
             const e = document.querySelector('.lc-runner-embed');
             if (!e) return null;
             const cs = getComputedStyle(e);
             return { w: cs.borderTopWidth, style: cs.borderTopStyle,
                      page: !!document.querySelector('#lc-run.lc-runner-embed,'
                            + ' .lc-runner-embed > #lc-run') };
           }"""
    )
    assert got, "the embedded render wears no .lc-runner-embed box"
    assert got["style"] != "none" and got["w"] != "0px", (
        "the embedded runner has no visible border: %r" % got
    )
    assert not got["page"], "the page-level runner took the embed border too"


@then("the injected file's own title stays out of the lesson")
def step_embed_h1_hidden(context):
    shown = context.page.evaluate(
        """() => [...document.querySelectorAll('.lc-runner-embed > .lc-run > h1')]
             .map(h => getComputedStyle(h).display)"""
    )
    assert shown, "the injected file brought no h1 — this proves nothing here"
    assert all(d == "none" for d in shown), (
        "the injected file's title doubled the lesson's heading: %r" % shown
    )


@then('the windowed embeds are titled "{first}" and "{second}"')
def step_win_titles(context, first, second):
    """title="Adoption Day" is the author's word; title="" asks for the
    injected file's own heading, which does not exist until the render
    lands — so the bar has to fill in afterwards, not at upgrade time."""
    got = context.page.evaluate(
        "() => [...document.querySelectorAll('.lc-runner-win .lc-win-title')]"
        ".map(e => e.textContent.trim())"
    )
    assert got == [first, second], "window titles: %r" % (got,)
    # the heading moved INTO the bar, so it must not also shout from the body
    shown = context.page.evaluate(
        """() => [...document.querySelectorAll('.lc-runner-win > .lc-run > h1')]
             .map(h => getComputedStyle(h).display)"""
    )
    assert all(d == "none" for d in shown), "the name is said twice: %r" % shown


@then("an embed with no title= stays a plain box")
def step_no_title_plain(context):
    n = context.page.evaluate(
        "() => document.querySelectorAll('.lc-runner-embed:not(.lc-runner-win)').length"
    )
    assert n == 1, "expected exactly one plain embed, found %d" % n


@then("the window dots are decoration, not controls")
def step_win_dots_decorative(context):
    """A control that looks like a control and does nothing is a lie told to
    a beginner. The dots are hidden from screen readers, take no focus and
    carry no pointer cursor."""
    got = context.page.evaluate(
        """() => [...document.querySelectorAll('.lc-win-dots')].map(d => ({
             hidden: d.getAttribute('aria-hidden'),
             cursor: getComputedStyle(d).cursor,
             focusable: !!d.querySelector('a, button, [tabindex], [role]') }))"""
    )
    assert got, "no window dots found"
    for d in got:
        assert d["hidden"] == "true", "the dots speak to a screen reader: %r" % d
        assert d["cursor"] != "pointer", "the dots invite a click they cannot honour: %r" % d
        assert not d["focusable"], "the dots take keyboard focus: %r" % d
