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
    ths = grid(context, gid).locator("thead th[data-col]")   # the ⋯ gutter is no column
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
    context.db_mark = len(getattr(context, "db_calls", []))
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
    context.db_mark = len(getattr(context, "db_calls", []))
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
    expect(pad.locator(".lc-datagrid tbody tr").first).to_be_attached(timeout=T)
    ta = pad.locator("textarea.lc-mdpad-in")
    ta.focus()
    context.page.evaluate("t => t.setSelectionRange(t.value.indexOf('Families.') + 9, t.value.indexOf('Families.') + 9)", ta.element_handle())
    for _ in range(3):
        context.page.keyboard.type(" more")
        context.page.wait_for_timeout(1200)
    expect(pad.locator(".lc-datagrid tbody tr").first).to_be_attached(timeout=T)


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


@when('I shift-hover over the grid "{gid}"')
def step_shift_hover_grid(context, gid):
    g = grid(context, gid)
    expect(g.locator(".lc-dg-chip").first).to_be_visible(timeout=T)
    g.scroll_into_view_if_needed()
    context.page.wait_for_timeout(300)
    box = g.bounding_box()
    context.page.evaluate(   # Alt+Shift pointermove: the x-ray's connected scene
        "([x, y]) => window.dispatchEvent(new PointerEvent('pointermove',"
        " {clientX: x, clientY: y, altKey: true, shiftKey: true, bubbles: true, cancelable: true}))",
        [box["x"] + box["width"] / 2, box["y"] + 20])
    context.page.wait_for_timeout(800)


@when('in the "{pad_id}" pad I rename "{old}" to "{new}", a letter at a time')
def step_rename_class(context, pad_id, old, new):
    pad = context.page.locator("[data-lc-id='" + pad_id + "']")
    context.page.wait_for_function("n => !!(window.lcModels && window.lcModels[n])", arg=old, timeout=30000)
    ta = pad.locator("textarea.lc-mdpad-in")
    ta.focus()
    at = context.page.evaluate("([t, o]) => t.value.indexOf('class ' + o) + 6", [ta.element_handle(), old])
    context.page.evaluate("([t, a, n]) => t.setSelectionRange(a, a + n)", [ta.element_handle(), at, len(old)])
    for i, ch in enumerate(new):
        context.page.keyboard.type(ch)
        context.page.wait_for_timeout(900)   # a pause: the preview catches up between letters


@then('the class "{old}" is gone from the page, "{new}" is there')
def step_class_gone(context, old, new):
    context.page.wait_for_function("n => !!(window.lcModels && window.lcModels[n])", arg=new, timeout=30000)
    context.page.wait_for_function(
        "n => { const d = document.querySelector('.lc-diagram'); return d && d.textContent.indexOf(n) >= 0; }",
        arg=new, timeout=30000)
    left = context.page.evaluate(
        "o => Object.keys(window.lcModels || {}).filter(k => k !== 'Family' && k !== 'Partner')", old)
    assert not left, "ghost classes left: %s" % left
    txt = context.page.evaluate("() => document.querySelector('.lc-diagram').textContent")
    assert old not in txt.replace(new, ""), "the diagram still draws " + old


@then('the card "{fid}" shows "{a}" in the same table after I click the row "{b}"')
def step_card_same_table(context, fid, a, b):
    body = context.page.locator(".lc-form[data-lc-id='" + fid + "'] .lc-form-body")
    expect(body).to_contain_text(a, timeout=T)
    context.page.evaluate("f => { document.querySelector(\".lc-form[data-lc-id='\" + f + \"'] .lc-form-grid\")._lcMark = 1; }", fid)
    step_click_row(context, b, "family_grid")
    expect(body).to_contain_text(b, timeout=T)
    same = context.page.evaluate("f => !!document.querySelector(\".lc-form[data-lc-id='\" + f + \"'] .lc-form-grid\")._lcMark", fid)
    assert same, "the card built a new table for the new row"


@then('the button New under "{gid}" and the verbs of "{fid}" are filled blue')
def step_blue(context, gid, fid):
    expect(grid(context, gid).locator("button.lc-dg-new")).to_have_css("background-color", "rgb(0, 102, 204)", timeout=T)
    step_click_row(context, "Nguyen", gid)
    live = context.page.locator(".lc-form[data-lc-id='" + fid + "'] .lc-form-verb:not(.lc-form-verb-off)").first
    expect(live).to_have_css("background-color", "rgb(0, 102, 204)", timeout=T)


@when('I mark the grid "{gid}" and type in the "{pad_id}" pad three times, pausing after each')
def step_mark_type(context, gid, pad_id):
    expect(grid(context, gid).locator("tbody tr").first).to_be_attached(timeout=T)
    context.page.evaluate("g => { document.querySelector(\".lc-datagrid[data-lc-id='\" + g + \"']\")._lcMark = 1; }", gid)
    step_type_pause(context, pad_id)


@then('the grid "{gid}" is the one I marked')
def step_grid_marked(context, gid):
    ok = context.page.evaluate("g => !!document.querySelector(\".lc-datagrid[data-lc-id='\" + g + \"']\")._lcMark", gid)
    assert ok, "typing prose rebuilt the grid"


@then('the stage labels of "{gid}" are centred')
def step_chips_centred(context, gid):
    expect(grid(context, gid).locator(".lc-dg-chip").first).to_have_css("text-align", "center", timeout=T)


@when('I widen the column "{col}" of "{gid}" by {px:d} pixels')
def step_widen(context, col, gid, px):
    th = grid(context, gid).locator("th[data-col='" + col + "']")
    expect(th).to_be_visible(timeout=T)
    th.scroll_into_view_if_needed()
    context.page.wait_for_timeout(300)
    context.w0 = th.bounding_box()["width"]
    g = th.locator(".lc-dg-grip").bounding_box()
    x, y = g["x"] + g["width"] / 2, g["y"] + g["height"] / 2
    context.page.mouse.move(x, y)
    context.page.mouse.down()
    context.page.mouse.move(x + px / 2, y)
    context.page.mouse.move(x + px, y)
    context.page.mouse.up()


@then('the column "{col}" of "{gid}" is still at least {px:d} pixels wider')
def step_wider(context, col, gid, px):
    context.page.wait_for_timeout(800)   # the verb repainted the table
    w = grid(context, gid).locator("th[data-col='" + col + "']").bounding_box()["width"]
    assert w >= context.w0 + px, "was %s, now %s" % (context.w0, w)


@then('the "{pad_id}" pad\'s busy mark is a white disc')
def step_busy_disc(context, pad_id):
    pad = context.page.locator("[data-lc-id='" + pad_id + "']")
    expect(pad.locator(".lc-mdpad-out")).to_be_attached(timeout=T)
    bg = context.page.evaluate(
        "p => { const w = document.querySelector(\"[data-lc-id='\" + p + \"']\"); w.setAttribute('data-lc-busy', '1');"
        " return getComputedStyle(w.querySelector('.lc-mdpad-out'), '::after').backgroundColor; }", pad_id)
    assert bg == "rgb(255, 255, 255)", bg


@then('the rows of "{gid}" wear a faint ⋯ in a gutter, and the first column holds only the name')
def step_gutter(context, gid):
    g = grid(context, gid)
    b = g.locator("tbody tr").last.locator("td.lc-dg-gut .lc-dg-rowmenu")
    expect(b).to_have_text("⋯", timeout=T)
    context.page.mouse.move(0, 0)
    op = float(b.evaluate("e => getComputedStyle(e).opacity"))
    assert op < 0.7, "the ⋯ is not light: opacity %s" % op
    first = g.locator("tbody tr").first.locator("td").nth(1)
    assert "⌄" not in first.inner_text() and "⋯" not in first.inner_text(), first.inner_text()


@when('I open the ⋯ of "{name}" in "{gid}"')
def step_gutter_menu(context, name, gid):
    row_of(context, gid, name).locator("td.lc-dg-gut .lc-dg-rowmenu").click()
    expect(context.page.locator(".lc-dg-menu")).to_be_visible(timeout=T)


@then('the menu offers "{verb}" and ends with "{label}"')
def step_menu_offers(context, verb, label):
    expect(context.page.locator(".lc-dg-menu button[data-verb='" + verb + "']")).to_be_visible(timeout=T)
    step_menu_last(context, label)


@then('the dataset "{ds}" has "{name}" with {n:d} walks')
def step_walks(context, ds, name, n):
    context.page.wait_for_function(
        "([d, nm, k]) => { const r = (window.lcDatasets[d] || []).find(r => String(r.name) === nm); return !!r && Number(r.walks) === k; }",
        arg=[ds, name, n], timeout=T)


def _sheet_csv(rows):
    return '"dog","walker","at"\n' + "\n".join('"' + x.split(", ")[0] + '","' + x.split(", ")[1] + '","1:00 PM"' for x in rows) + "\n"


@given('a Google Sheet "{sid}" holds the walks "{a}" and "{b}"')
def step_gsheet(context, sid, a, b):
    context.sheet_walks = [a, b]
    context.sheet_urls = []
    context.page.on("request", lambda r: context.sheet_urls.append(r.url) if "/gviz/" in r.url else None)
    context.page.route("**/docs.google.com/spreadsheets/d/" + sid + "/gviz/**", lambda r: r.fulfill(
        status=200, content_type="text/csv", headers={"Access-Control-Allow-Origin": "*"}, body=_sheet_csv(context.sheet_walks)))
    context.page.route("**/example.org/page.html*", lambda r: r.fulfill(
        status=200, content_type="text/html", headers={"Access-Control-Allow-Origin": "*"},
        body="<!DOCTYPE html><html><body>hello</body></html>"))


@then('the grid "{gid}" shows "{a}" and "{b}"')
def step_grid_shows(context, gid, a, b):
    g = grid(context, gid)
    expect(g).to_contain_text(a, timeout=T)
    expect(g).to_contain_text(b)


@then('the grid "{gid}" reads "{text}"')
def step_grid_text(context, gid, text):
    expect(grid(context, gid)).to_contain_text(text, timeout=T)


@when('the sheet "{sid}" gains the walk "{w}" and I press ↻ on "{gid}"')
def step_gain_reload(context, sid, w, gid):
    context.sheet_walks.append(w)
    grid(context, gid).locator("button.lc-dg-reload").click()


@when('the sheet "{sid}" gains the walk "{w}" and I come back to the page')
def step_gain_visible(context, sid, w):
    context.sheet_walks.append(w)
    context.page.wait_for_timeout(5200)   # a re-read is never more often than every 5 s
    context.page.evaluate("() => { document.dispatchEvent(new Event('visibilitychange')); }")


@then('the sheet was asked for its tab "{tab}"')
def step_sheet_tab(context, tab):
    assert any("sheet=" + tab in u for u in context.sheet_urls), context.sheet_urls


@given('a database table "{table}" that is empty')
def step_db(context, table):
    import json as _j
    from urllib.parse import urlparse, parse_qs
    context.db_rows, context.db_calls, context.db_next = [], [], [1]

    def handle(route):
        req = route.request
        u = urlparse(req.url)
        q = parse_qs(u.query)
        context.db_calls.append({"method": req.method, "url": req.url, "body": req.post_data,
                                 "apikey": req.headers.get("apikey")})
        if req.method == "GET":
            body = _j.dumps(sorted(context.db_rows, key=lambda r: r["id"]))
        elif req.method == "POST":
            for r in _j.loads(req.post_data or "[]"):
                r = dict(r); r["id"] = context.db_next[0]; context.db_next[0] += 1
                context.db_rows.append(r)
            body = ""
        elif req.method == "PATCH":
            rid = int(q["id"][0].split(".")[1])
            for r in context.db_rows:
                if r["id"] == rid:
                    r.update(_j.loads(req.post_data or "{}"))
            body = ""
        elif req.method == "DELETE":
            ids = [int(x) for x in q["id"][0].split("(")[1].rstrip(")").split(",")]
            context.db_rows[:] = [r for r in context.db_rows if r["id"] not in ids]
            body = ""
        else:
            body = ""
        route.fulfill(status=200 if req.method == "GET" else 201, content_type="application/json",
                      headers={"Access-Control-Allow-Origin": "*"}, body=body)
    context.page.route("**/demo.supabase.co/rest/v1/" + table + "*", handle)
    context.page.on("dialog", lambda d: d.accept())


@then('the grid "{gid}" has the columns "{cols}" and no row')
def step_cols_empty(context, gid, cols):
    step_cols(context, gid, cols)
    expect(grid(context, gid).locator("tbody tr")).to_have_count(0)


@then('Save under "{gid}" is off')
def step_save_off(context, gid):
    expect(grid(context, gid).locator("button.lc-dg-save")).to_be_disabled(timeout=T)


@when('I press Save under "{gid}"')
def step_press_save(context, gid):
    b = grid(context, gid).locator("button.lc-dg-save")
    expect(b).to_be_enabled(timeout=T)
    context.db_mark = len(getattr(context, "db_calls", []))
    b.click()


def _db_new(context, method):
    for _ in range(50):
        got = [c for c in context.db_calls[context.db_mark:] if c["method"] == method]
        if got:
            return got
        context.page.wait_for_timeout(200)
    raise AssertionError("no %s sent: %s" % (method, context.db_calls[context.db_mark:]))


@then('the table "{table}" received an insert of "{name}" at stage "{stage}", with its key')
def step_db_insert(context, table, name, stage):
    import json as _j
    c = _db_new(context, "POST")[0]
    rows = _j.loads(c["body"])
    assert len(rows) == 1 and rows[0].get("family") == name and rows[0].get("stage") == stage, rows
    assert "id" not in rows[0], rows
    assert c["apikey"] == "sb_publishable_test", c


@then('the grid "{gid}" shows the row "{name}" read back from the table')
def step_db_readback(context, gid, name):
    expect(row_of(context, gid, name)).to_be_visible(timeout=T)
    expect(grid(context, gid).locator("button.lc-dg-save")).to_be_disabled(timeout=T)
    expect(grid(context, gid).locator("thead th[data-col='id']")).to_have_count(0)


@then('the table "{table}" received an update of row {rid:d} with dog "{dog}"')
def step_db_update(context, table, rid, dog):
    import json as _j
    c = _db_new(context, "PATCH")[0]
    assert ("id=eq.%d" % rid) in c["url"], c
    assert _j.loads(c["body"]).get("dog") == dog, c
    assert not [x for x in context.db_calls[context.db_mark:] if x["method"] == "POST"], "an insert was sent for an edit"


@when('I open the verbs of "{name}" in "{gid}" and delete it')
def step_delete_row(context, name, gid):
    context.db_mark = len(getattr(context, "db_calls", []))
    step_open(context, name, gid)
    context.page.locator(".lc-dg-menu button[data-verb='delete']").click()


@then('the table "{table}" received a delete of row {rid:d}')
def step_db_delete(context, table, rid):
    c = _db_new(context, "DELETE")[0]
    assert ("id=in.(%d)" % rid) in c["url"], c


@given('a database "{table}" that cannot be reached')
def step_db_down(context, table):
    context.page.route("**/demo.supabase.co/rest/v1/" + table + "*", lambda route: route.abort())


@then('the grid "{gid}" says "{text}", with no error column')
def step_grid_says(context, gid, text):
    expect(grid(context, gid).locator(".lc-dg-say")).to_contain_text(text, timeout=T)
    expect(grid(context, gid).locator("thead th[data-col='⚠️']")).to_have_count(0)


@then('the grid "{gid}" still offers New, Save and Refresh')
def step_grid_offers(context, gid):
    g = grid(context, gid)
    for sel in ("button.lc-dg-new", "button.lc-dg-save", "button.lc-dg-refresh"):
        expect(g.locator(sel)).to_have_count(1)


# ── an unlisted table: a stand-in for the setup SQL's four functions ──────────
@given("a database with the Lightcode setup and no author yet")
def step_unl_db(context):
    import json as _j
    st = context.unl = {"authors": [], "tables": {}, "calls": [], "space": "5f2c9a01b7e3",
                        "keys": []}

    def handle(route):
        req = route.request
        fn = req.url.split("/rpc/")[-1].split("?")[0]
        a = _j.loads(req.post_data or "{}")
        st["calls"].append((fn, a))
        st["keys"].append(req.headers.get("apikey"))

        def ok(v):
            route.fulfill(status=200, content_type="application/json",
                          headers={"Access-Control-Allow-Origin": "*"}, body=_j.dumps(v))

        def no(msg):
            route.fulfill(status=400, content_type="application/json",
                          headers={"Access-Control-Allow-Origin": "*"}, body=_j.dumps({"message": "lc: " + msg}))
        if fn == "lc_claim":
            if not st["authors"]:
                st["authors"].append(a["token"])
            return ok(a["token"] in st["authors"])
        if fn == "lc_ensure":
            if a["token"] not in st["authors"]:
                return no("only the author makes tables")
            t = st["tables"].setdefault(a["tbl"], {"cols": [], "rows": [], "next": 1})
            for c in a["cols"]:
                if c["n"] not in t["cols"]:
                    t["cols"].append(c["n"])
            return ok(st["space"])      # one unlisted name for the whole database
        t = st["tables"].get(a.get("tbl"))
        if not t or a.get("share") not in (st["space"], t.get("share")):
            return no("no list by that name")
        if fn == "lc_read":   # keys come back sorted, as Postgres's jsonb hands them
            return ok([dict(sorted(dict(r, _change="insert").items())) for r in t["rows"]])
        if fn == "lc_save":
            for r in a["ins"]:
                r = {k: v for k, v in r.items() if k in t["cols"]}
                r["id"] = t["next"]; t["next"] += 1
                t["rows"].append(r)
            for u in a["upd"]:
                for r in t["rows"]:
                    if r["id"] == u["id"]:
                        r.update({k: v for k, v in u.items() if k in t["cols"]})
            t["rows"] = [r for r in t["rows"] if r["id"] not in a["del"]]
            return ok({"ins": len(a["ins"]), "upd": len(a["upd"]), "del": len(a["del"])})
        route.fulfill(status=404, body="")
    context.page.route("**/demo.supabase.co/rest/v1/rpc/*", handle)
    context.page.route("**/demo.supabase.co/rest/v1/walks*",
                       lambda route: route.fulfill(status=404, body="{}"))   # never read directly


@then("the grid \"{gid}\" asks for the list's unlisted name")
def step_unl_asks(context, gid):
    expect(grid(context, gid).locator("input.lc-dg-unl-name")).to_be_visible(timeout=T)
    expect(grid(context, gid).locator("button.lc-dg-save")).to_be_disabled()


@when('I say I am the author under "{gid}", with no key yet')
def step_unl_author(context, gid):
    g = grid(context, gid)
    g.locator("button.lc-dg-unl-me").click()
    # the author's field takes the name field's place, never sits beside it
    expect(g.locator("input.lc-dg-unl-name")).to_be_hidden()
    expect(g.locator("input.lc-dg-unl-akey")).to_be_visible()
    g.locator("button.lc-dg-unl-claim").click()


@then('the database has me as its author, and a table "{tbl}" made of "{cols}"')
def step_unl_made(context, tbl, cols):
    for _ in range(60):
        if tbl in context.unl["tables"]:
            break
        context.page.wait_for_timeout(200)
    assert len(context.unl["authors"]) == 1 and context.unl["authors"][0].startswith("lca_"), context.unl["authors"]
    got = context.unl["tables"][tbl]["cols"]
    assert got == [c.strip() for c in cols.split(",")], got


@then('the grid "{gid}" shows the name to share and my new author key')
def step_unl_show(context, gid):
    g = grid(context, gid)
    expect(g.locator("code.lc-dg-unl-show")).to_have_text("5f2c9a01b7e3", timeout=T)
    expect(g.locator(".lc-dg-unl-key code")).to_have_text(context.unl["authors"][0])
    expect(g.locator("input.lc-dg-unl-name")).to_have_count(0)


@when('I copy my author key under "{gid}"')
def step_unl_copy_key(context, gid):
    context.page.context.grant_permissions(["clipboard-read", "clipboard-write"])
    grid(context, gid).locator("button.lc-dg-unl-keycopy").click()


@then('the key leaves the grid "{gid}", and only the name to share stays')
def step_unl_key_gone(context, gid):
    g = grid(context, gid)
    expect(g.locator(".lc-dg-unl-key")).to_have_count(0, timeout=T)
    expect(g.locator("button.lc-dg-unl-copy")).to_have_count(1)
    expect(g.locator("code.lc-dg-unl-show")).to_have_text("5f2c9a01b7e3")
    assert context.page.evaluate("() => navigator.clipboard.readText()") == context.unl["authors"][0]


@then('the table "{tbl}" holds "{dog}", saved through its name')
def step_unl_saved(context, tbl, dog):
    for _ in range(50):
        if any(r.get("dog") == dog for r in context.unl["tables"][tbl]["rows"]):
            break
        context.page.wait_for_timeout(200)
    rows = context.unl["tables"][tbl]["rows"]
    assert [r["dog"] for r in rows] == [dog], rows
    saves = [a for f, a in context.unl["calls"] if f == "lc_save"]
    assert saves and saves[-1]["share"] == "5f2c9a01b7e3", saves


def _unl_paste(context, gid, name):
    g = grid(context, gid)
    box = g.locator("input.lc-dg-unl-name")
    expect(box).to_be_visible(timeout=T)
    box.fill(name)
    g.locator("button.lc-dg-unl-ok").click()


@when('a classmate opens the page on another device and pastes the name under "{gid}"')
def step_unl_classmate(context, gid):
    context.page.evaluate("() => { localStorage.removeItem('lc_author_demo'); localStorage.removeItem('lc_unlisted_demo_walks'); }")
    context.page.reload(wait_until="domcontentloaded")
    _unl_paste(context, gid, "5f2c9a01b7e3")


@then('the grid "{gid}" offers no name to share')
def step_unl_noshare(context, gid):
    expect(grid(context, gid).locator("code.lc-dg-unl-show")).to_have_count(0)
    expect(grid(context, gid).locator("input.lc-dg-unl-name")).to_have_count(0)


@when('a stranger pastes "{name}" under "{gid}"')
def step_unl_stranger(context, name, gid):
    context.page.evaluate("() => { localStorage.removeItem('lc_unlisted_demo_walks'); }")
    context.page.reload(wait_until="domcontentloaded")
    _unl_paste(context, gid, name)



@when('I type "{text}", the cell still open')
def step_type_open(context, text):
    cell = context.page.locator("td.lc-dg-typed.lc-dg-typing")
    expect(cell).to_be_focused(timeout=T)
    context.page.keyboard.type(text)


@when('I press Save under "{gid}" once, with the mouse')
def step_save_once_mouse(context, gid):
    b = grid(context, gid).locator("button.lc-dg-save")
    expect(b).to_be_enabled(timeout=T)
    box = b.bounding_box()
    context.page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)



@given('the shelter database holds a "{tbl}" table with "{dog}"')
def step_db_holds(context, tbl, dog):
    context.unl["tables"][tbl] = {"cols": ["dog", "walker"], "next": 2,
                                  "rows": [{"id": 1, "dog": dog, "walker": "Ana"}]}


@then('the page asked for nothing under "{gid}"')
def step_asked_nothing(context, gid):
    g = grid(context, gid)
    expect(g.locator("input.lc-dg-unl-name")).to_have_count(0)
    expect(g.locator(".lc-dg-unl")).to_have_count(0)      # nothing to say, no bar


@then('the database was read with the page\'s name and the key from databases.yml, never from the page')
def step_read_with(context):
    reads = [a for f, a in context.unl["calls"] if f == "lc_read"]
    assert reads and all(r["share"] == "5f2c9a01b7e3" and r["tbl"] == "walk" for r in reads), reads
    assert context.unl["keys"] and all(k == "sb_publishable_yml" for k in context.unl["keys"]), context.unl["keys"]
    src = context.page.evaluate("() => document.documentElement.outerHTML")
    assert "apikey=\"sb_publishable_yml\"" not in src.split("lc-db-table")[0], "the key showed in the page"


@then('the author is told the database\'s name to put on the "{db}" line under "{gid}"')
def step_author_hint(context, db, gid):
    g = grid(context, gid)
    expect(g.locator("code.lc-dg-unl-show")).to_have_text('unlisted="5f2c9a01b7e3"', timeout=T)
    expect(g.locator(".lc-dg-unl")).to_contain_text(db)



@then('the corner of "{gid}" holds ＋, ↻ and the save state, and no footer')
def step_corner(context, gid):
    g = grid(context, gid)
    c = g.locator(".lc-dg-corner")
    expect(c.locator("button.lc-dg-new")).to_have_text("＋", timeout=T)
    expect(c.locator("button.lc-dg-refresh")).to_have_count(1)
    expect(c.locator("button.lc-dg-save")).to_have_count(1)
    expect(g.locator(".lc-dg-foot")).to_have_count(0)
    gb, cb = g.bounding_box(), c.bounding_box()
    assert cb["y"] - gb["y"] < 20 and (gb["x"] + gb["width"]) - (cb["x"] + cb["width"]) < 20, (gb, cb)
    context.page.mouse.move(0, 0)
    op = float(c.locator("button.lc-dg-refresh").evaluate("e => getComputedStyle(e).opacity"))
    assert op < 0.5, "↻ shows before hovering: %s" % op


@then("nothing is sent while the new row is blank")
def step_nothing_blank(context):
    context.page.wait_for_timeout(1500)
    sent = [c for c in context.db_calls[context.db_mark:] if c["method"] != "GET"]
    assert not sent, sent



@when('I write the name the grid gave on the "{db}" line of the "{pad_id}" pad')
def step_write_name(context, db, pad_id):
    context.page.evaluate("""([db, pid]) => {
      const ta = document.querySelector(`[data-lc-id='${pid}'] .lc-mdpad-in`);
      ta.value = ta.value.replace(`{: .database #${db} }`, `{: .database #${db} unlisted="5f2c9a01b7e3" }`);
      ta.dispatchEvent(new Event('input', { bubbles: true }));
    }""", [db, pad_id])


@then('the grid "{gid}" says nothing more about names')
def step_no_names(context, gid):
    g = grid(context, gid)
    expect(g.locator(".lc-dg-unl")).to_have_count(0, timeout=T)
    reads = [a for f, a in context.unl["calls"] if f == "lc_read"]
    assert reads and reads[-1]["share"] == "5f2c9a01b7e3", reads
