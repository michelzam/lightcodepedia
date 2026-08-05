"""The Broken Wire — steps for the three defects that exercise it.

The lesson asks a learner to change ONE NAME: a table declares
source="ozaukee", nothing answers to that name, and the repair is made
through the ⚙️ on the table itself, inside a bench slot. Three separate
pieces of engine have to hold for that gesture to work end to end, and
each of these steps pins one of them:

  * the gear must open a component INSIDE a slot as a component (knobs),
    not as the div its rendered grid looks like from outside;
  * saving a knob must rewrite the IAL line in the LEARNER'S file, laying
    the author's starter down first;
  * a source= that resolves to nothing must come to rest on a visible,
    tappable message instead of waiting forever;
  * and a card must show the reader's own run, not the author's status=.
"""

from behave import given, when, then
from playwright.sync_api import expect


def _alt_move_on(page, locator):
    """Reveal the gear: xray_edit reads e.target, so the pointermove has to
    be dispatched ON the element, with altKey for x-ray mode."""
    locator.wait_for(state="visible", timeout=15_000)
    locator.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    locator.evaluate(
        "el => el.dispatchEvent(new PointerEvent('pointermove',"
        " {altKey: true, bubbles: true, cancelable: true}))"
    )
    page.wait_for_timeout(600)


# ── the gear, on a part that lives in the learner's own slot ───────────────

@when("I open the x-ray editor on the wired table")
def step_open_editor_on_wired(context):
    grid = context.page.locator(".lc-bench-slot .lc-datagrid").first
    _alt_move_on(context.page, grid)
    gear = context.page.locator("#lcx-gear")
    gear.wait_for(state="visible", timeout=10_000)
    gear.click(force=True)
    expect(context.page.locator("#lcx-content")).to_be_visible(timeout=5_000)


@then("the editor opened a component, not a plain block")
def step_editor_is_component(context):
    # A component editor is titled by its CLASS (".datagrid #wired"); a plain
    # block is titled by its tag ("text", "code", "div"). The knobs are the
    # other half: a block has none, and a grid rendered past the page scan
    # used to arrive here as exactly that — a div with no knobs.
    title = context.page.locator("#lcx-edit-title").inner_text()
    knobs = context.page.locator("#lcx-edit-body input[data-knob]").count()
    assert knobs > 0, (
        "the editor offered no knobs — it opened this as a plain block. "
        "Title was %r" % title)
    assert ".datagrid" in title, (
        "the editor titled this %r, not as the component it is" % title)


@then('the editor offers a "{knob}" knob')
def step_editor_offers_knob(context, knob):
    got = context.page.eval_on_selector_all(
        "#lcx-edit-body input[data-knob]",
        "els => els.map(e => e.getAttribute('data-knob'))")
    assert knob in got, "knobs offered were %r — no %r among them" % (got, knob)


@when('I set the "{knob}" knob to "{value}"')
def step_set_knob(context, knob, value):
    context.page.fill("#lcx-edit-body input[data-knob='" + knob + "']", value)


@when("I save, and the bench receives it")
def step_save_to_bench(context):
    """Press 💾 and WAIT FOR THE WRITES — never a fixed sleep.

    A first slot save is TWO commits: the author's starter, then the
    learner's change. Waiting for "a commit" returns on the starter and the
    real one is still in flight, so wait for the writing to STOP instead —
    the count holding still across two samples — which needs no scenario to
    say in advance how many it expects.
    """
    import time

    context.page.click("#lcx-keep")
    deadline, seen, stable = time.time() + 15, -1, 0
    while time.time() < deadline:
        now = len(getattr(context, "bench_commits", None) or [])
        stable = stable + 1 if now == seen and now > 0 else 0
        if stable >= 2:
            return
        seen = now
        context.page.wait_for_timeout(300)


@then("the first of them is the lesson's seed")
def step_first_is_seed(context):
    first = context.lc_hits[0]
    assert first.get("message", "").startswith("\U0001f4c4 starter"), (
        "the first commit is not labelled as the starter: %r"
        % first.get("message"))
    assert 'source="ozaukee"' in first["text"], (
        "the starter does not hold the author's broken wire: %r"
        % first["text"][:120])


@then("the last of them wires {knob} to {value}")
def step_last_wires(context, knob, value):
    want = knob + '="' + value + '"'
    text = context.lc_hits[-1]["text"]
    assert want in text, "committed file has no %s — %r" % (want, text[:200])


@then("the repaired table is the reader's own")
def step_slot_is_mine(context):
    expect(context.page.locator(".lc-bench-slot[data-lc-mine='1']").first
           ).to_be_visible(timeout=15_000)


# ── a source= that names nothing ──────────────────────────────────────────

@given("a table gives its dataset {ms:d}ms to arrive")
def step_bind_grace(context, ms):
    # add_init_script lands before any page script, so the grid reads this
    # instead of its four-second default.
    context.page.add_init_script(
        "window.lcDatagridBindGrace = " + str(ms) + ";")


@then('the waiting table comes to rest on "{text}"')
def step_waiting_table_rests(context, text):
    err = context.page.locator(".lc-datagrid-err", has_text=text).first
    expect(err).to_be_visible(timeout=15_000)
    # and it is no longer claiming to be loading: two messages about one
    # fact is how "stuck page" reads in the first place
    assert context.page.locator(".lc-datagrid-status").count() == 0, \
        "the grid still shows 'loading grid…' beside its empty message"


@then("that message is a tappable target")
def step_message_is_tappable(context):
    # the ⚙️ that repairs the wire is aimed with a thumb; the sliver of
    # "loading grid…" it replaces was ~20px and nearly unhittable.
    box = context.page.locator(".lc-datagrid-err").first.bounding_box()
    assert box and box["height"] >= 44, \
        "the empty message is only %spx tall" % (box and box["height"])


# ── a card that shows the reader's run, not the author's claim ────────────

@given('the run on page "{path}" is remembered as "{status}"')
@when('the run on page "{path}" is remembered as "{status}"')
def step_remember_run(context, path, status):
    # Keyed exactly as feature.md files it: the page's normalised path plus
    # the Nth-.feature name. normPath is the engine's own, so the test
    # cannot drift from the key the page writes.
    context.page.evaluate(
        "([p, s]) => {"
        " var k = (window.lcPageScores ? window.lcPageScores.norm(p) : p) + '#n0';"
        " var all = JSON.parse(localStorage.getItem('lc_features') || '{}');"
        " all[k] = { status: s, ts: '' };"
        " localStorage.setItem('lc_features', JSON.stringify(all));"
        " }",
        [path, status],
    )


@then('a card shows a "{status}" feature dot')
def step_card_dot(context, status):
    expect(context.page.locator(".lc-card .lc-feat-" + status).first
           ).to_be_visible(timeout=15_000)


@then("that card is marked as remembering my run")
def step_card_remembered(context):
    expect(context.page.locator(".lc-card[data-lc-remembered]").first
           ).to_be_visible(timeout=15_000)


@then('no card claims "{status}" for that page any more')
def step_card_not_status(context, status):
    n = context.page.locator(
        ".lc-card[data-lc-remembered] .lc-feat-" + status).count()
    assert n == 0, \
        "%d remembered card(s) still showing the author's %s" % (n, status)


# ── a name that answers to nothing: a bomb, never a ghost ─────────────────

def _shift_alt_hover(page, locator):
    locator.wait_for(state="visible", timeout=20_000)
    locator.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    locator.evaluate(
        "el => { const r = el.getBoundingClientRect();"
        " el.dispatchEvent(new PointerEvent('pointermove', {altKey: true,"
        " shiftKey: true, bubbles: true, cancelable: true,"
        " clientX: r.left + r.width / 2, clientY: r.top + r.height / 2})); }"
    )
    page.wait_for_timeout(1200)


@when("I sweep the lens over the wired table")
def step_lens_wired(context):
    _shift_alt_hover(context.page, context.page.locator(".lc-datagrid").first)


@then('the lens marks "{role}" as naming nothing')
def step_lens_bomb(context, role):
    row = context.page.locator("#lcx-scene .lcx-xray .bad", has_text=role).first
    expect(row).to_be_visible(timeout=30_000)
    expect(row).to_contain_text("nothing answers to this name")


@then('the lens draws no part called "{ident}"')
def step_no_ghost(context, ident):
    # The whole point: an absent target must not be MATERIALISED. A panel
    # reading "id = ozaukee / loaded = false" tells the reader the part
    # exists and is merely empty — the exact opposite of the truth.
    ghost = context.page.evaluate(
        """(id) => [...document.querySelectorAll('#lcx-scene .lcx-xray')]
             .filter(p => p.style.display !== 'none')
             .map(p => (p.textContent || '').replace(/\\s+/g, ' '))
             .filter(t => t.includes('id = ' + id))""",
        ident,
    )
    assert not ghost, "the lens fabricated a part for %r: %r" % (ident, ghost)


@then("the lens draws no wire from it")
def step_no_wire(context):
    n = context.page.locator("#lcx-scene svg .lcx-edge").count()
    assert n == 0, "%d wire(s) drawn to a part that does not exist" % n


# ── a dataset that reads the learner's own file ───────────────────────────

@then('the dataset "{name}" holds "{text}"')
def step_dataset_holds(context, name, text):
    got = context.page.evaluate(
        "(n) => JSON.stringify((window.lcDatasets || {})[n] || null)", name)
    assert got and text in got, \
        "dataset %r does not hold %r — it holds %s" % (name, text, got)


@when("I sweep the lens over the chart")
def step_lens_chart(context):
    _shift_alt_hover(context.page, context.page.locator(".lc-chart, canvas").first)


@then('the table is showing "{text}"')
def step_table_shows(context, text):
    expect(context.page.locator(".lc-datagrid").first
           ).to_contain_text(text, timeout=20_000)


# ── 💬 the reader's margin ────────────────────────────────────────────────

@when("I open the note composer on the lesson prose")
def step_open_composer(context):
    para = context.page.locator(".lc-run p", has_text="prose here belongs").first
    _alt_move_on(context.page, para)
    gear = context.page.locator("#lcx-gear")
    gear.wait_for(state="visible", timeout=10_000)
    # the badge IS the promise: on a vault block the tap opens the margin,
    # it does not edit — a reader must know which before touching it
    assert gear.text_content() == "💬", \
        "the badge on a read-only block reads %r, not 💬" % gear.text_content()
    gear.click(force=True)
    expect(context.page.locator("#lcx-note-text")).to_be_visible(timeout=5_000)


def _keep_note(context):
    import time

    context.page.click("#lcx-note-send")
    deadline = time.time() + 10
    while time.time() < deadline and not getattr(context, "bench_commits", None):
        context.page.wait_for_timeout(200)


@when('I write the note "{text}" and keep it')
def step_write_note(context, text):
    context.page.fill("#lcx-note-text", text)
    _keep_note(context)


@when("I clear the note and keep it")
def step_clear_note(context):
    # clearing is how a note is deleted — the section goes, git remembers
    ta = context.page.locator("#lcx-note-text")
    expect(ta).not_to_have_value("", timeout=10_000)   # the prefill must land first
    ta.fill("")
    _keep_note(context)


ANCHOR = "## «The prose here belongs to the course.»"


@then("the margin holds {n:d} section for the block's own words")
@then("the margin holds {n:d} sections for the block's own words")
def step_margin_sections(context, n):
    last = context.bench_commits[-1]["text"]
    got = last.count(ANCHOR)
    assert got == n, "expected %d section(s) anchored to the block, found %d: %r" % (
        n, got, last[:300])


@then('the committed margin no longer contains "{text}"')
def step_margin_lacks(context, text):
    last = context.bench_commits[-1]["text"]
    assert text not in last, "the margin still holds %r: %r" % (text, last[:300])


@then('the note area already holds "{text}"')
def step_note_prefilled(context, text):
    # the prefill is an async bench read — expect polls until it lands
    expect(context.page.locator("#lcx-note-text")).to_have_value(text, timeout=10_000)


@when("I sweep the x-ray over the lesson prose")
def step_sweep_prose(context):
    para = context.page.locator(".lc-run p", has_text="prose here belongs").first
    _alt_move_on(context.page, para)


@then("the noted block wears the margin mark")
def step_noted_mark(context):
    """Assert the mark is VISIBLE — not merely that a class was set.

    The first version of this step checked only .lc-noted and the body
    class, and passed happily through a release where the bubble was
    positioned outside the block's box and therefore clipped away to
    nothing. A decoration nobody can see is not a decoration, so measure
    the pseudo-element: it must have a box, and that box must sit inside
    both the block and the viewport.
    """
    context.page.wait_for_selector("p.lc-noted", timeout=10_000)
    assert context.page.evaluate(
        "() => document.body.classList.contains('lc-xray-deco')"), \
        "the x-ray is looking but the decoration layer is off"
    geo = context.page.evaluate(
        """() => {
             const el = document.querySelector('p.lc-noted');
             const cs = getComputedStyle(el, '::after');
             const r = el.getBoundingClientRect();
             return { content: cs.content, right: cs.right,
                      blockRight: r.right, blockTop: r.top,
                      vw: window.innerWidth };
           }"""
    )
    assert "💬" in (geo["content"] or ""), \
        "no 💬 in the ::after content: %r" % geo["content"]
    off = float((geo["right"] or "0px").replace("px", ""))
    assert off > 0, "the mark is flush with the edge — the gear will cover it"
    # its own box must land inside the block, and so inside the viewport
    assert geo["blockRight"] - off < geo["vw"], \
        "the mark is pushed off the right of the viewport (%r)" % geo


@then("the composer offers no editor controls")
def step_composer_pure(context):
    page = context.page
    assert page.locator("#lcx-edit-body input[data-knob]").count() == 0, \
        "the composer leaked knobs onto a read-only block"
    assert page.locator("#lcx-edit-body #lcx-content").count() == 0, \
        "the composer leaked the content editor onto a read-only block"
    assert page.locator("#lcx-apply").is_hidden(), "Apply visible on a vault block"
    assert page.locator("#lcx-keep").is_hidden(), "Save visible on a vault block"
    assert page.locator("#lcx-tabs").is_hidden(), \
        "the tab back to the editor is visible on a vault block"


@when("I open the x-ray editor on the slot's text")
def step_open_editor_slot_text(context):
    para = context.page.locator(".lc-bench-slot p", has_text="Wire me").first
    _alt_move_on(context.page, para)
    gear = context.page.locator("#lcx-gear")
    gear.wait_for(state="visible", timeout=10_000)
    assert gear.text_content() == "⚙️", \
        "inside their own slot the reader OWNS the block — expected ⚙️, got %r" \
        % gear.text_content()
    gear.click(force=True)
    expect(context.page.locator("#lcx-content")).to_be_visible(timeout=5_000)


@then("the editor offers an edit tab and a notes tab")
def step_tabs_offered(context):
    expect(context.page.locator("#lcx-tabs")).to_be_visible(timeout=5_000)
    expect(context.page.locator("#lcx-tab-edit")).to_be_visible()
    expect(context.page.locator("#lcx-tab-notes")).to_be_visible()


@when("I switch to the notes tab")
def step_switch_notes_tab(context):
    context.page.click("#lcx-tab-notes")


@then("the note area is ready to write")
def step_note_area_ready(context):
    ta = context.page.locator("#lcx-note-text")
    expect(ta).to_be_visible(timeout=5_000)
    expect(ta).to_be_editable()


# ── folder parent="true": the way out ─────────────────────────────────────

@then("a way up to the folder above is offered")
def step_way_up(context):
    up = context.page.locator(".lc-folder-up a").first
    expect(up).to_be_visible(timeout=20_000)
    # it must climb ONE level: the lesson is in courses/demo/mod, so up is
    # courses/demo — never the folder the reader is already standing in
    href = up.get_attribute("href") or ""
    assert "courses/demo/index.md" in href, \
        "the way up points at %r, not the folder above" % href
    assert "/mod/" not in href.split("courses/demo")[-1], \
        "the way up leads back into the same folder: %r" % href


@then("the way up is not a card in the grid")
def step_way_up_not_a_card(context):
    # it is navigation, not a sibling — it must sit outside .lc-cards
    n = context.page.locator(".lc-cards .lc-folder-up").count()
    assert n == 0, "the way up was rendered inside the card grid"
    expect(context.page.locator(".lc-folder-up")).to_have_count(1)
