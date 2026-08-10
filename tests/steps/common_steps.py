import os
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
# LOCAL HARNESS ONLY: a sandbox that cannot reach live services (map tile
# servers, …) adds their hostnames here via the env, comma-separated. CI
# never sets it, so a real regression cannot hide behind this.
JS_ERROR_IGNORE |= set(filter(None, os.environ.get(
    "JS_ERROR_IGNORE_EXTRA", "").split(",")))


@given("I have a clean browser page")
def step_clean_page(context):
    context.js_errors = []
    def _console(msg):
        if msg.type != "error":
            return
        # a resource error's text never names the resource — Chrome puts the
        # URL in location, and without it a 404 is undiagnosable from the
        # assertion message alone (2026-08-10)
        url = (msg.location or {}).get("url", "")
        text = msg.text + (f"  [{url}]" if url else "")
        if not any(s in text for s in JS_ERROR_IGNORE):
            context.js_errors.append(text)

    context.page.on("console", _console)
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


@then("the topbar brand shows this node's emoji and name")
def step_brand_names_node(context):
    # The brand is dynamic (repo-derived), never static text: an emoji marking
    # the node kind (🧪 lab, 💡 pedia/forks) + the repo's short name. Assert the
    # shape, not a hardcoded site name, so the same scenario passes on every node.
    brand = context.page.locator(".lc-brand")
    expect(brand).to_be_visible()
    text = brand.inner_text().strip()
    assert re.match(r"^(🧪|💡)\s\S+$", text), f"brand looks wrong: {text!r}"
