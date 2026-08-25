import re
from behave import given, when, then
from playwright.sync_api import expect


def _host(context, avatar_id):
    """The fixed overlay element the include appends to <body>."""
    return context.page.locator("#lc-avatar-" + avatar_id)


def _trigger(context, avatar_id):
    return context.page.locator("[data-avt-target='" + avatar_id + "']").first


@then('the avatar overlay "{avatar_id}" is visible')
def step_overlay_visible(context, avatar_id):
    expect(_host(context, avatar_id)).to_be_visible(timeout=15_000)


@when('I click the avatar trigger for "{avatar_id}"')
def step_click_trigger(context, avatar_id):
    # the trigger is a no-op until the avatar has registered itself
    expect(_host(context, avatar_id)).to_be_visible(timeout=15_000)
    trig = _trigger(context, avatar_id)
    trig.wait_for(state="visible", timeout=15_000)
    trig.click()
    context.page.wait_for_timeout(300)


@when('I tap the avatar face "{avatar_id}"')
def step_tap_face(context, avatar_id):
    # the face glides between anchors (1.6s transitions) — a tap mid-air
    # is exactly the user's gesture, so skip the stability wait
    _host(context, avatar_id).locator(".lc-avatar-char").click(force=True)
    context.page.wait_for_timeout(300)


@then('the paused remote of "{avatar_id}" offers prev, play, next and replay')
def step_remote_offers(context, avatar_id):
    ctl = _host(context, avatar_id).locator(".lc-avatar-ctl")
    expect(ctl).to_be_visible(timeout=5_000)
    for verb in ("prev", "play", "next", "replay"):
        expect(ctl.locator("[data-avt='%s']" % verb)).to_be_visible()


@when('I press "{verb}" on the paused remote of "{avatar_id}"')
def step_press_remote(context, verb, avatar_id):
    _host(context, avatar_id).locator("[data-avt='%s']" % verb).click()
    context.page.wait_for_timeout(300)


@then('the paused remote of "{avatar_id}" is hidden')
def step_remote_hidden(context, avatar_id):
    expect(_host(context, avatar_id).locator(".lc-avatar-ctl")).to_be_hidden()


@then('the avatar overlay "{avatar_id}" rides above the topbar')
def step_above_topbar(context, avatar_id):
    z = context.page.evaluate(
        """(id) => {
             const host = document.getElementById('lc-avatar-' + id);
             const bar = document.getElementById('lc-topbar');
             return { host: parseInt(getComputedStyle(host).zIndex || 0),
                      bar: bar ? parseInt(getComputedStyle(bar).zIndex || 0) : 0 };
           }""", avatar_id)
    assert z["host"] > z["bar"], "guide z %s under topbar z %s" % (z["host"], z["bar"])


@then('the avatar trigger for "{avatar_id}" shows the stop label')
def step_trigger_stop_label(context, avatar_id):
    expect(_trigger(context, avatar_id)).to_have_class(
        re.compile(r"playing"), timeout=5_000
    )


@then('the avatar "{avatar_id}" shows a "{selector}" character')
def step_avatar_char_kind(context, avatar_id, selector):
    # the character graphic appears only after its runtime (Rive/Lottie)
    # loads from the CDN — allow time for that round trip
    expect(_host(context, avatar_id).locator(selector)).to_be_visible(
        timeout=20_000
    )


@then('the avatar "{avatar_id}" is in the "{state}" state')
def step_avatar_state(context, avatar_id, state):
    expect(_host(context, avatar_id)).to_have_attribute(
        "data-state", state, timeout=5_000
    )


@when("I open the guide's ask panel")
def step_open_ask_panel(context):
    # the learner's path: tap the docked guide, then its 💬 Ask item
    # the menu opens from the guide's own seed button (clicking elsewhere on
    # the host builds the menu but leaves it closed)
    seed = context.page.locator(".lc-guide-seed").first
    seed.wait_for(state="visible", timeout=20_000)
    seed.click()
    ask = context.page.get_by_text("💬 Ask", exact=False).first
    ask.wait_for(state="visible", timeout=10_000)
    ask.click()
    context.page.wait_for_selector(".lc-guide-ask", timeout=10_000)


@then("the key prompt names the AI provider, not GitHub")
def step_prompt_names_provider(context):
    txt = context.page.locator(".lc-guide-ask").inner_text()
    ph = context.page.get_attribute(".lc-guide-ask input[type=password]", "placeholder") or ""
    assert "GitHub" not in txt, "the guide still asks for a GitHub token: %s" % txt
    assert not ph.startswith("ghp_"), "placeholder still a GitHub PAT: %s" % ph


@then("the saved-password identity matches the agents'")
def step_identity_matches(context):
    user = context.page.get_attribute(".lc-guide-ask input[name=username]", "value")
    assert user and user.startswith("lc-"), \
        "keychain identity is %r — autofill will not find the saved key" % user


@when("I click where the hidden avatar face sits")
def step_click_ghost(context):
    host = context.page.locator(".lc-avatar-host").first
    host.wait_for(state="attached", timeout=20_000)
    # docked idle: the host is opacity 0 but still laid out at fixed
    # coordinates — a real mouse click at its center is exactly what a
    # learner aiming at a button underneath delivers
    box = context.page.evaluate(
        """() => { const c = document.querySelector('.lc-avatar-char');
                   const r = c.getBoundingClientRect();
                   return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; }"""
    )
    context.page.mouse.click(box["x"], box["y"])
    context.page.wait_for_timeout(600)


@then("the avatar did not start playing")
def step_avatar_not_playing(context):
    playing = context.page.evaluate(
        """() => { const a = window._lcAvatars && window._lcAvatars.guide;
                   return !!(a && a.playing); }"""
    )
    assert not playing, "the ghost face swallowed the click and started the tour"


# ── a cut-off answer must never be filed ──────────────────────────────────
# The model can stop at max_tokens mid-sentence. Speaking the fragment is
# fine; committing it into the page (and voicing it) is not.

def _stub_completion(context, text, finish_reason):
    import json as _json

    body = _json.dumps({
        "choices": [{
            "message": {"content": text},
            "finish_reason": finish_reason,
        }],
        "usage": {"total_tokens": 11},
    })
    # WHAT WAS SENT matters as much as what came back: author mode is a
    # sentence added to the system prompt, so the request body is where a
    # learner-turned-author shows up.
    context.model_calls = []

    def _answer(route):
        try:
            context.model_calls.append(route.request.post_data or "")
        except Exception:
            pass
        route.fulfill(status=200, content_type="application/json", body=body)

    context.page.route("**/chat/completions*", _answer)


@given('the model endpoint stops mid-answer with "{text}"')
def step_stub_truncated(context, text):
    _stub_completion(context, text, "length")


@given('the model endpoint answers in full with "{text}"')
def step_stub_complete(context, text):
    _stub_completion(context, text, "stop")


@given("the editor is connected as the author")
def step_editor_connected(context):
    context.page.add_init_script(
        "localStorage.setItem('lc_ed_pat','ghp_author');"
        "localStorage.setItem('lc_ed_repo','acme/demo');"
    )


@when('I ask the guide "{question}"')
def step_ask_guide(context, question):
    context.execute_steps("When I open the guide's ask panel")
    panel = context.page.locator(".lc-guide-ask")
    panel.locator("textarea").fill(question)
    panel.locator("button").click()
    # let the stubbed answer arrive and the guide start speaking
    context.page.wait_for_timeout(1_200)


def _open_dock_menu(context):
    """The seed TOGGLES the menu, so clicking blind can close one that is
    already open and read an empty menu as 'the item is absent'."""
    seed = context.page.locator(".lc-guide-seed").first
    seed.wait_for(state="visible", timeout=20_000)
    menu = context.page.locator(".lc-guide-menu.open")
    for _ in range(3):
        if menu.count():
            return
        seed.click()
        context.page.wait_for_timeout(400)
    assert menu.count(), "the guide's dock menu never opened"


def _dock_menu_text(context):
    """The dock menu renders its items as one run of text, so read the menu
    rather than trying to locate an item by its own label."""
    _open_dock_menu(context)
    return context.page.evaluate(
        "() => Array.from(document.querySelectorAll('.lc-guide-menu'))"
        ".map(m => m.textContent).join(' ')"
    ) or ""


@then("the guide does not offer to keep the answer")
def step_no_keep(context):
    menu = _dock_menu_text(context)
    assert "Keep & voice" not in menu, (
        f"a cut-off answer was offered for keeping; menu was {menu!r}")


@then("the guide offers to keep the answer")
def step_offers_keep(context):
    menu = _dock_menu_text(context)
    assert "Keep & voice" in menu, (
        f"a complete answer was not offered for keeping; menu was {menu!r}")


@then('the guide never says "{snippet}"')
def step_never_says(context, snippet):
    spoken = context.page.evaluate(
        "() => Array.from(document.querySelectorAll('.lc-avatar-speech'))"
        ".map(n => n.textContent).join(' ')"
    )
    assert snippet.lower() not in (spoken or "").lower(), (
        f"the guide read the truncation notice aloud: {spoken!r}")


@given('the "{name}" bot is available')
def step_stub_bot(context, name):
    """loadBot fetches docs/bots/<name>.md from raw.githubusercontent — stub it
    or the guide answers 'bot could not be loaded' and never reaches the model."""
    body = (
        "# Stub bot\n\n"
        "```yaml\n"
        f"name: {name}\n"
        "temperature: 0.2\n"
        "max_tokens: 700\n"
        "```\n\n"
        "You are a stub tutor used by the test suite.\n"
    )

    def fulfill(route):
        route.fulfill(status=200, content_type="text/plain; charset=utf-8",
                      body=body)

    context.page.route(
        "**/raw.githubusercontent.com/**/docs/bots/" + name + ".md*", fulfill)
    context.page.route(
        "**/api.github.com/repos/**/contents/docs/bots/" + name + ".md*", fulfill)


# ── studio voice resolution across mounts ─────────────────────────────────
# The manifest namespaces recordings by the page's mount path; benches mount
# the same course elsewhere. These steps pin that a recording survives the
# move — and that only URL RESOLUTION is asserted, not decode: the fixture
# mp3 is a stub, and the src being set is what separates studio from TTS.

import hashlib
import json as _json

# 12 sync-framed bytes repeated — enough for <audio> to accept a src;
# playback decode is not part of the contract under test.
_SILENT_MP3 = (bytes([0xFF, 0xE3, 0x18, 0xC4]) + bytes(20)) * 12


@given('the voice manifest maps "{text}" to "{file}" under the mount "{slug}" for avatar "{aid}"')
def step_vox_manifest(context, text, file, slug, aid):
    key = hashlib.sha1(text.strip().encode()).hexdigest()[:16]
    body = _json.dumps({slug: {aid: {key: file}}})
    context.page.route(
        "**/assets/audio/vox.json*",
        lambda r: r.fulfill(status=200, content_type="application/json",
                            body=body),
    )


@given('the studio file "{file}" is served')
def step_serve_mp3(context, file):
    context.page.route(
        "**/assets/audio/" + file + "*",
        lambda r: r.fulfill(status=200, content_type="audio/mpeg",
                            body=_SILENT_MP3),
    )


@then('the avatar "{avatar_id}" speaks from the studio file "{file}"')
def step_speaks_from_studio(context, avatar_id, file):
    """The line resolved to the committed mp3 — TTS never sets audioEl.src."""
    context.page.wait_for_function(
        """([id, f]) => {
          const av = window._lcAvatars && window._lcAvatars[id];
          const a = av && (av.audioEl || av.voiceAudio);
          return !!(a && a.src && a.src.indexOf(f) >= 0);
        }""",
        arg=[avatar_id, file],
        timeout=15_000,
    )


@given("the AI provider key is connected")
def step_provider_key(context):
    """lcBotAsk keeps the model key under its own keychain identity; the
    guide only offers a question box once it is there."""
    context.page.add_init_script(
        "localStorage.setItem('lc_ai_key_gemini', 'test-key');"
        "localStorage.setItem('lc_agent_key', 'test-key');"
    )


@then("the ask panel says it is in author mode")
def step_author_mode_hint(context):
    txt = context.page.locator(".lc-guide-ask").inner_text()
    assert "author mode" in txt.lower(), txt


@then("the ask panel shows the day's AI spend")
def step_panel_spend(context):
    """The author is the heaviest user of every page they write, so the count
    is in front of them before they ask again."""
    txt = context.page.locator(".lc-guide-ask").inner_text()
    assert "📊" in txt, txt
    assert "question" in txt.lower() or "token" in txt.lower(), txt


# ── author mode is ownership, not a key ────────────────────────────────────
# Every onboarded learner holds an editor key — it is how their own bench
# saves. The question that separates them from the author is the one X-ray
# already asks: can this viewer PUSH to the repo the material came from?

def _stub_repo_push(context, repo, can_push):
    context.page.route(
        "**/api.github.com/repos/" + repo,
        lambda r: r.fulfill(status=200, content_type="application/json",
                            body=_json.dumps({"permissions": {"push": can_push}})))


@given('the viewer can push to "{repo}"')
def step_can_push(context, repo):
    _stub_repo_push(context, repo, True)


@given('the viewer cannot push to "{repo}"')
def step_cannot_push(context, repo):
    _stub_repo_push(context, repo, False)


@given("a learner key is connected to their own bench")
def step_learner_key(context):
    context.page.add_init_script(
        "localStorage.setItem('lc_ed_pat','ghp_learner');"
        "localStorage.setItem('lc_ed_repo','zamm-learner/bench');")


@then("the ask panel is not in author mode")
def step_no_author_hint(context):
    context.page.wait_for_timeout(600)   # the ownership answer is a request
    txt = context.page.locator(".lc-guide-ask").inner_text()
    assert "author mode" not in txt.lower(), txt


@then("the question reached the model without the author's licence")
def step_no_direct_licence(context):
    calls = getattr(context, "model_calls", [])
    assert calls, "the model was never asked"
    joined = " ".join(calls)
    assert "course AUTHOR" not in joined, joined[:400]


@then("the question reached the model with the author's licence")
def step_direct_licence(context):
    calls = getattr(context, "model_calls", [])
    assert calls, "the model was never asked"
    joined = " ".join(calls)
    assert "course AUTHOR" in joined, joined[:400]


@when('I ask "{question}" in the open panel')
def step_ask_in_open_panel(context, question):
    """The panel is already open (a hint was just read off it) — opening it
    again would click a menu the open panel covers."""
    panel = context.page.locator(".lc-guide-ask")
    panel.locator("textarea").fill(question)
    panel.locator("button").first.click()
    context.page.wait_for_timeout(1_200)
