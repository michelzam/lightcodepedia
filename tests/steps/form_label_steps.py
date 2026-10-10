"""A form's label column: fitted to its labels, moved by its grip."""
from behave import when, then


def _form(context, fid):
    sel = "[data-lc-id='%s']" % fid
    context.page.wait_for_selector(sel + " .lc-form-label-cell")
    return sel


def _label_width(context, sel):
    return context.page.eval_on_selector(
        sel + " .lc-form-label-cell", "c => c.getBoundingClientRect().width")


@when('I click row {n:d} of the "{gid}" grid')
def step_click_row(context, n, gid):
    rows = "[data-lc-id='%s'] .ag-center-cols-container .ag-row, [data-lc-id='%s'] tbody tr" % (gid, gid)
    context.page.wait_for_selector(rows)
    context.page.locator(rows).nth(n - 1).click()
    context.page.wait_for_timeout(300)


@then('the "{fid}" form\'s labels are whole')
def step_labels_whole(context, fid):
    sel = _form(context, fid)
    cut = context.page.eval_on_selector_all(
        sel + " .lc-form-label-cell",
        "cs => cs.filter(c => c.scrollWidth > c.clientWidth + 1).map(c => c.textContent.trim())")
    assert not cut, "labels cut off: %s" % cut


@then('the "{fid}" form gives its values at least half its width')
def step_values_half(context, fid):
    sel = _form(context, fid)
    label = _label_width(context, sel)
    whole = context.page.eval_on_selector(sel + " .lc-form-grid", "g => g.clientWidth")
    assert label <= whole / 2 + 1, "labels take %dpx of %dpx" % (label, whole)


@when('I drag the "{fid}" form\'s label line {dx:d}px to the right')
def step_drag(context, fid, dx):
    sel = _form(context, fid)
    context.label_before = _label_width(context, sel)
    box = context.page.locator(sel + " .lc-form-grip").bounding_box()
    assert box, "no grip on the line between labels and values"
    x, y = box["x"] + box["width"] / 2, box["y"] + 20
    m = context.page.mouse
    m.move(x, y)
    m.down()
    m.move(x + dx / 2, y)
    m.move(x + dx, y)
    m.up()
    context.page.wait_for_timeout(200)


@then('the "{fid}" form\'s label column grew by {dx:d}px')
def step_grew(context, fid, dx):
    sel = _form(context, fid)
    now = _label_width(context, sel)
    context.label_dragged = now
    assert abs(now - context.label_before - dx) <= 3, \
        "label column %d → %d, expected +%d" % (context.label_before, now, dx)


@then('the "{fid}" form shows "{text}"')
def step_shows(context, fid, text):
    sel = _form(context, fid)
    context.page.wait_for_function(
        "([s, t]) => (document.querySelector(s) || {}).textContent.includes(t)", arg=[sel, text])


@then('the "{fid}" form\'s label column kept its width')
def step_kept(context, fid):
    sel = _form(context, fid)
    now = _label_width(context, sel)
    assert abs(now - context.label_dragged) <= 1, \
        "the line went back: %d after the drag, %d on the next row" % (context.label_dragged, now)
