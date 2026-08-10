from behave import when, then
from playwright.sync_api import expect

# Three.js loads lazily from CDN, so the hive can take a while to appear
LOOP_TIMEOUT = 25_000

SEL_CANVAS = ".lc-build-loop canvas"
SEL_CHIP = ".lc-bl-legend button"
SEL_READ = ".lc-bl-read"
SEL_SPIN = ".lc-bl-bar button"
SEL_PIN = ".lc-bl-pin"


@then("the build loop canvas is visible")
def step_canvas_visible(context):
    expect(context.page.locator(SEL_CANVAS).first).to_be_visible(timeout=LOOP_TIMEOUT)


@then("the build loop shows {count:d} station chips")
def step_chip_count(context, count):
    chips = context.page.locator(SEL_CHIP)
    expect(chips).to_have_count(count, timeout=LOOP_TIMEOUT)


@then('the build loop chips include "{label}"')
def step_chip_named(context, label):
    expect(context.page.locator(SEL_CHIP, has_text=label).first).to_be_visible(
        timeout=LOOP_TIMEOUT
    )


@when('I hover the build loop chip "{label}"')
def step_hover_chip(context, label):
    chip = context.page.locator(SEL_CHIP, has_text=label).first
    chip.wait_for(state="visible", timeout=LOOP_TIMEOUT)
    chip.hover()
    context.page.wait_for_timeout(250)


@then('the build loop readout mentions "{snippet}"')
def step_readout(context, snippet):
    expect(context.page.locator(SEL_READ).first).to_contain_text(
        snippet, timeout=5_000
    )


@then("the page shows {count:d} build loops")
def step_loop_count(context, count):
    expect(context.page.locator(".lc-build-loop")).to_have_count(
        count, timeout=LOOP_TIMEOUT
    )


@when('I pin the build loop station "{label}"')
def step_pin_station(context, label):
    chip = context.page.locator(SEL_CHIP, has_text=label).first
    chip.wait_for(state="visible", timeout=LOOP_TIMEOUT)
    chip.click()
    context.page.wait_for_timeout(350)


@then("{count:d} legend is pinned to the loop")
@then("{count:d} legends are pinned to the loop")
def step_pin_count(context, count):
    expect(context.page.locator(SEL_PIN)).to_have_count(count, timeout=LOOP_TIMEOUT)


@then('the pinned legend mentions "{snippet}"')
def step_pin_text(context, snippet):
    expect(context.page.locator(SEL_PIN).first).to_contain_text(
        snippet, timeout=5_000
    )


@then("the pinned legend follows its station")
def step_pin_follows(context):
    """The card is re-anchored every frame, so a turning hive must move it."""
    card = context.page.locator(SEL_PIN).first
    card.wait_for(state="visible", timeout=LOOP_TIMEOUT)
    first = card.evaluate("el => el.style.transform")
    context.page.wait_for_timeout(1_500)
    second = card.evaluate("el => el.style.transform")
    assert first and second, f"legend has no anchor transform: {first!r} {second!r}"
    assert first != second, f"legend did not follow its station (stuck at {first})"


def _call_verb(context, verb, arg):
    """Exactly the path an avatar line takes: window.lcVerbs.act(verb, el, arg)."""
    ok = context.page.evaluate(
        "([v, a]) => window.lcVerbs.act(v, null, a)", [verb, arg]
    )
    assert ok, f'verb {verb}({arg!r}) was refused'
    context.page.wait_for_timeout(400)


@when('the narrator calls "{verb}" with "{arg}" on the loop')
def step_verb(context, verb, arg):
    _call_verb(context, verb, arg)


# behave's {arg} placeholder cannot match an empty quoted string — the
# bare-unpin step shipped UNDEFINED and pedia's full suite was the first
# behave parse to say so (2026-08-10). The argless call gets its own words.
@when('the narrator calls "{verb}" with nothing on the loop')
def step_verb_bare(context, verb):
    _call_verb(context, verb, None)


@then('the narrator verb "{verb}" with "{arg}" is refused')
def step_verb_refused(context, verb, arg):
    ok = context.page.evaluate(
        "([v, a]) => window.lcVerbs.act(v, null, a === '' ? null : a)", [verb, arg]
    )
    assert not ok, f'verb {verb}("{arg}") should have been refused'


@when("I click the build loop spin button")
def step_click_spin(context):
    btn = context.page.locator(SEL_SPIN).first
    btn.wait_for(state="visible", timeout=LOOP_TIMEOUT)
    btn.click()
    context.page.wait_for_timeout(200)


@then("the build loop spin button offers to resume")
def step_spin_paused(context):
    expect(context.page.locator(SEL_SPIN).first).to_contain_text(
        "spin", timeout=5_000
    )
    expect(context.page.locator(SEL_SPIN).first).not_to_contain_text(
        "pause", timeout=5_000
    )
