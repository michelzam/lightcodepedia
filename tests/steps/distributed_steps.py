import re
from behave import given, when, then
from playwright.sync_api import expect

T = 30_000


def _tab(context, n):
    tabs = getattr(context, "tabs", None)
    if tabs is None:
        tabs = context.tabs = {1: context.page}
    return tabs[n]


def _grid(page, gid):
    return page.locator(".lc-datagrid[data-lc-id='" + gid + "']")


def _row(page, gid, name):
    return _grid(page, gid).locator("tbody tr", has_text=name).first


def _col(page, gid, col):
    heads = [re.sub(r"\s*[↑↓]$", "", t.strip()).lower() for t in _grid(page, gid).locator("thead th").all_inner_texts()]
    return heads.index(col)


@when('I open "{path}" in tab {n:d}')
def step_open_tab(context, path, n):
    first = _tab(context, 1)
    # a popup of tab 1: the same browser context, so the browser's channel is shared
    with first.expect_popup() as pop:
        first.evaluate("() => window.open('about:blank', '_blank')")
    page = pop.value
    if getattr(context, "stub_page", None):
        context.stub_page(page)                    # the rig's CDN stubs
    for pat, handler in getattr(context, "stub_routes", []):
        page.route(pat, handler)                   # the documents the Background served
    context.tabs[n] = page
    page.goto(context.base_url + path)
    page.wait_for_load_state("load")


@then('in tab {n:d} the grid "{gid}" shows "{name}" with count "{count}", and ⋯ offers "{verb}"')
def step_tab_row_verb(context, n, gid, name, count, verb):
    step_tab_row(context, n, gid, name, count)
    page = _tab(context, n)
    _row(page, gid, name).locator("td.lc-dg-gut button").click()
    menu = page.locator(".lc-dg-menu")
    expect(menu.locator("button[data-verb='" + verb + "']")).to_be_visible(timeout=T)
    page.keyboard.press("Escape")
    page.mouse.click(5, 5)


@then('in tab {n:d} the grid "{gid}" shows "{name}" with count "{count}"')
def step_tab_row(context, n, gid, name, count):
    page = _tab(context, n)
    r = _row(page, gid, name)
    expect(r).to_be_visible(timeout=T)
    expect(r.locator("td").nth(_col(page, gid, "count"))).to_have_text(count, timeout=T)


@when('in tab {n:d} I press "{verb}" in the gutter of "{name}" in "{gid}"')
def step_tab_verb(context, n, verb, name, gid):
    page = _tab(context, n)
    _row(page, gid, name).locator("td.lc-dg-gut button").click()
    page.locator(".lc-dg-menu button[data-verb='" + verb + "']").click()


@then('in tab {n:d} the grid "{gid}" lists "{a}" and "{b}"')
def step_tab_lists(context, n, gid, a, b):
    g = _grid(_tab(context, n), gid)
    expect(g.locator("tbody tr", has_text=a).first).to_be_visible(timeout=T)
    expect(g.locator("tbody tr", has_text=b).first).to_be_visible(timeout=T)


@when('in tab {n:d} I press the button "{bid}"')
def step_tab_button(context, n, bid):
    _tab(context, n).locator("#" + bid + ", [data-lc-id='" + bid + "']").first.click()


@then('in tab {n:d} the grid "{gid}" shows "{text}"')
def step_tab_grid_text(context, n, gid, text):
    expect(_grid(_tab(context, n), gid)).to_contain_text(text, timeout=T)


@when("I close tab {n:d}")
def step_close_tab(context, n):
    # tab 1 owns the browser context (the harness opens it with browser.new_page):
    # closing it would close the popups too. Leaving the page closes the channel just the same.
    _tab(context, n).goto("about:blank")


@then('in tab {n:d} the grid "{gid}" says "{text}"')
def step_tab_grid_says(context, n, gid, text):
    expect(_grid(_tab(context, n), gid).locator(".lc-dg-say")).to_contain_text(text, timeout=15_000)





@when('in tab {n:d} I retype the model block of the "{pad_id}" pad three times')
def step_retype_model(context, n, pad_id):
    page = _tab(context, n)
    sel = "[data-lc-id='" + pad_id + "'] .lc-mdpad-in"
    expect(page.locator(sel)).to_be_attached(timeout=T)
    for k in range(3):
        base = page.evaluate("s => document.querySelector(s).value", sel)
        anchor = "        self.count += 1\n"
        assert anchor in base, base[:400]
        page.evaluate("""([s, v]) => { const ta = document.querySelector(s); ta.value = v;
          ta.dispatchEvent(new Event('input', { bubbles: true })); }""",
          [sel, base.replace(anchor, anchor + "    # again " + str(k) + "\n", 1)])
        page.wait_for_timeout(2500)
    page.wait_for_timeout(1500)


@then('after {secs:d} seconds, in tab {n:d} the grid "{gid}" lists one "{a}" and one "{b}"')
def step_traffic_once(context, secs, n, gid, a, b):
    page = _tab(context, n)
    page.wait_for_timeout(secs * 1000)
    rows = _grid(page, gid).locator("tbody tr").all_inner_texts()
    fa = [r for r in rows if a in r]
    fb = [r for r in rows if b in r]
    assert len(fa) == 1, "follow listed %d times: %s" % (len(fa), rows)
    assert len(fb) == 1, "bump listed %d times: %s" % (len(fb), rows)


@then('in tab {n:d} the grid "{gid}" wears ↻ in its corner')
def step_tab_refresh_corner(context, n, gid):
    expect(_grid(_tab(context, n), gid).locator(".lc-dg-corner .lc-dg-roreload")).to_be_attached(timeout=T)


@then('in tab {n:d} the server "{sid}" stands by')
def step_tab_standby(context, n, sid):
    expect(_tab(context, n).locator(".lc-server[data-lc-id='" + sid + "']")).to_have_attribute("data-lc-standby", "1", timeout=T)


@then('in tab {n:d} the grid "{gid}" has {k:d} row, with {r:d} or more requests')
def step_clients(context, n, gid, k, r):
    page = _tab(context, n)
    g = _grid(page, gid)
    expect(g.locator("tbody tr")).to_have_count(k, timeout=T)
    page.wait_for_timeout(500)
    got = int(g.locator("tbody tr").first.locator("td").nth(_col(page, gid, "requests")).inner_text().strip() or "0")
    assert got >= r, got


@then('in tab {n:d} the python "{code}" gives "{want}"')
def step_tab_python(context, n, code, want):
    page = _tab(context, n)
    page.evaluate("() => { window.__dbg = 'unset'; }")
    page.evaluate("c => window.lcPySend(c)", "import js\ntry:\n    js.window.__dbg = str(" + code + ")\nexcept Exception as e:\n    js.window.__dbg = 'ERR ' + repr(e)")
    for _ in range(20):
        got = page.evaluate("() => window.__dbg")
        if got == want:
            return
        page.wait_for_timeout(300)
    assert got == want, got


@when("I reload tab {n:d}")
def step_reload_tab(context, n):
    page = _tab(context, n)
    page.reload()
    page.wait_for_load_state("load")


@then('in tab {n:d} completion in the "{pad_id}" pad after "{text}" offers "{names}"')
def step_pad_completion(context, n, pad_id, text, names):
    page = _tab(context, n)
    sel = "[data-lc-id='" + pad_id + "'] .lc-mdpad-in"
    ok = page.evaluate("""([s, t, pid]) => {
      const ta = document.querySelector(s); const i = ta.value.lastIndexOf(t);
      if (i < 0) return 'no such text';
      ta.focus(); ta.setSelectionRange(i + t.length, i + t.length);
      const w = document.querySelector("[data-lc-id='" + pid + "']");
      if (!w._lcComplete) return 'no completion'; w._lcComplete(); return 'ok';
    }""", [sel, text, pad_id])
    assert ok == "ok", ok
    loc = page.locator("[data-lc-id='" + pad_id + "'] .lc-mdpad-comp .l")
    expect(loc.first).to_be_visible(timeout=5_000)
    labels = loc.all_inner_texts()
    want = [x.strip() for x in names.split(",")]
    for w in want:
        assert w in labels, "%s not offered: %s" % (w, labels)
