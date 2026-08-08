import re
from behave import when, then
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
    context.page.route(
        "**/chat/completions*",
        lambda r: r.fulfill(
            status=200, content_type="application/json", body=body),
    )


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
