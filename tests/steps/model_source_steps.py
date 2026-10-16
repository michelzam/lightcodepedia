import re
from behave import when, then
from playwright.sync_api import expect

T = 15000


def grid(context, gid):
    return context.page.locator(".lc-datagrid[data-lc-id='" + gid + "']")


def row_of(context, gid, name):
    return grid(context, gid).locator("tbody tr", has_text=name).first


@then('the grid "{gid}" has the columns "{cols}"')
def step_cols(context, gid, cols):
    ths = grid(context, gid).locator("thead th")
    expect(ths.first).to_be_visible(timeout=T)
    want = [c.strip() for c in cols.split(",")]
    got = [re.sub(r"\s*[↑↓]$", "", t.strip()).lower() for t in ths.all_inner_texts()]
    assert got == want, got


@then('the stage cell of "{name}" in "{gid}" is a chip with a caret')
def step_chip(context, name, gid):
    cell = row_of(context, gid, name).locator("td.lc-dg-state")
    expect(cell.locator(".lc-dg-chip")).to_be_visible(timeout=T)
    expect(cell.locator(".lc-dg-caret")).to_have_text("⌄")


@when('I open the verbs of "{name}" in "{gid}"')
def step_open(context, name, gid):
    row_of(context, gid, name).locator("td.lc-dg-state").click()
    expect(context.page.locator(".lc-dg-menu")).to_be_visible(timeout=T)   # on the body, never clipped


@then('the verb "{live}" is live and "{grey}" is grey, needing "{need}"')
def step_live_grey(context, live, grey, need):
    menu = context.page.locator(".lc-dg-menu")
    a = menu.locator("button[data-verb='" + live + "']")
    b = menu.locator("button[data-verb='" + grey + "']")
    expect(a).to_have_attribute("data-ok", "1")
    expect(b).to_have_attribute("data-ok", "0")
    assert need in (b.get_attribute("title") or ""), b.get_attribute("title")


@then('the menu ends with "{label}"')
def step_menu_last(context, label):
    last = context.page.locator(".lc-dg-menu button").last
    assert label in last.inner_text(), last.inner_text()


@when('I press the verb "{verb}"')
def step_press_verb(context, verb):
    context.page.locator(".lc-dg-menu button[data-verb='" + verb + "']").click()


@then('the grid "{gid}" says "{text}"')
def step_says(context, gid, text):
    expect(grid(context, gid).locator(".lc-dg-say")).to_contain_text(text, timeout=T)


@then('the stage of "{name}" in "{gid}" reads "{stage}"')
def step_stage_reads(context, name, gid, stage):
    expect(row_of(context, gid, name).locator(".lc-dg-chip")).to_have_text(stage, timeout=T)


def _ds_row(context, ds, name):
    return context.page.evaluate(
        "([d, n]) => (window.lcDatasets[d] || []).find(r => String(r.family) === n) || null", [ds, name])


@then('the dataset "{ds}" has "{name}" at stage "{stage}"')
def step_ds_stage(context, ds, name, stage):
    context.page.wait_for_function(
        "([d, n, s]) => { const r = (window.lcDatasets[d] || []).find(r => String(r.family) === n); return !!r && String(r.stage) === s; }",
        arg=[ds, name, stage], timeout=T)


@then('the dataset "{ds}" has "{name}" since "{day}"')
def step_ds_since(context, ds, name, day):
    context.page.wait_for_function(
        "([d, n, s]) => { const r = (window.lcDatasets[d] || []).find(r => String(r.family) === n); return !!r && String(r.since) === s; }",
        arg=[ds, name, day], timeout=T)


@when('I type "{text}" in the "{col}" cell of "{name}" in "{gid}"')
def step_type_cell(context, text, col, name, gid):
    cell = row_of(context, gid, name).locator("td.lc-dg-typed[data-col='" + col + "']")
    expect(cell).to_be_visible(timeout=T)
    cell.dblclick()      # a class grid opens a cell on a double click
    expect(cell).to_have_attribute("contenteditable", "true", timeout=T)
    context.page.keyboard.press("Control+A")
    context.page.keyboard.type(text)
    context.page.keyboard.press("Enter")


@when('I press New under "{gid}"')
def step_new(context, gid):
    grid(context, gid).locator("button.lc-dg-new").click()


@then('the grid "{gid}" has {n:d} rows and the dataset "{ds}" has {m:d} rows')
def step_counts(context, gid, n, ds, m):
    expect(grid(context, gid).locator("tbody tr")).to_have_count(n, timeout=T)
    context.page.wait_for_function("([d, m]) => (window.lcDatasets[d] || []).length === m", arg=[ds, m], timeout=T)


@when('I click the row "{name}" in "{gid}"')
def step_click_row(context, name, gid):
    row_of(context, gid, name).locator("td").first.click()


@then('the form "{fid}" shows the verbs "{verbs}" with "{grey}" grey')
def step_form_verbs(context, fid, verbs, grey):
    bar = context.page.locator("#" + fid + " .lc-form-verbs, .lc-form[data-lc-id='" + fid + "'] .lc-form-verbs").first
    expect(bar).to_be_visible(timeout=T)
    got = [b.strip().lower() for b in bar.locator("button").all_inner_texts()]
    want = [v.strip().lower() for v in verbs.split(",")]
    assert got == want, got
    off = bar.locator("button.lc-form-verb-off")
    expect(off).to_have_count(1)
    assert off.first.inner_text().strip().lower() == grey.lower()


@then('the "{pad_id}" pad shows the grid "{gid}" dressed, with no broken wire')
def step_pad_dressed_no_broken(context, pad_id, gid):
    pad = context.page.locator("[data-lc-id='" + pad_id + "']")
    chip = pad.locator(".lc-datagrid[data-lc-id='" + gid + "'] .lc-dg-chip").first
    expect(chip).to_be_visible(timeout=T)
    expect(pad.locator(".lc-mdpad-wires")).to_have_count(0)
    expect(pad.locator(".lc-mdpad-broken")).to_have_count(0)
    assert not pad.get_attribute("data-lc-broken"), pad.get_attribute("data-lc-broken")


@then('the form "{fid}" shows the state "{state}" as a chip, in its last row')
def step_form_state_chip(context, fid, state):
    form = context.page.locator(".lc-form[data-lc-id='" + fid + "']")
    chip = form.locator(".lc-form-body .lc-dg-chip")
    expect(chip).to_have_text(state, timeout=T)
    labels = [l.strip().lower() for l in form.locator(".lc-form-label-cell").all_inner_texts() if l.strip()]
    assert labels and labels[-1] == "stage", labels


@when('the selected object of "{gid}" is deleted in code')
def step_delete_selected(context, gid):
    obj = context.page.evaluate(
        "g => { const tr = document.querySelector('.lc-datagrid[data-lc-id=\"' + g + '\"] tbody tr.lc-dg-selected');"
        " const b = document.querySelector('.lc-datagrid[data-lc-id=\"' + g + '\"]').getAttribute('data-bind');"
        " const name = tr.querySelector('td').textContent.trim();"
        " const row = (window.lcDatasets[b] || []).find(r => String(r.family) === name); return row ? row.obj : null; }", gid)
    assert obj, "no selected object"
    context.page.evaluate("o => window.lcPySend(o + '.delete()')", obj)


@then('the selected row of "{gid}" is "{name}", and the form "{fid}" shows "{text}"')
def step_selected_and_form(context, gid, name, fid, text):
    sel = grid(context, gid).locator("tbody tr.lc-dg-selected")
    expect(sel).to_have_count(1, timeout=T)
    expect(sel).to_contain_text(name)
    expect(context.page.locator(".lc-form[data-lc-id='" + fid + "'] .lc-form-body")).to_contain_text(text, timeout=T)


@then("the verbs menu is fully on screen")
def step_menu_on_screen(context):
    menu = context.page.locator(".lc-dg-menu")
    expect(menu).to_be_visible(timeout=T)
    ok = context.page.evaluate(
        "() => { const r = document.querySelector('.lc-dg-menu').getBoundingClientRect();"
        " const g = document.querySelector('.lc-datagrid[data-lc-id=\"family_grid\"]').getBoundingClientRect();"
        " return { inViewport: r.top >= 0 && r.bottom <= window.innerHeight && r.left >= 0 && r.right <= window.innerWidth,"
        "          belowGrid: r.bottom > g.bottom, h: r.height }; }")
    assert ok["inViewport"] and ok["h"] > 40, ok


@when('I add a "{kind}" with New under "{gid}"')
def step_new_pick(context, gid, kind):
    grid(context, gid).locator("button.lc-dg-new").click()
    menu = context.page.locator(".lc-dg-kinds")
    if menu.count():      # a class with subclasses asks which one
        menu.locator("button[data-kind='" + kind + "']").click()


@then('the grid "{gid}" has exactly one selected row')
def step_one_selected(context, gid):
    expect(grid(context, gid).locator("tbody tr").first).to_be_visible(timeout=T)
    expect(grid(context, gid).locator("tbody tr.lc-dg-selected")).to_have_count(1, timeout=T)


@then('the New menu offers "{kinds}"')
def step_new_menu(context, kinds):
    menu = context.page.locator(".lc-dg-kinds")
    expect(menu).to_be_visible(timeout=T)
    got = [k.strip() for k in menu.locator("button").all_inner_texts()]
    assert got == [k.strip() for k in kinds.split(",")], got


@when('I pick "{kind}" in the New menu')
def step_pick_kind(context, kind):
    context.page.locator(".lc-dg-kinds button[data-kind='" + kind + "']").click()


@then('the selected row of "{gid}" is the new one, at stage "{stage}"')
def step_selected_new(context, gid, stage):
    sel = grid(context, gid).locator("tbody tr.lc-dg-selected")
    expect(sel).to_have_count(1, timeout=T)
    expect(sel.locator(".lc-dg-chip")).to_have_text(stage)
    for old in ("Nguyen", "Diallo", "Alvarez"):
        assert old not in sel.inner_text(), sel.inner_text()
    context.new_row = sel


@then('its verbs offer "{own}" beside "{inherited}"')
def step_own_verbs(context, own, inherited):
    context.new_row.locator("td.lc-dg-state").click()
    menu = context.page.locator(".lc-dg-menu")
    expect(menu.locator("button[data-verb='" + own + "']")).to_be_visible(timeout=T)
    expect(menu.locator("button[data-verb='" + inherited + "']")).to_be_visible()


@then('the "{col}" cell of "{name}" in "{gid}" is closed for typing')
def step_cell_closed(context, col, name, gid):
    cell = row_of(context, gid, name).locator("td.lc-dg-typed[data-col='" + col + "']")
    expect(cell).to_be_visible(timeout=T)
    cell.click()     # a tap on a row that is not selected only selects it
    assert cell.get_attribute("contenteditable") is None, "a single tap opened the cell"
    expect(row_of(context, gid, name)).to_have_class(re.compile("lc-dg-selected"))


@when('I double click the "{col}" cell of "{name}" in "{gid}" and type "{text}"')
def step_dbl_type(context, col, name, gid, text):
    cell = row_of(context, gid, name).locator("td.lc-dg-typed[data-col='" + col + "']")
    cell.dblclick()
    expect(cell).to_have_attribute("contenteditable", "true", timeout=T)
    sel = context.page.evaluate("() => String(window.getSelection())")
    assert sel.strip() == cell.inner_text().strip(), "the old value is not selected: " + repr(sel)
    context.page.keyboard.type(text)
    context.page.keyboard.press("Enter")


@then('the chip, the caret and the family name of "{name}" in "{gid}" share one middle line')
def step_chip_aligned(context, name, gid):
    r = row_of(context, gid, name)
    expect(r.locator(".lc-dg-chip")).to_be_visible(timeout=T)
    mids = context.page.evaluate(
        """tr => { const mid = e => { const b = e.getBoundingClientRect(); return (b.top + b.bottom) / 2; };
           const name = document.createRange(); name.selectNodeContents(tr.querySelector('td'));
           const nb = name.getBoundingClientRect();
           return { name: (nb.top + nb.bottom) / 2, chip: mid(tr.querySelector('.lc-dg-chip')), caret: mid(tr.querySelector('.lc-dg-caret')) }; }""",
        r.element_handle())
    assert abs(mids["chip"] - mids["name"]) <= 2.5 and abs(mids["caret"] - mids["name"]) <= 3.5, mids


@then('the "{pad_id}" pad marks lines "{lines}" as errors')
def step_pad_errs(context, pad_id, lines):
    pad = context.page.locator("[data-lc-id='" + pad_id + "']")
    want = ",".join(l.strip() for l in lines.split(","))
    context.page.wait_for_function(
        "([p, w]) => { const e = document.querySelector(\"[data-lc-id='\" + p + \"']\"); return e && e.getAttribute('data-lc-errors') === w; }",
        arg=[pad_id, want], timeout=T)
    for n in want.split(","):
        expect(pad.locator(".lc-mdpad-piano .ln.err[data-n='" + n + "']")).to_have_count(1)


@then('under the "{pad_id}" pad it says "{a}" and "{b}"')
def step_pad_errs_said(context, pad_id, a, b):
    strip = context.page.locator("[data-lc-id='" + pad_id + "'] .lc-mdpad-errs")
    expect(strip).to_contain_text(a, timeout=T)
    expect(strip).to_contain_text(b)


@when('I click inside "{blank}" in the "{pad_id}" pad and type "{text}"')
def step_click_blank(context, blank, pad_id, text):
    ta = context.page.locator("[data-lc-id='" + pad_id + "'] textarea.lc-mdpad-in")
    expect(ta).to_be_visible(timeout=T)
    at = context.page.evaluate("([t, b]) => t.value.indexOf(b) + 3", [ta.element_handle(), blank])
    assert at >= 3, "no " + blank + " in the pad"
    ta.focus()
    context.page.evaluate("([t, i]) => { t.setSelectionRange(i, i); t.dispatchEvent(new MouseEvent('click', {bubbles: true})); }",
                          [ta.element_handle(), at])
    context.page.keyboard.type(text)


@then("the \"{pad_id}\" pad reads '{text}'")
def step_pad_reads(context, pad_id, text):
    ta = context.page.locator("[data-lc-id='" + pad_id + "'] textarea.lc-mdpad-in")
    v = ta.input_value()
    assert text in v, v


@then('the "{pad_id}" pad\'s line {n:d} says "{text}" on itself, in no column of its own')
def step_err_on_line(context, pad_id, n, text):
    pad = context.page.locator("[data-lc-id='" + pad_id + "']")
    ln = pad.locator(".lc-mdpad-piano .ln.err[data-n='" + str(n) + "']")
    expect(ln).to_have_attribute("data-err", text, timeout=T)
    # the words never stand as a column beside the editor
    side = context.page.evaluate(
        "p => { const w = document.querySelector(\"[data-lc-id='\" + p + \"']\"), e = w.querySelector('.lc-mdpad-errs');"
        " return e ? e.getBoundingClientRect().width : 0; }", pad_id)
    assert side <= 2, "the error text takes room beside the pad: %spx" % side


@when('I type "{text}" and press Enter, without clicking')
def step_type_blind(context, text):
    cell = context.page.locator("td.lc-dg-typed.lc-dg-typing")
    expect(cell).to_have_count(1, timeout=T)
    expect(cell).to_be_focused()
    context.page.keyboard.type(text)
    context.page.keyboard.press("Enter")


@then('the stage chips of "{gid}" are all as wide, their carets in one column')
def step_chips_wide(context, gid):
    expect(grid(context, gid).locator(".lc-dg-chip").first).to_be_visible(timeout=T)
    got = context.page.evaluate(
        "g => [...document.querySelectorAll(\".lc-datagrid[data-lc-id='\" + g + \"'] td.lc-dg-state\")].map(td =>"
        " [Math.round(td.querySelector('.lc-dg-chip').getBoundingClientRect().width), Math.round(td.querySelector('.lc-dg-caret').getBoundingClientRect().left)])", gid)
    widths = {w for w, _ in got}
    lefts = {l for _, l in got}
    assert len(widths) == 1 and len(lefts) == 1, got


@then('the card in the "{pad_id}" pad shows "{text}"')
def step_card_shows(context, pad_id, text):
    form = context.page.locator("[data-lc-id='" + pad_id + "'] .lc-form .lc-form-body")
    expect(form).to_contain_text(text, timeout=T)


@when('I type in the "{pad_id}" pad three times, pausing after each')
def step_type_pause(context, pad_id):
    pad = context.page.locator("[data-lc-id='" + pad_id + "']")
    expect(pad.locator(".lc-dg-chip").first).to_be_attached(timeout=T)
    ta = pad.locator("textarea.lc-mdpad-in")
    ta.focus()
    context.page.evaluate("t => t.setSelectionRange(t.value.indexOf('Families.') + 9, t.value.indexOf('Families.') + 9)", ta.element_handle())
    for _ in range(3):
        context.page.keyboard.type(" more")
        context.page.wait_for_timeout(1200)
    expect(pad.locator(".lc-dg-chip").first).to_be_attached(timeout=T)


@then('the lists "{ids}" keep at most {n:d} listeners each')
def step_listeners(context, ids, n):
    for i in [x.strip() for x in ids.split(",")]:
        # a list change prunes the listeners of parts that have left the page
        context.page.evaluate("i => window.lcSetDataset(i, window.lcDatasets[i])", i)
        k = context.page.evaluate("i => (window.lcDatasetListeners[i] || []).length", i)
        assert k <= n, "%s has %d listeners" % (i, k)


@then('the form "{fid}" shows a field "{label}"')
def step_form_field(context, fid, label):
    form = context.page.locator(".lc-form[data-lc-id='" + fid + "'] .lc-form-body")
    expect(form).to_contain_text(label, timeout=T)


@then('the diagram in the section accordion names "{words}"')
def step_diagram_names(context, words):
    d = context.page.locator(".lc-acc-section .lc-diagram svg")
    expect(d).to_be_attached(timeout=30000)
    for w in [x.strip() for x in words.split(",")]:
        context.page.wait_for_function(
            "w => { const s = document.querySelector('.lc-acc-section .lc-diagram'); return s && s.textContent.indexOf(w) >= 0; }",
            arg=w, timeout=30000)
