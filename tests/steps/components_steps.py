import re
from behave import when, then
from playwright.sync_api import expect


@when('I click the grid row containing "{text}"')
def step_click_grid_row(context, text):
    row = context.page.locator(".ag-row", has_text=text).first
    row.wait_for(state="visible", timeout=20_000)
    row.click()
    context.page.wait_for_timeout(400)


@then('a form titled "{title}" is visible')
def step_form_titled(context, title):
    name = context.page.locator(".lc-form-title .lc-form-name", has_text=title).first
    expect(name).to_be_visible(timeout=10_000)


@when("I open the first accordion section")
def step_open_accordion(context):
    summary = context.page.locator(".lc-accordion details summary").first
    summary.wait_for(state="visible", timeout=15_000)
    summary.click()
    context.page.wait_for_timeout(600)  # lazy markdown render


@then("the accordion section body has content")
def step_accordion_body(context):
    body = context.page.locator(".lc-accordion details[open] .lc-ac-body").first
    expect(body).to_be_visible(timeout=10_000)
    assert body.inner_text().strip(), "accordion body is empty"


@then('an embedded iframe from "{host}" is present')
def step_iframe_present(context, host):
    frame = context.page.locator("iframe[src*='" + host + "']").first
    expect(frame).to_be_attached(timeout=10_000)


@when('I pick the quiz answer "{answer}"')
def step_pick_quiz_answer(context, answer):
    li = context.page.locator(".lc-quiz li", has_text=answer).first
    li.wait_for(state="visible", timeout=15_000)
    li.click()
    context._quiz_answer = answer
    context.page.wait_for_timeout(300)


@then("that quiz answer is marked correct")
def step_quiz_correct(context):
    li = context.page.locator(".lc-quiz li", has_text=context._quiz_answer).first
    expect(li).to_have_class(re.compile(r"lc-quiz-correct"), timeout=5_000)


@then("that quiz answer is marked wrong")
def step_quiz_wrong(context):
    li = context.page.locator(".lc-quiz li", has_text=context._quiz_answer).first
    expect(li).to_have_class(re.compile(r"lc-quiz-wrong"), timeout=5_000)


@when('I click the bound grid "{grid_id}" row containing "{text}"')
def step_click_bound_grid_row(context, grid_id, text):
    row = context.page.locator(
        ".lc-datagrid[data-lc-id='" + grid_id + "'] tbody tr", has_text=text
    ).first
    row.wait_for(state="visible", timeout=15_000)
    row.click()
    context.page.wait_for_timeout(500)


@then('the detail chart bound to "{grid_id}" renders a canvas')
def step_detail_chart_canvas(context, grid_id):
    canvas = context.page.locator(
        ".lc-chart[data-bound-to='" + grid_id + "'] canvas"
    ).first
    expect(canvas).to_be_visible(timeout=10_000)


@then("the markdown pad shows an editor and a rendered preview")
def step_mdpad(context):
    pad = context.page.locator(".lc-mdpad").first
    expect(pad).to_be_visible(timeout=15_000)
    expect(pad.locator("textarea.lc-mdpad-in")).to_be_visible()
    # the preview renders the seed markdown to HTML (a heading element appears)
    expect(pad.locator(".lc-mdpad-out h2")).to_be_visible(timeout=15_000)


@then("a live Python editor is visible")
def step_live_python_editor(context):
    pad = context.page.locator(".lc-pyrun").first
    expect(pad).to_be_visible(timeout=15_000)
    expect(pad.locator("textarea")).to_be_visible()


@then("a live SQL editor is visible")
def step_sql_editor_visible(context):
    expect(context.page.locator("textarea.lc-query-editor").first).to_be_visible(timeout=10_000)


@then("a red coloured word is rendered")
def step_red_colour(context):
    el = context.page.locator(".markdown-body .red").first
    el.wait_for(state="attached", timeout=10_000)
    color = context.page.evaluate(
        "() => { var e = document.querySelector('.markdown-body .red');"
        " return e ? getComputedStyle(e).color : null; }"
    )
    # #c0392b == rgb(192, 57, 43)
    assert color and color.replace(" ", "") == "rgb(192,57,43)", (
        "expected red rgb(192,57,43), got %r" % (color,)
    )


@then("the mdpad preview shows a red word")
def step_mdpad_red(context):
    el = context.page.locator(".lc-mdpad-out .red").first
    el.wait_for(state="attached", timeout=20_000)
    color = context.page.evaluate(
        "() => { var e = document.querySelector('.lc-mdpad-out .red');"
        " return e ? getComputedStyle(e).color : null; }"
    )
    assert color and color.replace(" ", "") == "rgb(192,57,43)", (
        "expected red in mdpad preview, got %r" % (color,)
    )


@then("a code keyword is syntax-coloured")
def step_code_keyword(context):
    # target the dedicated demo block (#lc-py-demo) so the assertion isn't a
    # race with the mdpad block, whose embedded python also produces .k
    el = context.page.locator("#lc-py-demo .k").first
    el.wait_for(state="attached", timeout=10_000)
    color = context.page.evaluate(
        "() => { var e = document.querySelector('#lc-py-demo .k');"
        " return e ? getComputedStyle(e).color : null; }"
    )
    # #cf222e == rgb(207, 34, 46)
    assert color and color.replace(" ", "") == "rgb(207,34,46)", (
        "expected keyword red rgb(207,34,46), got %r" % (color,)
    )


@then("the mdpad italic text is not coloured")
def step_mdpad_italic_not_red(context):
    # regression: a *italic* before a later {: .red} must NOT inherit the colour
    color = context.page.evaluate(
        "() => { var ems = document.querySelectorAll('.lc-mdpad-out em');"
        " for (var i = 0; i < ems.length; i++) {"
        "   if (/italic/.test(ems[i].textContent)) return getComputedStyle(ems[i]).color;"
        " } return null; }"
    )
    # .red is #c0392b == rgb(192, 57, 43); the italic word must not be that
    assert color and color.replace(" ", "") != "rgb(192,57,43)", (
        "italic text wrongly coloured red: %r" % (color,)
    )
