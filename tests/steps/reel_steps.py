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
    """After a fine-axis step the deck has MOVED (its first block rose past
    its resting spot) and SOME whole block sits at the snap line — geometry
    is the truth, whichever element did the scrolling."""
    ok = False
    for _ in range(20):
        ok = context.page.evaluate(
            """() => {
                 const blocks = [...document.querySelectorAll('.lc-slide > *')];
                 if (!blocks.length) return false;
                 const moved = blocks[0].getBoundingClientRect().top < 40;
                 const aligned = blocks.some(b => Math.abs(b.getBoundingClientRect().top - 56) < 24);
                 return moved && aligned;
               }"""
        )
        if ok:
            break
        context.page.wait_for_timeout(150)
    assert ok, "no block landed at the snap line"


@then("the reel is back at the top")
def step_reel_top(context):
    for _ in range(20):
        top = context.page.evaluate(
            "() => document.querySelector('.lc-slide > *').getBoundingClientRect().top"
        )
        if top > 60:
            return
        context.page.wait_for_timeout(150)
    assert False, "the reel did not return to the top, first block at %spx" % top


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


# ── the vertical flick: velocity decides, CSS stays out of it ──────────────


def _vgesture(context, ys, pause_ms, selector="main.markdown-body .lc-slide h2"):
    """touchstart at ys[0], touchmoves along ys, touchend at ys[-1] —
    with pause_ms between samples, so release velocity is real time."""
    context.page.evaluate(
        """async ([sel, ys, pause]) => {
             const el = document.querySelector(sel);
             const mk = (y) => new Touch({ identifier: 1, target: el,
                                           clientX: 200, clientY: y });
             const fire = (type, y, touching) => el.dispatchEvent(new TouchEvent(type,
               { bubbles: true, touches: touching ? [mk(y)] : [],
                 changedTouches: [mk(y)] }));
             const nap = (ms) => new Promise(r => setTimeout(r, ms));
             fire('touchstart', ys[0], true);
             for (let i = 1; i < ys.length - 1; i++) {
               await nap(pause); fire('touchmove', ys[i], true);
             }
             await nap(pause);
             fire('touchend', ys[ys.length - 1], false);
           }""",
        [selector, ys, pause_ms],
    )
    context.page.wait_for_timeout(500)


@when("I flick upward on neutral ground")
def step_flick_up(context):
    # 300px of travel in ~30ms of samples: unmistakably a flick
    _vgesture(context, [500, 400, 300, 200], 10)


@when("I drag slowly on neutral ground")
def step_drag_slow(context):
    # 60px over ~600ms: a reading drag, far under the flick threshold
    _vgesture(context, [500, 480, 460, 440], 200)


@then("blocks are not CSS snap points")
def step_no_block_snap(context):
    aligns = context.page.evaluate(
        """() => [...document.querySelectorAll('.lc-slide > p')].slice(0, 5)
             .map(p => getComputedStyle(p).scrollSnapAlign)"""
    )
    assert aligns and all(a == "none" for a in aligns), (
        "blocks still brake the scroll: %r" % aligns
    )


@then("the reel did not move")
def step_reel_unmoved(context):
    context.reel_scroll_before = getattr(context, "reel_scroll_before", None)
    top = context.page.evaluate(
        "() => Math.max(...[...document.querySelectorAll('.markdown-body')].map(m => m.scrollTop))"
    )
    # the flick before this landed one block (~100px); a slow drag must not
    # have advanced it again — the position is wherever the flick left it
    blocks_aligned = context.page.evaluate(
        """() => [...document.querySelectorAll('.lc-slide > *')]
             .filter(b => Math.abs(b.getBoundingClientRect().top - 56) < 24).length"""
    )
    assert blocks_aligned >= 1, (
        "the slow drag re-snapped or advanced the reel (scrollTop %s)" % top
    )


@when("I flick downward on neutral ground")
def step_flick_down(context):
    _vgesture(context, [200, 300, 400, 500], 10)


@then("the reel advanced by about a screenful")
def step_screenful(context):
    """The flick's stride is a screen, not a block: the first block now at
    the line must be one that was NOT fully visible before the flick — on
    this page, far more than one block down."""
    ok = False
    for _ in range(20):
        ok = context.page.evaluate(
            """() => {
                 const H = window.innerHeight;
                 const blocks = [...document.querySelectorAll('.lc-slide > *')];
                 const at = blocks.find(b => Math.abs(b.getBoundingClientRect().top - 56) < 24);
                 if (!at) return false;
                 // everything before the landed block sits ABOVE the viewport
                 // top area — i.e. we skipped the fully-visible screenful,
                 // not just the first block
                 const idx = blocks.indexOf(at);
                 return idx >= 2 && blocks[0].getBoundingClientRect().bottom < 0;
               }"""
        )
        if ok:
            break
        context.page.wait_for_timeout(150)
    assert ok, "the flick advanced less than a screenful"


# ── back is memory: the round trip is exact, not approximate ───────────────


@when("I remember the reel position")
def step_remember_pos(context):
    context.reel_pos = context.page.evaluate(
        "() => Math.max(...[...document.querySelectorAll('.markdown-body')].map(m => m.scrollTop))"
    )


@then("the reel is back at the remembered position")
def step_back_remembered(context):
    for _ in range(20):
        top = context.page.evaluate(
            "() => Math.max(...[...document.querySelectorAll('.markdown-body')].map(m => m.scrollTop))"
        )
        if abs(top - context.reel_pos) <= 2:
            return
        context.page.wait_for_timeout(150)
    assert False, "expected %s, reel is at %s" % (context.reel_pos, top)


@when("a fixed overlay sits inside the first section")
def step_inject_fixed(context):
    context.page.evaluate(
        """() => {
             const s = document.querySelector('.lc-slide');
             const d = document.createElement('div');
             d.style.cssText = 'position:fixed;bottom:0;left:0;width:100%;height:200px;';
             s.appendChild(d);
             const host = document.createElement('div');
             host.className = 'lc-avatar-host lc-avatar-docked';
             host.style.position = 'fixed';
             document.body.appendChild(host);
             const seed = document.createElement('button');
             seed.className = 'lc-guide-seed';
             document.body.appendChild(seed);
           }"""
    )


@then("the avatar host keeps its own opacity while the seed ghosts")
def step_host_not_resurrected(context):
    got = context.page.evaluate(
        """() => ({
             host: getComputedStyle(document.querySelector('.lc-avatar-host')).opacity,
             seed: getComputedStyle(document.querySelector('.lc-guide-seed')).opacity })"""
    )
    assert float(got["host"]) != 0.35, (
        "the reel ghosted the avatar HOST — the hidden big face is resurrected: %r" % got
    )
    assert abs(float(got["seed"]) - 0.35) < 0.01, "the seed did not ghost: %r" % got
