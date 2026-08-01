import json

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
    panel.locator(".lc-agent-token").fill(key)
    panel.locator(".lc-agent-auth button[type=submit]").click()
    expect(panel.locator(".lc-agent-prompt")).to_be_visible(timeout=10_000)
