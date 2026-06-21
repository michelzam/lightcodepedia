import re
from behave import given, when, then
from playwright.sync_api import expect

JS_ERROR_IGNORE = {
    "favicon",
    "ResizeObserver loop",
    "Non-Error promise rejection",
    # unauthenticated GitHub API calls get rate-limited from shared CI IPs;
    # the widgets handle it gracefully, but the browser still logs the 403
    "the server responded with a status of 403",
    # CDN libraries probe experimental APIs (Compute Pressure) on load;
    # Chrome logs the rejected probe as an error, functionality unaffected
    "compute-pressure",
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
    # Wait for the DOM, not "load": the load event waits for *every image*, so one
    # slow or dead external image (a CDN that hangs) blocks readiness even though
    # the page is fully interactive — cascading into spurious timeouts. Real
    # interactivity is verified by "the LC platform is loaded" (the runtime-injected
    # FAB) and per-component assertions. ("networkidle" is unusable too — WASM
    # downloads keep the network busy indefinitely.)
    context.page.wait_for_load_state("domcontentloaded", timeout=20_000)
    context.page.wait_for_timeout(800)


@then("the LC platform is loaded")
def step_lc_loaded(context):
    # FAB is always injected by the LC runtime — proves JS ran.
    # On pages without slides it may be hidden (data-no-slides), so check attachment only.
    expect(context.page.locator(".lc-slides-fab")).to_be_attached(timeout=10_000)


@then("there are no JS console errors")
def step_no_js_errors(context):
    assert not context.js_errors, (
        f"JS errors found:\n" + "\n".join(context.js_errors)
    )
