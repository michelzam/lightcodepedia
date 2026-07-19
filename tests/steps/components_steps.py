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


@then("a scanned subtree's root-absolute image resolves under the base path")
def step_base_path_heal(context):
    # scanElement() is the choke point every component's injected HTML passes
    # through. Force a project base (the suite serves at a domain root, where
    # lcBase is "") and confirm a freshly-injected root-absolute image gains the
    # base prefix — while a full URL would be left alone. Scoped to the subtree.
    src = context.page.evaluate(
        """() => {
          window.lcBase = "/lightcodelab";
          const box = document.createElement("div");
          document.body.appendChild(box);
          box.innerHTML = '<img id="_lc_heal" src="/assets/lab.jpg">';
          window.lcScanElement(box);
          return document.getElementById("_lc_heal").getAttribute("src");
        }"""
    )
    assert src == "/lightcodelab/assets/lab.jpg", "media not healed by scanElement: " + str(src)


@then("the block component's image is loaded, not broken")
def step_block_image_loaded(context):
    # the .block upgrader injects <img src="/assets/lab.jpg"> client-side; under
    # the base-path harness it must heal + download. naturalWidth stays 0 on a
    # 404, so this is the end-to-end guard the domain-root suite could not give.
    img = context.page.locator(".lc-block img").first
    img.wait_for(state="visible", timeout=20_000)
    context.page.wait_for_function(
        "el => el.complete && el.naturalWidth > 0",
        arg=img.element_handle(),
        timeout=20_000,
    )


@then("the folder gallery shows at least {n:d} cards")
def step_gallery_cards(context, n):
    # .folder enumerates from the build-time manifest (no GitHub API); on the
    # private lab the old API path 404'd for anonymous visitors. Cards proving.
    context.page.wait_for_selector(".lc-card h3 a", timeout=20_000)
    count = context.page.locator(".lc-cards .lc-card").count()
    assert count >= n, "only %d cards" % count


@then("the folder gallery shows no error card")
def step_gallery_no_error(context):
    txt = context.page.locator(".lc-cards").first.inner_text()
    assert "HTTP 4" not in txt and "not set" not in txt, txt[:200]


@then("the sitemap graph shows at least {n:d} nodes")
def step_sitemap_nodes(context, n):
    # .sitemap enumerates from the same build-time manifest (no GitHub API).
    context.page.wait_for_selector(".lc-sitemap .lc-sm-node", timeout=20_000)
    count = context.page.locator(".lc-sitemap .lc-sm-node").count()
    assert count >= n, "only %d nodes" % count
    assert context.page.locator(".lc-sm-msg", has_text="⚠").count() == 0, "sitemap error message shown"


@then("clicking a sitemap node opens its page")
def step_sitemap_node_click(context):
    # graph nodes are injected after every healing pass — their navigation must
    # still resolve under a project base (was a plain 404 on the deployed lab)
    context.page.locator(".lc-sitemap .lc-sm-node circle").first.click()
    context.page.wait_for_load_state()
    context.page.wait_for_timeout(500)
    assert "404" not in (context.page.title() or ""), context.page.url
    expect(context.page.locator("main h1").first).to_be_visible()
