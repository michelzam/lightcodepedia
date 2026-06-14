import re

from behave import when, then
from playwright.sync_api import expect


@when("I open the page editor")
def step_open_editor(context):
    fab = context.page.locator("#ed-fab")
    fab.wait_for(state="visible", timeout=15_000)
    fab.click()
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
