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
