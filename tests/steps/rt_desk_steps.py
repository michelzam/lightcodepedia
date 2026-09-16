import json
import re

from behave import given, then, when
from playwright.sync_api import expect

# The fire story (module_01): a learner tunes the desk agent's briefing and
# the audit compares seed prompt, two pads, and the VERDICT lines. The model
# is stubbed — the audit's arithmetic is what's under test, not the AI.


@given('the model desk answers with verdicts "{v1}" then "{v2}"')
def step_stub_model_desk(context, v1, v2):
    state = {"n": 0}

    def fulfill(route):
        state["n"] += 1
        v = v1 if state["n"] == 1 else v2
        body = json.dumps({
            "choices": [{"message": {
                "content": "Here is my feedback.\n\nVERDICT: " + v}}],
            "usage": {"total_tokens": 42},
        })
        route.fulfill(status=200, content_type="application/json", body=body)

    context.page.route("**/chat/completions*", fulfill)


@when('I brief the "{desk_id}" desk with "{text}"')
def step_brief_named_desk(context, desk_id, text):
    # the real flow is x-ray Keep → the block re-renders with the new yaml
    # and the panel republishes data-system; the step reproduces that final
    # state directly, which is exactly what the audit reads
    sel = '[data-lc-id="' + desk_id + '"]'
    panel = context.page.locator(sel)
    panel.wait_for(state="attached", timeout=15_000)
    context.page.evaluate(
        """([sel, t]) => document.querySelector(sel).setAttribute('data-system', t)""",
        [sel, text],
    )


@given("the model desk is unreachable")
def step_model_desk_down(context):
    # abort = the fetch never gets an HTTP answer — an ad-blocker's view
    context.page.route("**/chat/completions*", lambda route: route.abort())


@when('I ask the desk agent into the void "{prompt}"')
def step_ask_desk_void(context, prompt):
    panel = context.page.locator('[data-lc-id="desk"]')
    panel.locator(".lc-agent-prompt").fill(prompt)
    panel.locator(".lc-agent-send").click()


@then("the desk blames the road, not the badge")
def step_desk_blames_road(context):
    status = context.page.locator(
        '[data-lc-id="desk"] .lc-agent-status')
    expect(status).to_contain_text("Couldn't reach", timeout=20_000)
    expect(status).to_contain_text("ad-blocker", timeout=5_000)


@when('I retype the pad "{pad_id}" with')
@when('I retype the pad "{pad_id}" with:')
def step_retype_named_pad(context, pad_id):
    ta = context.page.locator(
        '[data-lc-id="' + pad_id + '"] .lc-mdpad-in')
    ta.wait_for(state="visible", timeout=15_000)
    ta.fill(context.text)


@when('I connect the "{agent_id}" agent with key "{key}"')
def step_connect_agent_key(context, agent_id, key):
    # the auth form is the only door now — the old silent PAT borrow died
    # with GitHub Models; sibling panels of the same provider follow along
    panel = context.page.locator('[data-lc-id="' + agent_id + '"]')
    panel.wait_for(state="attached", timeout=20_000)
    # the ring: one row per engine. A desk already open on another held key
    # keeps the ring folded — 🔑 opens it; the first row without a key is
    # the page's own engine
    if panel.locator(".lc-agent-auth").is_hidden():
        panel.locator(".lc-agent-key").click()
    row = panel.locator(".lc-agent-ring-row[data-held='0']").first
    row.locator("input[type=password]").fill(key)
    row.locator("button[type=submit]").click()
    expect(panel.locator(".lc-agent-prompt")).to_be_visible(timeout=10_000)


@given('a saved energy key "{key}" for provider "{pid}"')
def step_saved_energy_key(context, key, pid):
    context.page.add_init_script(
        "localStorage.setItem('lc_ai_key_" + pid + "', '" + key + "');"
    )


@then("the desk is already connected")
def step_desk_connected(context):
    from playwright.sync_api import expect
    panel = context.page.locator(".lc-agent").first
    expect(panel.locator(".lc-agent-prompt")).to_be_visible(timeout=15_000)
    expect(panel.locator(".lc-agent-auth")).to_be_hidden()


@when("I press the desk's forget-key button")
def step_forget_key(context):
    # 🔑 opens the ring; "forget" on the held row drops that key everywhere
    btn = context.page.locator(".lc-agent .lc-agent-key").first
    btn.wait_for(state="visible", timeout=15_000)
    btn.click()
    forget = context.page.locator(".lc-agent .lc-agent-ring-row[data-held='1'] [data-forget]").first
    forget.wait_for(state="visible", timeout=10_000)
    forget.click()
    context.page.wait_for_timeout(300)


@then('the saved energy key for "{pid}" is gone')
def step_energy_key_gone(context, pid):
    v = context.page.evaluate(
        "(k) => localStorage.getItem(k)", "lc_ai_key_" + pid
    )
    assert v is None, "key still on the device: %r" % v


# ── the gear on a vault lesson ─────────────────────────────────────────────

@when('I summon the gear on the "{desk_id}" desk')
def step_summon_gear(context, desk_id):
    """pointermove with altKey ON the desk — x-ray reads e.target"""
    panel = context.page.locator('[data-lc-id="' + desk_id + '"]')
    panel.wait_for(state="visible", timeout=20_000)
    panel.scroll_into_view_if_needed()
    context.page.wait_for_timeout(300)
    panel.evaluate("el => el.dispatchEvent(new PointerEvent('pointermove', {altKey: true, bubbles: true, cancelable: true}))")
    context.page.wait_for_timeout(600)


@then('the gear offers "{glyph}", not a note')
def step_gear_glyph(context, glyph):
    gear = context.page.locator("#lcx-gear")
    expect(gear).to_be_visible(timeout=5_000)
    expect(gear).to_have_text(glyph)


@when("I open the editor and replace the desk's sheet with")
def step_open_and_replace(context):
    context.page.locator("#lcx-gear").click(force=True)
    expect(context.page.locator("#lcx-content")).to_be_visible(timeout=5_000)
    context.page.fill("#lcx-content", context.text)
    context.page.click("#lcx-keep")
    # the slot writes the lesson's starter FIRST (the "before" of the change),
    # then the edit: wait for the commit that carries the new sheet
    want = [l for l in context.text.splitlines() if l.startswith("system:")][0]
    import time
    deadline = time.time() + 20
    while time.time() < deadline and not any(want in c["text"] for c in getattr(context, "bench_commits", [])):
        context.page.wait_for_timeout(200)


@then('the "{desk_id}" desk now carries a sheet mentioning "{word}"')
def step_desk_sheet(context, desk_id, word):
    panel = context.page.locator('[data-lc-id="' + desk_id + '"]')
    expect(panel).to_have_attribute("data-system", re.compile(word), timeout=20_000)
