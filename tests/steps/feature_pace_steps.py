"""The proof's reveal has a pace (feature_pace.feature)."""
import time

from behave import when, then
from playwright.sync_api import expect


@when('the feature "{fid}" is set to a pace of {ms:d} ms')
def step_set_pace(context, fid, ms):
    card = context.page.locator('[data-lc-id="%s"]' % fid)
    expect(card).to_be_attached(timeout=10_000)
    context.page.evaluate("([id, ms]) => document.querySelector('[data-lc-id=\"' + id + '\"]').setAttribute('data-pace', String(ms))", [fid, ms])


def _wait_first_tick(context, fid):
    card = context.page.locator('[data-lc-id="%s"]' % fid)
    first = card.locator(".lc-feature-step-icon.pass").first
    expect(first).to_be_visible(timeout=90_000)     # the runtime's first load is the slow part
    return card, time.monotonic()


@then("its checks arrive one at a time, about {ms:d} ms apart, the bar filling with them")
def step_paced(context, ms):
    card, t0 = _wait_first_tick(context, "temp_feature")
    steps = card.locator(".lc-feature-step-icon").count()
    assert steps >= 2, "a one-step card cannot show a pace"
    bar = card.locator(".lc-feature-progress i")
    expect(bar).to_be_attached()
    width = bar.evaluate("i => i.style.width")
    assert width != "100%", "the bar was already full at the first tick: " + width
    assert card.get_attribute("data-status") != "passing", "the verdict landed before the checks"
    expect(card).to_have_attribute("data-status", "passing", timeout=30_000)
    took = (time.monotonic() - t0) * 1000
    assert took >= (steps - 1) * ms * 0.7, "the checks landed too fast for a pace of %d ms: %.0f ms for %d steps" % (ms, took, steps)
    expect(bar).to_have_attribute("style", "width: 100%;")


@then("its verdict lands at once, without a bar")
def step_natural(context):
    card, t0 = _wait_first_tick(context, "temp_feature")
    expect(card).to_have_attribute("data-status", "passing", timeout=5_000)
    took = (time.monotonic() - t0) * 1000
    assert took < 1500, "natural speed took %.0f ms" % took
    assert card.locator(".lc-feature-progress").count() == 0, "a bar at natural speed"
