"""Steps for run_editor.feature — the run editor as a text field.
(`I undo in the "<id>" editor` lives in agent_bound_steps.py.)"""
from behave import when, then
from playwright.sync_api import expect


def _ta(context, run_id):
    return context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-code")


@when('I type "{text}" at the end of the "{run_id}" editor')
def step_type_at_end(context, text, run_id):
    ta = _ta(context, run_id)
    ta.click()
    context.page.keyboard.press("Control+End")
    context.page.keyboard.type(text)


@when('I press Tab in the "{run_id}" editor')
def step_press_tab(context, run_id):
    _ta(context, run_id).focus()
    context.page.keyboard.press("Tab")


@when('I replace the "{run_id}" editor\'s program with:')
def step_replace_program(context, run_id):
    ta = _ta(context, run_id)
    ta.focus()
    context.page.keyboard.press("Control+a")
    context.page.keyboard.insert_text(context.text)
    context.page.wait_for_timeout(100)


@when('I click Run in the "{run_id}" editor')
def step_click_run(context, run_id):
    context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-run").click()


@then('the "{run_id}" editor ends with "{text}"')
def step_ends_with(context, run_id, text):
    v = _ta(context, run_id).input_value()
    assert v.endswith(text), "editor ends with %r" % v[-30:]


@then('the "{run_id}" editor does not contain "{text}"')
def step_not_contains(context, run_id, text):
    v = _ta(context, run_id).input_value()
    assert text not in v, "editor still holds %r" % text


@then('the "{run_id}" editor\'s output reads "{line1}" then "{line2}"')
def step_output_reads(context, run_id, line1, line2):
    out = context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-out")
    expect(out).to_have_text(line1 + "\n" + line2, timeout=30_000)
