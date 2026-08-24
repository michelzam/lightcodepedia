import re

from behave import given, when, then
from playwright.sync_api import expect


@when("I open the page editor")
def step_open_editor(context):
    # Edit lives in the Modes pill now (the ✏️ FAB is retired chrome):
    # hover the pill, click the Edit entry.
    fab = context.page.locator(".lc-slides-fab")
    fab.wait_for(state="visible", timeout=15_000)
    fab.hover()
    btn = context.page.locator("#lc-bl-edit-btn")
    btn.wait_for(state="visible", timeout=5_000)
    btn.click()
    expect(context.page.locator("#ed-drawer")).to_have_class(
        re.compile(r"\bopen\b"), timeout=10_000
    )


@when('I click the editor "{elem_id}" button')
def step_click_editor_button(context, elem_id):
    btn = context.page.locator("#" + elem_id)
    btn.wait_for(state="visible", timeout=10_000)
    btn.click()
    context.page.wait_for_timeout(200)


@when('I switch to the editor "{name}" tab')
def step_switch_tab(context, name):
    tab = context.page.locator(".ed-tab[data-tab='" + name + "']")
    tab.wait_for(state="visible", timeout=10_000)
    tab.click()
    context.page.wait_for_timeout(200)


@then("the editor agent pane shows a prompt box")
def step_agent_prompt_visible(context):
    expect(context.page.locator("#ed-agent-prompt")).to_be_visible(timeout=10_000)


@then("the editor log pane is visible")
def step_log_pane_visible(context):
    expect(context.page.locator("#ed-log-pane")).to_be_visible(timeout=10_000)


@then("the editor features pane is visible")
def step_features_pane_visible(context):
    expect(context.page.locator("#ed-features-pane")).to_be_visible(timeout=10_000)


@when("I load sample components into the editor")
def step_load_sample(context):
    md = (
        "# Demo\n\n"
        "data\n{: .dataset #ds }\n\n"
        'grid\n{: .datagrid bind="ds" }\n\n'
        'chart\n{: .chart bind="ds" }\n'
    )
    context.page.evaluate(
        "(v) => { document.getElementById('ed-input').value = v; }", md
    )


@then("the editor diagram pane is visible")
def step_diagram_pane_visible(context):
    expect(context.page.locator("#ed-diagram-pane")).to_be_visible(timeout=10_000)


@then("the editor diagram renders a class graph")
def step_diagram_svg(context):
    pane = context.page.locator("#ed-diagram-pane")
    # the DOT engine (WASM) lazy-loads, then renders the inline SVG
    expect(pane.locator("svg").first).to_be_visible(timeout=25_000)
    expect(pane).to_contain_text("Datagrid", timeout=25_000)


@then("the raw editor is dark themed")
def step_raw_dark(context):
    bg = context.page.evaluate(
        "() => getComputedStyle(document.getElementById('ed-input')).backgroundColor"
    )
    # #1e1e2e (matches the mdpad editor) == rgb(30, 30, 46)
    assert bg.replace(" ", "") == "rgb(30,30,46)", "expected dark raw editor, got %r" % (bg,)


@when("I select the first block")
def step_select_first_block(context):
    row = context.page.locator("#ed-grid tr[data-idx]").first
    row.wait_for(state="visible", timeout=10_000)
    row.click()
    context.page.wait_for_timeout(400)


@then("the block content editor is dark themed")
def step_block_content_dark(context):
    ta = context.page.locator(".ebf-content-wrap textarea").first
    ta.wait_for(state="visible", timeout=10_000)
    bg = context.page.evaluate(
        "() => { var t = document.querySelector('.ebf-content-wrap textarea');"
        " return t ? getComputedStyle(t).backgroundColor : null; }"
    )
    assert bg and bg.replace(" ", "") == "rgb(30,30,46)", (
        "expected dark block content editor, got %r" % (bg,)
    )


@then("the editor formatting toolbar is visible")
def step_fmt_bar_visible(context):
    expect(
        context.page.locator(".ed-fmt-bar button[data-fmt='bold']").first
    ).to_be_visible(timeout=10_000)


@when("I bold a selection with the toolbar")
def step_toolbar_bold(context):
    # seed text, select it, then click Bold
    context.page.evaluate(
        "() => { var t = document.getElementById('ed-input');"
        " t.value = 'hello'; t.focus(); t.setSelectionRange(0, 5); }"
    )
    context.page.locator(".ed-fmt-bar button[data-fmt='bold']").first.click()
    context.page.wait_for_timeout(200)


@then('the raw editor contains "{snippet}"')
def step_raw_contains(context, snippet):
    val = context.page.evaluate("() => document.getElementById('ed-input').value")
    assert snippet in val, "expected %r in the raw editor, got %r" % (snippet, val)


@given("a stored key that GitHub refuses")
def step_bad_key(context):
    # a key the API rejects: every GitHub call 401s, exactly like an expired PAT
    context.page.route(
        "https://api.github.com/**",
        lambda route: route.fulfill(status=401, json={"message": "Bad credentials"}),
    )
    context.page.add_init_script(
        "localStorage.setItem('lc_ed_pat','ghp_revoked');"
        "localStorage.setItem('lc_ed_repo','michelzam/lightcodelab');"
    )


@then("the sign-in panel is offered")
def step_signin_offered(context):
    expect(context.page.locator("#ed-sidebar")).to_have_class(
        re.compile(r"\bed-open\b"), timeout=8_000
    )
    expect(context.page.locator("#ed-pat")).to_be_visible(timeout=8_000)


@given("the AI model endpoint is stubbed")
def step_stub_model(context):
    context.ai_bodies = []

    def fulfill(route):
        context.ai_bodies.append(route.request.post_data or "")
        route.fulfill(
            status=200, content_type="application/json",
            body='{"choices":[{"message":{"content":'
                 '"{\\"explanation\\":\\"noop\\",\\"edits\\":[]}"}}]}',
        )
    context.page.route("**/models.github.ai/**", fulfill)


@when("the editor content is")
@when("the editor content is:")
def step_set_editor_content(context):
    context.page.evaluate(
        "(text) => { const i = document.getElementById('ed-input'); "
        "i.value = text; i.dispatchEvent(new Event('input', {bubbles: true})); }",
        context.text,
    )


@when('I ask the editor AI to "{ask}"')
def step_ask_editor_ai(context, ask):
    context.page.fill("#ed-agent-prompt", ask)
    context.page.click("#ed-agent-ask")


@then("the AI request carried the embedded fragment")
def step_ai_request_has_fragment(context):
    # the fragment's TEXT must ride along — the reference line alone is what
    # the model saw before this feature
    for _ in range(40):
        if any("Embedded fragment: docs/_frag.md" in b and
               "building beats watching" in b for b in context.ai_bodies):
            return
        context.page.wait_for_timeout(250)
    raise AssertionError(
        f"AI bodies did not carry the fragment; got {len(context.ai_bodies)} request(s)"
        + (": " + context.ai_bodies[-1][:400] if context.ai_bodies else "")
    )


@when("I press the edit hotkey")
def step_press_edit_hotkey(context):
    context.page.keyboard.press("Alt+KeyE")
    context.page.wait_for_timeout(600)


@then("the editor drawer stays closed")
def step_drawer_closed(context):
    import re as _re
    body_class = context.page.evaluate("document.body.className")
    assert "ed-drawer-open" not in body_class, f"drawer opened: {body_class!r}"


@then("the pill offers no Edit item")
def step_no_edit_item(context):
    hidden = context.page.evaluate(
        "(document.getElementById('lc-bl-edit-btn') || {hidden: true}).hidden"
    )
    assert hidden, "the pill's Edit item is visible despite editable=0"


@given("a browser still paired to a learner's bench")
def step_paired_to_bench(context):
    """What ship/bay testing leaves behind: a key, and lc_ed_repo pointing at
    someone's bench rather than the site being browsed."""
    context.gh_repo_calls = []
    context.page.on("request", lambda r: context.gh_repo_calls.append(r.url)
                    if "api.github.com/repos/" in r.url else None)

    def gh(route):
        url = route.request.url
        if "/git/trees/" in url:
            route.fulfill(json={"sha": "HEAD", "tree": [
                {"path": "docs/events.md", "type": "blob", "sha": "s1"}],
                "truncated": False})
        elif "/contents/" in url:
            route.fulfill(json={"content": "IyBFdmVudHM=", "sha": "s1",
                                "name": "events.md", "path": "docs/events.md"})
        else:                                   # the repo probe itself
            full = url.split("/repos/", 1)[1].split("?")[0]
            route.fulfill(json={"full_name": full, "default_branch": "main",
                                "permissions": {"push": True}})

    context.page.route("https://api.github.com/repos/**", gh)
    context.page.add_init_script(
        "localStorage.setItem('lc_ed_pat','ghp_author');"
        "localStorage.setItem('lc_ed_repo','zam-academy/build-ai-fall26-zamm-student');"
    )


@then("the editor reads this site's own repo, not the bench")
def step_editor_targets_site(context):
    # the drawer names what it is connected to; the bench pairing itself is
    # left alone (the learner's progress record still belongs to it, which is
    # why the assertion reads the EDITOR's target, not every GitHub call)
    context.page.wait_for_function(
        "() => { const s = document.getElementById('ed-status');"
        "        return s && s.textContent.trim(); }", timeout=10_000)
    # textContent, not inner_text: the drawer may still be sliding in, and
    # Playwright reports "" for anything not yet visible
    status = (context.page.evaluate(
        "() => document.getElementById('ed-status').textContent") or "").strip()
    assert "zamm-student" not in status, \
        "the editor connected to the bench for a site page: %r" % status
    assert "lightcodelab" in status or "lightcodepedia" in status, \
        "the editor did not target this site's repo: %r" % status


@given("I open the editor on a page with two fenced blocks")
def step_open_with_fences(context):
    context.execute_steps('''
        When I navigate to "/components/examples/"
        And I wait for the page to be interactive
        When I open the page editor
        And I switch to the editor "raw" tab
    ''')
    md = (
        "# Demo\n\nProse before.\n\n"
        "```yaml\na: 1\nb: 2\nc: 3\n```\n"
        '{: .dataset #ds }\n\n'
        "Prose between.\n\n"
        "```python\nx = 1\ny = 2\nz = 3\n```\n"
        '{: .inspector #w }\n\n'
        "Prose after.\n"
    )
    context.ed_full = md
    context.page.evaluate(
        "(v) => { document.getElementById('ed-input').value = v; }", md)


@when("I press the fold button")
def step_fold(context):
    context.page.evaluate("window._lcEdFold.foldAll()")


@then("the display shrinks to marker lines")
def step_folded_display(context):
    n = context.page.evaluate("window._lcEdFold.count()")
    assert n == 2, "expected 2 folds, got %s" % n
    disp = context.page.evaluate(
        "() => Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value')"
        ".get.call(document.getElementById('ed-input'))")
    assert "▸ " in disp and "a: 1" not in disp, disp


@then("but the full source is still what a save would read")
@then("the full source is still what a save would read")
def step_value_full(context):
    val = context.page.evaluate("() => document.getElementById('ed-input').value")
    assert val == context.ed_full, "the virtual value lost content:\n" + val


@when("I click the first marker line")
def step_click_marker(context):
    context.page.evaluate('''() => {
      const i = document.getElementById('ed-input');
      const dv = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').get.call(i);
      const pos = dv.search(/\u2060/);
      i.focus(); i.setSelectionRange(pos, pos);
      i.dispatchEvent(new MouseEvent('click', {bubbles: true}));
    }''')


@then("that block is back in place")
def step_unfolded(context):
    n = context.page.evaluate("window._lcEdFold.count()")
    assert n == 1, "expected 1 remaining fold, got %s" % n
    disp = context.page.evaluate(
        "() => Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value')"
        ".get.call(document.getElementById('ed-input'))")
    assert "a: 1" in disp, "the yaml fence did not return"


@then("the gutter numbers stay source-true across the folds")
def step_gutter_source_true(context):
    # "Prose after." sits at a fixed SOURCE line; with both blocks folded the
    # display is far shorter, yet the gutter must still say the source number.
    src_no = context.ed_full.split("\n").index("Prose after.") + 1
    ok = context.page.evaluate('''(n) => {
      const gl = [...document.querySelectorAll('#ed-gutter-inner .ed-gl')];
      return gl.some(d => parseInt(d.textContent, 10) === n);
    }''', src_no)
    assert ok, "source line %s missing from the folded gutter" % src_no


@then("the markers wear their block's icon and type")
def step_marker_outfit(context):
    disp = context.page.evaluate(
        "() => Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value')"
        ".get.call(document.getElementById('ed-input'))")
    assert ".dataset #ds" in disp, "marker lost the dataset outfit:\n" + disp
    assert ".inspector #w" in disp, "marker lost the inspector outfit:\n" + disp
    # icons come from component-model.json — Dataset and Inspector both have one
    assert "\U0001F6E2" in disp or "\U0001F9EC" in disp, \
        "no component icon on any marker:\n" + disp
    # the machine half is invisible now: the count trails in words, the old
    # ⟢f19⟣ token is gone, the fold id rides as zero-width characters
    assert "6 lines" in disp, "no trailing line count:\n" + disp
    assert "⟢" not in disp, "the old visible fold token is back:\n" + disp
    assert "\u2060" in disp, "no invisible fold id on the markers:\n" + disp


@when("I refold it from the gutter arrow")
def step_refold_real_click(context):
    # a REAL pointer click. The arrow used to sit under the gutter's
    # pointer-events:none and only a dispatched event "worked" — this step
    # pins the honest path (Michel, 2026-08-23: "gutter click not working").
    context.page.locator("#ed-gutter-inner .ed-fold-a[data-foldline]").first.click()


@given("a connected editor whose repo serves a two-fence page")
def step_stub_fenced_repo(context):
    import base64
    md = (
        "# Demo\n\nProse before.\n\n"
        "```yaml\na: 1\nb: 2\nc: 3\n```\n"
        '{: .dataset #ds }\n\n'
        "Prose between.\n\n"
        "```python\nx = 1\ny = 2\nz = 3\n```\n"
        '{: .inspector #w }\n\n'
        "Prose after.\n"
    )
    context.ed_full = md
    b64 = base64.b64encode(md.encode()).decode()

    def gh(route):
        url = route.request.url
        if "/git/trees/" in url:
            route.fulfill(json={"sha": "HEAD", "tree": [
                {"path": "docs/events.md", "type": "blob", "sha": "s1"}],
                "truncated": False})
        elif "/contents/" in url:
            route.fulfill(json={"content": b64, "sha": "s1",
                                "name": "events.md", "path": "docs/events.md"})
        else:
            full = url.split("/repos/", 1)[1].split("?")[0]
            route.fulfill(json={"full_name": full, "default_branch": "main",
                                "permissions": {"push": True}})

    context.page.route("https://api.github.com/repos/**", gh)
    context.page.add_init_script(
        "localStorage.setItem('lc_ed_pat','ghp_author');"
        "localStorage.setItem('lc_ed_repo','michelzam/lightcodelab');")


@when("the editor has loaded the page's own file")
def step_wait_served_file(context):
    # the editor auto-targets docs/<page>.md when connected — wait for it
    context.page.wait_for_function(
        "() => document.getElementById('ed-input').value.indexOf('Prose after.') >= 0",
        timeout=15_000)


@then('the draft checker warns only about "{name}"')
def step_lint_only(context, name):
    # the checker is debounced — wait for the genuinely-broken name to land
    context.page.wait_for_function(
        "() => (document.getElementById('ed-lint-panel') || {innerHTML: ''})"
        ".innerHTML.indexOf('%s') >= 0" % name, timeout=15_000)
    items = context.page.evaluate(
        "() => [...document.querySelectorAll('#ed-lint-panel .ed-lint-item .msg')]"
        ".map(e => e.textContent)")
    refs = [m for m in items if "no such id" in m]
    assert len(refs) == 1 and name in refs[0], \
        "reference findings %r — wanted exactly one, about %s" % (refs, name)


@when("I close the page editor")
def step_close_editor(context):
    context.page.locator("#ed-close-btn").click()
    context.page.wait_for_timeout(400)
