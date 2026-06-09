import re
from behave import given, when, then
from playwright.sync_api import expect

JS_ERROR_IGNORE = {
    "favicon",
    "ResizeObserver loop",
    "Non-Error promise rejection",
}


@given("I have a clean browser page")
def step_clean_page(context):
    context.js_errors = []
    context.page.on("console", lambda msg: (
        context.js_errors.append(msg.text)
        if msg.type == "error" and not any(s in msg.text for s in JS_ERROR_IGNORE)
        else None
    ))
    context.page.on("pageerror", lambda err: context.js_errors.append(str(err)))


@when('I navigate to "{path}"')
def step_navigate(context, path):
    context.page.goto(context.base_url + path, wait_until="domcontentloaded")


@when("I wait for the page to be interactive")
def step_wait_interactive(context):
    # Use "load" rather than "networkidle" — WASM downloads keep network busy indefinitely
    context.page.wait_for_load_state("load", timeout=20_000)
    context.page.wait_for_timeout(800)


@then("the LC platform is loaded")
def step_lc_loaded(context):
    # FAB is injected by the LC runtime on every page — proves JS ran
    expect(context.page.locator(".lc-slides-fab")).to_be_visible(timeout=10_000)


@then("there are no JS console errors")
def step_no_js_errors(context):
    assert not context.js_errors, (
        f"JS errors found:\n" + "\n".join(context.js_errors)
    )
