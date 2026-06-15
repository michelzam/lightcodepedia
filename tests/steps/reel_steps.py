import re

from behave import when, then
from playwright.sync_api import expect


@then("the page is in reel mode")
def step_reel_on(context):
    expect(context.page.locator("body")).to_have_class(
        re.compile(r"\blc-reel-active\b"), timeout=10_000
    )


@then("the page is not in reel mode")
def step_reel_off(context):
    expect(context.page.locator("body")).not_to_have_class(
        re.compile(r"\blc-reel-active\b"), timeout=10_000
    )


@then("the content is a vertical scroll-snap container")
def step_reel_snap(context):
    snap = context.page.evaluate(
        "() => getComputedStyle(document.querySelector('main.markdown-body')).scrollSnapType"
    )
    assert snap and "y" in snap, "expected a y scroll-snap container, got %r" % (snap,)


@then("the reel shows a sticky title bar")
def step_reel_bar(context):
    expect(context.page.locator(".lc-reel-bar")).to_be_visible(timeout=10_000)
    # the bar carries the page's common title (non-empty) and a position counter
    expect(context.page.locator(".lc-reel-bar-title")).to_contain_text(
        re.compile(r"\S"), timeout=10_000
    )
    expect(context.page.locator(".lc-reel-bar-progress")).to_contain_text(
        "/", timeout=10_000
    )


@when("I exit reel mode")
def step_reel_exit(context):
    context.page.evaluate("() => window.lcReel && window.lcReel.exit()")
    context.page.wait_for_timeout(200)


@when("I enter reel mode")
def step_reel_enter(context):
    context.page.evaluate("() => window.lcReel && window.lcReel.enter()")
    context.page.wait_for_timeout(300)


@when("I press the browser back button")
def step_reel_back(context):
    # same-document history entry (pushed on reel enter) — fire popstate
    context.page.evaluate("() => history.back()")
    context.page.wait_for_timeout(500)


@when("I click the reel back button")
def step_reel_back_btn(context):
    context.page.locator(".lc-reel-back").click()
    context.page.wait_for_timeout(500)
