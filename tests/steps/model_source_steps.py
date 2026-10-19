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


@then('the stage cell of "{name}" in "{gid}" is a chip, with no caret')
def step_chip(context, name, gid):
    cell = row_of(context, gid, name).locator("td.lc-dg-state")
    expect(cell.locator(".lc-dg-chip")).to_be_visible(timeout=T)
    expect(cell.locator(".lc-dg-caret")).to_have_count(0)


@when('I open the verbs of "{name}" in "{gid}"')
def step_open(context, name, gid):
    row_of(context, gid, name).locator("td.lc-dg-gut button").click()
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
    row_of(context, gid, name).locator("td:not(.lc-dg-gut)").first.click()


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
        " const name = tr.querySelector('td:not(.lc-dg-gut)').textContent.trim();"
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
    context.new_row.locator("td.lc-dg-gut button").click()
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


@then('the chip and the family name of "{name}" in "{gid}" share one middle line')
def step_chip_aligned(context, name, gid):
    r = row_of(context, gid, name)
    expect(r.locator(".lc-dg-chip")).to_be_visible(timeout=T)
    mids = context.page.evaluate(
        """tr => { const mid = e => { const b = e.getBoundingClientRect(); return (b.top + b.bottom) / 2; };
           const name = document.createRange(); name.selectNodeContents(tr.querySelector('td:not(.lc-dg-gut)'));
           const nb = name.getBoundingClientRect();
           return { name: (nb.top + nb.bottom) / 2, chip: mid(tr.querySelector('.lc-dg-chip')) }; }""",
        r.element_handle())
    assert abs(mids["chip"] - mids["name"]) <= 2.5, mids


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


@then('the stage chips of "{gid}" are all as wide')
def step_chips_wide(context, gid):
    expect(grid(context, gid).locator(".lc-dg-chip").first).to_be_visible(timeout=T)
    got = context.page.evaluate(
        "g => [...document.querySelectorAll(\".lc-datagrid[data-lc-id='\" + g + \"'] td.lc-dg-state\")].map(td =>"
        " Math.round(td.querySelector('.lc-dg-chip').getBoundingClientRect().width))", gid)
    assert len(set(got)) == 1 and got, got


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
    grid(context, gid).locator("button.lc-dg-roreload").click()


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
                if c["n"] == "_sub" and "_sub" not in t["cols"]:
                    t["cols"].append("_sub")
                    continue
                if c.get("was") and c["was"] in t["cols"] and c["n"] not in t["cols"]:
                    t["cols"][t["cols"].index(c["was"])] = c["n"]
                    for r in t["rows"]:
                        r[c["n"]] = r.pop(c["was"], None)
                if c["n"] not in t["cols"]:
                    t["cols"].append(c["n"])
                # as Postgres: a type changed in the class retypes the column
                typ = c.get("t", "str") if c.get("t") in ("int", "float", "bool") else "str"
                old_t = t.setdefault("types", {}).get(c["n"])
                if old_t is not None and old_t != typ and typ in ("int", "float"):
                    for r in t["rows"]:
                        v = r.get(c["n"])
                        if v is None or str(v).strip() == "":
                            r[c["n"]] = None
                            continue
                        try:
                            r[c["n"]] = int(v) if typ == "int" else float(v)
                        except ValueError:
                            return no(c["n"] + " holds a value that is not " + typ + ", fix it in the grid, then ↻")
                t["types"][c["n"]] = typ
            return ok(st["space"])      # one unlisted name for the whole database
        if fn == "lc_drop":
            if a["token"] not in st["authors"]:
                return no("only the author changes tables")
            t = st["tables"][a["tbl"]]
            for c in a["cols"]:
                if c != "id" and not c.startswith("_") and c in t["cols"]:
                    t["cols"].remove(c)
                    for r in t["rows"]:
                        r.pop(c, None)
            return ok(len(a["cols"]))
        t = st["tables"].get(a.get("tbl"))
        if not t or a.get("share") not in (st["space"], t.get("share")):
            return no("no list by that name")
        if fn == "lc_read":   # keys come back sorted, as Postgres's jsonb hands them
            return ok([dict(sorted(dict(r, _change="insert").items())) for r in t["rows"]])
        if fn == "lc_save":
            if st.get("refuse"):
                st["refuse"] = False
                return no(st.get("refuse_why", "refused"))
            # as Postgres: a number column takes a number or null, never ""
            for r in a["ins"] + a["upd"]:
                for k, v in r.items():
                    if v == "" and t.get("types", {}).get(k) in ("int", "float", "bool"):
                        return no('invalid input syntax for type bigint: ""')
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
    order = c.evaluate("e => [...e.querySelectorAll('button')].map(b => b.classList.contains('lc-dg-new') ? 'new' : b.classList.contains('lc-dg-save') ? 'save' : b.classList.contains('lc-dg-refresh') ? 'refresh' : 'other')")
    assert order[-3:] == ["refresh", "save", "new"], "right to left must read ＋, status, ↻: " + str(order)
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



@then('the title of "{gid}" wears "{icon}" instead of "▦", saying "{text}"')
def step_title_icon(context, gid, icon, text):
    bar = grid(context, gid).locator(".lc-dg-titlebar")
    expect(bar).to_contain_text(icon, timeout=T)
    assert "▦" not in bar.inner_text(), bar.inner_text()
    expect(bar).to_have_attribute("title", text)


@then('the menu\'s "{verb}" reads "{label}", saying "{text}"')
def step_menu_label(context, verb, label, text):
    b = context.page.locator(".lc-dg-menu button[data-verb='" + verb + "']")
    expect(b.locator("span")).to_have_text(label, timeout=T)
    expect(b).to_have_attribute("title", text)


@then('the form "{fid}" has a button "{label}"')
def step_form_button(context, fid, label):
    expect(context.page.locator("[data-lc-id='" + fid + "'] .lc-form-verb, .lc-form[data-lc-id='" + fid + "'] ~ .lc-form-verbs .lc-form-verb").filter(has_text=label).first).to_be_visible(timeout=T)



@then('the form "{fid}" shows no "{field}" field')
def step_form_no_field(context, fid, field):
    form = context.page.locator("[data-lc-id='" + fid + "']")
    expect(form).to_contain_text("Biscuit", timeout=T)
    assert "hour" not in form.inner_text().lower(), form.inner_text()



@given('the shelter database holds the dogs "{a}" and "{b}", and a walk of "{dog}" by "{walker}"')
def step_db_dogs(context, a, b, dog, walker):
    t = context.unl["tables"]
    t["dog"] = {"cols": ["name"], "next": 3, "rows": [{"id": 1, "name": a}, {"id": 2, "name": b}]}
    did = 1 if dog == a else 2
    t["walk"] = {"cols": ["dog", "walker"], "next": 2, "rows": [{"id": 1, "dog": str(did), "walker": walker}]}


@then('the walk of "{walker}" in "{gid}" names the dog "{dog}", among "{dogs}"')
def step_walk_dog(context, walker, gid, dog, dogs):
    cell = row_of(context, gid, walker).locator("td.lc-dg-refcell")
    expect(cell.locator(".lc-dg-refval")).to_have_text(dog, timeout=T)          # plain, like any other cell
    expect(cell.locator(".lc-dg-caret")).to_have_text("⌄")
    assert cell.locator("select").count() == 0
    assert not [c for c in context.unl["calls"] if c[0] == "lc_save"], "reading the walks saved them back"
    cell.click()
    menu = context.page.locator(".lc-dg-refmenu")
    expect(menu).to_be_visible(timeout=T)
    opts = [o.strip() for o in menu.locator("button[data-obj]:not([data-obj=''])").all_inner_texts()]
    assert opts == [d.strip() for d in dogs.split(",")], opts
    mb, cb = menu.bounding_box(), cell.bounding_box()
    assert mb["width"] >= max(cb["width"], 180) - 1, (mb, cb)      # roomy, never narrower than its cell
    expect(menu.locator(".lc-dg-cur")).to_contain_text(dog)
    context.page.keyboard.press("Escape")
    context.page.mouse.click(5, 5)


@then('the column "{col}" of "{gid}" wears "{icon}"')
def step_col_icon(context, col, gid, icon):
    expect(grid(context, gid).locator("thead th[data-col='" + col + "']")).to_contain_text(icon, timeout=T)


@when('I pick the dog "{dog}" for the walk of "{walker}" in "{gid}"')
def step_pick_dog(context, dog, walker, gid):
    row_of(context, gid, walker).locator("td.lc-dg-refcell").click()
    context.page.locator(".lc-dg-refmenu button[data-obj]", has_text=dog).click()


@then('the table "{tbl}" saved the walk of "{walker}" with the dog\'s id {did:d}')
def step_saved_ref(context, tbl, walker, did):
    for _ in range(50):
        rows = context.unl["tables"][tbl]["rows"]
        if any(r.get("walker") == walker and str(r.get("dog")) == str(did) for r in rows):
            return
        context.page.wait_for_timeout(200)
    raise AssertionError(str(context.unl["tables"][tbl]["rows"]) + " " + str([c for c in context.unl["calls"] if c[0] == "lc_save"]))



@then('the form "{fid}" names the dog "{dog}", never "{internal}"')
def step_form_dog(context, fid, dog, internal):
    form = context.page.locator("[data-lc-id='" + fid + "']")
    expect(form).to_contain_text(dog, timeout=T)
    assert internal not in form.inner_text(), form.inner_text()



@given('the shelter database holds a "{tbl}" table with an old "{old}" column, and "{dog}" walked by "{who}"')
def step_db_old(context, tbl, old, dog, who):
    context.unl["tables"][tbl] = {"cols": ["dog", "walker", old], "next": 2,
                                  "rows": [{"id": 1, "dog": dog, "walker": who, old: "2"}]}


@given("I am the shelter's author on this device")
def step_i_am_author(context):
    key = "lca_" + "a" * 32
    context.unl["authors"].append(key)
    context.page.add_init_script("try { localStorage.setItem('lc_author_demo', '" + key + "'); } catch (e) {}")


@then('the table "{tbl}" renamed "{old}" to "{new}", keeping "{value}"')
def step_renamed(context, tbl, old, new, value):
    for _ in range(50):
        t = context.unl["tables"][tbl]
        if new in t["cols"] and old not in t["cols"]:
            assert any(r.get(new) == value for r in t["rows"]), t
            return
        context.page.wait_for_timeout(200)
    raise AssertionError(str(context.unl["tables"][tbl]) + " " + str(context.unl["calls"]))


def _open_panel(context, gid):
    b = grid(context, gid).locator(".lc-dg-corner button.lc-dg-tidy, .lc-dg-corner button.lc-dg-struct").first
    expect(b).to_be_visible(timeout=T)
    b.click()
    panel = context.page.locator(".lc-struct-panel")
    expect(panel).to_be_visible(timeout=T)
    return panel


@then('the corner of "{gid}" offers 🧹 for "{cols}"')
def step_tidy_offered(context, gid, cols):
    # 🧹 lives in the structure panel (Michel, 2026-10-18): the corner opens it
    panel = _open_panel(context, gid)
    items = " ".join(panel.locator(".lc-struct-tidy li").all_inner_texts())
    for c in cols.split(", "):
        assert c in items, items
    panel.locator(".lc-struct-later").click()


@when('I tidy the table under "{gid}", confirming')
def step_tidy(context, gid):
    panel = _open_panel(context, gid)
    for box in panel.locator(".lc-struct-tidy input[type=checkbox]").all():
        box.check()
    panel.locator(".lc-struct-apply").click()
    expect(panel).to_have_count(0, timeout=T)


@then('the table "{tbl}" has no column "{col}", and no 🧹 is left under "{gid}"')
def step_no_col(context, tbl, col, gid):
    for _ in range(50):
        if col not in context.unl["tables"][tbl]["cols"]:
            break
        context.page.wait_for_timeout(200)
    assert col not in context.unl["tables"][tbl]["cols"], context.unl["tables"][tbl]
    expect(grid(context, gid).locator("button.lc-dg-tidy")).to_have_count(0, timeout=T)



@then('the walk of "{walker}" in "{gid}" shows "{text}" in its computed "{col}" column, read-only')
def step_computed(context, walker, gid, text, col):
    cell = row_of(context, gid, walker).locator("td").nth(
        [t.strip().lower() for t in grid(context, gid).locator("thead th").all_inner_texts()].index(col))
    expect(cell).to_have_text(text, timeout=T)
    assert cell.get_attribute("contenteditable") != "true" and "lc-dg-typed" not in (cell.get_attribute("class") or "")
    saves = [a for f, a in context.unl["calls"] if f == "lc_save"]
    assert not any(col in r for x in saves for r in x["ins"] + x["upd"]), saves


@then('the table "{tbl}" has no column "{col}"')
def step_no_column(context, tbl, col):
    assert col not in context.unl["tables"][tbl]["cols"], context.unl["tables"][tbl]



@then('the model "{mid}" asks which class wears "{src}"')
def step_model_asks(context, mid, src):
    el = context.page.locator("[data-lc-id='" + mid + "']")
    expect(el).to_have_attribute("data-lc-warn", re.compile("which class wears it"), timeout=T)



@when('I type the attribute "{line}" into the class in the "{pad_id}" pad, letter by letter')
def step_type_attr(context, line, pad_id):
    context.db_ensures0 = len([c for c in context.unl["calls"] if c[0] == "lc_ensure"])
    sel = "[data-lc-id='" + pad_id + "'] .lc-mdpad-in"
    base = context.page.evaluate("s => document.querySelector(s).value", sel)
    anchor = "    walker = Attr(str)\n"
    assert anchor in base, base
    for i in range(1, len(line) + 1):
        v = base.replace(anchor, anchor + "    " + line[:i] + "\n", 1)
        context.page.evaluate("""([s, v]) => { const ta = document.querySelector(s); ta.value = v;
          ta.dispatchEvent(new Event('input', { bubbles: true })); }""", [sel, v])
        context.page.wait_for_timeout(250)
    context.page.wait_for_timeout(2500)


@then('no column was made while typing, and 🔄 under "{gid}" offers "{col}"')
def step_no_cols_typing(context, gid, col):
    ens = [c for c in context.unl["calls"] if c[0] == "lc_ensure"][context.db_ensures0:]
    assert not ens, "columns made while typing: " + str(ens)
    panel = _open_panel(context, gid)
    plan = " ".join(panel.locator(".lc-struct-plan li").all_inner_texts())
    assert col in plan, plan
    panel.locator(".lc-struct-later").click()


@when('I apply the structure under "{gid}"')
def step_apply_under(context, gid):
    panel = _open_panel(context, gid)
    panel.locator(".lc-struct-apply").click()
    expect(panel).to_have_count(0, timeout=T)


@when('I press ↻ under "{gid}"')
def step_press_refresh(context, gid):
    grid(context, gid).locator("button.lc-dg-refresh").click()


@then('the table "{tbl}" gained the column "{col}", and no other')
def step_gained_only(context, tbl, col):
    for _ in range(50):
        cols = context.unl["tables"][tbl]["cols"]
        if col in cols:
            break
        context.page.wait_for_timeout(200)
    cols = context.unl["tables"][tbl]["cols"]
    assert col in cols and not [c for c in cols if c != col and col.startswith(c[:1]) and c not in ("dog", "walker")], cols



@when('the "{pad_id}" pad redraws its class twice while the walk is saving')
def step_redraw_twice(context, pad_id):
    sel = "[data-lc-id='" + pad_id + "'] .lc-mdpad-in"
    for extra in ("\n", ""):
        context.page.evaluate("""([s, x]) => { const ta = document.querySelector(s);
          ta.value = ta.value.replace("    walker = Attr(str)\\n", "    walker = Attr(str)\\n" + x).replace("\\n\\n\\n", "\\n\\n");
          ta.dispatchEvent(new Event('input', { bubbles: true })); }""", [sel, extra])
        context.page.wait_for_timeout(300)
    context.page.wait_for_timeout(3000)


@then('the table "{tbl}" holds "{dog}" once')
def step_holds_once(context, tbl, dog):
    rows = [r for r in context.unl["tables"][tbl]["rows"] if dog in (str(r.get("dog")), str(r.get("walker")))]
    assert len(rows) == 1, context.unl["tables"][tbl]["rows"]



@when('the page\'s picture of the "{tbl}" table is lost, and the grid saves')
def step_snap_lost(context, tbl):
    context.db_saves0 = len([c for c in context.unl["calls"] if c[0] == "lc_save"])
    context.page.evaluate("""t => { const r = window.lcRemote['shelter_' + t]; r.snap = {};
      return window.lcDatasetSave('shelter_' + t); }""", tbl)
    context.page.wait_for_timeout(1500)


@then("no walk is sent again")
def step_none_again(context):
    saves = [a for f, a in context.unl["calls"] if f == "lc_save"][context.db_saves0:]
    assert not any(x["ins"] for x in saves), saves



@given('the shelter\'s "{tbl}" table holds a walk, a "{a}" and a "{b}"')
def step_db_kinds(context, tbl, a, b):
    context.unl["tables"][tbl] = {"cols": ["dog", "walker", "_sub"], "next": 4,
        "rows": [{"id": 1, "dog": "Lucky", "walker": "Ana", "_sub": None},
                 {"id": 2, "dog": "Fern", "walker": "Ben", "_sub": a},
                 {"id": 3, "dog": "Rex", "walker": "Cleo", "_sub": b}]}


@then('the walk by "{who}" is a "{kind}" in the grid "{gid}"')
def step_is_kind(context, who, kind, gid):
    k = None
    for _ in range(50):
        k = context.page.evaluate("""w => { const r = (window.lcDatasets.Walk || []).find(x => x.walker === w);
          return r ? (r._kind || 'Walk') : null; }""", who)
        if k == kind:
            return
        context.page.wait_for_timeout(200)
    raise AssertionError(str(k))


@then('the table "{tbl}" calls the walk by "{who}" a "{kind}"')
def step_table_kind(context, tbl, who, kind):
    for _ in range(50):
        r = [x for x in context.unl["tables"][tbl]["rows"] if x.get("walker") == who][0]
        if (r.get("_sub") or "") == kind:
            return
        context.page.wait_for_timeout(200)
    raise AssertionError(str(context.unl["tables"][tbl]["rows"]))



@then('the table "{tbl}" calls the walk by "{who}" by no class')
def step_table_nokind(context, tbl, who):
    step_table_kind(context, tbl, who, "")



@then('the row of "{who}" in "{gid}" wears "{icon}" in its gutter, which opens its verbs')
def step_gutter_icon(context, who, gid, icon):
    b = row_of(context, gid, who).locator("td.lc-dg-gut .lc-dg-rowmenu")
    expect(b).to_have_text(icon, timeout=T)
    b.click()
    expect(context.page.locator(".lc-dg-menu button[data-verb='delete']")).to_be_visible(timeout=T)
    context.page.keyboard.press("Escape")
    context.page.mouse.click(5, 5)



@when('I delete the walk by "{who}" in "{gid}", reading the question')
def step_delete_reading(context, who, gid):
    context.asked = []
    def on(d):
        context.asked.append(d.message)
        d.dismiss()
    context.page.once("dialog", on)
    row_of(context, gid, who).locator("td.lc-dg-gut .lc-dg-rowmenu").click()
    context.page.locator(".lc-dg-menu button[data-verb='delete']").click()
    context.page.wait_for_timeout(500)


@then('the question was "{text}"')
def step_question(context, text):
    assert context.asked == [text], context.asked



@then('the table "{tbl}" holds a "{kind}" of "{dog}"')
def step_table_kind_of(context, tbl, kind, dog):
    for _ in range(50):
        rs = [x for x in context.unl["tables"][tbl]["rows"] if x.get("dog") == dog]
        if rs and (rs[0].get("_sub") or "") == kind:
            return
        context.page.wait_for_timeout(200)
    raise AssertionError(str(context.unl["tables"][tbl]["rows"]))


@then('the corner of "{gid}" says saved')
def step_corner_saved(context, gid):
    expect(grid(context, gid).locator("button.lc-dg-save")).to_have_text("✓", timeout=T)


@when('the database refuses the next save with "{why}"')
def step_refuse_next(context, why):
    context.unl["refuse"] = True
    context.unl["refuse_why"] = why


@then('the grid "{gid}" says "{text}" under it, no hover needed')
def step_grid_says(context, gid, text):
    expect(grid(context, gid).locator(".lc-dg-say")).to_contain_text(text, timeout=T)


@then('the corner of "{gid}" offers no 🧹')
def step_no_tidy(context, gid):
    expect(grid(context, gid).locator("button.lc-dg-tidy")).to_have_count(0, timeout=T)


@when('I tap the gutter of "{who}" in "{gid}"')
def step_tap_gutter(context, who, gid):
    row_of(context, gid, who).locator("td.lc-dg-gut .lc-dg-rowmenu").click()


@then('the row of "{who}" is the selection of "{gid}", its verbs open')
def step_gutter_selects(context, who, gid):
    expect(grid(context, gid).locator("tbody tr.lc-dg-selected")).to_have_count(1, timeout=T)
    expect(grid(context, gid).locator("tbody tr.lc-dg-selected")).to_contain_text(who, timeout=T)
    expect(context.page.locator(".lc-dg-menu button[data-verb='delete']")).to_be_visible(timeout=T)
    context.page.keyboard.press("Escape")
    context.page.mouse.click(5, 5)


@given('the shelter\'s "{tbl}" table holds a walk by "{who}" at "{hour}"')
def step_db_walk_at(context, tbl, who, hour):
    context.unl["tables"][tbl] = {"cols": ["walker", "hour"], "next": 2,
                                  "types": {"walker": "str", "hour": "str"},
                                  "rows": [{"id": 1, "walker": who, "hour": hour}]}


@then('the table "{tbl}" holds a walk by "{who}" at "{hour}", and no "{col}" column')
def step_db_walk_saved(context, tbl, who, hour, col):
    t = context.unl["tables"][tbl]
    for _ in range(50):
        if any(r.get("walker") == who and r.get("hour") == hour for r in t["rows"]):
            break
        context.page.wait_for_timeout(200)
    else:
        raise AssertionError(str(t["rows"]))
    assert col not in t["cols"], t["cols"]
    saves = [a for f, a in context.unl["calls"] if f == "lc_save"]
    assert not any(col in r for x in saves for r in x["ins"] + x["upd"]), saves


@then('the "{col}" cells of "{gid}" stay closed, and the grid says "{text}"')
def step_cells_closed_say(context, col, gid, text):
    g = grid(context, gid)
    expect(g.locator("tbody tr").first).to_be_visible(timeout=T)
    expect(g.locator(".lc-dg-say")).to_contain_text(text, timeout=T)
    assert g.locator("td.lc-dg-typed[data-col='" + col + "']").count() == 0, "the cells open"


@given('the shelter\'s "{tbl}" table holds a text "{col}" column, blank for "{who}" and "{b}" for "{who2}"')
def step_db_text_col(context, tbl, col, who, b, who2):
    a = ""
    context.unl["tables"][tbl] = {"cols": ["walker", col, "_sub"], "next": 3,
                                  "types": {"walker": "str", col: "str"},
                                  "rows": [{"id": 1, "walker": who, col: a, "_sub": "Sprint"},
                                           {"id": 2, "walker": who2, col: b, "_sub": "Sprint"}]}


@then('the table "{tbl}" made "{col}" a number: none for "{who}", {n:d} for "{who2}"')
def step_db_retyped(context, tbl, col, who, n, who2):
    t = context.unl["tables"][tbl]
    for _ in range(50):
        if t["types"].get(col) == "int":
            break
        context.page.wait_for_timeout(200)
    rows = {r["walker"]: r.get(col) for r in t["rows"]}
    assert t["types"].get(col) == "int" and rows[who] is None and rows[who2] == n, (t["types"], rows)


@when('I run "{verb}" on the walk by "{who}" in "{gid}"')
def step_press_verb(context, verb, who, gid):
    row_of(context, gid, who).locator("td.lc-dg-gut .lc-dg-rowmenu").click()
    context.page.locator(".lc-dg-menu button[data-verb='" + verb + "']").click()


@then('the table "{tbl}" saved {n:d} {col} for "{who}", and the grid says nothing wrong')
def step_db_saved_n(context, tbl, n, col, who):
    t = context.unl["tables"][tbl]
    for _ in range(60):
        r = [x for x in t["rows"] if x.get("walker") == who][0]
        if r.get(col) == n:
            break
        context.page.wait_for_timeout(250)
    else:
        raise AssertionError(str(t["rows"]))
    says = grid(context, "walks").locator(".lc-dg-say")
    assert not says.count() or "⚠" not in says.first.inner_text(), says.first.inner_text()


@when('I tap "{verb}" in the form "{fid}"')
def step_form_press(context, verb, fid):
    b = context.page.locator("[data-lc-id='" + fid + "']").locator("..").locator(".lc-form-verbs button", has_text=verb).first
    expect(b).to_be_visible(timeout=T)
    b.click()


@then('the form "{fid}" says "{text}"')
def step_form_says(context, fid, text):
    # said in the form's own frame (the one that holds its verbs), not only under a grid
    f = context.page.locator("[data-lc-say]:has([data-lc-id='" + fid + "']), [data-lc-id='" + fid + "'][data-lc-say]").first
    expect(f.locator(".lc-dg-say").first).to_contain_text(text, timeout=T)


@given('the shelter database holds the dogs "{a}" and "{b}", a walk of "{d1}" by "{w1}" and one of "{d2}" by "{w2}"')
def step_db_two_walks(context, a, b, d1, w1, d2, w2):
    t = context.unl["tables"]
    t["dog"] = {"cols": ["name"], "next": 3, "rows": [{"id": 1, "name": a}, {"id": 2, "name": b}]}
    ids = {a: "1", b: "2"}
    t["walk"] = {"cols": ["dog", "walker"], "next": 3,
                 "rows": [{"id": 1, "dog": ids[d1], "walker": w1}, {"id": 2, "dog": ids[d2], "walker": w2}]}


@when('I tap the dog of "{who}" in "{gid}"')
def step_tap_dog(context, who, gid):
    row_of(context, gid, who).locator("td.lc-dg-refcell").click()


@then('the row of "{who}" is selected in "{gid}" and the dogs are offered')
def step_dog_row_selected(context, who, gid):
    expect(context.page.locator(".lc-dg-refmenu")).to_be_visible(timeout=T)
    sel = grid(context, gid).locator("tbody tr.lc-dg-selected")
    expect(sel).to_have_count(1, timeout=T)
    expect(sel).to_contain_text(who)


@when('I pick "{dog}" in the open list')
def step_pick_open(context, dog):
    context.page.locator(".lc-dg-refmenu button[data-obj]", has_text=dog).first.click()


@then('the form "{fid}" shows "{text}"')
def step_form_shows(context, fid, text):
    expect(context.page.locator("[data-lc-id='" + fid + "']")).to_contain_text(text, timeout=T)


@when('I pick the dog "{dog}" in the form "{fid}", from the same list as the grid\'s')
def step_form_pick_dog(context, dog, fid):
    form = context.page.locator("[data-lc-id='" + fid + "']")
    pick = form.locator(".lc-form-refpick").first
    expect(pick).to_be_visible(timeout=T)
    assert form.locator("select").count() == 0, "the form still shows a native list"
    pick.click()
    menu = context.page.locator(".lc-dg-refmenu")
    expect(menu).to_be_visible(timeout=T)
    menu.locator("button[data-obj]", has_text=dog).first.click()


@then('every row of "{gid}" wears the gutter, which opens its verbs')
def step_every_gutter(context, gid):
    g = grid(context, gid)
    expect(g.locator("tbody tr").first).to_be_visible(timeout=T)
    n = g.locator("tbody tr").count()
    expect(g.locator("tbody tr td.lc-dg-gut .lc-dg-rowmenu")).to_have_count(n, timeout=T)
    g.locator("tbody tr td.lc-dg-gut .lc-dg-rowmenu").first.click()
    expect(context.page.locator(".lc-dg-menu button[data-verb='delete']")).to_be_visible(timeout=T)
    context.page.keyboard.press("Escape")
    context.page.mouse.click(5, 5)


def _hhmm(context):
    return context.page.evaluate("() => { const d = new Date(); const p = n => String(n).padStart(2, '0'); return [p(d.getHours()) + ':' + p(d.getMinutes()), p(d.getHours()) + ':' + p((d.getMinutes() + 59) % 60)]; }")


def _col(context, gid, name):
    ths = grid(context, gid).locator("thead th").all_inner_texts()
    cols = [re.sub(r"\s*[↑↓]$", "", t.strip()).lower() for t in ths]
    return cols.index(name)


@then('the row "{name}" of "{gid}" has an empty "{col}" cell')
def step_empty_cell(context, name, gid, col):
    r = row_of(context, gid, name)
    expect(r).to_be_visible(timeout=T)
    expect(r.locator("td").nth(_col(context, gid, col))).to_have_text("")


@then('the row "{name}" of "{gid}" shows "{text}" in "{col}"')
def step_cell_shows(context, name, gid, text, col):
    r = row_of(context, gid, name)
    expect(r).to_be_visible(timeout=T)
    expect(r.locator("td").nth(_col(context, gid, col))).to_have_text(text, timeout=T)


@then('the row "{name}" of "{gid}" shows the hour of this minute in "{col}"')
def step_cell_now(context, name, gid, col):
    r = row_of(context, gid, name)
    expect(r).to_be_visible(timeout=T)
    cell = r.locator("td").nth(_col(context, gid, col))
    expect(cell).not_to_have_text("", timeout=T)
    assert cell.inner_text().strip() in _hhmm(context), cell.inner_text()


@then('the new row of "{gid}" says "{note}" and the hour of this minute')
def step_new_row_born(context, gid, note):
    r = grid(context, gid).locator("tbody tr.lc-dg-selected").first
    expect(r.locator("td", has_text=note)).to_have_count(1, timeout=T)
    cell = r.locator("td").nth(_col(context, gid, "at"))
    assert cell.inner_text().strip() in _hhmm(context), cell.inner_text()


@when('I run the python "{code}"')
def step_run_py(context, code):
    context.page.evaluate("c => window.lcPySend(c)", code)








@then("DEBUG proof error")
def step_debug_proof(context):
    pg = context.page
    pg.wait_for_timeout(1000)
    print("ERR:", [t[:400] for t in pg.locator("[data-lc-id='born_proof'] .lc-feature-step-err").all_inner_texts()])


@then('the verbs of "{fid}" read "{names}"')
def step_verbs_order(context, fid, names):
    bar = context.page.locator("#" + fid + " .lc-form-verbs, .lc-form[data-lc-id='" + fid + "'] .lc-form-verbs, [data-lc-id='" + fid + "'] ~ .lc-form-verbs").first
    want = [n.strip() for n in names.split(",")]
    expect(bar.locator("button.lc-form-verb")).to_have_count(len(want), timeout=T)
    got = [re.sub(r"^\S+\s+", "", t.strip()) if not t.strip()[0].isalpha() else t.strip() for t in bar.locator("button.lc-form-verb").all_inner_texts()]
    assert got == want, got







@when('I edit the "{col}" cell of "{name}" in "{gid}" to "{text}"')
def step_edit_plain_cell(context, col, name, gid, text):
    """a plain grid's cell (no class): contenteditable on double click"""
    r = row_of(context, gid, name)
    heads = [re.sub(r"\s*[↑↓]$", "", t.strip()).lower() for t in grid(context, gid).locator("thead th").all_inner_texts()]
    cell = r.locator("td").nth(heads.index(col))
    cell.dblclick()
    expect(cell).to_have_attribute("contenteditable", "true", timeout=T)
    context.page.keyboard.press("Control+A")
    context.page.keyboard.type(text)
    context.page.keyboard.press("Enter")


@then('the table "{tbl}" now has "{dog}" walked by "{who}", saved through its name')
def step_unl_saved_walker(context, tbl, dog, who):
    for _ in range(50):
        if any(r.get("dog") == dog and r.get("walker") == who for r in context.unl["tables"][tbl]["rows"]):
            break
        context.page.wait_for_timeout(200)
    rows = context.unl["tables"][tbl]["rows"]
    assert [(r["dog"], r["walker"]) for r in rows] == [(dog, who)], rows
    saves = [a for f, a in context.unl["calls"] if f == "lc_save"]
    assert saves and saves[-1]["share"] == "5f2c9a01b7e3", saves
