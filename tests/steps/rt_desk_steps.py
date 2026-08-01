import json

from behave import given, when
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

    context.page.route(
        "**/models.github.ai/inference/chat/completions", fulfill)


@when('I brief the desk agent with "{text}"')
def step_brief_desk(context, text):
    # the real flow is x-ray Keep → the block re-renders with the new yaml
    # and the panel republishes data-system; the step reproduces that final
    # state directly, which is exactly what the audit reads
    panel = context.page.locator('[data-lc-id="desk"]')
    panel.wait_for(state="attached", timeout=15_000)
    context.page.evaluate(
        """([sel, t]) => document.querySelector(sel).setAttribute('data-system', t)""",
        ['[data-lc-id="desk"]', text],
    )


@when('I ask the desk agent "{prompt}"')
def step_ask_desk(context, prompt):
    panel = context.page.locator('[data-lc-id="desk"]')
    before = panel.locator(".lc-agent-log-entry").count()
    panel.locator(".lc-agent-prompt").fill(prompt)
    panel.locator(".lc-agent-send").click()
    # the visible panel is single-shot; the sitting's ledger appends
    expect(panel.locator(".lc-agent-log-entry")).to_have_count(
        before + 1, timeout=20_000)


@when('I retype the pad "{pad_id}" with')
@when('I retype the pad "{pad_id}" with:')
def step_retype_named_pad(context, pad_id):
    ta = context.page.locator(
        '[data-lc-id="' + pad_id + '"] .lc-mdpad-in')
    ta.wait_for(state="visible", timeout=15_000)
    ta.fill(context.text)
