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



# ── the keyboard: the pill, the shortcuts sheet, High contrast ────────────

@when("I focus the Modes pill")
def step_focus_pill(context):
    context.page.focus(".lc-slides-fab")


@then("the shortcuts sheet is open with focus on its close button")
def step_keys_open(context):
    expect(context.page.locator("#lc-keys")).to_be_visible(timeout=5_000)
    assert context.page.evaluate("() => document.activeElement && document.activeElement.id") == "lc-keys-close"


@then("the shortcuts sheet is closed and focus is back on the Modes pill")
def step_keys_closed(context):
    expect(context.page.locator("#lc-keys")).to_be_hidden(timeout=5_000)
    assert context.page.evaluate(
        "() => document.activeElement && document.activeElement.classList.contains('lc-slides-fab')"), "focus did not come home"


@then('the shortcuts sheet says High contrast is "{state}"')
def step_keys_contrast_state(context, state):
    expect(context.page.locator("#lc-keys-contrast")).to_have_text(state, timeout=5_000)


@then("the page is in High contrast")
def step_contrast_on(context):
    expect(context.page.locator("html")).to_have_attribute("data-theme", "contrast", timeout=5_000)


@then("the page is not in High contrast")
def step_contrast_off(context):
    context.page.wait_for_function("() => !document.documentElement.hasAttribute('data-theme')", timeout=5_000)


def _popup_items(context):
    return context.page.evaluate(
        """() => Array.from(document.querySelectorAll('#lc-bl-popup .lc-bl-popup-item'))
                 .filter(b => !b.hidden && b.offsetParent !== null).map(b => b.id)""")


@then("the modes popup is open with focus on its first item")
def step_popup_open_focused(context):
    expect(context.page.locator("#lc-bl-popup")).to_have_class(re.compile(r"\bopen\b"), timeout=5_000)
    items = _popup_items(context)
    assert context.page.evaluate("() => document.activeElement.id") == items[0], items


@then("focus is on the second item of the modes popup")
def step_popup_second(context):
    items = _popup_items(context)
    assert context.page.evaluate("() => document.activeElement.id") == items[1], items


@then("the modes popup is closed and focus is back on the Modes pill")
def step_popup_closed(context):
    expect(context.page.locator("#lc-bl-popup")).not_to_have_class(re.compile(r"\bopen\b"), timeout=5_000)
    assert context.page.evaluate(
        "() => document.activeElement && document.activeElement.classList.contains('lc-slides-fab')"), "focus did not come home"


@then("no visible text on the page is smaller than {px:d} pixels")
def step_no_tiny_text(context, px):
    """WAVE flags text at ten pixels and under as very small; under High
    contrast nothing we paint should be there."""
    bad = context.page.evaluate(
        """(min) => { const out = [];
          document.querySelectorAll('body *').forEach(el => {
            const cs = getComputedStyle(el);
            if (cs.display === 'none' || cs.visibility === 'hidden') return;
            const r = el.getBoundingClientRect(); if (!r.width || !r.height) return;
            if (!Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim())) return;
            if (el.closest('#ed-drawer, .lc-fn-popover, .ag-root-wrapper, #lc-keys')) return;
            const f = parseFloat(cs.fontSize);
            if (f < min) out.push(el.tagName.toLowerCase() + '.' + (el.className || '') + ' "' + el.textContent.trim().slice(0, 30) + '" ' + f.toFixed(1) + 'px');
          }); return out; }""", px)
    assert not bad, "text under %dpx:\n  %s" % (px, "\n  ".join(bad))


# ── the needs-review bucket: what axe could not decide ────────────────

@when("a paragraph over a picture is planted on the page")
def step_plant_over_picture(context):
    """a background image is the classic case axe cannot read a contrast
    through — it files the element as incomplete, never as a pass"""
    context.page.evaluate(
        """() => { const p = document.createElement('p'); p.id = 'lc-planted-bg'; p.textContent = 'text over a picture';
                   p.style.cssText = 'background-image:url(data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==);color:#777;padding:4px';
                   document.querySelector('main, article, body').appendChild(p); }""")


@then("the audit reports no confirmed issues, and elements for a human look")
def step_audit_review_count(context):
    """the tutorial's own ⓘ badges are already a human's call (one letter is
    too short for the engine to read a contrast); the planted paragraph joins them"""
    ok = context.page.locator("#ed-a11y-list .ed-a11y-ok")
    expect(ok).to_be_visible(timeout=20_000)
    expect(ok).to_contain_text("No confirmed issues")
    try:
        expect(ok.locator(".ed-a11y-review-n")).to_contain_text("need a human look", timeout=5_000)
    except AssertionError:
        raise AssertionError("the audit read: " + context.page.locator("#ed-a11y-list").inner_text()[:500])
    assert context.page.locator(".ed-a11y-row[data-kind='review']").count() >= 1


@then('the human-look rows are grouped by rule, "{rule}" among them')
def step_review_groups(context, rule):
    groups = context.page.locator("#ed-a11y-list details.ed-a11y-group")
    assert groups.count() >= 1, context.page.locator("#ed-a11y-list").inner_text()[:400]
    g = context.page.locator("#ed-a11y-list details.ed-a11y-group[data-rule='" + rule + "']").first
    expect(g).to_be_visible(timeout=5_000)
    assert "element" in g.locator("summary span").text_content()
    context.page.evaluate("() => document.querySelectorAll('#ed-a11y-list details').forEach(d => d.open = true)")


@then('the audit shows its rules with their values, "{rule}" set to "{value}"')
def step_rules_shown(context, rule, value):
    """rules with defaults, always on screen — the auditor answers for them"""
    box = context.page.locator("#ed-a11y-rules")
    expect(box).to_be_visible(timeout=5_000)
    context.page.evaluate("() => { const d = document.getElementById('ed-a11y-rules'); if (d) d.open = true; }")
    row = box.locator("tr", has_text=rule).first
    expect(row).to_be_visible(timeout=5_000)
    assert row.locator("td b").text_content() == value, row.inner_text()


@then('each chip row names the md block it sits in, its count there, and a ratio decided by the rule "{rule}"')
def step_review_measured(context, rule):
    """the unit a person can act on is the fence they wrote: every row names
    that block (kind + title), the chips it holds, one verdict by rule"""
    rows = context.page.locator(".ed-a11y-row[data-kind='review'][data-of='help']")
    assert rows.count() >= 2, context.page.locator("#ed-a11y-list").inner_text()[:400]
    seen = set()
    for i in range(rows.count()):
        row = rows.nth(i)
        md = row.get_attribute("data-md") or ""
        assert md.startswith("block "), md            # the fence's kind, then its title
        seen.add(md)
        assert row.get_attribute("data-verdict") in ("pass", "fail"), row.inner_text()
        assert re.match(r"\d+ × help$", row.locator(".ed-a11y-kind").text_content().strip())
        assert rule in row.locator(".ed-a11y-byrule").text_content()
        assert re.search(r"\d+(\.\d+)?:1", row.locator("i").text_content()), row.inner_text()
    assert len(seen) >= 2, seen                        # distinct blocks, each named


@then('the planted paragraph\'s look row names "{rule}" and says why the engine could not decide')
def step_review_row(context, rule):
    row = context.page.locator(".ed-a11y-row[data-kind='review'][data-rule='" + rule + "'][data-sel='#lc-planted-bg']").first
    expect(row).to_be_visible(timeout=5_000)
    expect(row.locator("b")).to_have_text("look")
    assert "could not be determined" in row.locator("i").text_content(), row.inner_text()


@then("clicking that row outlines the planted paragraph")
def step_review_click(context):
    context.page.locator(".ed-a11y-row[data-kind='review'][data-sel='#lc-planted-bg']").first.click()
    expect(context.page.locator("#lc-planted-bg")).to_have_class(re.compile(r"ed-a11y-outline"), timeout=5_000)
