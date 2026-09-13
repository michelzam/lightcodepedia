"""What we paint ourselves must read: WCAG 1.4.3 contrast, computed live.

The axe scan runs privately on the live site and names its nodes; this is
the rig-side twin for the colours WE choose — the ones a fix can change and
a later edit can quietly undo. Effective background is the nearest painted
ancestor; opacity along the way is blended in, since fading text is the
usual way contrast is lost without touching a colour.
"""
from behave import then

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
