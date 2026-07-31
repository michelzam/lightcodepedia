from behave import when, then
from playwright.sync_api import expect

# The trophy FAB's reset: before the fix, the popover rebuilt its own HTML on
# every MutationObserver tick (a rebuild IS a mutation — a permanent loop),
# so the reset button was replaced every frame and a click could land on a
# detached node. Playwright's stability wait makes that failure loud: this
# scenario times out on the broken engine.


@when("I answer the quiz correctly")
def step_answer_quiz(context):
    context.page.click(".lc-quiz li[role=radio] >> nth=0")


@when("I open the trophy and reset the score")
def step_reset_score(context):
    context.page.click(".lc-score-fab")
    expect(context.page.locator(".lc-score-popover")).to_be_visible(timeout=5_000)
    context.page.click(".lc-score-reset")


@then("the score store is empty")
def step_score_store_empty(context):
    context.page.wait_for_function(
        "() => { try { return Object.keys(JSON.parse("
        "localStorage.getItem('lc_scores') || '{}')).length === 0; }"
        " catch (e) { return false; } }",
        timeout=10_000,
    )


@when("the runner page reloads")
def step_runner_reload(context):
    context.page.reload()
    expect(context.page.locator(".lc-quiz").first).to_be_visible(timeout=15_000)
