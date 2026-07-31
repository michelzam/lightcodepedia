import re
from behave import when, then, step
from playwright.sync_api import expect

# Selectors — CSS wrapper classes come from _WRAP in the Python SSOT
SEL_GRID = ".lc-datagrid"
SEL_CHART = ".lc-chart"
SEL_BUTTON = ".lc-button"
SEL_MAP = ".lc-map"
SEL_XRAY_PANEL = ".lcx-xray"
SEL_FAB = ".lc-slides-fab"
SEL_POPUP = "#lc-bl-popup"
SEL_XRAY_BTN = "#lc-bl-xray-btn"
SEL_PRESENT_BTN = "#lc-bl-present-btn"


def _alt_hover(page, locator):
    """Dispatch pointermove with altKey=true over an element to activate x-ray."""
    locator.wait_for(state="visible", timeout=15_000)
    locator.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    box = locator.bounding_box()
    cx = box["x"] + box["width"] / 2
    cy = box["y"] + box["height"] / 2
    page.evaluate(
        "([x, y]) => window.dispatchEvent(new PointerEvent('pointermove',"
        " {clientX: x, clientY: y, altKey: true, bubbles: true, cancelable: true}))",
        [cx, cy]
    )
    page.wait_for_timeout(800)


@when("I hover over the first grid component")
def step_hover_grid(context):
    _alt_hover(context.page, context.page.locator(SEL_GRID).first)


@when("I hover over the chart component")
def step_hover_chart(context):
    _alt_hover(context.page, context.page.locator(SEL_CHART).first)


@when("I hover over the map component")
def step_hover_map(context):
    _alt_hover(context.page, context.page.locator(SEL_MAP).first)


@when("I hover over the scene3d component")
def step_hover_scene3d(context):
    scene = context.page.locator(".lc-scene3d").first
    # wait for the Three.js canvas so the upgrade is complete before hovering
    context.page.locator(".lc-scene3d canvas").first.wait_for(
        state="visible", timeout=25_000
    )
    _alt_hover(context.page, scene)


@when('I hover over the avatar overlay "{avatar_id}"')
def step_hover_avatar(context, avatar_id):
    host = context.page.locator("#lc-avatar-" + avatar_id)
    # the avatar registers itself async (Rive/Lottie from the CDN) — hovering
    # before it upgrades makes x-ray read a not-yet-identified node. Wait for
    # the overlay to exist first, the same way the scene3d hover waits for its
    # canvas; without it the identify races and flakes on slow CDN runs.
    host.wait_for(state="visible", timeout=25_000)
    _alt_hover(context.page, host)


@then("an x-ray panel is visible")
def step_xray_visible(context):
    panel = context.page.locator(SEL_XRAY_PANEL).first
    expect(panel).to_be_visible(timeout=8_000)


@then("the x-ray panel shows a component class name")
def step_xray_has_class(context):
    panel = context.page.locator(SEL_XRAY_PANEL).first
    text = panel.inner_text()
    assert text.strip(), "X-ray panel is empty"


@then('the x-ray panel mentions "{keyword}"')
def step_xray_mentions(context, keyword):
    panel = context.page.locator(SEL_XRAY_PANEL).first
    expect(panel).to_contain_text(keyword, timeout=3_000)


@then("the x-ray panel shows a code block")
def step_xray_has_code(context):
    code = context.page.locator(".lcx-xray .code").first
    expect(code).to_be_visible(timeout=3_000)


@then("the x-ray panel is within the viewport bounds")
def step_xray_in_viewport(context):
    vw = context.page.evaluate("window.innerWidth")
    vh = context.page.evaluate("window.innerHeight")
    panel = context.page.locator(SEL_XRAY_PANEL).first
    box = panel.bounding_box()
    assert box is not None, "Could not get x-ray panel bounding box"
    assert box["x"] >= 0, f"Panel overflows left: x={box['x']}"
    assert box["y"] >= 0, f"Panel overflows top: y={box['y']}"
    assert box["x"] + box["width"] <= vw + 4, (
        f"Panel overflows right: x+w={box['x']+box['width']} > vw={vw}"
    )
    assert box["y"] + box["height"] <= vh + 4, (
        f"Panel overflows bottom: y+h={box['y']+box['height']} > vh={vh}"
    )


# --- FAB / touch steps ---

@then("the slides FAB button is visible")
def step_fab_visible(context):
    expect(context.page.locator(SEL_FAB)).to_be_visible(timeout=10_000)


@when("I click the slides FAB button")
def step_click_fab(context):
    fab = context.page.locator(SEL_FAB)
    expect(fab).to_be_visible(timeout=10_000)
    fab.click()
    context.page.wait_for_timeout(300)


@step("I tap the slides FAB button")
def step_tap_fab(context):
    fab = context.page.locator(SEL_FAB)
    expect(fab).to_be_visible(timeout=10_000)
    fab.tap()
    context.page.wait_for_timeout(400)


@when("I tap the X-ray option in the popup")
def step_tap_xray_option(context):
    btn = context.page.locator(SEL_XRAY_BTN)
    expect(btn).to_be_visible(timeout=3_000)
    btn.tap()
    context.page.wait_for_timeout(300)


@when("I click the Present option in the popup")
def step_click_present(context):
    btn = context.page.locator(SEL_PRESENT_BTN)
    expect(btn).to_be_visible(timeout=3_000)
    btn.click()
    context.page.wait_for_timeout(300)


@step("I tap the first grid component")
def step_tap_grid(context):
    el = context.page.locator(SEL_GRID).first
    el.wait_for(state="visible", timeout=15_000)
    el.tap()
    context.page.wait_for_timeout(400)


@then("the FAB popup is visible")
def step_popup_visible(context):
    expect(context.page.locator(SEL_POPUP)).to_be_visible(timeout=3_000)


@then("the FAB popup is not visible")
def step_popup_hidden(context):
    expect(context.page.locator(SEL_POPUP)).to_be_hidden(timeout=3_000)


@then('the popup contains a "{label}" option')
def step_popup_has_option(context, label):
    popup = context.page.locator(SEL_POPUP)
    expect(popup).to_contain_text(label, timeout=2_000)


@then("the popup contains an X-ray option")
def step_popup_has_xray(context):
    expect(context.page.locator(SEL_XRAY_BTN)).to_be_visible(timeout=2_000)


@then("the FAB button has the xray-active style")
def step_fab_active(context):
    fab = context.page.locator(SEL_FAB)
    expect(fab).to_have_class(re.compile(r"lc-xray-active"), timeout=3_000)


@then("the FAB button does not have the xray-active style")
def step_fab_inactive(context):
    fab = context.page.locator(SEL_FAB)
    expect(fab).not_to_have_class(re.compile(r"lc-xray-active"), timeout=3_000)


def _shift_alt_hover(page, locator):
    """Pointermove with Alt+Shift — the connected-scene x-ray mode."""
    locator.wait_for(state="visible", timeout=15_000)
    locator.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    box = locator.bounding_box()
    cx = box["x"] + box["width"] / 2
    cy = box["y"] + box["height"] / 2
    page.evaluate(
        "([x, y]) => window.dispatchEvent(new PointerEvent('pointermove',"
        " {clientX: x, clientY: y, altKey: true, shiftKey: true,"
        "  bubbles: true, cancelable: true}))",
        [cx, cy]
    )
    page.wait_for_timeout(800)


@when("I shift-hover over the chart component")
def step_shift_hover_chart(context):
    _shift_alt_hover(context.page, context.page.locator(SEL_CHART).first)


@then('the x-ray scene mentions "{keyword}"')
def step_scene_mentions(context, keyword):
    scene = context.page.locator("#lcx-scene")
    # the MicroPython engine loads lazily; the scene rebuilds when ready
    expect(scene).to_contain_text(keyword, timeout=30_000)


@when('I shift-hover over the avatar overlay "{avatar_id}"')
def step_shift_hover_avatar(context, avatar_id):
    host = context.page.locator("#lc-avatar-" + avatar_id)
    host.wait_for(state="visible", timeout=25_000)   # same async-upgrade wait as the plain hover
    _shift_alt_hover(context.page, host)


# ── X-ray inline editing: Keep's two honest paths ──────────────────────

def _alt_move_on(page, locator):
    """pointermove with altKey dispatched ON the element (xray_edit reads
    e.target, so the window-level dispatch used for panels won't do)."""
    locator.wait_for(state="visible", timeout=15_000)
    locator.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    locator.evaluate(
        "el => el.dispatchEvent(new PointerEvent('pointermove',"
        " {altKey: true, bubbles: true, cancelable: true}))"
    )
    page.wait_for_timeout(600)


@when("I am connected as a builder with a stubbed repo")
def step_connected_stub(context):
    import base64
    import json

    context.gh_commits = []
    with open("docs/tutorial101.md", encoding="utf-8") as f:
        src = f.read()

    def gh_stub(route, req):
        if req.method == "GET" and "/contents/docs/" in req.url:
            route.fulfill(json={
                "content": base64.b64encode(src.encode()).decode(),
                "sha": "stub-sha",
            })
        elif req.method == "PUT" and "/contents/docs/" in req.url:
            context.gh_commits.append(json.loads(req.post_data))
            route.fulfill(json={"content": {"sha": "stub-sha-2"}})
        else:
            route.continue_()

    context.page.route("https://api.github.com/**", gh_stub)
    context.page.evaluate(
        "() => { localStorage.setItem('lc_ed_pat', 'ghp_stub');"
        " localStorage.setItem('lc_ed_repo', 'stub/lightcodelab'); }"
    )


@when("I open the x-ray editor on the local dog block")
def step_open_xray_editor(context):
    para = context.page.locator("main p", has_text="Cute, huh").first
    _alt_move_on(context.page, para)
    gear = context.page.locator("#lcx-gear")
    gear.wait_for(state="visible", timeout=5_000)
    gear.click(force=True)
    expect(context.page.locator("#lcx-content")).to_be_visible(timeout=5_000)


@when('I change the block content to "{text}"')
def step_change_block_content(context, text):
    context.page.fill("#lcx-content", text)


@when("I keep the changes")
def step_keep_changes(context):
    """Click Keep, then WAIT FOR THE COMMIT — never a fixed sleep.

    Keeping is a GET of the page source followed by a PUT, both through the
    route stub. A one-second sleep passed for months and then went red the day
    the page under test got slightly busier, which says nothing about the
    feature and everything about the assertion. Poll for the outcome instead.
    """
    import time

    context.page.click("#lcx-keep")
    deadline = time.time() + 10
    while time.time() < deadline and not getattr(context, "gh_commits", None):
        context.page.wait_for_timeout(200)


@then('the stubbed repo received a commit containing "{text}"')
def step_commit_received(context, text):
    import base64

    # The engine ALWAYS says why it declined — "couldn't safely locate this
    # block", "Save failed: …" — and this step used to discard it, leaving a
    # bare "no commit" that fits a dozen causes. Report what the page said.
    if not context.gh_commits:
        toast = context.page.evaluate(
            """() => { const t = document.getElementById('lcx-toast');
                       return t ? (t.textContent || '').trim() : '(no toast element)'; }"""
        )
        state = context.page.evaluate(
            """() => { const f = document.getElementById('ed-fab');
                       const r = document.querySelector('.lc-run[data-lc-src-path]');
                       return JSON.stringify({
                         pagePath: f && f.dataset ? f.dataset.pagePath : null,
                         runSrc: r ? r.dataset.lcSrcPath : null,
                         repo: localStorage.getItem('lc_ed_repo'),
                         hasPat: !!localStorage.getItem('lc_ed_pat'),
                         origLen: (document.getElementById('lcx-content') || {}).value?.length ?? null,
                         anchor: (document.getElementById('lcx-toast') || {}).dataset?.lcAnchor ?? null,
                         hits: (document.getElementById('lcx-toast') || {}).dataset?.lcHits ?? null,
                         ordinal: (document.getElementById('lcx-toast') || {}).dataset?.lcOrdinal ?? null,
                       }); }"""
        )
        raise AssertionError(
            "no commit reached the stubbed repo — toast said: %r · state: %s" % (toast, state)
        )
    body = context.gh_commits[-1]
    content = base64.b64decode(body["content"]).decode("utf-8")
    assert text in content, "committed content lacks the edit"
    assert "Cute, huh — this local dog?" not in content, "original text was not replaced"
    assert body["message"].startswith("Inline edit:"), body["message"]


@then("keeping the changes invites me to create an account")
def step_keep_invites(context):
    messages = []
    context.page.once("dialog", lambda d: (messages.append(d.message), d.dismiss()))
    context.page.click("#lcx-keep")
    context.page.wait_for_timeout(500)
    assert messages and "account" in messages[0].lower(), messages


@then("a green save toast confirms it")
def step_save_toast(context):
    expect(context.page.locator("#lcx-toast")).to_contain_text("Saved", timeout=8000)


@then("the touch gesture hint appears")
def step_touch_hint(context):
    # the two-finger pipelines gesture is invisible without this toast
    hint = context.page.locator("#lcx-touch-hint")
    expect(hint).to_be_visible(timeout=5_000)
    expect(hint).to_contain_text("two fingers", timeout=2_000)
