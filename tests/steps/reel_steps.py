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


@when("I exit reel mode")
def step_reel_exit(context):
    context.page.evaluate("() => window.lcReel && window.lcReel.exit()")
    context.page.wait_for_timeout(200)
