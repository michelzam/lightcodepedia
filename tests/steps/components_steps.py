import re
from behave import when, then
from playwright.sync_api import expect


@when('I click the grid row containing "{text}"')
def step_click_grid_row(context, text):
    row = context.page.locator(".ag-row", has_text=text).first
    row.wait_for(state="visible", timeout=20_000)
    row.click()
    context.page.wait_for_timeout(400)


@then('a form titled "{title}" is visible')
def step_form_titled(context, title):
    name = context.page.locator(".lc-form-title .lc-form-name", has_text=title).first
    expect(name).to_be_visible(timeout=10_000)


@when("I open the first accordion section")
def step_open_accordion(context):
    summary = context.page.locator(".lc-accordion details summary").first
    summary.wait_for(state="visible", timeout=15_000)
    summary.click()
    context.page.wait_for_timeout(600)  # lazy markdown render


@then("the accordion section body has content")
def step_accordion_body(context):
    body = context.page.locator(".lc-accordion details[open] .lc-ac-body").first
    expect(body).to_be_visible(timeout=10_000)
    assert body.inner_text().strip(), "accordion body is empty"


@then('an embedded iframe from "{host}" is present')
def step_iframe_present(context, host):
    frame = context.page.locator("iframe[src*='" + host + "']").first
    expect(frame).to_be_attached(timeout=10_000)


@when('I pick the quiz answer "{answer}"')
def step_pick_quiz_answer(context, answer):
    li = context.page.locator(".lc-quiz li", has_text=answer).first
    li.wait_for(state="visible", timeout=15_000)
    li.click()
    context._quiz_answer = answer
    context.page.wait_for_timeout(300)


@then("that quiz answer is marked correct")
def step_quiz_correct(context):
    li = context.page.locator(".lc-quiz li", has_text=context._quiz_answer).first
    expect(li).to_have_class(re.compile(r"lc-quiz-correct"), timeout=5_000)


@then("that quiz answer is marked wrong")
def step_quiz_wrong(context):
    li = context.page.locator(".lc-quiz li", has_text=context._quiz_answer).first
    expect(li).to_have_class(re.compile(r"lc-quiz-wrong"), timeout=5_000)


@when('I click the bound grid "{grid_id}" row containing "{text}"')
def step_click_bound_grid_row(context, grid_id, text):
    row = context.page.locator(
        ".lc-datagrid[data-lc-id='" + grid_id + "'] tbody tr", has_text=text
    ).first
    row.wait_for(state="visible", timeout=15_000)
    row.click()
    context.page.wait_for_timeout(500)


@then('the detail chart bound to "{grid_id}" renders a canvas')
def step_detail_chart_canvas(context, grid_id):
    canvas = context.page.locator(
        ".lc-chart[data-bound-to='" + grid_id + "'] canvas"
    ).first
    expect(canvas).to_be_visible(timeout=10_000)


@then("the markdown pad shows an editor and a rendered preview")
def step_mdpad(context):
    pad = context.page.locator(".lc-mdpad").first
    expect(pad).to_be_visible(timeout=15_000)
    expect(pad.locator("textarea.lc-mdpad-in")).to_be_visible()
    # the preview renders the seed markdown to HTML (a heading element appears)
    expect(pad.locator(".lc-mdpad-out h2")).to_be_visible(timeout=15_000)


@then("a live Python editor is visible")
def step_live_python_editor(context):
    pad = context.page.locator(".lc-pyrun").first
    expect(pad).to_be_visible(timeout=15_000)
    expect(pad.locator("textarea")).to_be_visible()


@then("a live SQL editor is visible")
def step_sql_editor_visible(context):
    expect(context.page.locator("textarea.lc-query-editor").first).to_be_visible(timeout=10_000)


@then("a red coloured word is rendered")
def step_red_colour(context):
    el = context.page.locator(".markdown-body .red").first
    el.wait_for(state="attached", timeout=10_000)
    color = context.page.evaluate(
        "() => { var e = document.querySelector('.markdown-body .red');"
        " return e ? getComputedStyle(e).color : null; }"
    )
    # #c0392b == rgb(192, 57, 43)
    assert color and color.replace(" ", "") == "rgb(192,57,43)", (
        "expected red rgb(192,57,43), got %r" % (color,)
    )


@then("the mdpad preview shows a red word")
def step_mdpad_red(context):
    el = context.page.locator(".lc-mdpad-out .red").first
    el.wait_for(state="attached", timeout=20_000)
    color = context.page.evaluate(
        "() => { var e = document.querySelector('.lc-mdpad-out .red');"
        " return e ? getComputedStyle(e).color : null; }"
    )
    assert color and color.replace(" ", "") == "rgb(192,57,43)", (
        "expected red in mdpad preview, got %r" % (color,)
    )


@then("the mdpad italic text is not coloured")
def step_mdpad_italic_not_red(context):
    # regression: a *italic* before a later {: .red} must NOT inherit the colour
    color = context.page.evaluate(
        "() => { var ems = document.querySelectorAll('.lc-mdpad-out em');"
        " for (var i = 0; i < ems.length; i++) {"
        "   if (/italic/.test(ems[i].textContent)) return getComputedStyle(ems[i]).color;"
        " } return null; }"
    )
    # .red is #c0392b == rgb(192, 57, 43); the italic word must not be that
    assert color and color.replace(" ", "") != "rgb(192,57,43)", (
        "italic text wrongly coloured red: %r" % (color,)
    )


@then("a scanned subtree's root-absolute image resolves under the base path")
def step_base_path_heal(context):
    # scanElement() is the choke point every component's injected HTML passes
    # through. Force a project base (the suite serves at a domain root, where
    # lcBase is "") and confirm a freshly-injected root-absolute image gains the
    # base prefix — while a full URL would be left alone. Scoped to the subtree.
    src = context.page.evaluate(
        """() => {
          window.lcBase = "/lightcodelab";
          const box = document.createElement("div");
          document.body.appendChild(box);
          box.innerHTML = '<img id="_lc_heal" src="/assets/lab.jpg">';
          window.lcScanElement(box);
          return document.getElementById("_lc_heal").getAttribute("src");
        }"""
    )
    assert src == "/lightcodelab/assets/lab.jpg", "media not healed by scanElement: " + str(src)


@then("the block component's image is loaded, not broken")
def step_block_image_loaded(context):
    # the .block upgrader injects <img src="/assets/lab.jpg"> client-side; under
    # the base-path harness it must heal + download. naturalWidth stays 0 on a
    # 404, so this is the end-to-end guard the domain-root suite could not give.
    img = context.page.locator(".lc-block img").first
    img.wait_for(state="visible", timeout=20_000)
    context.page.wait_for_function(
        "el => el.complete && el.naturalWidth > 0",
        arg=img.element_handle(),
        timeout=20_000,
    )


@then("the folder gallery shows at least {n:d} cards")
def step_gallery_cards(context, n):
    # .folder enumerates from the build-time manifest (no GitHub API); on the
    # private lab the old API path 404'd for anonymous visitors. Cards proving.
    context.page.wait_for_selector(".lc-card h3 a", timeout=20_000)
    count = context.page.locator(".lc-cards .lc-card").count()
    assert count >= n, "only %d cards" % count


@then("the folder gallery shows no error card")
def step_gallery_no_error(context):
    txt = context.page.locator(".lc-cards").first.inner_text()
    assert "HTTP 4" not in txt and "not set" not in txt, txt[:200]


@then("the sitemap graph shows at least {n:d} nodes")
def step_sitemap_nodes(context, n):
    # .sitemap enumerates from the same build-time manifest (no GitHub API).
    context.page.wait_for_selector(".lc-sitemap .lc-sm-node", timeout=20_000)
    count = context.page.locator(".lc-sitemap .lc-sm-node").count()
    assert count >= n, "only %d nodes" % count
    assert context.page.locator(".lc-sm-msg", has_text="⚠").count() == 0, "sitemap error message shown"


@then("clicking a sitemap node opens its page")
def step_sitemap_node_click(context):
    # graph nodes are injected after every healing pass — their navigation must
    # still resolve under a project base (was a plain 404 on the deployed lab)
    context.page.locator(".lc-sitemap .lc-sm-node circle").first.click()
    context.page.wait_for_load_state()
    context.page.wait_for_timeout(500)
    assert "404" not in (context.page.title() or ""), context.page.url
    expect(context.page.locator("main h1").first).to_be_visible()


@then("every footnote on the page resolves")
def step_footnotes_resolve(context):
    got = context.page.evaluate(
        """() => ({
             refs: document.querySelectorAll('sup[id^=fnref] a.footnote').length,
             defs: document.querySelectorAll('div.footnotes li[id^=fn]').length,
             raw: (document.body.innerText.match(/\\[\\^\\w+\\]/g) || []),
           })"""
    )
    assert got["refs"] >= 4, "expected the page's footnote refs to render: %r" % got
    assert got["defs"] >= 4, "expected their definitions to survive: %r" % got
    assert not got["raw"], "raw footnote markup left on the page: %r" % got["raw"]


# ── Accessibility: keyboard operability ──────────────────────────────────────
# axe cannot see these. It reports zero keyboard violations on a page whose
# quiz answers are <li> with a click listener, because "this element has a
# handler and no keyboard path" is not statically decidable. So the keyboard
# dimension is covered here, in the suite that already gates every push.


@when('I tab to the quiz answer "{answer}"')
def step_tab_to_quiz_answer(context, answer):
    """Press Tab until it lands there — never .focus().

    .focus() moves focus programmatically and succeeds on an element no Tab
    could ever reach, so the first version of this step passed against a
    keyboard-dead quiz. Only walking the real tab order proves anything.
    """
    li = context.page.locator(".lc-quiz li", has_text=answer).first
    li.wait_for(state="visible", timeout=15_000)
    context.page.evaluate("() => (document.body.focus(), document.activeElement.blur())")
    for _ in range(120):
        context.page.keyboard.press("Tab")
        # It must BE a quiz option, not merely contain the words: tutorial101
        # has "breed: Labrador Retriever" in a form above the quiz, so a text
        # match alone stopped on that input and pressed Enter into a textbox.
        if context.page.evaluate(
            """t => { const a = document.activeElement;
                      return !!a && a.matches('.lc-quiz li')
                             && (a.textContent || '').includes(t); }""",
            answer,
        ):
            context._quiz_answer = answer
            return
    raise AssertionError("Tab never reached the answer %r — it is not in the tab order" % answer)


@then("that quiz answer is the focused element")
def step_quiz_focused(context):
    focused = context.page.evaluate(
        "() => (document.activeElement && document.activeElement.textContent || '').trim()"
    )
    assert context._quiz_answer in focused, (
        "expected the answer to hold focus, got: " + focused[:80]
    )


@when('I press "{key}"')
def step_press_key(context, key):
    context.page.keyboard.press(key)
    context.page.wait_for_timeout(300)


@then('the quiz answer "{answer}" exposes the role "{role}"')
def step_quiz_role(context, answer, role):
    li = context.page.locator(".lc-quiz li", has_text=answer).first
    expect(li).to_have_attribute("role", role, timeout=5_000)


@then('the quiz answer "{answer}" is announced as checked')
def step_quiz_checked(context, answer):
    li = context.page.locator(".lc-quiz li", has_text=answer).first
    expect(li).to_have_attribute("aria-checked", "true", timeout=5_000)


@then("every quiz answer is reachable by keyboard")
def step_quiz_all_reachable(context):
    missing = context.page.evaluate(
        """() => Array.from(document.querySelectorAll('.lc-quiz li'))
                 .filter(li => li.getAttribute('tabindex') === null)
                 .map(li => (li.textContent || '').trim().slice(0, 40))"""
    )
    assert not missing, "answers with no tab stop: " + repr(missing)


@then("that quiz answer is not the focused element")
def step_quiz_not_focused(context):
    focused = context.page.evaluate(
        "() => (document.activeElement && document.activeElement.textContent || '').trim()"
    )
    assert context._quiz_answer not in focused, (
        "focus should have moved off the answer, still on: " + focused[:80]
    )


@then("every agent form field has an accessible name")
def step_agent_fields_named(context):
    # axe's `label` rule: a placeholder is not a name, and an off-screen
    # input is still in the accessibility tree. Mirror the rule's inputs —
    # aria-label, aria-labelledby, title, or a <label> that points here.
    unnamed = context.page.evaluate(
        """() => Array.from(document.querySelectorAll(
                   '.lc-agent input, .lc-agent textarea, .lc-agent select'))
                 .filter(el => {
                   if (el.type === 'hidden') return false;
                   if (el.getAttribute('aria-label')) return false;
                   if (el.getAttribute('aria-labelledby')) return false;
                   if (el.getAttribute('title')) return false;
                   if (el.id && document.querySelector(
                         'label[for="' + CSS.escape(el.id) + '"]')) return false;
                   if (el.closest('label')) return false;
                   return true;
                 })
                 .map(el => el.tagName.toLowerCase() + '[' +
                            (el.type || '') + '] ' +
                            (el.className || '') + ' ph=' +
                            (el.getAttribute('placeholder') || '—'))"""
    )
    assert not unnamed, (
        "%d agent field(s) with no accessible name:\n  %s"
        % (len(unnamed), "\n  ".join(unnamed))
    )


# ── accessible names on inputs (axe rule "label") ─────────────────────────
# The engine's editors and form fields are visually framed by their chrome
# but were programmatically nameless. These pin the accessible name at the
# source components, so the private axe ratchet never goes red on them again.

_NAME_PROBE = """(sel) => {
  const bad = [];
  document.querySelectorAll(sel).forEach(el => {
    const name = el.getAttribute('aria-label')
      || (el.labels && el.labels.length)
      || el.getAttribute('aria-labelledby')
      || el.getAttribute('title');
    if (!name) bad.push(el.outerHTML.slice(0, 120));
  });
  return bad;
}"""


@then("every code editor on the page exposes an accessible name")
def step_editors_named(context):
    bad = context.page.evaluate(
        _NAME_PROBE, ".lc-pyrun-code, .lc-pyrepl-input, .lc-mdpad-in")
    assert not bad, "nameless editors:\n" + "\n".join(bad)


@then("every form control on the page exposes an accessible name")
def step_form_named(context):
    bad = context.page.evaluate(
        _NAME_PROBE,
        ".lc-form-bool input, .lc-form-select, input[type=range].lc-form-range")
    assert not bad, "nameless form controls:\n" + "\n".join(bad)


# ── the page's own tags, beside its title ─────────────────────────────────
# A page's tags live on its features, which are hidden by default, so the
# folder card showed them and the page itself showed nothing. The chips ride
# INSIDE the h1: that is what keeps the title on one line.

def _title_tags(context):
    return context.page.evaluate(
        """() => Array.from(document.querySelectorAll('h1 .lc-title-tag'))
                     .map(el => el.textContent.trim())""")


@then('the page title shows the tags "{names}"')
def step_title_tags(context, names):
    want = [n.strip() for n in names.split(",") if n.strip()]
    got = _title_tags(context)
    for n in want:
        assert n in got, f"missing tag {n!r} beside the title; got {got}"


@then("the tags sit inside the page title")
def step_title_tags_inline(context):
    # the chip's OWN h1 — on a runner page the document's first h1 is the
    # host page's hidden title, not the rendered document's
    inside = context.page.evaluate(
        """() => {
             const chip = document.querySelector('.lc-title-tag');
             return !!(chip && chip.closest('h1'));
           }""")
    assert inside, "the tag chips are not inside the h1 — the title gained a line"


@then("the page title shows no tags")
def step_title_no_tags(context):
    got = _title_tags(context)
    assert not got, f"expected a bare title, got {got}"


@then("a QR on the page encodes this page's address")
def step_qr_here(context):
    """The library draws into a table/canvas, so the assertion is on what the
    upgrader was handed: the here="true" widget must exist and carry a code,
    and its caption must be the fence's only line."""
    got = context.page.evaluate(
        """() => {
             const w = Array.from(document.querySelectorAll('.lc-qr')).find(
               el => el.querySelector('.lc-qr-label')
                  && /this page/i.test(el.querySelector('.lc-qr-label').textContent));
             return w ? {found: true, text: w.getAttribute('data-lc-text'),
                         href: location.href} : {found: false};
           }""")
    assert got["found"], "no .qr with the here caption rendered"
    assert got["text"] == got["href"], f"encoded {got['text']!r}, page is {got['href']!r}"


@then("a round image embed is on the page")
def step_round_embed(context):
    box = context.page.locator(".lc-embed-circle img").first
    expect(box).to_be_visible(timeout=15_000)
    radius = context.page.evaluate(
        """() => getComputedStyle(document.querySelector('.lc-embed-circle img')).borderRadius""")
    assert "50%" in radius, f"not round: border-radius is {radius!r}"


@then('the chart "{cid}" reports {n:d} bars')
def step_chart_bar_count(context, cid, n):
    """What the model would read: rects if the chart drew SVG, otherwise the
    count the canvas recorded."""
    got = context.page.evaluate(
        """(id) => {
             const el = document.querySelector(`[data-lc-id="${id}"]`)
                     || document.querySelector('.lc-chart');
             if (!el) return null;
             const rects = el.querySelectorAll('rect').length;
             return rects || parseInt(el.getAttribute('data-lc-bars') || '0', 10);
           }""", cid)
    assert got == n, f"the chart reports {got} bars, expected {n}"


# ── paper ───────────────────────────────────────────────────────────────────
# The PDF export (tools/export_pdfs.py) prints through this same stylesheet,
# so what the workflow produces is what these steps assert.
@when("the page is shown as it would print")
def step_emulate_print(context):
    context.page.emulate_media(media="print")
    context.page.wait_for_timeout(300)


@then("no button is offered on paper")
def step_no_buttons_on_paper(context):
    left = context.page.evaluate("""() => [...document.querySelectorAll(
      '#lc-topbar, .lc-edit-fab, .lc-feature-run, .lc-guide-ask, .lc-mode-fab')]
      .filter(el => el.getBoundingClientRect().height > 0)
      .map(el => el.id || el.className)""")
    assert not left, "these would print: %r" % left


@then("every accordion is open on paper")
def step_accordions_open(context):
    hidden = context.page.evaluate("""() => [...document.querySelectorAll('details')]
      .filter(d => { const body = [...d.children].find(c => c.tagName !== 'SUMMARY');
                     return body && body.getBoundingClientRect().height === 0; }).length""")
    assert hidden == 0, "%d accordion(s) would print as a hole" % hidden


# ── cols="2;1" ──────────────────────────────────────────────────────────────
def _grid_widths(context, template_kind):
    """Every .lc-blocks on the page, as its measured column widths."""
    return context.page.evaluate("""() => [...document.querySelectorAll('.lc-blocks')]
      .map(b => getComputedStyle(b).gridTemplateColumns.split(' ')
        .map(w => Math.round(parseFloat(w))))""")


@then("a weighted block splits its width two to one")
def step_weighted_cols(context):
    grids = _grid_widths(context, "weighted")
    two_to_one = [g for g in grids
                  if len(g) == 2 and g[1] and 1.9 <= g[0] / g[1] <= 2.1]
    assert two_to_one, "no 2:1 grid on the page — got %r" % grids


@then('a plain "cols" block still splits evenly')
def step_even_cols(context):
    grids = _grid_widths(context, "even")
    even = [g for g in grids if len(g) == 2 and g[1] and 0.98 <= g[0] / g[1] <= 1.02]
    assert even, "the old cols=\"2\" meaning changed — got %r" % grids


@then("an accordion given an id can be opened by that id")
def step_accordion_by_id(context):
    """Build one the way a page does, then drive it the way a script line
    does: window.lcVerbs.act('open', <the element the id resolves to>)."""
    got = context.page.evaluate("""() => {
      const pre = document.createElement('pre');
      pre.id = 'tour_target';
      const code = document.createElement('code');
      code.textContent = '### One\\nfirst\\n\\n### Two\\nsecond\\n';
      pre.appendChild(code);
      document.querySelector('.markdown-body, main, body').appendChild(pre);
      window.lcUpgradeAccordion ? window.lcUpgradeAccordion(pre) : window.lcScanElement(pre.parentNode);
      pre.className = 'accordion';
      window.lcScanElement(document.body);
      const el = document.getElementById('tour_target');
      if (!el || !el.classList.contains('lc-accordion')) return { kept: false };
      window.lcVerbs.act('open', el);
      const open1 = [...el.querySelectorAll('details')].filter(d => d.open).length;
      window.lcVerbs.act('close', el);
      const open2 = [...el.querySelectorAll('details')].filter(d => d.open).length;
      return { kept: true, opened: open1, closed: open2 };
    }""")
    assert got.get("kept"), "the accordion dropped the author's id"
    assert got["opened"] == 2 and got["closed"] == 0, got


# ── 〰️ seam ─────────────────────────────────────────────────────────────────
@then("each seam says its register out loud")
def step_seam_labels(context):
    seams = context.page.evaluate("""() => [...document.querySelectorAll('.lc-seam')]
      .map(s => ((s.querySelector('.lc-seam-label') || {}).textContent || '').trim())""")
    assert len(seams) >= 3, "expected the three borders, got %r" % seams
    approved = {"The app starts here", "A course tool", "Back to the lesson"}
    assert set(seams) <= approved, "a seam drifted off the vocabulary: %r" % seams


@then("a seam is still a rule, for a screen reader")
def step_seam_semantics(context):
    got = context.page.evaluate("""() => [...document.querySelectorAll('.lc-seam')].map(s => {
      const r = s.querySelector('hr');
      return { rule: !!r, spoken: r ? r.getAttribute('aria-label') : null }; })""")
    assert all(g["rule"] for g in got), "the seam lost its <hr>: %r" % got
    assert all(g["spoken"] for g in got), "the border is silent to a reader: %r" % got


@then("each tone reaches its own cards")
def step_tone_classes(context):
    got = context.page.evaluate(
        """() => [...document.querySelectorAll('.lc-blocks')]
             .map(e => (e.className.match(/lc-tone-(\\w+)/) || [])[1] || '')
             .filter(Boolean)"""
    )
    for want in ("paper", "app", "tool"):
        assert want in got, "tone %r never reached a wrapper: %r" % (want, got)
    assert set(got) <= {"paper", "app", "tool"}, "a fourth tone appeared: %r" % got
    # a toned wrapper is still an ordinary block grid, cards and all
    n = context.page.evaluate(
        "() => document.querySelectorAll('.lc-tone-app .lc-block').length"
    )
    assert n >= 1, "the app tone swallowed its cards"


@then("an unknown tone leaves the card plain")
def step_tone_unknown(context):
    # the knob is not a spelling test: a typo must cost the reader nothing
    cls = context.page.evaluate(
        """() => {
             const p = document.createElement('pre');
             p.className = 'blocks';
             p.setAttribute('tone', 'chartreuse');
             p.textContent = '### x\\nbody';
             document.querySelector('main').appendChild(p);
             window.lcScanElement(document.querySelector('main'));
             const w = document.querySelector('main > .lc-blocks:last-of-type');
             return w ? w.className : 'gone';
           }"""
    )
    assert "lc-tone-" not in cls, "an unknown tone invented a look: %r" % cls


# ── the runner refuses input() rather than freezing the tab ─────────────────

def _type_into_runner(page, code):
    box = page.locator(".lc-pyrun").first
    ed = box.locator("textarea").first
    ed.click()
    page.keyboard.press("Control+a")
    page.keyboard.type(code)
    box.locator(".lc-pyrun-run").first.click()
    return box


@when("I run a program that adds numbers until a blank line")
def step_run_loop_program(context):
    context.runner = _type_into_runner(context.page, (
        "total = 0\n"
        "while True:\n"
        "    line = input(\"number (blank to stop): \")\n"
        "    if not line:\n"
        "        break\n"
        "    total += int(line)\n"
        "print(\"total:\", total)"))


@when("I run a program that prints two lines")
def step_run_two_prints(context):
    context.runner = _type_into_runner(context.page, 'print("a")\nprint("b")')


@when('I answer "{first}", then "{second}", then nothing')
def step_answer_three(context, first, second):
    for value in (first, second, ""):
        context.page.wait_for_selector(".lc-pyrun-ask-box", timeout=25_000)
        box = context.runner.locator(".lc-pyrun-ask-box").first
        box.fill(value)
        box.press("Enter")


@then('the console shows the whole conversation, ending in "{tail}"')
def step_console_transcript(context, tail):
    out = context.runner.locator(".lc-pyrun-out").first
    expect(out).to_contain_text(tail, timeout=25_000)
    text = out.text_content() or ""
    # every question asked appears with the answer beside it, as a terminal shows it
    assert text.count("number (blank to stop):") == 3, text
    assert "3" in text and "4" in text, text


@then("the console shows them on two lines")
def step_two_lines(context):
    out = context.runner.locator(".lc-pyrun-out").first
    expect(out).to_contain_text("a", timeout=25_000)
    text = (out.text_content() or "").strip()
    assert text.splitlines()[:2] == ["a", "b"], repr(text)


@then("a titled block wears the window bar, and its title")
def step_titled_block_is_a_window(context):
    win = context.page.locator(".lc-block-win").first
    expect(win).to_be_visible(timeout=15_000)
    expect(win.locator(".lc-win-dots")).to_be_visible()
    title = (win.locator(".lc-win-title").first.text_content() or "").strip()
    assert title == "Lucky's day", "the window bar lost its title: %r" % title


@then("an untitled block is still a plain card")
def step_untitled_block_is_a_card(context):
    # the page is full of plain .block cards — none of them may have grown a bar
    plain = context.page.locator(".lc-blocks:not(.lc-block-win .lc-blocks)")
    assert plain.count() > 0, "no plain blocks on the block page"
    bars = context.page.evaluate(
        """() => [...document.querySelectorAll('.lc-blocks')]
             .filter(b => !b.closest('.lc-block-win'))
             .filter(b => b.querySelector('.lc-win-bar')).length""")
    assert bars == 0, "%d untitled block(s) grew a window bar" % bars


# ── the inspector's verbs: engine steps, so every published page can use them
# (they lived in the lab-only classroom4 steps and pedia's run had them undefined, 2026-09-04)
@when('I press "{verb}" on the "{elid}" inspector')
def step_press(context, verb, elid):
    context.page.locator(
        '[data-lc-inspector="%s"] [data-card] button[data-m="%s"]' % (elid, verb)).first.click()

@then('the "{verb}" verb on the "{elid}" inspector is enabled')
def step_verb_enabled(context, verb, elid):
    btn = context.page.locator(
        '[data-lc-inspector="%s"] [data-card] button[data-m="%s"]' % (elid, verb)).first
    expect(btn).to_be_visible(timeout=45_000)
    expect(btn).to_be_enabled(timeout=15_000)

@then('the "{verb}" verb on the "{elid}" inspector explains "{tip}"')
def step_verb_tip(context, verb, elid, tip):
    btn = context.page.locator(
        '[data-lc-inspector="%s"] [data-card] button[data-m="%s"]' % (elid, verb)).first
    expect(btn).to_be_visible(timeout=45_000)
    expect(btn).to_have_attribute("title", tip, timeout=15_000)

@then('the "{verb}" verb on the "{elid}" inspector is disabled')
def step_verb_disabled(context, verb, elid):
    btn = context.page.locator(
        '[data-lc-inspector="%s"] [data-card] button[data-m="%s"]' % (elid, verb)).first
    expect(btn).to_be_visible(timeout=45_000)
    expect(btn).to_be_disabled()
