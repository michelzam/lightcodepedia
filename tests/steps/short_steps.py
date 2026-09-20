"""🎬 Short next walk — the owner's checkbox in Doc's menu (rt_short.feature)."""
import json as _json
import base64 as _b64
import re

from behave import given, when, then
from playwright.sync_api import expect



def _open_dock_menu(context):
    """the seed toggles the menu — click until it is open (mirrors avatar_steps)"""
    seed = context.page.locator(".lc-guide-seed").first
    seed.wait_for(state="visible", timeout=20_000)
    menu = context.page.locator(".lc-guide-menu.open")
    for _ in range(3):
        if menu.count():
            return
        seed.click()
        context.page.wait_for_timeout(400)
    assert menu.count(), "the guide's dock menu never opened"


@given("the tab capture is stubbed with a painted canvas")
def step_stub_capture(context):
    # getDisplayMedia needs a picker and a real display; the engine takes any
    # MediaStream from window.lcShortCapture instead — a canvas that keeps
    # repainting so the recorder receives frames.
    context.page.add_init_script(
        """window.lcShortCapture = function () {
             var c = document.createElement('canvas'); c.width = 320; c.height = 180;
             var ctx = c.getContext('2d'), i = 0;
             setInterval(function () { i++; ctx.fillStyle = i % 2 ? '#3366cc' : '#cc6633';
                                       ctx.fillRect(0, 0, 320, 180); }, 80);
             return c.captureStream(15);
           };"""
    )


@given("the YouTube upload is stubbed")
def step_stub_youtube(context):
    context.page.add_init_script(
        "try { localStorage.setItem('lc_yt_access', 'yt-test-token');"
        "      localStorage.setItem('lc_yt_expiry', String(Date.now() + 3600000)); } catch (e) {}"
    )
    context.yt_posts = []

    cors = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "POST, PUT, OPTIONS",
            "Access-Control-Expose-Headers": "Location"}

    def fulfill(route):
        req = route.request
        if req.method == "POST":
            context.yt_posts.append(req.post_data or "")
            route.fulfill(status=200, headers=dict(cors, Location=
                "https://www.googleapis.com/upload/youtube/v3/videos?upload_id=stub"), body="")
            return
        if req.method == "PUT":
            route.fulfill(status=200, headers=dict(cors, **{"Content-Type": "application/json"}),
                          body='{"id":"stub1234"}')
            return
        route.fulfill(status=204, headers=cors, body="")
    # a regex: the glob's * stops short of the "?uploadType=…" query
    context.page.route(re.compile(r"https://www\.googleapis\.com/upload/youtube/v3/videos.*"), fulfill)


def _menu_text(context):
    _open_dock_menu(context)
    return context.page.evaluate(
        "() => Array.from(document.querySelectorAll('.lc-guide-menu.open button'))"
        ".map(b => b.textContent).join(' | ')"
    ) or ""


@then('the guide\'s menu offers "{label}"')
def step_menu_offers(context, label):
    # ownership resolves async; the menu re-renders once it is known
    for _ in range(20):
        if label in _menu_text(context):
            return
        context.page.wait_for_timeout(250)
    raise AssertionError(f"{label!r} never appeared; menu: {_menu_text(context)!r}")


@then('the guide\'s menu does not offer "{label}"')
def step_menu_lacks(context, label):
    context.page.wait_for_timeout(1500)
    text = _menu_text(context)
    assert label not in text, f"{label!r} is offered to a learner; menu: {text!r}"


@when('I tick "{label}" in the guide\'s menu')
def step_tick(context, label):
    step_menu_offers(context, label)
    btn = context.page.locator(".lc-guide-menu.open button", has_text=label).first
    expect(btn).to_have_attribute("aria-checked", "false")
    btn.click()


@when("I close the Short dialog")
def step_close_dialog(context):
    context.page.locator(".lc-short-ov .lc-rec-panel-close").click()
    expect(context.page.locator(".lc-short-ov")).to_have_count(0, timeout=5_000)


@then('the guide\'s menu shows "{label}" unticked')
def step_unticked(context, label):
    assert context.page.evaluate("!window.lcShort.armed()"), "still armed"
    _open_dock_menu(context)
    btn = context.page.locator(".lc-guide-menu.open button", has_text=label).first
    expect(btn).to_have_attribute("aria-checked", "false", timeout=5_000)
    context.page.keyboard.press("Escape")
    context.page.evaluate("document.querySelector('.lc-guide-menu.open') && document.querySelector('.lc-guide-menu.open').classList.remove('open')")



@then("the Short review dialog shows the clip")
def step_review_dialog(context):
    vid = context.page.locator(".lc-short-ov video")
    expect(vid).to_have_attribute("src", re.compile(r"^blob:"), timeout=30_000)
    meta = context.page.locator(".lc-short-ov .lc-rec-review-meta")
    expect(meta).to_contain_text("🎬 Short")


@when("I upload the Short, embedded on this page")
def step_upload_embedded(context):
    context.page.locator(".lc-short-ov .lc-short-embed").check()
    context.page.locator(".lc-short-ov .lc-short-up").click()
    st = context.page.locator(".lc-short-ov .lc-short-status")
    try:
        expect(st).to_contain_text("embedded", timeout=15_000)
    except AssertionError:
        raise AssertionError("the Short was not embedded; status: " + (st.text_content() or ""))


@then("the Short went to YouTube unlisted")
def step_unlisted(context):
    assert context.yt_posts, "no upload was started"
    meta = _json.loads(context.yt_posts[-1])
    assert meta.get("status", {}).get("privacyStatus") == "unlisted", meta


@then('"{path}" now carries a folded Shorts accordion with Short {n:d}')
def step_accordion(context, path, n):
    bodies = [b for p, b in getattr(context, "keep_puts", []) if p == path and b]
    assert bodies, f"no commit to {path!r}; PUTs: {[p for p, _ in getattr(context, 'keep_puts', [])]}"
    content = _b64.b64decode(_json.loads(bodies[-1])["content"]).decode("utf-8")
    assert content.count("{: .accordion #shorts }") == 1, content
    assert f"### 🎬 Short {n} ·" in content, content
    assert f"[▶️ Short {n}](https://youtu.be/stub1234)\n{{: .video }}" in content, content
    # the accordion is the LAST block of the page, one section per clip
    assert content.rstrip().endswith("{: .accordion #shorts }"), content[-200:]
    assert content.count("### 🎬 Short ") == n, content


@then("the Shorts accordion is folded")
def step_acc_folded(context):
    acc = context.page.locator("#shorts.lc-accordion, .lc-accordion#shorts, [data-lc-id='shorts']").first
    expect(acc).to_be_visible(timeout=10_000)
    d = acc.locator("details").first
    expect(d).to_have_count(1)
    assert not d.evaluate("d => d.open"), "the Shorts accordion opened by itself"
    context.short_acc = acc


@when("I unfold the Shorts accordion")
def step_acc_unfold(context):
    context.short_acc.locator("summary").first.click()


@then("the Short plays inside it")
def step_acc_video(context):
    frame = context.short_acc.locator("iframe.lc-video, .lc-video iframe, iframe[src*='stub1234']").first
    expect(frame).to_be_visible(timeout=10_000)
    assert "stub1234" in (frame.get_attribute("src") or ""), frame.get_attribute("src")


@then("the page wears the phone frame")
def step_frame_on(context):
    expect(context.page.locator("body")).to_have_class(re.compile(r"\blc-short-frame\b"), timeout=5_000)
    # the column is 9:16 of the viewport's height, centred, and Doc's seed sits inside it
    box = context.page.evaluate("""() => {
      const vw = innerWidth, vh = innerHeight, w = vh * 9 / 16, g = Math.max(0, (vw - w) / 2);
      const m = document.querySelector('.markdown-body').getBoundingClientRect();
      const s = document.querySelector('.lc-guide-seed').getBoundingClientRect();
      return { g, ml: m.left, mr: m.right, vw, sr: s.right }; }""")
    assert abs(box["ml"] - box["g"]) < 2 and abs(box["mr"] - (box["vw"] - box["g"])) < 2, box
    assert box["sr"] <= box["vw"] - box["g"] + 1, box


@then("the phone frame is off")
def step_frame_off(context):
    expect(context.page.locator("body")).not_to_have_class(re.compile(r"\blc-short-frame\b"), timeout=5_000)
