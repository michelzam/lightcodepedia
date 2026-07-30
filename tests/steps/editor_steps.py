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
