import re
from behave import when, then, step
from playwright.sync_api import expect

# Selectors — adjust if DOM structure changes
SEL_GRID = "[data-lc-type='datagrid'], .ag-root-wrapper, [class*='lc-datagrid']"
SEL_CHART = "[data-lc-type='chart'], canvas[data-lc-id]"
SEL_BUTTON = "[data-lc-type='button'], .lc-btn"
SEL_XRAY_PANEL = ".lcx-xray"
SEL_FAB = ".lc-slides-fab"
SEL_POPUP = "#lc-bl-popup"
SEL_XRAY_BTN = "#lc-bl-xray-btn"
SEL_PRESENT_BTN = "#lc-bl-present-btn"


@when("I hover over the first grid component")
def step_hover_grid(context):
    el = context.page.locator(SEL_GRID).first
    el.wait_for(state="visible", timeout=15_000)
    el.hover()
    # Give x-ray update() time to fire and paint the panel
    context.page.wait_for_timeout(800)


@when("I hover over the chart component")
def step_hover_chart(context):
    el = context.page.locator(SEL_CHART).first
    el.wait_for(state="visible", timeout=15_000)
    el.hover()
    context.page.wait_for_timeout(800)


@when("I hover over a button component")
def step_hover_button(context):
    el = context.page.locator(SEL_BUTTON).first
    el.wait_for(state="visible", timeout=15_000)
    el.hover()
    context.page.wait_for_timeout(800)


@then("an x-ray panel is visible")
def step_xray_visible(context):
    panel = context.page.locator(SEL_XRAY_PANEL).first
    expect(panel).to_be_visible(timeout=8_000)


@then("the x-ray panel shows a component class name")
def step_xray_has_class(context):
    panel = context.page.locator(SEL_XRAY_PANEL).first
    text = panel.inner_text()
    assert text.strip(), "X-ray panel is empty"


@then('the x-ray panel mentions "{keyword}"')
def step_xray_mentions(context, keyword):
    panel = context.page.locator(SEL_XRAY_PANEL).first
    expect(panel).to_contain_text(keyword, timeout=3_000)


@then("the x-ray panel shows a code block")
def step_xray_has_code(context):
    code = context.page.locator(".lcx-xray .code").first
    expect(code).to_be_visible(timeout=3_000)


@then("the x-ray panel is within the viewport bounds")
def step_xray_in_viewport(context):
    vw = context.page.evaluate("window.innerWidth")
    vh = context.page.evaluate("window.innerHeight")
    panel = context.page.locator(SEL_XRAY_PANEL).first
    box = panel.bounding_box()
    assert box is not None, "Could not get x-ray panel bounding box"
    assert box["x"] >= 0, f"Panel overflows left: x={box['x']}"
    assert box["y"] >= 0, f"Panel overflows top: y={box['y']}"
    assert box["x"] + box["width"] <= vw + 4, (
        f"Panel overflows right: x+w={box['x']+box['width']} > vw={vw}"
    )
    assert box["y"] + box["height"] <= vh + 4, (
        f"Panel overflows bottom: y+h={box['y']+box['height']} > vh={vh}"
    )


# --- FAB / touch steps ---

@then("the slides FAB button is visible")
def step_fab_visible(context):
    expect(context.page.locator(SEL_FAB)).to_be_visible(timeout=10_000)


@when("I click the slides FAB button")
def step_click_fab(context):
    fab = context.page.locator(SEL_FAB)
    expect(fab).to_be_visible(timeout=10_000)
    fab.click()
    context.page.wait_for_timeout(300)


@step("I tap the slides FAB button")
def step_tap_fab(context):
    fab = context.page.locator(SEL_FAB)
    expect(fab).to_be_visible(timeout=10_000)
    fab.tap()
    context.page.wait_for_timeout(400)


@when("I tap the X-ray option in the popup")
def step_tap_xray_option(context):
    btn = context.page.locator(SEL_XRAY_BTN)
    expect(btn).to_be_visible(timeout=3_000)
    btn.tap()
    context.page.wait_for_timeout(300)


@when("I click the Present option in the popup")
def step_click_present(context):
    btn = context.page.locator(SEL_PRESENT_BTN)
    expect(btn).to_be_visible(timeout=3_000)
    btn.click()
    context.page.wait_for_timeout(300)


@step("I tap the first grid component")
def step_tap_grid(context):
    el = context.page.locator(SEL_GRID).first
    el.wait_for(state="visible", timeout=15_000)
    el.tap()
    context.page.wait_for_timeout(400)


@then("the FAB popup is visible")
def step_popup_visible(context):
    expect(context.page.locator(SEL_POPUP)).to_be_visible(timeout=3_000)


@then("the FAB popup is not visible")
def step_popup_hidden(context):
    expect(context.page.locator(SEL_POPUP)).to_be_hidden(timeout=3_000)


@then('the popup contains a "{label}" option')
def step_popup_has_option(context, label):
    popup = context.page.locator(SEL_POPUP)
    expect(popup).to_contain_text(label, timeout=2_000)


@then("the popup contains an X-ray option")
def step_popup_has_xray(context):
    expect(context.page.locator(SEL_XRAY_BTN)).to_be_visible(timeout=2_000)


@then("the FAB button has the xray-active style")
def step_fab_active(context):
    fab = context.page.locator(SEL_FAB)
    expect(fab).to_have_class(re.compile(r"lc-xray-active"), timeout=3_000)


@then("the FAB button does not have the xray-active style")
def step_fab_inactive(context):
    fab = context.page.locator(SEL_FAB)
    expect(fab).not_to_have_class(re.compile(r"lc-xray-active"), timeout=3_000)
