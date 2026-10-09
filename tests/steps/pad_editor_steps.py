"""Steps for pad_editor.feature — the markdown pad as a painted text field."""
from behave import when, then
from playwright.sync_api import expect


def _ta(context, pad_id):
    return context.page.locator("[data-lc-id='" + pad_id + "'] .lc-mdpad-in")


def _mirror(context, pad_id):
    return context.page.locator("[data-lc-id='" + pad_id + "'] .lc-mdpad-piano")


@when('I type "{text}" at the end of the "{pad_id}" pad')
def step_pad_type(context, text, pad_id):
    ta = _ta(context, pad_id)
    ta.click()
    context.page.keyboard.press("Control+End")
    context.page.keyboard.type(text)


@when('I undo in the "{pad_id}" pad')
def step_pad_undo(context, pad_id):
    _ta(context, pad_id).focus()
    context.page.keyboard.press("Control+z")
    context.page.wait_for_timeout(400)


@then('the "{pad_id}" pad ends with "{text}"')
def step_pad_ends(context, pad_id, text):
    v = _ta(context, pad_id).input_value()
    assert v.endswith(text), "pad ends with %r" % v[-30:]


@then('the "{pad_id}" pad does not contain "{text}"')
def step_pad_not(context, pad_id, text):
    v = _ta(context, pad_id).input_value()
    assert text not in v, "pad still holds %r" % text


@then('the "{pad_id}" pad\'s mirror shows "{text}"')
def step_mirror_shows(context, pad_id, text):
    expect(_mirror(context, pad_id)).to_contain_text(text, timeout=5_000)


@then('the "{pad_id}" pad\'s mirror does not show "{text}"')
def step_mirror_not(context, pad_id, text):
    expect(_mirror(context, pad_id)).not_to_contain_text(text, timeout=5_000)


@when('I press "{label}" on the "{pad_id}" pad')
def step_pad_press(context, label, pad_id):
    btn = context.page.locator("[data-lc-id='" + pad_id + "'] .lc-mdpad-fold")
    expect(btn).to_have_text(label)
    btn.click()


@then('the "{pad_id}" pad\'s source is folded away')
def step_pad_folded(context, pad_id):
    expect(context.page.locator("[data-lc-id='" + pad_id + "'] .lc-mdpad-src")).to_be_hidden()
    expect(context.page.locator("[data-lc-id='" + pad_id + "']")).to_have_attribute("data-lc-folded", "1")


@then('the "{pad_id}" pad\'s preview spans the pad')
def step_pad_preview_spans(context, pad_id):
    w = context.page.evaluate(
        "(id) => { const p = document.querySelector(`[data-lc-id='${id}']`); const o = p.querySelector('.lc-mdpad-out');"
        " return [p.getBoundingClientRect().width, o.getBoundingClientRect().width]; }", pad_id)
    assert w[1] >= w[0] - 2, "preview %s of pad %s" % (w[1], w[0])


@then('the "{pad_id}" pad\'s source is shown again')
def step_pad_unfolded(context, pad_id):
    expect(context.page.locator("[data-lc-id='" + pad_id + "'] .lc-mdpad-src")).to_be_visible()
