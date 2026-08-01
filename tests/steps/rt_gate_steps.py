from behave import then
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
