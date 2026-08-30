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
               if (b.indexOf('<') === 0) return b;
               if (b.indexOf('```') === 0) {
                 var inner = b.split('\\n').slice(1, -1).join('\\n');
                 return '<pre><code>' + inner + '</code></pre>';
               }
               if (b.indexOf('## ') === 0) return '<h2>' + b.slice(3) + '</h2>';
               if (b.indexOf('# ')  === 0) return '<h1>' + b.slice(2) + '</h1>';
               if (b.indexOf('- ') === 0) {
                 return '<ul>' + b.split('\\n').map(function (l) {
                   return '<li>' + l.replace(/^- /, '') + '</li>';
                 }).join('') + '</ul>';
               }
               var im = b.match(/^!\\[([^\\]]*)\\]\\(([^)]+)\\)$/);
               if (im) return '<img alt="' + im[1] + '" src="' + im[2] + '">';
               b = b.replace(/\\[([^\\]]*)\\]\\(([^)]+)\\)/g,
                             '<a href="$2">$1</a>');
               return b ? '<p>' + b + '</p>' : '';
             }).join('');
           } };"""
    )


@given('the GitHub contents API serves "{path}" with the document')
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


@given('the committable GitHub page "{path}" serves')
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
            # shape matters: the editor's save reads content.sha AND commit.sha
            route.fulfill(status=200, content_type="application/json",
                          body='{"content":{"sha":"new-sha"},'
                               '"commit":{"sha":"abc1234def"}}')
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


@given('the GitHub contents API slowly serves "{path}" with the document')
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


@then('the editor is editing "{path}"')
def step_editor_file(context, path):
    # the original bug class: an editor opened on /run must edit the RENDERED
    # file, never docs/run.md (the vehicle)
    expect(context.page.locator("#ed-filename")).to_contain_text(path, timeout=10_000)


@then('the editor preview shows "{text}"')
def step_editor_preview_shows(context, text):
    # the preview body is stamped with the rendered file's folder, so the
    # {: .embed } fragment resolves folder-relative INSIDE edit mode too
    expect(context.page.locator("#ed-preview")).to_contain_text(text, timeout=10_000)


@given('the editor repo "{repo}" grants push')
def step_repo_grants_push(context, repo):
    def fulfill(route):
        route.fulfill(status=200, content_type="application/json",
                      body='{"full_name":"%s","permissions":{"push":true}}' % repo)
    # exact repo root only — /contents/ routes are registered separately
    context.page.route("**/api.github.com/repos/" + repo, fulfill)


@when('I append "{text}" to the editor and save')
def step_append_and_save(context, text):
    context.page.evaluate(
        "(t) => { const i = document.getElementById('ed-input');"
        " i.value = i.value + '\\n\\n' + t;"
        " i.dispatchEvent(new Event('input', {bubbles: true})); }",
        text,
    )
    # saveFile asks for a commit message via a native prompt(); Playwright
    # DISMISSES dialogs by default, which silently aborts the save
    context.page.once("dialog", lambda d: d.accept("bdd: save round-trip"))
    context.page.click("#ed-save-btn")


@then('the rendered file\'s commit carries "{text}"')
def step_commit_carries(context, text):
    import base64 as _b64
    import json as _json
    for _ in range(40):
        for p, body in context.keep_puts:
            if not body:
                continue
            try:
                content = _b64.b64decode(_json.loads(body).get("content", "")).decode("utf-8")
            except Exception:
                continue
            if text in content:
                return
        context.page.wait_for_timeout(250)
    raise AssertionError(
        f"no PUT carried {text!r}; PUTs to: {[p for p, _ in context.keep_puts]}")


@when('the runner hash-navigates to "{src}"')
def step_hash_navigate(context, src):
    context.page.evaluate("(s) => { location.hash = '#src=' + s; }", src)
    context.page.wait_for_timeout(800)


@then("the Present and Reel options are hidden again")
def step_modes_hidden(context):
    # visible-but-dead is the bug: a no-deck render must RE-hide the modes
    context.page.wait_for_function(
        """() => {
            const p = document.getElementById('lc-bl-present-btn');
            const r = document.getElementById('lc-bl-reel-btn');
            return p && p.hidden && r && r.hidden;
        }""",
        timeout=10_000,
    )


@then('the verb "close" folds every accordion section')
def step_verb_close(context):
    n = context.page.evaluate(
        "() => { window.lcVerbs.act('close');"
        " return document.querySelectorAll('.markdown-body details[open]').length; }"
    )
    assert n == 0, f"{n} section(s) still open after close"


@then('the verb "open" with "{title}" unfolds the matching section only')
def step_verb_open_arg(context, title):
    opened = context.page.evaluate(
        """(t) => { window.lcVerbs.act('open', null, t);
             return Array.from(document.querySelectorAll('.markdown-body details[open] summary'))
                         .map(s => s.textContent.trim()); }""",
        title,
    )
    assert opened and all(title.lower() in s.lower() for s in opened), \
        f"opened sections: {opened!r}"


@then('the verb "present" enters present mode')
def step_verb_present(context):
    context.page.evaluate("window.lcVerbs.act('present')")
    context.page.wait_for_function(
        "() => document.body.classList.contains('lc-slides-active')", timeout=5_000)


@then('the verb "xray" turns the pipes on and stays on when asked again')
def step_verb_xray(context):
    ok = context.page.evaluate("window.lcVerbs.act('xray')")
    assert ok, "the xray verb reported failure"
    context.page.wait_for_function(
        "() => window.lcMode.current() === 'xray'", timeout=5_000)
    # a tour line calling it again must hold the pipes up, not flip them off
    context.page.evaluate("window.lcVerbs.act('xray')")
    mode = context.page.evaluate("window.lcMode.current()")
    assert mode == "xray", f"a second call toggled the pipes off: {mode!r}"


@then('the verb "xray" reveals the wiring scene and it survives a mouse move')
def step_verb_xray_reveals(context):
    ok = context.page.evaluate("window.lcVerbs.act('xray')")
    assert ok, "the xray verb reported failure"
    context.page.wait_for_function(
        "() => { const s = document.getElementById('lcx-scene');"
        "        return s && s.style.display === 'block'"
        "            && s.querySelectorAll('svg .lcx-pipe, svg path, svg line').length > 0; }",
        timeout=10_000)
    # a bare mouse move used to wipe the scene — the tour's hold must survive it
    context.page.mouse.move(10, 10)
    context.page.wait_for_timeout(300)
    shown = context.page.evaluate(
        "() => document.getElementById('lcx-scene').style.display")
    assert shown == "block", f"a mouse move wiped the verb's scene: {shown!r}"


@then("the docked source ghost floats above the ghosts that use it")
def step_ghost_source_above(context):
    # the 👻 layout contract: an invisible source (a dataset) docks on the
    # right margin ABOVE every component that reads it, so its drop pipes
    # run down-then-left and never cross (Michel, 2026-08-18)
    got = context.page.evaluate(
        "() => { const ps = [...document.querySelectorAll('.lcx-xray')]"
        "          .filter(p => p.style.display === 'block');"
        "        const t = p => ((p.querySelector('.t')||{}).textContent || '');"
        "        const src = ps.find(p => t(p).includes('Dataset'));"
        "        const users = ps.filter(p => p !== src);"
        "        if (!src || !users.length) return null;"
        "        return { srcBottom: src.offsetTop + src.offsetHeight,"
        "                 userTop: Math.min(...users.map(u => u.offsetTop)),"
        "                 haunted: t(src).includes('👻') }; }")
    assert got, "no dataset ghost in the scene"
    assert got["haunted"], "the source panel lost its 👻"
    assert got["srcBottom"] <= got["userTop"], \
        "source ghost not above its users: %r" % got


@then('the verb "read" folds the wiring scene away')
def step_verb_read_folds(context):
    context.page.evaluate("window.lcVerbs.act('read')")
    context.page.wait_for_function(
        "() => { const s = document.getElementById('lcx-scene');"
        "        return !s || s.style.display !== 'block'; }", timeout=5_000)


@then('the verb "xray" with seconds returns the page to read by itself')
def step_verb_xray_timed(context):
    context.page.evaluate("window.lcVerbs.act('xray', null, '0.4')")
    context.page.wait_for_function(
        "() => window.lcMode.current() === 'xray'", timeout=5_000)
    context.page.wait_for_function(
        "() => window.lcMode.current() === 'read'", timeout=5_000)


@then('the verb "open" targets the "{title}" section title as its subject')
def step_verb_subject(context, title):
    got = context.page.evaluate(
        """(t) => { const el = window.lcVerbs.target('open', null, t);
             return el ? { tag: el.tagName, text: el.textContent.trim() } : null; }""",
        title,
    )
    assert got and got["tag"] == "SUMMARY" and title.lower() in got["text"].lower(), \
        f"subject: {got!r}"


@when('a stub datagrid holds rows for "{a}" and "{b}"')
def step_stub_grid(context, a, b):
    # hermetic: ag-grid's CDN is blocked here — the verb talks to the grid's
    # registered API and to rendered rows, both of which this stub provides;
    # the real grid rides the same contract in CI's full suite
    context.page.evaluate(
        """([a, b]) => {
            const g = document.createElement('div');
            g.className = 'lc-datagrid'; g.id = 'lc-datagrid-bdd';
            g.innerHTML = '<div class="ag-row">' + a + '</div>' +
                          '<div class="ag-row">' + b + '</div>';
            document.querySelector('.markdown-body').appendChild(g);
            const nodes = [
              { data: { name: a }, selected: false,
                setSelected(v) { this.selected = v; window._bddSel = a; } },
              { data: { name: b }, selected: false,
                setSelected(v) { this.selected = v; window._bddSel = b; } },
            ];
            window.lcMasterDetail._apis['bdd'] =
              { forEachNode(cb) { nodes.forEach(cb); } };
            g.setAttribute('data-lc-id', 'bdd');
        }""",
        [a, b],
    )


@then('the verb "select" with "{name}" selects that row and stands at it')
def step_verb_select(context, name):
    got = context.page.evaluate(
        """(n) => {
            const ok = window.lcVerbs.act('select', document.getElementById('lc-datagrid-bdd'), n);
            const subj = window.lcVerbs.target('select', document.getElementById('lc-datagrid-bdd'), n);
            return { ok, selected: window._bddSel, subject: subj ? subj.textContent.trim() : null };
        }""",
        name,
    )
    assert got["ok"] and got["selected"] == name and got["subject"] == name, f"{got!r}"


@then('the verb "select" with "{name}" lights that row in the bound table')
def step_verb_select_light(context, name):
    """The REAL road: a dataset-bound grid, no stub — the guide resolves the
    grid by its id exactly as a story's at: does, and the row must end up
    lit and standing as the verb's subject."""
    context.page.wait_for_selector(".lc-datagrid tbody tr", timeout=15_000)
    got = context.page.evaluate(
        """(n) => {
            const g = window.lcAvatarResolve('monthly_grid');
            const ok = window.lcVerbs.act('select', g, n);
            const subj = window.lcVerbs.target('select', g, n);
            const lit = Array.from(document.querySelectorAll('.lc-dg-selected'))
                             .map(r => r.textContent.trim());
            return { ok, lit, subject: subj ? subj.textContent.trim() : null };
        }""",
        name,
    )
    assert got["ok"], "the verb did nothing on a dataset-bound grid: %r" % (got,)
    assert any(name in row for row in got["lit"]), \
        "no row lit for %r — lit: %r" % (name, got["lit"])
    assert got["subject"] and name in got["subject"], \
        "the guide would stand nowhere useful: %r" % (got["subject"],)


@given("a tour yaml shim with a stage direction is preinstalled")
def step_tour_yaml_shim(context):
    # a bare do: line (no say) followed by narration — the dead-beat case
    context.page.add_init_script(
        "window.jsyaml = { load: function () { return"
        " { script: [ { do: 'open' }, { say: 'After the beat' } ] }; },"
        " dump: function (o) { return JSON.stringify(o) + '\\n'; } };"
    )


@when("I play the guide's tour")
def step_play_tour(context):
    context.page.wait_for_selector("#guide_seed", timeout=10_000)
    context.page.click("#guide_seed")
    tour = context.page.get_by_text("Play tour")
    expect(tour).to_be_visible(timeout=5_000)
    tour.click()


@then('the section unfolds and the narration reaches "{text}"')
def step_tour_advances(context, text):
    # the action line must open the section AND hand over quickly — an empty
    # bubble hanging on a fake sentence was the dead beat
    context.page.wait_for_function(
        "() => document.querySelector('.lc-run details[open]') !== null", timeout=10_000)
    expect(context.page.locator(".lc-avatar-speech")).to_contain_text(text, timeout=10_000)


@given("a tour yaml shim with a voice cue is preinstalled")
def step_tour_yaml_shim_cue(context):
    # a bare at: line (walk only, no say) then a line carrying a <break>
    # voice-cue tag: the tour must advance past the walk without a dead
    # beat, and the tag must never reach the bubble
    context.page.add_init_script(
        "window.jsyaml = { load: function () { return"
        " { script: [ { at: 'h1' },"
        "             { say: 'Take <break time=\"0.3s\" /> a breath' } ] }; },"
        " dump: function (o) { return JSON.stringify(o) + '\\n'; } };"
    )


@then('the bubble narrates "{text}" without the cue tag')
def step_bubble_no_cue(context, text):
    expect(context.page.locator(".lc-avatar-speech")).to_contain_text(
        text, timeout=10_000
    )
    leaked = context.page.evaluate(
        "document.querySelector('.lc-avatar-speech').textContent.includes('<break')"
    )
    assert not leaked, "the voice-cue tag leaked into the bubble"
