import re

from behave import when, then
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
