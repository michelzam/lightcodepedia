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
