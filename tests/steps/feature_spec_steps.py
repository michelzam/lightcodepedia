from behave import when, then
from playwright.sync_api import expect


def _unfold(page):
    """A fenced accordion renders its body only when a reader opens it — so a
    page whose demo lives in a panel has no demo until then (the pitch
    elevator, 2026-09-01). The suite opens every fold first: where the author
    put the demo is not the suite's business."""
    page.evaluate(
        "document.querySelectorAll('details').forEach(function(d){ d.open = true; });")
    page.wait_for_timeout(400)


@when('I wait for the selector "{css}"')
def step_wait_selector(context, css):
    # file-backed components (e.g. tabs) render after an async fetch; wait for
    # them to exist before driving them from the in-page runner.
    _unfold(context.page)
    context.page.locator(css).first.wait_for(state="visible", timeout=20_000)


@when('I wait for {n:d} elements matching "{css}"')
def step_wait_count(context, n, css):
    # AG Grid renders rows progressively — the first row appearing does not mean
    # all rows are in the DOM. Wait for the exact count before asserting on it.
    expect(context.page.locator(css)).to_have_count(n, timeout=20_000)


@when("I run the page's embedded features")
def step_run_features(context):
    # cards upgrade after the render settles — on a cold load the fence is
    # still plain text for a beat, and counting buttons then is a race
    context.page.locator(".lc-feature").first.wait_for(
        state="attached", timeout=30_000
    )
    # Hidden features (visible=false) render display:none. Un-hide so their
    # ▶ Run buttons are interactable, then click each one.
    context.page.evaluate(
        "document.querySelectorAll('.lc-feature')"
        ".forEach(function(c){ c.classList.remove('lc-feature-hidden'); });"
    )
    # A proof may live in a folded section — and a fenced panel has not even
    # rendered until it is opened (2026-09-01).
    _unfold(context.page)
    btns = context.page.locator(".lc-feature .lc-feature-run")
    btns.first.wait_for(state="visible", timeout=20_000)
    n = btns.count()
    assert n > 0, "no runnable embedded features found on page"
    for i in range(n):
        btn = btns.nth(i)
        # async widgets (e.g. related-card grids) can still be settling and shift
        # layout under the button; scroll it in and give the click room.
        btn.scroll_into_view_if_needed(timeout=10_000)
        btn.click(timeout=20_000)


@then("every embedded feature passes")
def step_features_pass(context):
    cards = context.page.locator(".lc-feature")
    n = cards.count()
    assert n > 0, "no embedded features on page"
    for i in range(n):
        # the passing badge appears only when the MicroPython runner finishes green
        try:
            expect(
                cards.nth(i).locator(".lc-feature-badge-passing")
            ).to_be_visible(timeout=45_000)
        except AssertionError:
            # surface the in-page runner's own error text (step + builtin rows)
            # which never reaches behave otherwise — makes failures diagnosable
            try:
                detail = (cards.nth(i).inner_text() or "")[:1200]
            except Exception as e:
                detail = "<could not read feature card: %s>" % e
            raise AssertionError(
                "embedded feature #%d did not pass.\n--- card ---\n%s" % (i, detail)
            )
