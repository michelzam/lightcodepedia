from behave import when, then
from playwright.sync_api import expect


@then("the vitals card is off")
def step_vitals_off(context):
    card = context.page.locator(".lc-vitals")
    expect(card).to_be_visible(timeout=15_000)
    expect(card).not_to_have_class("lc-vitals on")
    expect(card.locator(".lc-vitals-text")).to_contain_text("off")


@when("I turn the vitals switch on")
def step_vitals_switch_on(context):
    context.page.locator(".lc-vitals-switch").click()
    expect(context.page.locator(".lc-vitals")).to_have_class(
        "lc-vitals on", timeout=5_000
    )


@then("the vitals card shows at least {n:d} samples")
def step_vitals_samples(context, n):
    # one sample lands on switch-on, the rest on the interval (2 s default)
    context.page.wait_for_function(
        "(n) => { const v = document.querySelector('.lc-vitals');"
        " return v && parseInt(v.getAttribute('data-samples') || 0) >= n; }",
        arg=n,
        timeout=20_000,
    )


@then('the "{dataset_id}" grid explains its columns on hover')
def step_grid_hints(context, dataset_id):
    import re as _re
    sel = ".lc-datagrid[data-bind='" + dataset_id + "']"
    th = context.page.locator(sel + " th.lc-th-hint").first
    try:
        expect(th).to_have_attribute("title", _re.compile(r".{10,}"), timeout=15_000)
    except Exception:
        # no more theories: dump what the live DOM actually contains
        evidence = context.page.evaluate(
            "(sel) => {"
            "  const g = document.querySelector(sel);"
            "  const thead = g && g.querySelector('thead');"
            "  return JSON.stringify({"
            "    grid: !!g,"
            "    wrapAttrs: g ? Array.from(g.attributes).map(a => a.name + '=' + a.value.slice(0, 40)) : null,"
            "    thead: thead ? thead.outerHTML.slice(0, 500) : null,"
            "    prettify: typeof window.lcPrettifyKey,"
            "    elemsWithHintsAttr: document.querySelectorAll('[hints]').length,"
            "    unconsumedIALs: Array.from(document.querySelectorAll('p'))"
            "      .filter(x => (x.textContent || '').indexOf('hints=') >= 0)"
            "      .map(x => x.textContent.slice(0, 120)),"
            "    gridsBound: document.querySelectorAll(sel).length,"
            "  });"
            "}",
            sel,
        )
        raise AssertionError("no hinted headers — DOM evidence: " + str(evidence))


@then("the model check card reports no broken references")
def step_modelcheck_card(context):
    card = context.page.locator(".lc-modelcheck")
    expect(card).to_be_visible(timeout=15_000)
    try:
        # the card re-checks at 0.8/3/7 s while async components settle
        context.page.wait_for_function(
            "() => { const c = document.querySelector('.lc-modelcheck');"
            " return c && c.getAttribute('data-broken') === '0'"
            " && parseInt(c.getAttribute('data-checked') || 0) > 0; }",
            timeout=20_000,
        )
    except Exception:
        detail = context.page.evaluate(
            "window.lcModelCheck ? JSON.stringify(window.lcModelCheck()) : 'lcModelCheck missing'"
        )
        raise AssertionError(f"model check card stayed broken: {detail}")


@then('an accordion title mirrors "{txt}"')
def step_acc_live(context, txt):
    context.page.wait_for_function(
        "(t) => Array.from(document.querySelectorAll('.lc-acc-live'))"
        ".some(n => (n.textContent || '').includes(t))",
        arg=txt,
        timeout=15_000,
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
