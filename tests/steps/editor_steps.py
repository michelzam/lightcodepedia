from behave import when, then
from playwright.sync_api import expect


@when("I open the page editor")
def step_open_editor(context):
    fab = context.page.locator("#ed-fab")
    fab.wait_for(state="visible", timeout=15_000)
    fab.click()
    expect(context.page.locator("#ed-drawer")).to_have_class(
        # the drawer adds the "open" class when shown
        __import__("re").compile(r"\bopen\b"), timeout=10_000
    )


@when('I switch to the editor "{name}" tab')
def step_switch_tab(context, name):
    tab = context.page.locator(".ed-tab[data-tab='" + name + "']")
    tab.wait_for(state="visible", timeout=10_000)
    tab.click()
    context.page.wait_for_timeout(200)


@then("the editor agent pane shows a prompt box")
def step_agent_prompt_visible(context):
    expect(context.page.locator("#ed-agent-prompt")).to_be_visible(timeout=10_000)
