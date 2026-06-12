from behave import then
from playwright.sync_api import expect


@then("the vitals card shows at least {n:d} samples")
def step_vitals_samples(context, n):
    # one sample lands immediately, the rest on the interval (2 s default)
    context.page.wait_for_function(
        "(n) => { const v = document.querySelector('.lc-vitals');"
        " return v && parseInt(v.getAttribute('data-samples') || 0) >= n; }",
        arg=n,
        timeout=20_000,
    )


@then("the model check card reports no broken references")
def step_modelcheck_card(context):
    card = context.page.locator(".lc-modelcheck")
    expect(card).to_be_visible(timeout=15_000)
    # the card re-checks at 0.8/3/7 s while async components settle
    context.page.wait_for_function(
        "() => { const c = document.querySelector('.lc-modelcheck');"
        " return c && c.getAttribute('data-broken') === '0'"
        " && parseInt(c.getAttribute('data-checked') || 0) > 0; }",
        timeout=20_000,
    )


@then("the page passes the model integrity check")
def step_modelcheck_page(context):
    try:
        context.page.wait_for_function(
            "() => { if (!window.lcModelCheck) return false;"
            " const r = window.lcModelCheck();"
            " return r.checked > 0 && r.broken.length === 0; }",
            timeout=20_000,
        )
    except Exception:
        detail = context.page.evaluate(
            "window.lcModelCheck ? JSON.stringify(window.lcModelCheck()) : 'lcModelCheck missing'"
        )
        raise AssertionError(f"model integrity failed: {detail}")
