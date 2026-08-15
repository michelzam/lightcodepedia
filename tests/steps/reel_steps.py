import re

from behave import when, then
from playwright.sync_api import expect


@then("the page is in reel mode")
def step_reel_on(context):
    expect(context.page.locator("body")).to_have_class(
        re.compile(r"\blc-reel-active\b"), timeout=10_000
    )


@then("the page is not in reel mode")
def step_reel_off(context):
    expect(context.page.locator("body")).not_to_have_class(
        re.compile(r"\blc-reel-active\b"), timeout=10_000
    )


@then("the content is a vertical scroll-snap container")
def step_reel_snap(context):
    snap = context.page.evaluate(
        "() => getComputedStyle(document.querySelector('main.markdown-body')).scrollSnapType"
    )
    assert snap and "y" in snap, "expected a y scroll-snap container, got %r" % (snap,)


@then("the reel shows a sticky title bar")
def step_reel_bar(context):
    expect(context.page.locator(".lc-reel-bar")).to_be_visible(timeout=10_000)
    # the bar carries the page's common title (non-empty) and a position counter
    expect(context.page.locator(".lc-reel-bar-title")).to_contain_text(
        re.compile(r"\S"), timeout=10_000
    )
    expect(context.page.locator(".lc-reel-bar-progress")).to_contain_text(
        "/", timeout=10_000
    )


@when("I exit reel mode")
def step_reel_exit(context):
    context.page.evaluate("() => window.lcReel && window.lcReel.exit()")
    context.page.wait_for_timeout(200)


@when("I enter reel mode")
def step_reel_enter(context):
    context.page.evaluate("() => window.lcReel && window.lcReel.enter()")
    context.page.wait_for_timeout(300)


@when("I press the browser back button")
def step_reel_back(context):
    # same-document history entry (pushed on reel enter) — fire popstate
    context.page.evaluate("() => history.back()")
    context.page.wait_for_timeout(500)


@when("I click the reel back button")
def step_reel_back_btn(context):
    context.page.locator(".lc-reel-back").click()
    context.page.wait_for_timeout(500)


# ── the title, and only the title ──────────────────────────────────────────
# The engine paints a page's tags as pills inside its own h1. A raw
# textContent read of that heading therefore returns the title WELDED to
# every tag ("🧱 Blockui"), and that string was what the reel bar and the
# section picker showed (Michel, 2026-08-14).


@then("the page's title carries tag pills")
def step_title_has_pills(context):
    pills = context.page.evaluate(
        "() => [...document.querySelectorAll('.lc-title-tag')].map(e => e.textContent.trim())"
    )
    assert pills, "this page grew no tag pills — the scenario proves nothing here"
    context.title_pills = pills


@then("the reel bar shows the title without the pills")
def step_bar_title_clean(context):
    shown = (
        context.page.evaluate(
            "() => (document.querySelector('.lc-reel-bar-title') || {}).textContent"
        )
        or ""
    ).strip()
    assert shown, "the reel bar has no title"
    for pill in context.title_pills:
        assert not shown.endswith(pill), "the bar welded a tag onto the title: %r" % shown
        assert pill not in shown.replace(" ", ""), (
            "the bar shows the tag %r inside the title: %r" % (pill, shown)
        )


@then("the section picker shows titles without the pills")
def step_picker_titles_clean(context):
    opts = context.page.evaluate(
        "() => [...document.querySelectorAll('.lc-slides-nav-jump option')].map(o => o.textContent)"
    )
    assert opts, "no section picker to check"
    for pill in context.title_pills:
        for label in opts:
            assert pill not in label.replace(" ", ""), (
                "a picker label welded the tag %r: %r" % (pill, label)
            )


# ── keyboard paging ────────────────────────────────────────────────────────


def _reel_at(context):
    txt = (
        context.page.evaluate(
            "() => (document.querySelector('.lc-reel-bar-progress') || {}).textContent"
        )
        or ""
    )
    return txt.split("/")[0].strip()


@then('the reel is at section {n}')
def step_reel_at(context, n):
    for _ in range(20):
        if _reel_at(context) == n:
            return
        context.page.wait_for_timeout(150)
    assert False, "expected section %s, the bar says %r" % (n, _reel_at(context))


@when("I press the down arrow")
def step_reel_down(context):
    context.page.keyboard.press("ArrowDown")
    context.page.wait_for_timeout(400)


@when("I press the up arrow")
def step_reel_up(context):
    context.page.keyboard.press("ArrowUp")
    context.page.wait_for_timeout(400)
