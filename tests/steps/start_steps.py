import re
from behave import when, then
from playwright.sync_api import expect

SEL_STEP = "#lc-wizard .lcw-step"
SEL_PAT_RESULT = "#lcw-pat-result"
SEL_KARMA_BADGE = ".lcw-karma-badge"


def _step_el(context, n):
    return context.page.locator("#lcw-s" + str(n))


@then("the wizard shows {n:d} steps")
def step_wizard_count(context, n):
    expect(context.page.locator(SEL_STEP)).to_have_count(n, timeout=10_000)


@then("wizard step {n:d} is active")
def step_wizard_active(context, n):
    expect(_step_el(context, n)).to_have_class(re.compile(r"lcw-active"), timeout=5_000)


@then("wizard step {n:d} is done")
def step_wizard_done(context, n):
    expect(_step_el(context, n)).to_have_class(re.compile(r"lcw-done"), timeout=5_000)


@then("wizard steps {a:d} through {b:d} are locked")
def step_wizard_locked(context, a, b):
    for n in range(a, b + 1):
        expect(_step_el(context, n)).to_have_class(
            re.compile(r"lcw-locked"), timeout=5_000
        )


@when('I click the wizard button "{label}"')
def step_click_wizard_button(context, label):
    btn = context.page.locator("#lc-wizard button", has_text=label).first
    btn.wait_for(state="visible", timeout=10_000)
    btn.click()
    context.page.wait_for_timeout(300)


@then('the access-key result shows an error mentioning "{text}"')
def step_pat_error(context, text):
    res = context.page.locator(SEL_PAT_RESULT)
    expect(res).to_have_class(re.compile(r"err"), timeout=5_000)
    expect(res).to_contain_text(text, timeout=2_000)


@then('a wizard step advertises "{label}" karma')
def step_karma_badge(context, label):
    badge = context.page.locator(SEL_KARMA_BADGE, has_text=label).first
    expect(badge).to_be_attached(timeout=5_000)
