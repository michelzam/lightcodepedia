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
    context.page.keyboard.type(text.replace("\\n", "\n"))     # "\n" in the feature is a new line


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


@then('the "{pad_id}" pad\'s text keeps every decoration glued to its line')
def step_pad_glued(context, pad_id):
    """A seed is a fence, and a fence is verbatim: the runner used to put a
    blank line above every decoration in it (Michel, 2026-10-09)."""
    ta = _ta(context, pad_id)
    ta.wait_for(state="attached", timeout=20_000)
    v = ta.input_value()
    assert "{: .dataset" in v, "the pad lost its seed: %r" % v[:200]
    assert "\n\n{:" not in v, "a blank line above a decoration: %r" % v[max(0, v.find("\n\n{:") - 40):v.find("\n\n{:") + 30]


def _gutter_icon(context, pad_id, n):
    sel = "[data-lc-id='%s'] .lc-mdpad-piano .ln[data-n='%d']" % (pad_id, n)
    context.page.wait_for_selector(sel, state="attached", timeout=20_000)
    return context.page.eval_on_selector(sel, "l => l.getAttribute('data-ic') || ''")


@then('the "{pad_id}" pad\'s gutter shows "{a}" on line {la:d}, "{b}" on line {lb:d} and "{c}" on line {lc:d}')
def step_gutter_icons(context, pad_id, a, la, b, lb, c, lc):
    # the icons arrive with the component model, a fetch after the first paint
    context.page.wait_for_function(
        "s => document.querySelector(s)",
        arg="[data-lc-id='%s'] .lc-mdpad-piano .ln[data-ic]" % pad_id, timeout=20_000)
    for want, n in ((a, la), (b, lb), (c, lc)):
        got = _gutter_icon(context, pad_id, n)
        assert got == want, "line %d wears %r, expected %r" % (n, got, want)


@then('the "{pad_id}" pad\'s gutter shows no icon on line {n:d}')
def step_gutter_none(context, pad_id, n):
    got = _gutter_icon(context, pad_id, n)
    assert not got, "line %d wears %r — an id alone names no component" % (n, got)


@then('the "{pad_id}" pad\'s text keeps every decoration glued to its line, fences aside')
def step_pad_glued_fences_aside(context, pad_id):
    """A saved copy healed on load; a fence inside the learner's text stays
    verbatim — code shown as code is not a decoration."""
    ta = _ta(context, pad_id)
    ta.wait_for(state="attached", timeout=20_000)
    v = ta.input_value()
    assert "[dogs](dogs.yaml)\n{: .dataset #dogs }" in v, "the dataset's decoration still floats: %r" % v
    assert "[The dogs](#)\n{: .datagrid" in v, "the datagrid's decoration still floats: %r" % v
    assert "[kept](#)\n\n{: .verbatim }" in v, "a fence's text was touched: %r" % v


@then('the "{pad_id}" pad paints the dataset\'s columns in turns')
def step_pad_csv_piano(context, pad_id):
    """Michel, 2026-10-10: "a csv snippet should be displayed in alternate
    colors every column (kinda piano)" — the pad's rows fence included."""
    sel = "[data-lc-id='%s'] .lc-mdpad-piano" % pad_id
    got = context.page.eval_on_selector(
        sel, "p => [...p.querySelectorAll('.md-c0, .md-c1')].slice(0, 4).map(s => s.className + ':' + s.textContent)")
    assert got[:2] == ["md-c0:family", "md-c1:dog"], "columns not painted in turns: %r" % got


def _pad_heights(context, pad_id):
    return context.page.evaluate("""(id) => {
      const w = document.querySelector("[data-lc-id='" + id + "']");
      const h = (s) => Math.round(w.querySelector(s).getBoundingClientRect().height);
      return { pad: Math.round(w.getBoundingClientRect().height), editor: h('.lc-mdpad-in'), preview: h('.lc-mdpad-out') };
    }""", pad_id)


@when('I drag the "{pad_id}" pad\'s grip {dy:d}px {way}')
def step_drag_grip(context, pad_id, dy, way):
    if not hasattr(context, "pad_h0"):
        context.pad_h0 = _pad_heights(context, pad_id)
    grip = context.page.locator("[data-lc-id='%s'] .lc-mdpad-grip" % pad_id)
    grip.scroll_into_view_if_needed()
    box = grip.bounding_box()
    assert box, "no grip under the pad"
    x, y = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
    d = dy if way == "down" else -dy
    m = context.page.mouse
    m.move(x, y); m.down(); m.move(x, y + d / 2); m.move(x, y + d); m.up()
    context.page.wait_for_timeout(200)


@then('the "{pad_id}" pad\'s editor and preview grew by about {dy:d}px')
def step_pad_grew(context, pad_id, dy):
    h = _pad_heights(context, pad_id)
    for k in ("editor", "preview"):
        grown = h[k] - context.pad_h0[k]
        assert abs(grown - dy) <= 12, "%s grew %dpx, expected about %d (%r → %r)" % (k, grown, dy, context.pad_h0, h)


@then('the "{pad_id}" pad\'s editor and preview are shorter than at first')
def step_pad_shorter(context, pad_id):
    h = _pad_heights(context, pad_id)
    for k in ("editor", "preview"):
        assert h[k] < context.pad_h0[k], "%s did not shrink: %r → %r" % (k, context.pad_h0, h)


@when('I double-click the "{pad_id}" pad\'s grip')
def step_dbl_grip(context, pad_id):
    context.page.locator("[data-lc-id='%s'] .lc-mdpad-grip" % pad_id).dblclick()
    context.page.wait_for_timeout(200)


@then('the "{pad_id}" pad is back to its own height')
def step_pad_back(context, pad_id):
    h = _pad_heights(context, pad_id)
    assert abs(h["pad"] - context.pad_h0["pad"]) <= 2, "%r → %r" % (context.pad_h0, h)


@when('I put the caret in "{word}" of \'{context_text}\' in the "{pad_id}" pad')
def step_caret_in(context, word, context_text, pad_id):
    ta = _ta(context, pad_id)
    ta.wait_for(state="attached", timeout=20_000)
    ok = context.page.evaluate("""([id, ctx, word]) => {
      const t = document.querySelector("[data-lc-id='" + id + "'] .lc-mdpad-in");
      const i = t.value.indexOf(ctx); if (i < 0) return false;
      const at = i + ctx.indexOf(word) + 1;
      t.focus(); t.setSelectionRange(at, at);
      t.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
      return true;
    }""", [pad_id, context_text, word])
    assert ok, "%r is not in the pad" % context_text
    context.page.wait_for_timeout(700)


@then('the "{pad_id}" pad lights {n:d} wires of "{word}"')
def step_wires(context, pad_id, n, word):
    got = context.page.eval_on_selector_all(
        "[data-lc-id='%s'] .lc-mdpad-piano .md-wire" % pad_id, "ws => ws.map(w => w.textContent)")
    assert got == [word] * n, "lit %r, expected %d × %r" % (got, n, word)


@then('the "{pad_id}" pad lights no wire')
def step_no_wire(context, pad_id):
    got = context.page.eval_on_selector_all(
        "[data-lc-id='%s'] .lc-mdpad-piano .md-wire" % pad_id, "ws => ws.map(w => w.textContent)")
    assert not got, "lit %r for a word that is only prose" % got


def _out_w(context, pad_id):
    return context.page.evaluate(
        "(id) => Math.round(document.querySelector(\"[data-lc-id='\" + id + \"'] .lc-mdpad-out\").getBoundingClientRect().width)", pad_id)


@when('I drag the "{pad_id}" pad\'s splitter {dx:d}px to the right')
def step_drag_split(context, pad_id, dx):
    context.out_w0 = _out_w(context, pad_id)
    sp = context.page.locator("[data-lc-id='%s'] .lc-mdpad-split" % pad_id)
    sp.scroll_into_view_if_needed()
    box = sp.bounding_box()
    assert box, "no splitter between preview and editor"
    x, y = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
    m = context.page.mouse
    m.move(x, y); m.down(); m.move(x + dx / 2, y); m.move(x + dx, y); m.up()
    context.page.wait_for_timeout(200)


@then('the "{pad_id}" pad\'s preview grew by about {dx:d}px')
def step_out_grew(context, pad_id, dx):
    w = _out_w(context, pad_id)
    assert abs(w - context.out_w0 - dx) <= 12, "preview %d → %d, expected +%d" % (context.out_w0, w, dx)


@when('I double-click the "{pad_id}" pad\'s splitter')
def step_dbl_split(context, pad_id):
    context.page.locator("[data-lc-id='%s'] .lc-mdpad-split" % pad_id).dblclick()
    context.page.wait_for_timeout(200)


@then('the "{pad_id}" pad\'s preview is back to its own width')
def step_out_back(context, pad_id):
    w = _out_w(context, pad_id)
    assert abs(w - context.out_w0) <= 2, "preview %d, was %d" % (w, context.out_w0)


@when('I rest the pointer on the gutter of line {n:d} in the "{pad_id}" pad')
def step_rest_gutter(context, n, pad_id):
    sel = "[data-lc-id='%s'] .lc-mdpad-piano .ln[data-n='%d']" % (pad_id, n)
    context.page.wait_for_selector(sel + "[data-ic]", state="attached", timeout=20_000)
    ta = _ta(context, pad_id)
    ta.scroll_into_view_if_needed()
    ln = context.page.locator(sel).bounding_box()
    tb = ta.bounding_box()
    context.page.mouse.move(tb["x"] + 8, ln["y"] + ln["height"] / 2)
    context.page.mouse.move(tb["x"] + 10, ln["y"] + ln["height"] / 2)


@then('after a second the "{pad_id}" pad\'s gutter says "{text}"')
def step_tip(context, pad_id, text):
    tip = context.page.locator("[data-lc-id='%s'] .lc-mdpad-tip" % pad_id)
    context.page.wait_for_timeout(500)
    assert tip.is_hidden(), "the label showed before the second was up"
    expect(tip).to_have_text(text, timeout=2_000)


@then('the "{pad_id}" pad\'s current block holds "{a}" and "{b}"')
def step_now_block(context, pad_id, a, b):
    txt = context.page.eval_on_selector(
        "[data-lc-id='%s'] .lc-mdpad-piano .now" % pad_id, "e => e.textContent")
    assert a in txt and b in txt, "the lit block reads %r" % txt


@then('the "{pad_id}" pad shows no splitter')
def step_pad_no_splitter(context, pad_id):
    """Michel, 2026-10-11: the handle stayed over the preview once the
    editor was hidden — its own display beat [hidden]."""
    expect(context.page.locator("[data-lc-id='" + pad_id + "'] .lc-mdpad-split")).to_be_hidden(timeout=3_000)


@then('the "{pad_id}" pad\'s splitter is back')
def step_pad_splitter_back(context, pad_id):
    expect(context.page.locator("[data-lc-id='" + pad_id + "'] .lc-mdpad-split")).to_be_visible(timeout=3_000)


def _pad(context, pad_id):
    return context.page.locator("[data-lc-id='" + pad_id + "']")


@when('I press ⌘F in the "{pad_id}" pad and look for "{q}"')
def step_find_open(context, pad_id, q):
    ta = _pad(context, pad_id).locator(".lc-mdpad-in")
    ta.click()
    ta.press("Control+f")
    box = _pad(context, pad_id).locator(".lc-mdpad-find input")
    expect(box).to_be_focused(timeout=3_000)
    box.fill(q)
    context.page.wait_for_timeout(300)


def _find_count(context, pad_id):
    t = _pad(context, pad_id).locator(".lc-mdpad-find .n").inner_text().strip()
    at, n = t.split("/")
    return int(at), int(n)


@then('the "{pad_id}" pad\'s finder counts more than {k:d} match')
def step_find_count(context, pad_id, k):
    at, n = _find_count(context, pad_id)
    assert n > k, "finder counts %d" % n


@then('the "{pad_id}" pad\'s mirror lights the current match')
def step_find_lit(context, pad_id):
    expect(_pad(context, pad_id).locator(".lc-mdpad-piano .md-find-at")).to_have_count(1, timeout=3_000)


@when('I press {key} in the "{pad_id}" pad\'s finder')
def step_find_key(context, key, pad_id):
    k = {"↓": "ArrowDown", "↑": "ArrowUp", "Escape": "Escape"}[key]
    _pad(context, pad_id).locator(".lc-mdpad-find input").press(k)
    context.page.wait_for_timeout(200)


@then('the "{pad_id}" pad\'s finder is on match {k:d}')
def step_find_on(context, pad_id, k):
    at, n = _find_count(context, pad_id)
    assert at == k, "finder on %d/%d" % (at, n)


@then('the "{pad_id}" pad\'s finder is gone')
def step_find_gone(context, pad_id):
    expect(_pad(context, pad_id).locator(".lc-mdpad-find")).to_have_count(0)


@then('the "{pad_id}" pad\'s selection reads "{text}"')
def step_find_sel(context, pad_id, text):
    got = _pad(context, pad_id).locator(".lc-mdpad-in").evaluate(
        "t => t.value.slice(t.selectionStart, t.selectionEnd)")
    assert got.lower() == text.lower(), "selection %r" % got


def _val(context, pad_id):
    return _pad(context, pad_id).locator(".lc-mdpad-in").evaluate("t => t.value")


@when('I ⌘-click the caret in the "{pad_id}" pad')
def step_cmd_click(context, pad_id):
    _pad(context, pad_id).locator(".lc-mdpad-in").evaluate(
        "t => t.dispatchEvent(new MouseEvent('click', {bubbles: true, ctrlKey: true, metaKey: true}))")
    context.page.wait_for_timeout(300)


@then('the "{pad_id}" pad selects "{text}" on the line "{line}"')
@then('the "{pad_id}" pad selects "{text}" on the line \'{line}\'')
def step_sel_on_line(context, pad_id, text, line):
    got = _pad(context, pad_id).locator(".lc-mdpad-in").evaluate("""t => {
      const v = t.value, a = t.selectionStart, b = t.selectionEnd;
      const ls = v.lastIndexOf("\\n", a - 1) + 1, le = v.indexOf("\\n", a);
      return [v.slice(a, b), v.slice(ls, le < 0 ? v.length : le)];
    }""")
    assert got[0] == text and got[1].strip() == line, "selection %r on line %r" % tuple(got)


def _f2(context, pad_id, to, enter=True):
    ta = _pad(context, pad_id).locator(".lc-mdpad-in")
    ta.press("F2")
    inp = _pad(context, pad_id).locator(".lc-mdpad-rename input")
    expect(inp).to_be_focused(timeout=3_000)
    inp.fill(to)
    if enter:
        inp.press("Enter")
    context.page.wait_for_timeout(300)


@when('I rename it to "{to}" with F2 in the "{pad_id}" pad')
def step_f2(context, to, pad_id):
    _f2(context, pad_id, to)


@when('I try F2 to "{to}" in the "{pad_id}" pad')
def step_f2_try(context, to, pad_id):
    _f2(context, pad_id, to, enter=False)


@then('the "{pad_id}" pad\'s rename box says "{text}"')
def step_f2_says(context, pad_id, text):
    expect(_pad(context, pad_id).locator(".lc-mdpad-rename .n")).to_have_text(text)
    expect(_pad(context, pad_id).locator(".lc-mdpad-rename [data-ok]")).to_be_disabled()


@then('the "{pad_id}" pad holds "{a}", \'{b}\', "{c}" and \'{d}\'')
def step_holds4(context, pad_id, a, b, c, d):
    v = _val(context, pad_id)
    for t in (a, b, c, d):
        assert t in v, "%r not in the pad" % t


@then('the "{pad_id}" pad holds {q}')
def step_holds(context, pad_id, q):
    t = q[1:-1] if q[:1] in "\"'" and q[-1:] == q[:1] else q
    v = _val(context, pad_id)
    assert t in v, "%r not in the pad:\n%s" % (t, v)


@when('I press "{keys}" in the "{pad_id}" pad')
def step_press(context, keys, pad_id):
    _pad(context, pad_id).locator(".lc-mdpad-in").press(keys)
    context.page.wait_for_timeout(300)


@then('in the "{pad_id}" pad "{a}" comes before "{b}"')
def step_before(context, pad_id, a, b):
    v = _val(context, pad_id)
    assert a in v and b in v and v.index(a) < v.index(b), "order wrong:\n" + v


@then('the "{pad_id}" pad\'s caret is still in "{t}"')
def step_caret_in_t(context, pad_id, t):
    ok = context.page.evaluate("""([id, t]) => {
      const ta = document.querySelector("[data-lc-id='" + id + "'] .lc-mdpad-in");
      const i = ta.value.indexOf(t); return ta.selectionStart >= i && ta.selectionStart <= i + t.length;
    }""", [pad_id, t])
    assert ok, "the caret left " + t


@then('the "{pad_id}" pad shows no 🔍 pill')
def step_no_find_pill(context, pad_id):
    expect(_pad(context, pad_id).locator(".lc-mdpad-findbtn")).to_be_hidden()


@when('I put the caret at the start of the "{pad_id}" pad')
def step_caret_start(context, pad_id):
    ta = _pad(context, pad_id).locator(".lc-mdpad-in")
    ta.focus()
    ta.evaluate("t => t.setSelectionRange(0, 0)")


@then('the "{pad_id}" pad shows its 🔍 pill')
def step_find_pill(context, pad_id):
    expect(_pad(context, pad_id).locator(".lc-mdpad-findbtn")).to_be_visible()


@when('I type "{text}" on a new line at the end of the "{pad_id}" pad')
def step_type_newline(context, text, pad_id):
    ta = _pad(context, pad_id).locator(".lc-mdpad-in")
    ta.click()
    ta.press("Control+End")
    ta.press("Enter")
    ta.press("Enter")
    ta.type(text, delay=40)
    context.page.wait_for_timeout(500)


@when('I type "{text}" in the "{pad_id}" pad')
def step_type_here(context, text, pad_id):
    _pad(context, pad_id).locator(".lc-mdpad-in").type(text, delay=40)
    context.page.wait_for_timeout(500)


def _offers(context, pad_id):
    loc = _pad(context, pad_id).locator(".lc-mdpad-comp .l")
    expect(loc.first).to_be_visible(timeout=3_000)
    return loc.all_inner_texts()


@then('the "{pad_id}" pad offers "{first}" first')
def step_offers_first(context, pad_id, first):
    got = _offers(context, pad_id)
    assert got and got[0] == first, "offers %r" % got


@then('the "{pad_id}" pad offers "{a}" and "{b}"')
def step_offers_two(context, pad_id, a, b):
    got = _offers(context, pad_id)
    assert a in got and b in got, "offers %r" % got


@when('I accept the offer in the "{pad_id}" pad')
def step_accept(context, pad_id):
    _pad(context, pad_id).locator(".lc-mdpad-in").press("Enter")
    context.page.wait_for_timeout(500)


@then('the "{pad_id}" pad selects "{text}"')
def step_selects(context, pad_id, text):
    got = _pad(context, pad_id).locator(".lc-mdpad-in").evaluate("t => t.value.slice(t.selectionStart, t.selectionEnd)")
    assert got == text, "selection %r" % got


@then('the "{pad_id}" pad\'s preview marks "{text}"')
def step_ghost(context, pad_id, text):
    expect(_pad(context, pad_id).locator(".lc-mdpad-ghost span")).to_have_text(text, timeout=5_000)


@then('the "{pad_id}" pad shows no ? pill, even hovered')
def step_no_help_pill(context, pad_id):
    _pad(context, pad_id).hover()
    expect(_pad(context, pad_id).locator(".lc-mdpad-helpbtn")).to_be_hidden()


@when('I press the "{pad_id}" pad\'s ? pill')
def step_help_pill(context, pad_id):
    _pad(context, pad_id).hover()
    _pad(context, pad_id).locator(".lc-mdpad-helpbtn").click()


@then('the "{pad_id}" pad\'s help mentions "{a}" and "{b}"')
def step_help_mentions(context, pad_id, a, b):
    card = _pad(context, pad_id).locator(".lc-mdpad-help")
    expect(card).to_contain_text(a)
    expect(card).to_contain_text(b)


@when('I put the caret at the start of the line holding "{text}" in the "{pad_id}" pad')
def step_caret_line(context, text, pad_id):
    ok = _pad(context, pad_id).locator(".lc-mdpad-in").evaluate("""(t, x) => {
      const i = t.value.indexOf(x); if (i < 0) return false;
      const ls = t.value.lastIndexOf("\\n", i - 1) + 1; t.focus(); t.setSelectionRange(ls, ls); return true; }""", text)
    assert ok, "%r is not in the pad" % text


@then('the "{pad_id}" pad\'s editor has let the focus go')
def step_focus_left(context, pad_id):
    still = _pad(context, pad_id).locator(".lc-mdpad-in").evaluate("t => document.activeElement === t")
    assert not still, "the editor kept the focus"


@when('I fold the "{pad_id}" pad')
def step_fold_pad(context, pad_id):
    ok = context.page.evaluate(
        "id => window.lcVerbs.act('fold', document.querySelector(\"[data-lc-id='\" + id + \"']\"))", pad_id)
    assert ok, "the fold verb did not answer"
    expect(context.page.locator("[data-lc-id='" + pad_id + "']")).to_have_attribute("data-lc-folded", "1")


@then('the "{pad_id}" pad\'s editor is open')
def step_pad_open(context, pad_id):
    pad = context.page.locator("[data-lc-id='" + pad_id + "']")
    expect(pad).not_to_have_attribute("data-lc-folded", "1", timeout=5_000)
    expect(pad.locator(".lc-mdpad-src")).to_be_visible()


_WATCH = """(id) => { const w = document.querySelector(`[data-lc-id='${id}']`);
  const src = w.querySelector('.lc-mdpad-src'), out = w.querySelector('.lc-mdpad-out'), ta = w.querySelector('.lc-mdpad-in');
  const box = (e) => { const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.right)]; };
  window._lcSlide = [];
  const look = () => { if (src.offsetParent || src.getClientRects().length)
      window._lcSlide.push({src: box(src), ta: box(ta), out: box(out)}); };
  look(); const t = setInterval(look, 30); setTimeout(() => clearInterval(t), 700);
  w.querySelector('.lc-mdpad-fold').click(); }"""


def _slide(context, pad_id):
    context.page.evaluate(_WATCH, pad_id)
    context.page.wait_for_timeout(800)
    return context.page.evaluate("() => window._lcSlide")


@when('I fold the "{pad_id}" pad, watching it slide')
def step_fold_watch(context, pad_id):
    context.slide = _slide(context, pad_id)


@when('I unfold the "{pad_id}" pad, watching it slide')
def step_unfold_watch(context, pad_id):
    context.slide = _slide(context, pad_id)


def _still_and_swept(frames, forward):
    assert len(frames) >= 5, "too few frames of the slide: %s" % frames
    src0 = frames[0]["src"] if forward else frames[-1]["src"]
    for f in frames:
        assert abs(f["src"][1] - src0[1]) <= 1, "the editor's right edge moved: %s" % frames
        assert abs(f["ta"][0] - src0[0]) <= 1 or abs(f["src"][0] - src0[0]) <= 1, "the editor's text moved: %s" % frames
    rights = [f["out"][1] for f in frames]
    mid = [r for r in rights if src0[0] + 5 < r < src0[1] - 5]
    assert mid, "the preview never stood over the editor mid-slide: %s" % rights
    pairs = list(zip(rights, rights[1:]))
    assert all((b >= a - 1) if forward else (b <= a + 1) for a, b in pairs), "the preview's edge went back and forth: %s" % rights


@then("the editor stood still while the preview's right edge swept over it, left to right")
def step_swept_over(context):
    _still_and_swept(context.slide, True)


@then("the editor stood still while the preview's right edge swept back, right to left")
def step_swept_back(context):
    _still_and_swept(context.slide, False)


@when('I click at the start of "{line}" in the "{pad_id}" pad and press Tab')
def step_click_line_tab(context, line, pad_id):
    p = context.page
    sel = "[data-lc-id='" + pad_id + "'] .lc-mdpad-in"
    p.evaluate("([s, l]) => { const ta = document.querySelector(s); const a = ta.value.indexOf(l); ta.focus(); ta.setSelectionRange(a, a); ta.dispatchEvent(new MouseEvent('click', { bubbles: true })); }", [sel, line])
    p.keyboard.press("Tab")
    p.wait_for_timeout(300)


@then('the "{pad_id}" pad indented "{line}" by four spaces, nothing selected')
def step_pad_indented(context, pad_id, line):
    p = context.page
    sel = "[data-lc-id='" + pad_id + "'] .lc-mdpad-in"
    v = p.evaluate("s => document.querySelector(s).value", sel)
    assert ("\n    " + line) in v, repr(v)
    picked = p.evaluate("s => { const t = document.querySelector(s); return t.value.slice(t.selectionStart, t.selectionEnd); }", sel)
    assert picked == "", "Tab jumped to " + repr(picked)


@then('completion in the "{pad_id}" pad after "{text}" offers "{names}"')
def step_pad_completion_offers(context, pad_id, text, names):
    # the same door the distributed suite opens, on one page: the caret after
    # the text, Ctrl+Space, the labels of the list in order
    sel = "[data-lc-id='" + pad_id + "'] .lc-mdpad-in"
    ok = context.page.evaluate("""([s, t, pid]) => {
      const ta = document.querySelector(s); const i = ta.value.lastIndexOf(t);
      if (i < 0) return 'no such text';
      ta.focus(); ta.setSelectionRange(i + t.length, i + t.length);
      const w = document.querySelector("[data-lc-id='" + pid + "']");
      if (!w._lcComplete) return 'no completion'; w._lcComplete(); return 'ok';
    }""", [sel, text, pad_id])
    assert ok == "ok", ok
    loc = context.page.locator("[data-lc-id='" + pad_id + "'] .lc-mdpad-comp .l")
    expect(loc.first).to_be_visible(timeout=5_000)
    labels = sorted(loc.all_inner_texts())
    want = sorted(n.strip() for n in names.split(","))
    assert labels == want, "offered %s, wanted %s" % (labels, want)
    context.page.keyboard.press("Escape")


@then('completion in the "{pad_id}" pad after "{text}" includes "{names}"')
def step_pad_completion_includes(context, pad_id, text, names):
    sel = "[data-lc-id='" + pad_id + "'] .lc-mdpad-in"
    ok = context.page.evaluate("""([s, t, pid]) => {
      const ta = document.querySelector(s); const i = ta.value.lastIndexOf(t);
      if (i < 0) return 'no such text';
      ta.focus(); ta.setSelectionRange(i + t.length, i + t.length);
      const w = document.querySelector("[data-lc-id='" + pid + "']");
      if (!w._lcComplete) return 'no completion'; w._lcComplete(); return 'ok';
    }""", [sel, text, pad_id])
    assert ok == "ok", ok
    loc = context.page.locator("[data-lc-id='" + pad_id + "'] .lc-mdpad-comp .l")
    expect(loc.first).to_be_visible(timeout=5_000)
    labels = loc.all_inner_texts()
    missing = [n.strip() for n in names.split(",") if n.strip() not in labels]
    assert not missing, "missing %s in %s" % (missing, labels)
    context.page.keyboard.press("Escape")
