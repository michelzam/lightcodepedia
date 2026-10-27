import re
"""Steps for run_editor.feature — the run editor as a text field.
(`I undo in the "<id>" editor` lives in agent_bound_steps.py.)"""
from behave import when, then
from playwright.sync_api import expect


def _ta(context, run_id):
    return context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-code")


@when('I type "{text}" at the end of the "{run_id}" editor')
def step_type_at_end(context, text, run_id):
    ta = _ta(context, run_id)
    ta.click()
    context.page.keyboard.press("Control+End")
    context.page.keyboard.type(text)


@when('I press Tab in the "{run_id}" editor')
def step_press_tab(context, run_id):
    _ta(context, run_id).focus()
    context.page.keyboard.press("Tab")


@when('I replace the "{run_id}" editor\'s program with:')
@when('I replace the "{run_id}" editor\'s program with')   # behave 1.2.6 (pedia) strips the colon before a docstring; 1.3 keeps it
def step_replace_program(context, run_id):
    ta = _ta(context, run_id)
    ta.focus()
    context.page.keyboard.press("Control+a")
    context.page.keyboard.insert_text(context.text)
    context.page.wait_for_timeout(100)


@when('I click Run in the "{run_id}" editor')
def step_click_run(context, run_id):
    context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-run").click()


@then('the "{run_id}" editor ends with "{text}"')
def step_ends_with(context, run_id, text):
    v = _ta(context, run_id).input_value()
    assert v.endswith(text), "editor ends with %r" % v[-30:]


@then('the "{run_id}" editor does not contain "{text}"')
def step_not_contains(context, run_id, text):
    v = _ta(context, run_id).input_value()
    assert text not in v, "editor still holds %r" % text


@then('the "{run_id}" editor\'s output reads "{line1}" then "{line2}"')
def step_output_reads(context, run_id, line1, line2):
    out = context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-out")
    expect(out).to_have_text(line1 + "\n" + line2, timeout=30_000)


@when('I select the lines "{first}" to "{last}" of the "{run_id}" editor')
def step_select_lines(context, first, last, run_id):
    ta = _ta(context, run_id)
    v = ta.input_value()
    a, b = v.index(first), v.index(last) + len(last)
    ta.focus()
    ta.evaluate("(el, r) => el.setSelectionRange(r[0], r[1])", [a, b])


@when('I press Shift+Tab in the "{run_id}" editor')
def step_press_shift_tab(context, run_id):
    _ta(context, run_id).focus()
    context.page.keyboard.press("Shift+Tab")


@then('the "{run_id}" editor reads "{text}"')
def step_editor_reads(context, run_id, text):
    v = _ta(context, run_id).input_value()
    want = text.replace("\\n", "\n")
    assert v == want, "editor reads %r" % v


@then('the "{run_id}" editor\'s selection reads "{text}"')
def step_selection_reads(context, run_id, text):
    ta = _ta(context, run_id)
    sel = ta.evaluate("el => el.value.slice(el.selectionStart, el.selectionEnd)")
    want = text.replace("\\n", "\n")
    assert sel == want, "selection reads %r" % sel


@then('the "{run_id}" console shows "{text}" while it plays')
def step_console_frame(context, run_id, text):
    out = context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-out")
    expect(out).to_contain_text(text, timeout=15_000)


@then('the "{run_id}" console ends on "{text}" without "{gone}"')
def step_console_last_frame(context, run_id, text, gone):
    out = context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-out")
    context.page.wait_for_function(
        "el => !el.hasAttribute('data-lc-playing')", arg=out.element_handle(), timeout=20_000)
    got = out.inner_text()
    assert text in got and gone not in got, got


@then('the "{run_id}" editor\'s output shows:')
@then('the "{run_id}" editor\'s output shows')   # behave 1.2.6 (pedia) strips the colon before a docstring; 1.3 keeps it
def step_output_shows_block(context, run_id):
    out = context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-out")
    expect(out).to_contain_text(context.text, timeout=30_000)


@then('the "{run_id}" editor\'s output shows "{text}"')
def step_output_shows(context, run_id, text):
    out = context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-out")
    expect(out).to_contain_text(text.replace('\\"', '"'), timeout=30_000)


@when('I click Test in the "{run_id}" editor')
def step_click_test(context, run_id):
    context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-test").click()


@when('I press Dr. mypy in the "{run_id}" editor')
def step_click_mypy(context, run_id):
    context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-mypy").click()


@then('the "{run_id}" editor\'s tests read "{text}"')
def step_tests_read(context, run_id, text):
    summary = context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-test-summary")
    expect(summary).to_have_text(text, timeout=30_000)


@when('I replace "{old}" with "{new}" in the "{run_id}" editor')
def step_replace_in_editor(context, old, new, run_id):
    ta = _ta(context, run_id)
    v = ta.input_value()
    assert old in v, "no %r in the editor" % old
    ta.evaluate("(el, v) => { el.value = v; el.dispatchEvent(new Event('input')); }", v.replace(old, new, 1))


@then("the page carries the doctest stand-in")
def step_has_pycheck(context):
    ok = context.page.evaluate("() => !!(window.lcPyBefore && window.LC_PY_SHIM && window.lcDrMypy)")
    assert ok, "pycheck.md did not load: no doctest, no Dr. mypy on this page"


@then('the engine file "{path}" uses no regex lookbehind')
def step_no_lookbehind(context, path):
    import os, re
    root = os.path.join(os.path.dirname(__file__), "..", "..")
    src = open(os.path.join(root, path), encoding="utf-8").read()
    hits = [n + 1 for n, l in enumerate(src.split("\n")) if re.search(r"\(\?<[=!]", l)]
    assert not hits, "lookbehind on line(s) %s — older Safari refuses the whole script" % hits


@then('the "{pad_id}" pad counts "{tally}" examples passing')
def step_pad_tally(context, pad_id, tally):
    pad = context.page.locator("[data-lc-id='" + pad_id + "']")
    expect(pad).to_have_attribute("data-lc-doctest", tally, timeout=30_000)


@when('I replace "{old}" with "{new}" in the "{pad_id}" pad')
def step_replace_in_pad(context, old, new, pad_id):
    ta = context.page.locator("[data-lc-id='" + pad_id + "'] textarea.lc-mdpad-in")
    old, new = old.replace("\\n", "\n"), new.replace("\\n", "\n")
    v = ta.input_value()
    assert old in v, "no %r in the pad" % old
    ta.evaluate("(el, v) => { el.value = v; el.dispatchEvent(new Event('input')); }", v.replace(old, new, 1))


@then('the "{pad_id}" pad marks no line as an error')
def step_pad_clean(context, pad_id):
    pad = context.page.locator("[data-lc-id='" + pad_id + "']")
    context.page.wait_for_function(
        "p => { const e = document.querySelector(\"[data-lc-id='\" + p + \"']\"); return e && !e.hasAttribute('data-lc-errors'); }",
        arg=pad_id, timeout=30_000)


@then('the "{run_id}" editor played {n:d} notes, the last "{note}"')
def step_editor_played(context, run_id, n, note):
    """what play() queued, as the block records it (song.md): a count and the last note"""
    from playwright.sync_api import expect
    el = context.page.locator("#lc-pyrun-" + run_id)
    expect(el).to_have_attribute("data-lc-played", str(n), timeout=20_000)
    expect(el).to_have_attribute("data-lc-last-note", note)


@then('the "{run_id}" editor\'s output ends with "{text}"')
def step_editor_output_ends(context, run_id, text):
    from playwright.sync_api import expect
    out = context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-out")
    expect(out).to_contain_text(text, timeout=20_000)


@then('the "{run_id}" editor played {n:d} notes')
def step_editor_played_none(context, run_id, n):
    """🧪 Test runs the docstrings' examples, never the program: nothing is queued"""
    el = context.page.locator("#lc-pyrun-" + run_id)
    assert int(el.get_attribute("data-lc-played") or 0) == n, "notes were queued by the test button"


def _sub(context, run_id, token):
    subs = context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-subs .lc-sub")
    n = subs.count()
    for i in range(n):
        el = subs.nth(i)
        if el.text_content() == token:
            return el
    raise AssertionError("no subtitle on %r in %s" % (token, run_id))


@then('the "{run_id}" editor subtitles "{token}" as "{kind}"')
def step_subtitled_as(context, run_id, token, kind):
    sub = _sub(context, run_id, token).get_attribute("data-sub") or ""
    assert sub.startswith(kind), "%r reads %r, not %r" % (token, sub, kind)


@when('I tap the subtitle "{token}" in the "{run_id}" editor')
def step_tap_subtitle(context, token, run_id):
    _sub(context, run_id, token).click()


@then('the "{run_id}" editor\'s subtitle line reads "{text}"')
def step_subline(context, run_id, text):
    from playwright.sync_api import expect
    expect(context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-subline")).to_contain_text(text)


@when('I press 💬 Subtitles in the "{run_id}" editor')
def step_press_subtitles(context, run_id):
    context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-subs-btn").click()


@then('the "{run_id}" editor is back to editing')
def step_back_to_editing(context, run_id):
    from playwright.sync_api import expect
    root = context.page.locator("#lc-pyrun-" + run_id)
    expect(root.locator(".lc-pyrun-subs")).to_be_hidden()
    expect(root).not_to_have_class(re.compile(r"lc-pyrun-subtitled"))


@then('the "{run_id}" editor shows its subtitles')
def step_shows_subtitles(context, run_id):
    from playwright.sync_api import expect
    expect(context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-subs .lc-sub").first).to_be_visible()


@then('the "{run_id}" editor\'s run button reads "{text}"')
def step_run_button_reads(context, run_id, text):
    from playwright.sync_api import expect
    expect(context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-run")).to_have_text(text)


@then('the "{run_id}" editor\'s "{which}" button is an icon with the tooltip "{tip}"')
def step_icon_button(context, run_id, which, tip):
    btn = context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-" + which)
    assert "lc-pyrun-icon" in (btn.get_attribute("class") or ""), "not an icon button"
    assert (btn.get_attribute("title") or "").startswith(tip), btn.get_attribute("title")
    assert len((btn.text_content() or "").strip()) <= 2, "the button still carries a word: %r" % btn.text_content()


@then('the "{run_id}" editor\'s subtitles switch is "{state}"')
def step_switch_state(context, run_id, state):
    from playwright.sync_api import expect
    sw = context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-subs-btn")
    expect(sw).to_have_attribute("role", "switch")
    expect(sw).to_have_attribute("aria-checked", state)


@when('I put the caret at the end of the "{run_id}" editor')
def step_caret_end(context, run_id):
    ta = _ta(context, run_id)
    ta.focus()
    ta.evaluate("el => { const n = el.value.replace(/\\n$/, '').length; el.setSelectionRange(n, n); }")


@when('I press Ctrl+Space in the "{run_id}" editor')
def step_ctrl_space(context, run_id):
    _ta(context, run_id).press("Control+Space")


@when('I press Escape in the "{run_id}" editor')
def step_escape(context, run_id):
    _ta(context, run_id).press("Escape")


@then('the "{run_id}" editor offers "{a}" and "{b}"')
def step_offers(context, run_id, a, b=None):
    from playwright.sync_api import expect
    root = context.page.locator("#lc-pyrun-" + run_id)
    expect(root).to_have_attribute("data-lc-comp", re.compile(r"(^|,)" + re.escape(a) + r"(,|$)"), timeout=5_000)
    if b:
        expect(root).to_have_attribute("data-lc-comp", re.compile(r"(^|,)" + re.escape(b) + r"(,|$)"))


@when('I accept the completion in the "{run_id}" editor')
def step_accept_completion(context, run_id):
    _ta(context, run_id).press("Enter")


@when('I select the word "{word}" in the "{run_id}" editor')
def step_select_word(context, word, run_id):
    ta = _ta(context, run_id)
    ta.focus()
    ta.evaluate("""(el, w) => { const i = el.value.indexOf(w); el.setSelectionRange(i, i + w.length);
      el.dispatchEvent(new Event('select')); }""", word)


@then('the "{run_id}" editor lights {n:d} other occurrences of "{word}"')
def step_lights(context, run_id, n, word):
    from playwright.sync_api import expect
    root = context.page.locator("#lc-pyrun-" + run_id)
    expect(root).to_have_attribute("data-lc-lit", word + ":" + str(n), timeout=5_000)
    expect(root.locator(".lc-pyrun-marks mark")).to_have_count(n)


@then('the "{run_id}" editor offers the name "{a}"')
def step_offers_one(context, run_id, a):
    step_offers(context, run_id, a)


@then('the "{run_id}" editor\'s captions colour "{token}" as a bold keyword')
def step_caption_kw(context, run_id, token):
    el = _sub(context, run_id, token)
    assert "lc-sub-kw" in (el.get_attribute("class") or ""), el.get_attribute("class")
    weight = el.evaluate("e => getComputedStyle(e).fontWeight")
    assert weight in ("700", "bold"), weight


@then('the "{run_id}" editor\'s captions colour "{token}" as a string')
def step_caption_string(context, run_id, token):
    subs = context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-subs .lc-sub-string")
    texts = [subs.nth(i).text_content() for i in range(subs.count())]
    assert any(token in t for t in texts), texts


@when('I fold the block at "{token}" in the "{run_id}" editor')
def step_fold(context, token, run_id):
    line = _sub(context, run_id, token).evaluate("e => e.closest('.lc-sub-line').getAttribute('data-l')")
    context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-gutter .lc-pyrun-gfold[data-l='" + line + "']").click()


@then('the "{run_id}" editor hides {n:d} captioned lines')
def step_hidden_lines(context, run_id, n):
    from playwright.sync_api import expect
    expect(context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-subs .lc-sub-line.lc-sub-hidden")).to_have_count(n)


@then('the "{run_id}" editor\'s clear button reads "{text}"')
def step_clear_reads(context, run_id, text):
    from playwright.sync_api import expect
    btn = context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-clear")
    expect(btn).to_have_text(text)
    assert "lc-pyrun-icon" not in (btn.get_attribute("class") or "")


@when('I drag the "{run_id}" editor\'s grip down by {px:d} pixels')
def step_drag_grip(context, run_id, px):
    grip = context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-grip")
    context.h0 = _ta(context, run_id).evaluate("el => el.getBoundingClientRect().height")
    box = grip.bounding_box()
    x, y = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
    context.page.mouse.move(x, y); context.page.mouse.down(); context.page.mouse.move(x, y + px, steps=6); context.page.mouse.up()


@then('the "{run_id}" editor grew by about {px:d} pixels')
def step_grew(context, run_id, px):
    h1 = _ta(context, run_id).evaluate("el => el.getBoundingClientRect().height")
    assert abs((h1 - context.h0) - px) <= 8, "grew by %s, not %s" % (h1 - context.h0, px)


@when('I double-click the "{run_id}" editor\'s grip')
def step_dblclick_grip(context, run_id):
    context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-grip").dblclick()


@then('the "{run_id}" editor is back to its own height')
def step_own_height(context, run_id):
    h = _ta(context, run_id).evaluate("el => el.style.height")
    assert h == "", "a dragged height is still set: %r" % h


@then('the "{run_id}" editor\'s captions count as many lines as the program')
def step_caption_lines(context, run_id):
    n_prog = _ta(context, run_id).evaluate("el => el.value.split('\\n').length")
    n_caps = context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-subs .lc-sub-line").count()
    assert n_caps == n_prog, "%d captioned lines for %d program lines" % (n_caps, n_prog)
    h_caps = context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-subs").evaluate("el => el.scrollHeight")
    h_prog = _ta(context, run_id).evaluate("el => el.scrollHeight")
    assert abs(h_caps - h_prog) <= 24, "captions %dpx tall, the program %dpx" % (h_caps, h_prog)


@then('the "{run_id}" editor\'s gutter numbers {n:d} lines')
def step_gutter_numbers(context, run_id, n):
    txt = context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-gutter-inner").text_content() or ""
    assert len(txt.split("\n")) == n, "the gutter reads %r" % txt
