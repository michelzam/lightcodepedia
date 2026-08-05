import json

from behave import given, then, when
from playwright.sync_api import expect

# bound= regression net: the legacy editor binding is pinned by asserting on
# the REQUEST the agent sends (the augmented prompt must carry the editor's
# code) and on the Apply write-back. The expression form asserts the same
# request now carries the evaluated cell value instead.


@given('the recording model endpoint replies with a python fix "{code}"')
def step_recording_model(context, code):
    context.model_asks = []

    def fulfill(route):
        try:
            context.model_asks.append(route.request.post_data or "")
        except Exception:
            context.model_asks.append("")
        body = json.dumps({
            "choices": [{"message": {
                "content": "Try this:\n\n```python\n" + code + "\n```"}}],
            "usage": {"total_tokens": 7},
        })
        route.fulfill(status=200, content_type="application/json", body=body)

    context.page.route("**/chat/completions*", fulfill)


@when('I ask the "{agent_id}" agent "{prompt}"')
def step_ask_named_agent(context, agent_id, prompt):
    panel = context.page.locator('[data-lc-id="' + agent_id + '"]')
    panel.wait_for(state="attached", timeout=20_000)
    before = panel.locator(".lc-agent-log-entry").count()
    panel.locator(".lc-agent-prompt").fill(prompt)
    panel.locator(".lc-agent-send").click()
    # the visible panel is single-shot; the sitting's ledger appends
    expect(panel.locator(".lc-agent-log-entry")).to_have_count(
        before + 1, timeout=20_000)


@then('the model request carried the editor code "{snippet}"')
def step_request_carried(context, snippet):
    assert context.model_asks, "no model request was recorded"
    assert snippet in context.model_asks[-1], context.model_asks[-1][:600]


@when("I apply the agent's fix")
def step_apply_fix(context):
    btn = context.page.locator(".lc-agent-apply").first
    btn.wait_for(state="visible", timeout=10_000)
    btn.click()


@then('the "{run_id}" editor now holds "{code}"')
def step_editor_holds(context, run_id, code):
    ta = context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-code")
    expect(ta).to_have_value(code, timeout=10_000)


@given('the model endpoint rejects with an array-wrapped 404 saying "{message}"')
def step_stub_array_error(context, message):
    body = json.dumps([{"error": {"code": 404, "message": message,
                                  "status": "NOT_FOUND"}}])
    context.page.route(
        "**/chat/completions*",
        lambda r: r.fulfill(status=404, content_type="application/json",
                            body=body))


@then('the desk relays "{message}"')
def step_desk_relays(context, message):
    status = context.page.locator('[data-lc-id="desk"] .lc-agent-status')
    expect(status).to_contain_text(message, timeout=15_000)


@given('the model endpoint answers 429 saying "{message}"')
def step_stub_429(context, message):
    body = json.dumps([{"error": {"code": 429, "message": message,
                                  "status": "RESOURCE_EXHAUSTED"}}])
    context.page.route(
        "**/chat/completions*",
        lambda r: r.fulfill(status=429, content_type="application/json",
                            body=body))


# ── the energy key's life on a device ────────────────────────────────────
# Michel, 2026-08-05: the key had to be pasted again after every refresh.
# Storage was never the problem — three paths THREW A VALID KEY AWAY:
# a 403 at any desk, a 403 at the join door, and the door's network catch.
# These pin the survival rules, because a discarded key is invisible until
# a learner is asked for it again.

KEY_SLOT = "lc_ai_key_gemini"


@given('an energy key "{key}" is already saved on this device')
def step_key_preinstalled(context, key):
    context.page.add_init_script(
        "localStorage.setItem(%s, %s);" % (json.dumps(KEY_SLOT), json.dumps(key))
    )


@given('the model endpoint answers with status {status:d} saying "{message}"')
def step_stub_status(context, status, message):
    body = json.dumps([{"error": {"code": status, "message": message}}])
    context.page.route(
        "**/chat/completions*",
        lambda r: r.fulfill(status=status, content_type="application/json",
                            body=body))


@then("the energy key is still saved on this device")
def step_key_kept(context):
    # poll: the wipe happened inside the ask's promise chain, so a bare read
    # could pass simply by looking too early
    context.page.wait_for_timeout(700)
    got = context.page.evaluate("k => localStorage.getItem(k)", KEY_SLOT)
    assert got, "the key was thrown away — a 403 says nothing about the key itself"


@then("the energy key is gone from this device")
def step_key_dropped(context):
    context.page.wait_for_function(
        "k => localStorage.getItem(k) === null", arg=KEY_SLOT, timeout=15_000)


@then("the desk is still connected")
def step_desk_connected(context):
    panel = context.page.locator('[data-lc-id="desk"]')
    expect(panel.locator(".lc-agent-body")).to_be_visible(timeout=15_000)
    expect(panel.locator(".lc-agent-auth")).to_be_hidden(timeout=5_000)


@then("every desk on the page is connected")
def step_all_desks_connected(context):
    panels = context.page.locator(".lc-agent")
    n = panels.count()
    assert n, "no agent panel rendered"
    for i in range(n):
        expect(panels.nth(i).locator(".lc-agent-body")).to_be_visible(timeout=15_000)


@then('the desk asks for a key and explains "{needle}"')
def step_desk_asks_with_reason(context, needle):
    panel = context.page.locator('[data-lc-id="desk"]')
    expect(panel.locator(".lc-agent-auth")).to_be_visible(timeout=15_000)
    # the reason must be ON THE FORM: the chat status line it used to be
    # written to is hidden the moment the key is dropped
    msg = panel.locator(".lc-agent-authmsg")
    expect(msg).to_be_visible(timeout=10_000)
    expect(msg).to_contain_text(needle, timeout=5_000)
