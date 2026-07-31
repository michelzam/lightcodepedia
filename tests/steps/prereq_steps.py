import json

from behave import given, then
from playwright.sync_api import expect

# The prerequisite gate on runner renders: scores live under gh:owner/repo/…
# content keys (score.md's canon), and the gate must read exactly those.


@given('the learner has earned points on "{key}"')
def step_seed_score(context, key):
    seed = json.dumps({key: {"won": 2, "total": 3}})
    context.page.add_init_script(
        "try { localStorage.setItem('lc_scores', %s); } catch (e) {}"
        % json.dumps(seed)
    )


@then('a prerequisite gate offers "{title}"')
def step_gate_offers(context, title):
    gate = context.page.locator(".lc-prereq")
    expect(gate).to_be_visible(timeout=10_000)
    expect(gate.locator("a", has_text=title)).to_be_visible(timeout=5_000)


@then('the gated content "{text}" is hidden')
def step_gated_hidden(context, text):
    expect(context.page.get_by_text(text)).to_be_hidden(timeout=10_000)


@then("the prerequisites are met")
def step_prereq_met(context):
    expect(context.page.locator(".lc-prereq-met")).to_be_visible(timeout=10_000)


@then('the gated content "{text}" is visible')
def step_gated_visible(context, text):
    expect(context.page.get_by_text(text)).to_be_visible(timeout=10_000)
