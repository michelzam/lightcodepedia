from behave import when, then
from playwright.sync_api import expect


@then('the homework pill shows "{text}"')
def step_hw_pill(context, text):
    pill = context.page.locator(".lc-hw-pill")
    expect(pill).to_be_visible(timeout=10_000)
    expect(pill).to_contain_text(text, timeout=10_000)


@then("the homework session is stored")
def step_hw_stored(context):
    active = context.page.evaluate("() => localStorage.getItem('lc_hw_active')")
    assert active and "93629601" in active, (
        "expected lc_hw_active with the student id, got %r" % (active,)
    )


@when("a quiz is graded correct")
def step_hw_grade(context):
    context.page.evaluate(
        "() => window.lcQuizScore && window.lcQuizScore.update('hw_probe', true)"
    )
    context.page.wait_for_timeout(400)


@then("the homework score is at least {n:d}")
def step_hw_score(context, n):
    txt = context.page.locator(".lc-hw-score").inner_text()
    won = int(txt.split("/")[0].strip())
    assert won >= n, "expected homework score >= %d, got %r" % (n, txt)
