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
    expect(grid(context, gid).locator(".lc-dg-menu")).to_be_visible(timeout=T)


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
    cell.click()
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
