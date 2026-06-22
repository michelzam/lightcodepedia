from behave import when, then
from playwright.sync_api import expect


@when('I wait for the selector "{css}"')
def step_wait_selector(context, css):
    # file-backed components (e.g. tabs) render after an async fetch; wait for
    # them to exist before driving them from the in-page runner.
    context.page.locator(css).first.wait_for(state="visible", timeout=20_000)


@when("I run the page's embedded features")
def step_run_features(context):
    # Hidden features (visible=false) render display:none. Un-hide so their
    # ▶ Run buttons are interactable, then click each one.
    context.page.evaluate(
        "document.querySelectorAll('.lc-feature')"
        ".forEach(function(c){ c.classList.remove('lc-feature-hidden'); });"
    )
    btns = context.page.locator(".lc-feature .lc-feature-run")
    n = btns.count()
    assert n > 0, "no runnable embedded features found on page"
    for i in range(n):
        btns.nth(i).click()


@then("every embedded feature passes")
def step_features_pass(context):
    cards = context.page.locator(".lc-feature")
    n = cards.count()
    assert n > 0, "no embedded features on page"
    for i in range(n):
        # the passing badge appears only when the MicroPython runner finishes green
        expect(
            cards.nth(i).locator(".lc-feature-badge-passing")
        ).to_be_visible(timeout=45_000)
