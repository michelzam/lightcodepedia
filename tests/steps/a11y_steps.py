"""What we paint ourselves must read: WCAG 1.4.3 contrast, computed live.

The axe scan runs privately on the live site and names its nodes; this is
the rig-side twin for the colours WE choose — the ones a fix can change and
a later edit can quietly undo. Effective background is the nearest painted
ancestor; opacity along the way is blended in, since fading text is the
usual way contrast is lost without touching a colour.
"""
import re

from behave import given, then, when
from playwright.sync_api import expect

_CONTRAST = """(sel) => {
  const lum = c => { const [r, g, b] = c.map(v => { v /= 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
  const parse = s => { const m = (s || '').match(/rgba?\\(([^)]+)\\)/); if (!m) return null;
    const p = m[1].split(',').map(parseFloat); return { c: [p[0], p[1], p[2]], a: p.length > 3 ? p[3] : 1 }; };
  const bgOf = el => { let n = el.parentElement;
    while (n) { const bg = parse(getComputedStyle(n).backgroundColor); if (bg && bg.a > 0) return bg.c; n = n.parentElement; }
    return [255, 255, 255]; };
  const opOf = el => { let o = 1, n = el;
    while (n && n !== document.documentElement) { o *= parseFloat(getComputedStyle(n).opacity || 1); n = n.parentElement; } return o; };
  const out = { seen: 0, bad: [] };
  document.querySelectorAll(sel).forEach(el => {
    if (!(el.textContent || '').trim()) return;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') return;
    const fg = parse(cs.color); if (!fg) return;
    out.seen++;
    const own = parse(cs.backgroundColor);
    const bg = (own && own.a > 0) ? own.c : bgOf(el);
    const op = opOf(el) * fg.a;
    const mix = fg.c.map((v, i) => v * op + bg[i] * (1 - op));
    const l1 = lum(mix), l2 = lum(bg);
    const r = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
    const px = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight, 10) >= 700;
    const large = px >= 24 || (bold && px >= 18.66);
    if (r < (large ? 3 : 4.5)) out.bad.push('"' + el.textContent.trim().slice(0, 40) + '" ' + r.toFixed(2) + ':1');
  });
  return out;
}"""


@then('the text in "{selector}" reads at AA contrast')
def step_aa_contrast(context, selector):
    context.page.wait_for_selector(selector, state="attached", timeout=15_000)
    got = context.page.evaluate(_CONTRAST, selector)
    assert got["seen"] > 0, "nothing with text matched %r — the check proved nothing" % selector
    assert not got["bad"], "under AA contrast in %r:\n  %s" % (selector, "\n  ".join(got["bad"]))


@then("every field hidden for the password manager still carries a name")
def step_hidden_named(context):
    bad = context.page.evaluate(
        """() => Array.from(document.querySelectorAll('input[name="username"][tabindex="-1"]'))
                 .filter(i => !(i.getAttribute('aria-label') || '').trim() && !i.labels?.length)
                 .map(i => i.outerHTML.slice(0, 120))""")
    assert not bad, "nameless hidden fields:\n" + "\n".join(bad)


@then("no footnote carries a retired role")
def step_footnote_roles(context):
    context.page.wait_for_selector("div.footnotes li", state="attached", timeout=10_000)
    context.page.wait_for_timeout(300)
    n = context.page.evaluate("() => document.querySelectorAll('li[role=\"doc-endnote\"]').length")
    assert n == 0, "%d footnotes still stamped doc-endnote" % n


@given("the GitHub API answers 404 for anything else")
def step_gh_404(context):
    """Registered first, asked last: whatever no later stub serves is a
    clean 'not found' — the road a learner meets on a page the vault never
    received."""
    context.page.route("**/api.github.com/**",
                       lambda r: r.fulfill(status=404, json={"message": "Not Found"}))



@then("every map marker carries a role and a name of its own")
def step_markers_named(context):
    context.page.wait_for_selector(".maplibregl-marker", state="attached", timeout=20_000)
    context.page.wait_for_timeout(500)
    got = context.page.evaluate(
        """() => Array.from(document.querySelectorAll('.maplibregl-marker')).map(m => ({
              role: m.getAttribute('role') || '', name: m.getAttribute('aria-label') || '' }))""")
    assert got, "no markers rendered"
    bad = [g for g in got if not g["role"] or not g["name"] or g["name"] == "Map marker"]
    assert not bad, "markers with no role or a library name: %r" % bad


@then("every grid scroll region is a tab stop")
def step_grid_scroll_focusable(context):
    context.page.wait_for_selector(".ag-body-viewport", state="attached", timeout=20_000)
    context.page.wait_for_function(
        "() => Array.from(document.querySelectorAll('.ag-body-viewport'))"
        "        .every(v => v.querySelector('[tabindex=\"0\"]'))", timeout=10_000)


@then("no quiz answer contains a focusable descendant")
def step_answers_single_control(context):
    context.page.wait_for_selector("li[role=radio], li[role=checkbox]", state="attached", timeout=10_000)
    bad = context.page.evaluate(
        """() => Array.from(document.querySelectorAll('li[role=radio], li[role=checkbox]'))
                 .filter(li => li.querySelector('a[href], button, input, select, textarea, [tabindex]'))
                 .map(li => li.textContent.trim().slice(0, 40))""")
    assert not bad, "answers holding a second control: %r" % bad


@then("the footnote mark inside an answer still opens its popover")
def step_answer_footnote_popover(context):
    mark = context.page.locator("li[role=radio] .lc-fn-ref, li[role=checkbox] .lc-fn-ref").first
    mark.click()
    popover = context.page.locator(".lc-fn-popover.lc-fn-visible")
    expect(popover).to_be_visible(timeout=5_000)
    assert popover.text_content().strip(), "the popover opened empty"



# ── the editor's ♿ Audit tab ──────────────────────────────────────────────

@when("a nameless text field is planted on the page")
def step_plant_nameless(context):
    context.page.evaluate(
        """() => { const i = document.createElement('input'); i.type = 'text'; i.id = 'lc-planted';
                   document.querySelector('main, article, body').appendChild(i); }""")


@when("the planted field is removed")
def step_unplant(context):
    context.page.evaluate("() => { const i = document.getElementById('lc-planted'); if (i) i.remove(); }")


@when("I press the editor's audit button")
def step_press_audit(context):
    context.page.click("#ed-a11y-run")


@then('the audit lists a "{rule}" finding')
def step_audit_lists(context, rule):
    row = context.page.locator(".ed-a11y-row[data-rule='" + rule + "']").first
    expect(row).to_be_visible(timeout=20_000)


@then("clicking that finding outlines the planted field")
def step_audit_click(context):
    context.page.locator(".ed-a11y-row[data-rule='label']").first.click()
    expect(context.page.locator("#lc-planted")).to_have_class(re.compile(r"ed-a11y-outline"), timeout=5_000)


@then("the audit reports no issues")
def step_audit_clean(context):
    ok = context.page.locator("#ed-a11y-list .ed-a11y-ok")
    try:
        expect(ok).to_be_visible(timeout=20_000)
    except AssertionError:
        raise AssertionError("the audit still lists: " + context.page.locator("#ed-a11y-list").inner_text()[:600])


@when("I unfold the rules that passed")
def step_unfold_passes(context):
    context.page.click("#ed-a11y-show-passes")


@then("the audit lists the rules that passed, each with its level and the elements it checked")
def step_passes_listed(context):
    """What already works is worth showing (Michel, 2026-09-15)."""
    box = context.page.locator("#ed-a11y-passes")
    expect(box).to_be_visible(timeout=5_000)
    rows = box.locator(".ed-a11y-pass")
    assert rows.count() >= 20, "too few rules listed as passed: %d" % rows.count()
    first = rows.first
    assert first.locator("b.ok").text_content() in ("A", "AA")
    assert "checked" in first.locator("span").text_content()
    assert first.locator("a").get_attribute("href", timeout=2_000).startswith("http")
