import re

from behave import given, when, then
from playwright.sync_api import expect

# RT slides parity (slides.md lcSlidesRebuild + runner.md hook): a page-level
# runner render re-partitions its root into .lc-slide sections so Present and
# Reel work on RT-rendered courses. The gh: source is served by a stubbed
# contents API route; marked is shimmed via an init script so the scenario is
# hermetic (no CDN) and deterministic in CI and locally alike.


@given("a marked shim is preinstalled")
def step_marked_shim(context):
    # add_init_script runs before any page script, so lcLoadMarked's
    # window.marked short-circuit takes the shim and never touches the CDN.
    # It only needs to be faithful for the fixture: #/## headings + paragraphs.
    context.page.add_init_script(
        """window.marked = { parse: function (s) {
             return s.split(/\\n\\n+/).map(function (b) {
               b = b.trim();
               if (b.indexOf('```') === 0) {
                 var inner = b.split('\\n').slice(1, -1).join('\\n');
                 return '<pre><code>' + inner + '</code></pre>';
               }
               if (b.indexOf('## ') === 0) return '<h2>' + b.slice(3) + '</h2>';
               if (b.indexOf('# ')  === 0) return '<h1>' + b.slice(2) + '</h1>';
               var im = b.match(/^!\\[([^\\]]*)\\]\\(([^)]+)\\)$/);
               if (im) return '<img alt="' + im[1] + '" src="' + im[2] + '">';
               b = b.replace(/\\[([^\\]]*)\\]\\(([^)]+)\\)/g,
                             '<a href="$2">$1</a>');
               return b ? '<p>' + b + '</p>' : '';
             }).join('');
           } };"""
    )


@given('the GitHub contents API serves "{path}" with the document:')
def step_stub_contents_doc(context, path):
    body = context.text

    def fulfill(route):
        route.fulfill(status=200, content_type="text/plain; charset=utf-8",
                      body=body)
    context.page.route("**/api.github.com/repos/**/contents/" + path + "*", fulfill)
    context.page.route("**/raw.githubusercontent.com/**/" + path + "*", fulfill)
    context.page.route("**/raw.githubusercontent.com//main/" + path + "*", fulfill)


@then("the runner render partitions into {n:d} slides")
def step_runner_slides(context, n):
    expect(context.page.locator(".lc-run .lc-slide")).to_have_count(n, timeout=10_000)


@then("the page is in present mode")
def step_present_mode(context):
    expect(context.page.locator("body")).to_have_class(
        re.compile(r"lc-slides-active"), timeout=5_000
    )


@then('the active slide shows "{text}"')
def step_active_slide_shows(context, text):
    # VISIBLE, not just present: the page-load partition wraps /run's content
    # in an outer .lc-slide, and a display:none anywhere on that ancestor
    # chain blanks the screen while to_contain_text alone still passes.
    active = context.page.locator('.lc-run .lc-slide[data-active="true"]')
    expect(active).to_be_visible(timeout=5_000)
    expect(active).to_contain_text(text, timeout=5_000)


@then("the first rendered slide is visible")
def step_first_slide_visible(context):
    expect(context.page.locator(".lc-run .lc-slide").first).to_be_visible(timeout=5_000)


@when("I click the Reel option in the popup")
def step_click_reel_option(context):
    btn = context.page.locator("#lc-bl-reel-btn")
    expect(btn).to_be_visible(timeout=3_000)
    btn.click()
    context.page.wait_for_timeout(400)


@then('the page score key is "{key}"')
def step_score_key(context, key):
    got = context.page.evaluate("window.lcPageScores.norm(location.href)")
    assert got == key, f"score key {got!r}, expected {key!r}"


@then("a card href to that render produces the same score key")
def step_card_key_matches(context):
    page_key = context.page.evaluate("window.lcPageScores.norm(location.href)")
    card_key = context.page.evaluate(
        "window.lcPageScores.norm('run.html#src=gh:acme/demo/courses/demo/mod/index.md')"
    )
    assert card_key == page_key, f"card key {card_key!r} != page key {page_key!r}"


@given("a yaml shim declaring knowledge self is preinstalled")
def step_yaml_shim(context):
    # parseBot only needs the knowledge list out of the bot's yaml fence;
    # jsyaml itself lives on a CDN the sandbox blocks
    context.page.add_init_script(
        "window.jsyaml = { load: function () { return { knowledge: ['self'] } } };"
    )


@given('the counting GitHub contents API serves "{path}" as "{name}"')
def step_stub_counting(context, path, name):
    if not hasattr(context, "hits"):
        context.hits = {}
    context.hits[name] = 0

    def fulfill(route):
        context.hits[name] += 1
        route.fulfill(status=200, content_type="text/plain; charset=utf-8",
                      body="## Fragment\n\nBecause building beats watching.")
    context.page.route("**/api.github.com/repos/**/contents/" + path + "*", fulfill)
    context.page.route("**/raw.githubusercontent.com/**/" + path + "*", fulfill)
    context.page.route("**/raw.githubusercontent.com//main/" + path + "*", fulfill)


@when('I note the fragment hit count for "{name}"')
def step_note_hits(context, name):
    context.hits_before = context.hits.get(name, 0)


@when("I inject a tutor agent into the render root")
def step_inject_agent(context):
    context.page.evaluate(
        """() => {
            const root = document.querySelector('#lc-run');
            const p = document.createElement('p');
            p.className = 'agent';
            p.setAttribute('bot', 'tutor');
            p.textContent = 'Ask the tutor.';
            root.appendChild(p);
            window.lcUpgradeAgent(p);
        }"""
    )


@then('the fragment "{name}" is fetched again as tutor knowledge')
def step_fragment_refetched(context, name):
    # the page's own embed already fetched it once at render; the tutor's
    # knowledge assembly must fetch it AGAIN — that second hit is the proof
    for _ in range(40):
        if context.hits.get(name, 0) > context.hits_before:
            return
        context.page.wait_for_timeout(250)
    raise AssertionError(
        f"fragment {name!r}: {context.hits.get(name, 0)} hits, "
        f"expected more than {context.hits_before}"
    )


@given("a yaml shim is preinstalled")
def step_yaml_shim_generic(context):
    # keepAnswer only DUMPS (the created fence); the committed body's yaml
    # fidelity is not what this scenario asserts — the target path is
    context.page.add_init_script(
        "window.jsyaml = { load: function () { return {}; },"
        "                  dump: function (o) { return JSON.stringify(o) + '\\n'; } };"
    )


@given("a builder key and editor repo are connected")
def step_key_and_repo(context):
    context.page.add_init_script(
        "try { localStorage.setItem('lc_ed_pat', 'bdd-test-key');"
        "      localStorage.setItem('lc_ed_repo', 'acme/demo'); } catch (e) {}"
    )


@given('the committable GitHub page "{path}" serves:')
def step_committable_page(context, path):
    import base64 as _b64
    import json as _json
    doc = context.text
    if not hasattr(context, "keep_puts"):
        context.keep_puts = []

    def fulfill(route):
        req = route.request
        if req.method == "PUT":
            context.keep_puts.append((path, req.post_data or ""))
            route.fulfill(status=200, content_type="application/json",
                          body='{"content":{}}')
            return
        if "raw" in (req.headers.get("accept") or ""):
            route.fulfill(status=200, content_type="text/plain; charset=utf-8",
                          body=doc)
            return
        env = {"content": _b64.b64encode(doc.encode()).decode(), "sha": "stub-sha"}
        route.fulfill(status=200, content_type="application/json",
                      body=_json.dumps(env))
    context.page.route("**/api.github.com/repos/**/contents/" + path + "*", fulfill)


@given('commits to "{path}" are watched')
def step_watch_commits(context, path):
    if not hasattr(context, "keep_puts"):
        context.keep_puts = []

    def fulfill(route):
        if route.request.method == "PUT":
            context.keep_puts.append((path, route.request.post_data or ""))
        route.fulfill(status=404, content_type="application/json", body="{}")
    context.page.route("**/api.github.com/repos/**/contents/" + path + "*", fulfill)


@when("the guide holds an unsaved answer")
def step_guide_answer(context):
    context.page.evaluate("window.lcGuideOn(true)")
    context.page.wait_for_selector("#guide_seed", timeout=5_000)
    context.page.evaluate(
        """() => {
            const av = window._lcAvatars['site_guide'];
            av._lastAnswer = { question: 'What is this page about?',
                               steps: [{ say: 'It is a demo course.' }] };
        }"""
    )


@when("I click the guide's Keep & voice")
def step_click_keep(context):
    context.page.click("#guide_seed")
    keep = context.page.get_by_text("📌 Keep & voice")
    expect(keep).to_be_visible(timeout=3_000)
    keep.click()


@then('the story is committed to "{path}"')
def step_story_committed(context, path):
    import base64 as _b64
    for _ in range(40):
        for p, body in context.keep_puts:
            if p != path or not body:
                continue
            try:
                import json as _json
                content = _b64.b64decode(_json.loads(body).get("content", "")).decode("utf-8")
            except Exception:
                continue
            if "What is this page about?" in content:
                return
        context.page.wait_for_timeout(250)
    raise AssertionError(f"no story commit to {path!r}; PUTs: "
                         f"{[p for p, _ in context.keep_puts]}")


@then('nothing was committed to "{path}"')
def step_no_commit(context, path):
    bad = [p for p, _ in context.keep_puts if p == path]
    assert not bad, f"unexpected commit(s) to {path!r}"


@given("a story yaml shim is preinstalled")
def step_story_yaml_shim(context):
    # the avatar fence parses through jsyaml (CDN-blocked here); a fixed cfg
    # with one kept story is all the eviction scenario needs
    context.page.add_init_script(
        "window.jsyaml = { load: function () { return"
        " { script: [], stories: { 'My kept story': ['hello there'] } }; },"
        " dump: function (o) { return JSON.stringify(o) + '\\n'; } };"
    )


@given("the learner has the generic guide enabled")
def step_generic_guide_on(context):
    context.page.add_init_script(
        "try { localStorage.setItem('lc_guide_on', '1'); } catch (e) {}"
    )


@given('the GitHub contents API slowly serves "{path}" with the document:')
def step_stub_contents_slow(context, path):
    import time as _time
    body = context.text

    def fulfill(route):
        # slower than the generic guide's 900ms summon timer — the exact
        # live race: generic squats the seed first, the render lands after
        _time.sleep(1.6)
        route.fulfill(status=200, content_type="text/plain; charset=utf-8",
                      body=body)
    context.page.route("**/api.github.com/repos/**/contents/" + path + "*", fulfill)
    context.page.route("**/raw.githubusercontent.com/**/" + path + "*", fulfill)


@then("the authored guide holds the only seed")
def step_authored_seed(context):
    context.page.wait_for_function(
        """() => {
            const seeds = document.querySelectorAll('#guide_seed');
            const avs = window._lcAvatars || {};
            return seeds.length === 1 &&
                   !seeds[0].dataset.lcGeneric &&
                   !avs.site_guide && !!avs.guide;
        }""",
        timeout=10_000,
    )


@then("no avatar face floats undocked")
def step_no_undocked_face(context):
    undocked = context.page.evaluate(
        "document.querySelectorAll('.lc-avatar-host:not(.lc-avatar-docked)').length"
    )
    assert undocked == 0, f"{undocked} avatar host(s) undocked"
