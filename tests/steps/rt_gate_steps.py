from behave import then
import re
from playwright.sync_api import expect

# visible="= <feature>.passing" — the cells engine gates blocks on feature
# state. Hidden must mean HIDDEN (computed display none), and open must be
# the real thing, not just a class.


@then('the text "{text}" is hidden')
def step_text_hidden(context, text):
    el = context.page.locator('[visible^="="]', has_text=text).first
    el.wait_for(state="attached", timeout=15_000)
    expect(el).to_be_hidden(timeout=10_000)


@then('the text "{text}" becomes visible')
def step_text_visible(context, text):
    el = context.page.locator('[visible^="="]', has_text=text).first
    expect(el).to_be_visible(timeout=15_000)


@then("a confetti burst appears")
def step_confetti(context):
    # the burst self-cleans in ~2s — catch it (or its reduced-motion twin)
    context.page.wait_for_function(
        "() => document.querySelectorAll('.lc-confetti, .lc-confetti-quiet').length > 0",
        timeout=10_000,
    )


@when("the confetti has cleared")
def step_confetti_cleared(context):
    # the burst removes itself after ~2.3s; wait it out so the next
    # assertion counts a FRESH one
    context.page.wait_for_function(
        "() => document.querySelectorAll('.lc-confetti, .lc-confetti-quiet').length === 0",
        timeout=10_000,
    )


@then("no confetti burst appears")
def step_no_confetti(context):
    context.page.wait_for_timeout(1500)
    n = context.page.evaluate(
        "() => document.querySelectorAll('.lc-confetti, .lc-confetti-quiet').length")
    assert n == 0, "a re-run of a green card threw confetti (%d pieces)" % n


# ── a gate rewritten in the x-ray, and a shut gate under the x-ray ─────────
from behave import given, when


@given('a key that may keep edits to "{repo}"')
def step_key_keeps(context, repo):
    """the editor's Keep commits after it re-renders; the commit is stubbed
    so the scenario is about the page, not the repo"""
    def put(route, req):
        if req.method == "PUT":
            route.fulfill(json={"content": {"sha": "kept-1"}})
        else:
            route.fallback()
    context.page.route("https://api.github.com/repos/" + repo + "/contents/**", put)
    context.page.route("https://api.github.com/repos/" + repo + "/git/trees/**",
                       lambda r: r.fulfill(json={"sha": "HEAD", "tree": [], "truncated": False}))
    context.page.add_init_script(
        "localStorage.setItem('lc_ed_pat', 'ghp_stub');"
        "localStorage.setItem('lc_ed_repo', '" + repo + "');"
    )


def _card(context, cid):
    return context.page.locator('[data-lc-id="' + cid + '"][visible^="="]').first


@then('the card "{cid}" is open')
def step_card_open(context, cid):
    expect(_card(context, cid)).to_be_visible(timeout=15_000)


@then('the card "{cid}" is shut')
def step_card_shut(context, cid):
    el = _card(context, cid)
    el.wait_for(state="attached", timeout=15_000)
    expect(el).to_be_hidden(timeout=15_000)


@when('I rewrite the gate of "{cid}" to "{expr}" in the x-ray')
def step_rewrite_gate(context, cid, expr):
    card = context.page.locator('[data-lc-id="' + cid + '"]').first
    card.scroll_into_view_if_needed()
    context.page.wait_for_timeout(300)
    card.evaluate("el => el.dispatchEvent(new PointerEvent('pointermove', {altKey: true, bubbles: true, cancelable: true}))")
    context.page.wait_for_timeout(600)
    context.page.locator("#lcx-gear").click(force=True)
    knob = context.page.locator("#lcx-edit-body input[data-knob='visible']")
    expect(knob).to_be_visible(timeout=5_000)
    knob.fill(expr)
    context.page.click("#lcx-keep")
    context.page.wait_for_timeout(1500)


@when('the form "{fid}" gets "{key}" = "{value}"')
def step_form_set(context, fid, key, value):
    context.page.evaluate("([f, k, v]) => window.lcFormSet(f, k, v)", [fid, key, value])
    context.page.wait_for_timeout(800)


@when("the x-ray looks at the page")
def step_xray_looks(context):
    context.page.locator("h1").first.evaluate(
        "el => el.dispatchEvent(new PointerEvent('pointermove', {altKey: true, bubbles: true, cancelable: true}))")
    context.page.wait_for_timeout(600)
    expect(context.page.locator("body")).to_have_class(re.compile(r"lc-xray-deco"), timeout=5_000)


@then('the card "{cid}" stands as a ghost')
def step_card_ghost(context, cid):
    el = _card(context, cid)
    expect(el).to_be_visible(timeout=5_000)
    assert "lc-vis-show" not in (el.get_attribute("class") or ""), "the ghost is a real open, not a ghost"


@then('the gear can be summoned on "{cid}"')
def step_gear_on(context, cid):
    card = context.page.locator('[data-lc-id="' + cid + '"]').first
    card.evaluate("el => el.dispatchEvent(new PointerEvent('pointermove', {altKey: true, bubbles: true, cancelable: true}))")
    expect(context.page.locator("#lcx-gear")).to_be_visible(timeout=5_000)


@when('the form "{fid}" gets "{key}" cleared')
def step_form_clear(context, fid, key):
    step_form_set(context, fid, key, "")
