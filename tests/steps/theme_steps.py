import re
from behave import when, then
from playwright.sync_api import expect

# The "High contrast" display toggle lives in the bottom-left pill (slides.md).
# The FAB / popup steps it leans on ("I tap the slides FAB button", the popup
# contains "{label}" option) come from xray_steps.py — behave loads every step
# module globally, so this file only adds what is contrast-specific.

SEL_CONTRAST_BTN = "#lc-bl-contrast-btn"


@when("I click the High contrast option in the popup")
def step_click_contrast(context):
    btn = context.page.locator(SEL_CONTRAST_BTN)
    expect(btn).to_be_visible(timeout=3_000)
    btn.click()
    context.page.wait_for_timeout(300)


@then("the page uses the high-contrast theme")
def step_theme_contrast(context):
    expect(context.page.locator("html")).to_have_attribute(
        "data-theme", "contrast", timeout=3_000
    )


@then("the page uses the default theme")
def step_theme_default(context):
    # default = the attribute is absent (no override), never the string "contrast"
    value = context.page.locator("html").get_attribute("data-theme")
    assert value != "contrast", f'expected default theme, got data-theme={value!r}'


@then("the High contrast option is marked active")
def step_contrast_marked(context):
    btn = context.page.locator(SEL_CONTRAST_BTN)
    expect(btn).to_have_class(re.compile(r"lc-mode-on"), timeout=3_000)
    expect(btn).to_have_attribute("aria-checked", "true", timeout=3_000)
