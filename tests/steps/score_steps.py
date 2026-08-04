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
    context.page.reload(wait_until="domcontentloaded")
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
    context.page.reload(wait_until="domcontentloaded")
    context.page.wait_for_timeout(1000)


@then('a card score tag shows "{score}"')
def step_card_tag(context, score):
    expect(
        context.page.locator(".lc-card-score", has_text=score).first
    ).to_be_visible(timeout=10_000)


@when('the score for page "{path}" becomes "{score}"')
def step_score_changes_live(context, path, score):
    # a score moving WITHOUT a reload — what answering a quiz actually does:
    # write the store, then let the page notice. No reload on purpose; that is
    # exactly the case a write-once badge could not survive.
    won, total = (int(x) for x in score.split("/"))
    context.page.evaluate(
        "([p, w, t]) => {"
        " var s = JSON.parse(localStorage.getItem('lc_scores') || '{}');"
        " s[p] = { won: w, total: t, ts: '' };"
        " localStorage.setItem('lc_scores', JSON.stringify(s));"
        " window.lcQuizScore.update('live-probe', true);"
        " }",
        [path, won, total],
    )
    context.page.wait_for_timeout(500)


@then('no card still shows "{score}"')
def step_no_stale_card(context, score):
    n = context.page.locator(".lc-card-score", has_text=score).count()
    assert n == 0, "%d card(s) still showing the stale score %s" % (n, score)


@then("a feature card is remembered as passing")
def step_feature_remembered(context):
    # the store is the fact; the card reflecting it is what the reader sees
    context.page.wait_for_timeout(1500)
    kept = context.page.evaluate("() => localStorage.getItem('lc_features')")
    assert kept and "passing" in kept, "no run result was remembered: %r" % kept
    marked = context.page.locator(".lc-feature[data-lc-remembered]").count()
    assert marked > 0, "the remembered result never reached a card"
