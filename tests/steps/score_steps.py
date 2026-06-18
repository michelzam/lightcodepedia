from behave import when, then
from playwright.sync_api import expect


@when('I record quiz answers "{score}" and reload')
def step_record_reload(context, score):
    won, total = (int(x) for x in score.split("/"))
    context.page.evaluate(
        "([won, total]) => {"
        " for (var i = 0; i < total; i++) window.lcQuizScore.update('demo' + i, i < won);"
        " }",
        [won, total],
    )
    context.page.wait_for_timeout(200)
    context.page.reload(wait_until="load")
    context.page.wait_for_timeout(800)


@then('the score badge shows "{score}"')
def step_score_badge(context, score):
    fab = context.page.locator(".lc-score-fab")
    expect(fab).to_be_visible(timeout=10_000)
    expect(fab.locator(".lc-score-fab-label")).to_have_text(score, timeout=10_000)


@when('I store a score "{score}" for page "{path}"')
def step_store_score(context, score, path):
    won, total = (int(x) for x in score.split("/"))
    context.page.evaluate(
        "([p, w, t]) => {"
        " var s = JSON.parse(localStorage.getItem('lc_scores') || '{}');"
        " s[p] = { won: w, total: t, ts: '' };"
        " localStorage.setItem('lc_scores', JSON.stringify(s));"
        " }",
        [path, won, total],
    )


@when("I reload the page")
def step_reload(context):
    context.page.reload(wait_until="load")
    context.page.wait_for_timeout(1000)


@then('a card score tag shows "{score}"')
def step_card_tag(context, score):
    expect(
        context.page.locator(".lc-card-score", has_text=score).first
    ).to_be_visible(timeout=10_000)
