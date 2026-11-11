from behave import when, then
from playwright.sync_api import expect

# Three.js + js-yaml load lazily from CDN, so the scene can take a while
SCENE_TIMEOUT = 25_000

SEL_CANVAS = ".lc-scene3d canvas"
SEL_CARD = ".lc-s3d-card"
SEL_METHOD_BTN = ".lc-s3d-methods button"
SEL_CONSOLE = ".lc-s3d-console"


@then("the 3D scene canvas is visible")
def step_canvas_visible(context):
    expect(context.page.locator(SEL_CANVAS).first).to_be_visible(timeout=SCENE_TIMEOUT)


@then('the scene shows an attribute panel for "{title}"')
def step_panel_for(context, title):
    card = context.page.locator(SEL_CARD, has_text=title).first
    expect(card).to_be_visible(timeout=SCENE_TIMEOUT)


@when('I call the "{name}" method on the scene')
def step_call_method(context, name):
    btn = context.page.locator(SEL_METHOD_BTN, has_text=name + "()").first
    btn.wait_for(state="visible", timeout=SCENE_TIMEOUT)
    btn.click()
    context.page.wait_for_timeout(300)


@when('I change the dog colour to "{colour}"')
def step_change_colour(context, colour):
    sel = context.page.locator(SEL_CARD + " select").first
    sel.wait_for(state="visible", timeout=SCENE_TIMEOUT)
    sel.select_option(label=colour)
    context.page.wait_for_timeout(300)


@then('the scene console logs "{snippet}"')
def step_console_logs(context, snippet):
    expect(context.page.locator(SEL_CONSOLE).first).to_contain_text(
        snippet, timeout=5_000
    )


@then('the scene\'s "{name}" button is grey')
def step_method_grey(context, name):
    btn = context.page.locator(SEL_METHOD_BTN, has_text=name + "()").first
    btn.wait_for(state="visible", timeout=SCENE_TIMEOUT)
    expect(btn).to_be_disabled()


@then("the scene says Wanda is adopted")
def step_wanda_adopted(context):
    expect(context.page.locator(".lc-s3d-win").first).to_be_visible(timeout=5_000)


@then("the scene says Wanda is not adopted yet")
def step_wanda_not_adopted(context):
    expect(context.page.locator(".lc-s3d-win").first).to_be_hidden()


@then('the scene console never mentions "{snippet}"')
def step_console_never(context, snippet):
    expect(context.page.locator(SEL_CONSOLE).first).not_to_contain_text(snippet)


@then("the scene console still holds its first line, and scrolls")
def step_console_keeps_all(context):
    box = context.page.locator(SEL_CONSOLE).first
    expect(box.locator("div").first).to_contain_text(context.lc_first_console_line)
    assert box.evaluate("e => getComputedStyle(e).overflowY") == "auto", "the console does not scroll"


@when("I call the scene methods {times:d} times, noting the first")
def step_many_calls(context, times):
    btn = context.page.locator(SEL_METHOD_BTN, has_text="run()").first
    btn.wait_for(state="visible", timeout=SCENE_TIMEOUT)
    btn.click()
    context.lc_first_console_line = ">>> lucky.run()"
    for _ in range(times - 1):
        context.page.locator(SEL_METHOD_BTN, has_text="wag_tail()").first.click()
    context.page.wait_for_timeout(300)
