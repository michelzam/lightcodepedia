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


# ── double navigation: ←/→ + « » + swipe = sections, ↑/↓ = blocks ──────────


@when("I press the right arrow")
def step_reel_right(context):
    context.page.keyboard.press("ArrowRight")
    context.page.wait_for_timeout(400)


@when("I press the left arrow")
def step_reel_left(context):
    context.page.keyboard.press("ArrowLeft")
    context.page.wait_for_timeout(400)


@when("I click the next-section chevron")
def step_reel_chevron(context):
    context.page.click('.lc-reel-sec[data-sec="1"]')
    context.page.wait_for_timeout(400)


def _swipe(context, from_x, to_x, selector="main.markdown-body"):
    """Synthesize the touch pair the engine listens for: touchstart at
    from_x, touchend at to_x, on the given surface."""
    context.page.evaluate(
        """([sel, x0, x1]) => {
             const el = document.querySelector(sel);
             const mk = (x) => new Touch({ identifier: 1, target: el,
                                           clientX: x, clientY: 300 });
             el.dispatchEvent(new TouchEvent('touchstart',
               { bubbles: true, touches: [mk(x0)], changedTouches: [mk(x0)] }));
             el.dispatchEvent(new TouchEvent('touchend',
               { bubbles: true, touches: [], changedTouches: [mk(x1)] }));
           }""",
        [selector, from_x, to_x],
    )
    context.page.wait_for_timeout(400)


@when("I swipe right-to-left on neutral ground")
def step_swipe_next(context):
    _swipe(context, 320, 60, "main.markdown-body .lc-slide h2")


@when("I swipe left-to-right on neutral ground")
def step_swipe_prev(context):
    _swipe(context, 60, 320, "main.markdown-body .lc-slide h2")


@when("I swipe right-to-left over a guarded surface")
def step_swipe_guarded(context):
    # a fenced code block owns its own horizontal scroll — the reel must
    # not steal a drag that starts there
    _swipe(context, 320, 60, ".lc-slide pre")


@then("the reel scrolled to align a block under the bar")
def step_block_aligned(context):
    """After ↓ the scroller has moved, and SOME top-level block sits at the
    snap line (the bar clearance) — a whole idea, not a mid-paragraph cut."""
    ok = False
    for _ in range(20):
        ok = context.page.evaluate(
            """() => {
                 const scrolled = [...document.querySelectorAll('.markdown-body')]
                   .some(m => m.scrollTop > 10);
                 if (!scrolled) return false;
                 const blocks = [...document.querySelectorAll('.lc-slide > *')];
                 return blocks.some(b => Math.abs(b.getBoundingClientRect().top - 56) < 24);
               }"""
        )
        if ok:
            break
        context.page.wait_for_timeout(150)
    assert ok, "no block landed at the snap line after ArrowDown"


@then("the reel is back at the top")
def step_reel_top(context):
    for _ in range(20):
        top = context.page.evaluate(
            "() => Math.max(...[...document.querySelectorAll('.markdown-body')].map(m => m.scrollTop))"
        )
        if top < 10:
            return
        context.page.wait_for_timeout(150)
    assert False, "the reel did not return to the top, scrollTop=%s" % top


@then("the reel bar title is the current section's heading")
def step_bar_names_section(context):
    got = context.page.evaluate(
        """() => {
             const i = (() => {
               const main = document.querySelector('main.markdown-body');
               const top = main.getBoundingClientRect().top;
               let best = 0, d0 = Infinity;
               document.querySelectorAll('.lc-slide').forEach((s, i) => {
                 const d = Math.abs(s.getBoundingClientRect().top - top);
                 if (d < d0) { d0 = d; best = i; }
               });
               return best;
             })();
             const s = document.querySelectorAll('.lc-slide')[i];
             const h = s.querySelector('h2, h1');
             return { bar: (document.querySelector('.lc-reel-bar-title') || {}).textContent,
                      heading: h ? h.textContent : '' };
           }"""
    )
    bar = (got["bar"] or "").strip()
    assert bar, "the bar is empty"
    # the heading may carry tag pills; the bar text must be its clean prefix
    assert got["heading"].startswith(bar), "bar %r vs heading %r" % (bar, got["heading"])
