"""The mechanics module 02's flow lesson stands on.

Proven here before a word of the lesson exists, because the failure mode is
silent: a condition that never fires leaves a step shut for ever, the proof
goes red, and the learner is told they made a mistake they did not make.
"""
from behave import when, then
from playwright.sync_api import expect


def _vis(context, sid):
    """Rendered visibility, the way the lesson's own proof will read it —
    Object.visible in steps_runtime asks getComputedStyle, and that is exactly
    how the cells engine hides a block (display:none until .lc-vis-show)."""
    return context.page.evaluate(
        """(sid) => {
             const el = document.querySelector("[data-lc-id='" + sid + "']")
                     || document.getElementById(sid);
             if (!el) return "MISSING";
             const cs = getComputedStyle(el);
             return (cs.display !== "none" && cs.visibility !== "hidden")
                    ? "open" : "shut";
           }""", sid)


@when("I wait for the cells to settle")
def step_cells_settle(context):
    # the first recompute needs the page's Python runtime to boot, so poll for
    # a decision rather than sleeping a guessed number of seconds
    # wait for ANY upgraded component, not one page's form — page 3 has no #ask
    context.page.wait_for_function(
        """() => !!document.querySelector('[data-lc-id]')""", timeout=40_000)
    context.page.wait_for_timeout(2500)


@then('the step "{sid}" is open')
def step_open(context, sid):
    got = _vis(context, sid)
    assert got == "open", 'step %r is %s, expected open' % (sid, got)


@then('the step "{sid}" is shut')
def step_shut(context, sid):
    got = _vis(context, sid)
    assert got == "shut", 'step %r is %s, expected shut' % (sid, got)


@when('I type "{text}" into the step "{sid}"')
def step_type(context, text, sid):
    """A form is an AG Grid of key/value cells, not a page of <input>s — the
    value cell is a div until you double-click it. Typing straight into the DOM
    found nothing and silently changed nothing, which made an earlier version
    of these scenarios pass for the wrong reason. Drive it the way a learner
    does: double-click the value, type, commit with Enter.
    """
    form = context.page.locator("[data-lc-id='%s']" % sid)
    form.wait_for(state="visible", timeout=20_000)
    # column 2 is the value; column 1 holds the field name
    cell = form.locator(".ag-cell").nth(1)
    cell.wait_for(state="visible", timeout=20_000)
    cell.dblclick()
    editor = form.locator('input[type="text"]').first
    editor.wait_for(state="visible", timeout=10_000)
    editor.fill(text)
    editor.press("Enter")
    context.page.wait_for_timeout(2500)      # lc-model-changed -> recompute


@then('dump the fields of "{sid}"')
def step_dump_fields(context, sid):
    html = context.page.evaluate(
        """(sid) => {
             const f = document.querySelector("[data-lc-id='" + sid + "']");
             if (!f) return "MISSING";
             const b = f.querySelector(".lc-form-body") || f;
             return b.innerHTML.replace(/\\s+/g, " ").slice(0, 900);
           }""", sid)
    print("\n---- fields of %s ----\n%s\n" % (sid, html))


# ── the lesson's own proof, run against the real file ─────────────────────
# Serving the repo file through the gh: stub means the scenario tests the
# LESSON, not a copy of it that can drift away from it.

def _serve_course_page(context, path, transform=None):
    """Serve a REAL lesson file through the gh: stub, so these scenarios test
    the lesson and not a copy that can drift from it.

    THE SUITE ALSO RUNS IN PEDIA, which publishes the engine and carries no
    courses/ folder — so the file simply is not there, and four scenarios blew
    up with FileNotFoundError against a perfectly healthy engine (2026-08-07:
    326 passed, 4 failed, all of them mine). Content lives in the lab; stand
    aside anywhere else rather than failing.
    """
    import os

    if not os.path.isfile(path):
        context.scenario.skip("%s is not in this repo — course content lives "
                              "in the lab, the engine is published here" % path)
        return
    with open(path, encoding="utf-8") as f:
        body = f.read()
    if transform:
        body = transform(body)
    context.lesson_body = body

    def fulfill(route):
        route.fulfill(status=200, content_type="text/plain; charset=utf-8",
                      body=context.lesson_body)
    context.page.route("**/api.github.com/repos/**/contents/" + path + "*", fulfill)
    context.page.route("**/raw.githubusercontent.com/**/" + path + "*", fulfill)


@given('the runner serves the course page "{path}"')
def step_serve_course(context, path):
    context.lesson_path = path
    _serve_course_page(context, path)


@given("the learner has changed card 3 to follow the visit")
def step_apply_fix(context):
    """The one edit the lesson asks for. If this string ever stops matching the
    page, the scenario fails loudly rather than testing nothing."""
    def fix(body):
        broken = 'title="3️⃣ Home — the fee" visible="= ask.dog"'
        fixed = 'title="3️⃣ Home — the fee" visible="= meet.when"'
        assert broken in body, "card 3 no longer carries the knob the lesson asks to change"
        return body.replace(broken, fixed)
    _serve_course_page(context, context.lesson_path, fix)


@given("the learner has finished the welcome and turned its link into a button")
def step_first_screen_fix(context):
    """Module 04's first beat, both edits the page asks for: a finished title
    and `{: .button }` under the link. Loud if the seed drifts."""
    def fix(body):
        title, link = "# 🐾 Welcome to …", "[wihumane.org](https://www.wihumane.org)\n"
        assert title in body and link in body, "the welcome seed no longer carries the title or the link the lesson asks to change"
        return body.replace(title, "# 🐾 Welcome to the shelter") \
                   .replace(link, link + "{: .button }\n")
    _serve_course_page(context, context.lesson_path, fix)


@given("the learner has given the dog pile a table")
def step_dogs_fix(context):
    """Module 04's second screen: the two lines under the pile's dataset
    decoration that give it a face. Loud if the seed drifts."""
    def fix(body):
        line = '[dogs](../module_00/dogs.yaml)\n{: .dataset #dogs }\n'
        assert line in body, "the dogs seed no longer carries the dataset line the lesson builds on"
        return body.replace(line, line + '\n[The dogs](#)\n{: .datagrid source="dogs" }\n')
    _serve_course_page(context, context.lesson_path, fix)


@given('the runner serves the course file "{path}"')
def step_serve_course_file(context, path):
    """A file BESIDE the lesson (a dataset's own yaml) — its own closure, so
    the lesson's body and the file's never share one variable."""
    import os
    if not os.path.isfile(path):
        context.scenario.skip("%s is not in this repo — course content lives in the lab" % path)
        return
    with open(path, encoding="utf-8") as f:
        body = f.read()

    def fulfill(route):
        route.fulfill(status=200, content_type="text/plain; charset=utf-8", body=body)
    context.page.route("**/api.github.com/repos/**/contents/" + path + "*", fulfill)
    context.page.route("**/raw.githubusercontent.com/**/" + path + "*", fulfill)


@given("the learner has given the pile a card and a chart")
def step_faces_fix(context):
    def fix(body):
        line = '{: .datagrid #dog_grid source="dogs" rows="5" }\n'
        assert line in body, "the faces seed no longer carries the named table the lesson builds on"
        card = '{: .form master="dog_grid" compute="photo = f\'https://placedog.net/400/240?id={pic}\'" }\n'
        return body.replace(line, line + '\n[The dog](#)\n' + card +
                                         '\n[Fees](#)\n{: .chart source="dogs" x="name" y="fee" }\n')
    _serve_course_page(context, context.lesson_path, fix)


@given("the learner has written the chart's beat")
def step_beat_fix(context):
    def fix(body):
        seed = "- user: …\n- ui: …\n- command: …\n- event: …\n"
        assert seed in body, "the beat seed no longer carries the four dotted notes"
        return body.replace(seed, "- user: The coordinator\n- ui: the fees chart\n"
                                  "- command: Compare the fees\n- event: The dearest dog is known\n")
    _serve_course_page(context, context.lesson_path, fix)


@then("the story pad stacks its preview above its source")
def step_pad_rows(context):
    """layout="rows": a landscape document gets the whole width."""
    pad = context.page.locator("[data-lc-id='my_beat'].lc-mdpad.lc-mdpad-rows")
    pad.wait_for(state="attached", timeout=20_000)
    assert context.page.evaluate(
        "() => getComputedStyle(document.querySelector(\"[data-lc-id='my_beat'].lc-mdpad\")).flexDirection") == "column"


@then('the pad\'s preview wears app chrome titled "{title}"')
def step_app_chrome(context, title):
    """A saved AND decorated pad is a page of the learner's app: its preview
    carries a title bar that mirrors the page's own # line."""
    head = context.page.locator(".lc-mdpad-out.lc-mdpad-app .lc-mdpad-apptitle").first
    head.wait_for(state="attached", timeout=20_000)
    expect(head).to_contain_text(title, timeout=10_000)


@when("I run the lesson's proof")
def step_run_proof(context):
    card = context.page.locator(".lc-feature").first
    card.wait_for(state="attached", timeout=30_000)
    # A lesson page partitions into SLIDES inside the runner, so the proof sits
    # on an inactive one and its ▶ is hidden. Reveal every slide (and any
    # visible= gate on the card itself) before reaching for the button.
    context.page.evaluate(
        """() => {
             // The lesson's own {: .prerequisite } locks every block after it
             // until the previous page is done, and a fresh test browser has
             // finished nothing. It re-applies lc-prereq-hidden on rescan, so
             // strip the gate itself — rt_prereq.feature owns that behaviour,
             // these scenarios own the proof.
             document.querySelectorAll('.lc-prereq').forEach(g => g.remove());
             document.querySelectorAll('.lc-prereq-hidden')
                     .forEach(h => h.classList.remove('lc-prereq-hidden'));
             document.querySelectorAll('.lc-slide').forEach(s => {
               s.removeAttribute('hidden');
               s.style.display = 'block';
               s.setAttribute('data-active', 'true');
             });
             document.querySelectorAll('.lc-feature').forEach(c => {
               c.classList.remove('lc-feature-hidden');
               c.style.display = 'block';
             });
           }""")
    context.page.wait_for_timeout(400)
    btn = card.locator(".lc-feature-run").first
    btn.wait_for(state="visible", timeout=30_000)
    btn.scroll_into_view_if_needed(timeout=10_000)
    btn.click(timeout=20_000)


def _status(context, want):
    """Assert on the card's own data-status, not on a badge being visible.
    data-status IS the engine's signal — cells.md reads it to publish a
    feature's `passing` into the page's scopes — and it does not depend on the
    badge having layout, which inside a revealed slide it may not.
    """
    import time

    card = context.page.locator(".lc-feature").first
    card.wait_for(state="attached", timeout=30_000)
    deadline, got = time.time() + 90, ""
    while time.time() < deadline:
        got = card.get_attribute("data-status") or ""
        if got in ("passing", "failing"):
            break
        context.page.wait_for_timeout(500)
    if got != want:
        raise AssertionError(
            "proof status is %r, expected %r — the card says:\n%s"
            % (got, want, (card.inner_text() or "")[:900]))


@then("the lesson's proof is red")
def step_proof_red(context):
    _status(context, "failing")


@then("the lesson's proof is green")
def step_proof_green(context):
    _status(context, "passing")


@when("dump why the run button hides")
def step_dump_hidden(context):
    import json
    info = context.page.evaluate(
        """() => {
             const b = document.querySelector('.lc-feature-run');
             if (!b) return "no button";
             const chain = [];
             let el = b;
             while (el && el !== document.documentElement) {
               const cs = getComputedStyle(el);
               chain.push({
                 tag: el.tagName.toLowerCase() + (el.id ? "#" + el.id : ""),
                 cls: (el.className || "").toString().slice(0, 90),
                 display: cs.display, visibility: cs.visibility,
                 hidden: el.hasAttribute("hidden"),
                 vis: el.getAttribute("visible"),
                 h: el.getBoundingClientRect().height
               });
               el = el.parentElement;
             }
             return { body: document.body.className, chain: chain };
           }""")
    print("\n---- why hidden ----\n" + json.dumps(info, indent=1)[:2200] + "\n")


@given("the learner has pointed the middle line at the visited query")
def step_fix_stat_bind(context):
    def fix(body):
        broken = "🐕 **{= reservations.count }** met a dog."
        fixed = "🐕 **{= visited.count }** met a dog."
        assert broken in body, "the middle line no longer carries the formula the lesson asks to change"
        return body.replace(broken, fixed)
    _serve_course_page(context, context.lesson_path, fix)


@then("report why the gate did not reopen")
def step_cell_err(context):
    info = context.page.evaluate(
        """() => {
             const vis = () => {
               const el = document.querySelector("[data-lc-id='home']");
               return el ? getComputedStyle(el).display : "MISSING";
             };
             const before = vis();
             const ret = window.lcFormSet ? window.lcFormSet("meet", "when", "Thu") : "NO lcFormSet";
             return { before: before, lcFormSet_returned: ret, afterSync: vis(),
                      err: window._lcCellErr || null };
           }""")
    print("\n---- cells diagnostic ----\n%r\n" % info)


@then('the tally reads "{want}"')
def step_tally(context, want):
    import time

    deadline, got = time.time() + 30, ""
    while time.time() < deadline:
        got = context.page.evaluate(
            """() => { const el = document.getElementById('tally');
                       return el ? el.textContent.replace(/\\s+/g,' ').trim() : 'MISSING'; }""")
        if got == want:
            return
        context.page.wait_for_timeout(500)
    raise AssertionError("the tally reads %r, expected %r" % (got, want))


@given('"{path}" answers {secs:d} seconds late with {n:d} rows')
def step_late_csv(context, path, secs, n):
    """a table that lands after the cells' first paint — the handler sleeps,
    the page keeps rendering, the count arrives late"""
    import time
    body = "name\n" + "\n".join("row%d" % i for i in range(n)) + "\n"

    def slow(route):
        time.sleep(secs)
        route.fulfill(status=200, content_type="text/csv", body=body)

    context.page.route("**" + path + "*", slow)


@when("a family clicks the first dog in the pad's table")
def step_click_pad_dog(context):
    """The pad's own table — a dataset-bound grid is the light table of
    dataset.md (plain <tr>s, not AG rows). The first dog, clicked as a family
    would; the slides revealed first, as the proof step does."""
    context.page.evaluate(
        """() => {
             document.querySelectorAll('.lc-prereq').forEach(g => g.remove());
             document.querySelectorAll('.lc-prereq-hidden').forEach(h => h.classList.remove('lc-prereq-hidden'));
             document.querySelectorAll('.lc-slide').forEach(s => {
               s.removeAttribute('hidden'); s.style.display = 'block'; s.setAttribute('data-active', 'true');
             });
           }""")
    row = context.page.locator(
        "[data-lc-id='faces_screen'] .lc-datagrid[data-lc-id='dog_grid'] tbody tr").first
    row.wait_for(state="visible", timeout=30_000)
    row.click()
    context.page.wait_for_timeout(3000)      # the bus -> the card, and the formula's first run


@then("the card shows that dog's photo")
def step_card_photo(context):
    """A photo the CARD computed (compute= on the form): an <img> from the
    pictures site, while the table it follows still shows its own columns."""
    img = context.page.locator("[data-lc-id='faces_screen'] .lc-form img[src*='placedog']").first
    try:
        img.wait_for(state="attached", timeout=15_000)
    except Exception:
        info = context.page.evaluate(
            """() => {
                 const pad = document.querySelector("[data-lc-id='faces_screen']");
                 const f = pad && pad.querySelector(".lc-form");
                 return f ? (f.querySelector('.lc-form-body') || f).innerText.replace(/\\s+/g, ' ').slice(0, 400) : "NO FORM";
               }""")
        raise AssertionError("the card shows no photo — the card reads: %r" % (info,))
    heads = context.page.locator(
        "[data-lc-id='faces_screen'] .lc-datagrid[data-lc-id='dog_grid'] th").all_inner_texts()
    assert not any("photo" in h.lower() for h in heads), \
        "the table grew a photo column — the card computes, the list stays a list: %r" % (heads,)


@when("the learner types the card under the table, compute= on it")
def step_type_card(context):
    """The learner's own path — the lines typed into the pad's source, the
    preview re-rendering live — not a file served with the lines already in.
    No click afterwards: the table publishes its first row when it paints,
    and a card subscribing later receives that row (Michel, 2026-10-06:
    'the form has still no picture')."""
    context.page.evaluate(
        """() => {
             document.querySelectorAll('.lc-prereq').forEach(g => g.remove());
             document.querySelectorAll('.lc-prereq-hidden').forEach(h => h.classList.remove('lc-prereq-hidden'));
             document.querySelectorAll('.lc-slide').forEach(s => {
               s.removeAttribute('hidden'); s.style.display = 'block'; s.setAttribute('data-active', 'true');
             });
           }""")
    ta = context.page.locator("[data-lc-id='faces_screen'] .lc-mdpad-in")
    ta.wait_for(state="visible", timeout=20_000)
    card = ('\n[The dog](#)\n{: .form master="dog_grid" '
            'compute="photo = f\'https://placedog.net/400/240?id={pic}\'" }\n')
    ta.fill(ta.input_value().rstrip("\n") + "\n" + card)
    context.page.wait_for_timeout(4000)      # debounce, re-render, the formula's run


@when("the learner types the plain card under the table")
def step_type_plain_card(context):
    """Step one of the lesson: master= only. The card follows, shows the
    pic NUMBER, and has no face yet — the beat the next step answers."""
    context.page.evaluate(
        """() => {
             document.querySelectorAll('.lc-prereq').forEach(g => g.remove());
             document.querySelectorAll('.lc-prereq-hidden').forEach(h => h.classList.remove('lc-prereq-hidden'));
             document.querySelectorAll('.lc-slide').forEach(s => {
               s.removeAttribute('hidden'); s.style.display = 'block'; s.setAttribute('data-active', 'true');
             });
           }""")
    ta = context.page.locator("[data-lc-id='faces_screen'] .lc-mdpad-in")
    ta.wait_for(state="visible", timeout=20_000)
    ta.fill(ta.input_value().rstrip("\n") + '\n\n[The dog](#)\n{: .form master="dog_grid" }\n')
    context.page.wait_for_timeout(3000)


@then("the card shows the pic number and no face")
def step_card_number(context):
    form = context.page.locator("[data-lc-id='faces_screen'] .lc-form").first
    form.wait_for(state="attached", timeout=15_000)
    text = form.inner_text()
    assert "101" in text, "the card does not show the first dog's pic number: %r" % text[:300]
    assert form.locator("img").count() == 0, "the plain card already wears a picture — the lesson's second step has nothing left to teach"


@when('I run the lesson\'s check "{fid}"')
def step_run_named_check(context, fid):
    """A named card — a page may carry a Definition of Done beside its proof."""
    context.page.evaluate(
        """() => {
             document.querySelectorAll('.lc-prereq').forEach(g => g.remove());
             document.querySelectorAll('.lc-prereq-hidden').forEach(h => h.classList.remove('lc-prereq-hidden'));
             document.querySelectorAll('.lc-slide').forEach(s => { s.removeAttribute('hidden'); s.style.display = 'block'; s.setAttribute('data-active', 'true'); });
             document.querySelectorAll('.lc-feature').forEach(c => { c.classList.remove('lc-feature-hidden'); c.style.display = 'block'; });
           }""")
    card = context.page.locator('.lc-feature[data-lc-id="' + fid + '"]').first
    card.wait_for(state="attached", timeout=30_000)
    btn = card.locator(".lc-feature-run").first
    btn.wait_for(state="visible", timeout=30_000)
    btn.scroll_into_view_if_needed(timeout=10_000)
    btn.click(timeout=20_000)


def _named_status(context, fid, want):
    import time
    card = context.page.locator('.lc-feature[data-lc-id="' + fid + '"]').first
    deadline, got = time.time() + 90, ""
    while time.time() < deadline:
        got = card.get_attribute("data-status") or ""
        if got in ("passing", "failing"):
            break
        context.page.wait_for_timeout(500)
    if got != want:
        raise AssertionError("check %s is %r, expected %r — the card says:\n%s" % (fid, got, want, (card.inner_text() or "")[:900]))


@then('the lesson\'s check "{fid}" is green')
def step_named_green(context, fid):
    _named_status(context, fid, "passing")


@then('the lesson\'s check "{fid}" is red')
def step_named_red(context, fid):
    _named_status(context, fid, "failing")


# ── Module 05 in the pad (Michel, 2026-10-09) ────────────────────────────
M05_CHECK = (
    "```gherkin\n"
    "Feature: Only families still waiting get a call\n"
    "  Scenario: Nobody who already met their dog is in the list\n"
    "    Given the list my page builds\n"
    "    :::python\n"
    "    self.list: Query = self.page.to_call\n"
    "    :::\n"
    "    When the coordinator reads it\n"
    "    Then every family in it is still waiting\n"
    "    :::python\n"
    "    met: list[str] = [m for m in self.list.values(\"met\") if m]\n"
    "    assert not met, f\"{len(met)} families already met their dog\"\n"
    "    :::\n"
    "```\n"
    "{: .feature #call_check visible=\"true\" }\n")


@given("the learner has added the datagrid and the button")
def step_builder_fix(context):
    """Module 05's playground: the two catalogue components under their
    items, placeholder swapped, items ticked. Loud if the seed drifts."""
    def fix(body):
        items = ("- [ ] a datagrid of the families waiting\n"
                 "- [ ] a button to call the next family\n")
        assert items in body, "the playground seed no longer carries its two checklist items"
        return body.replace(items,
            "- [x] a datagrid of the families waiting\n\n"
            "[Families](#)\n{: .datagrid source=\"reservations\" }\n\n"
            "- [x] a button to call the next family\n\n"
            "[📞 Call the next family](#)\n{: .button #call_btn }\n")
    _serve_course_page(context, context.lesson_path, fix)


M05_LIST_ITEMS = ("- [ ] a query: the families to call\n"
                  "- [ ] a datagrid on its answer\n"
                  "- [ ] a line that counts them\n"
                  "- [ ] a form: the next family to call\n"
                  "- [ ] a button that calls them, one after the other\n")

M05_APP = ("```sql\nSELECT family, dog, asked, met FROM reservations\n```\n"
           "{: .query bind=\"reservations\" #to_call }\n\n"
           "[Families to call](#)\n{: .datagrid #call_list source=\"to_call\" }\n\n"
           "{= to_call.count } families are waiting.\n\n"
           "[Next family](#)\n{: .form #next_family master=\"call_list\" title=\"📞 Next family\" }\n\n"
           "[📞 Call the next family](#)\n{: .button #call_btn }\n"
           "```python\n"
           "family = button.page.next_family.data.family\n"
           "names = button.page.to_call.values(\"family\")\n"
           "button.text = \"✅ \" + family + \" called\"\n"
           "button.page.call_list.select(names.index(family) + 2)\n"
           "```\n{: .onclick }\n")


@given("the learner has built the follow-up app")
def step_list_fix(context):
    """Module 05's real page: the lesson's own lines, the items ticked."""
    def fix(body):
        assert M05_LIST_ITEMS in body, "the follow-up seed no longer carries the five checklist items"
        return body.replace(M05_LIST_ITEMS, M05_LIST_ITEMS.replace("- [ ]", "- [x]") + "\n" + M05_APP)
    _serve_course_page(context, context.lesson_path, fix)


@given("the learner has built the follow-up app with the datagrid's decoration alone")
def step_list_fix_lone(context):
    """Michel's pad, 2026-10-09: the datagrid's decoration alone after a blank
    line lands on the query before it — the query becomes a grid of every
    reservation and the proof finds no query. The proof must say why."""
    def fix(body):
        assert M05_LIST_ITEMS in body, "the follow-up seed no longer carries the five checklist items"
        app = M05_APP.replace("[Families to call](#)\n{: .datagrid", "\n{: .datagrid")
        return body.replace(M05_LIST_ITEMS, M05_LIST_ITEMS.replace("- [ ]", "- [x]") + "\n" + app)
    _serve_course_page(context, context.lesson_path, fix)


@then('the lesson\'s check "{fid}" says "{text}"')
def step_named_says(context, fid, text):
    card = context.page.locator('.lc-feature[data-lc-id="' + fid + '"]').first
    expect(card).to_contain_text(text, timeout=20_000)


@then('the pad\'s preview reads "{text}"')
def step_pad_reads(context, text):
    out = context.page.locator(".lc-mdpad-out").first
    out.wait_for(state="attached", timeout=20_000)
    expect(out).to_contain_text(text, timeout=10_000)


@given("the learner has written the check at the bottom of the page")
def step_proof_check(context):
    """The check from the lesson, typed at the end of the learner's page —
    inside the pad, where it runs."""
    def fix(body):
        tail = "{: .onclick }\n`````\n"
        assert tail in body, "the proof seed no longer ends with the button's onclick"
        return body.replace(tail, "{: .onclick }\n\n" + M05_CHECK + "`````\n", 1)
    _serve_course_page(context, context.lesson_path, fix)


def _pad_textarea(context):
    ta = context.page.locator(".lc-mdpad .lc-mdpad-in").first
    ta.wait_for(state="attached", timeout=20_000)
    return ta


@when("the learner runs the check inside the pad")
def step_run_inner_check(context):
    card = context.page.locator('.lc-mdpad-out .lc-feature[data-lc-id="call_check"]').first
    card.wait_for(state="attached", timeout=30_000)
    btn = card.locator(".lc-feature-run").first
    btn.wait_for(state="visible", timeout=30_000)
    btn.scroll_into_view_if_needed(timeout=10_000)
    btn.click(timeout=20_000)


def _inner_status(context, want):
    import time
    card = context.page.locator('.lc-mdpad-out .lc-feature[data-lc-id="call_check"]').first
    deadline, got = time.time() + 90, ""
    while time.time() < deadline:
        got = card.get_attribute("data-status") or ""
        if got in ("passing", "failing"):
            break
        context.page.wait_for_timeout(500)
    if got != want:
        raise AssertionError("the check inside the pad is %r, expected %r — the card says:\n%s"
                             % (got, want, (card.inner_text() or "")[:900]))


@then("the check inside the pad is red")
def step_inner_red(context):
    _inner_status(context, "failing")


@then("the check inside the pad is green")
def step_inner_green(context):
    _inner_status(context, "passing")


@when("the learner fixes the question with WHERE met = ''")
def step_fix_question(context):
    """Four words in the query, typed in the pad's text side; the preview
    re-renders and the cell recounts."""
    ta = _pad_textarea(context)
    old = "SELECT family, dog, asked, met FROM reservations\n"
    text = ta.input_value()
    assert old in text, "the pad no longer carries the question the lesson asks to fix"
    context.page.evaluate(
        """([sel, t]) => { const ta = document.querySelector(sel); ta.focus(); ta.select();
                          document.execCommand('insertText', false, t); }""",
        [".lc-mdpad .lc-mdpad-in", text.replace(old, "SELECT family, dog, asked, met FROM reservations WHERE met = ''\n")])
    context.page.wait_for_timeout(1500)


@given("the learner has built an app of their own")
def step_own_app_fix(context):
    """Module 05's closing pad: a purpose line and the five items, the
    lesson's own vocabulary, ticked."""
    def fix(body):
        purpose = "(one sentence: what this app does, and for whom)\n"
        items = ("- [ ] a dataset of your own\n"
                 "- [ ] a datagrid on it\n"
                 "- [ ] a line that counts something\n"
                 "- [ ] a button with a job\n"
                 "- [ ] a check that goes red before it goes green\n")
        assert purpose in body and items in body, "the own-app seed no longer carries its purpose line and five items"
        return body.replace(purpose, "Who has paid the club dues, for the treasurer.\n").replace(items,
            "- [x] a dataset of your own\n\n"
            "```\nmember,paid\nAva,yes\nBen,\n```\n{: .dataset #members }\n\n"
            "- [x] a datagrid on it\n\n"
            "[Members](#)\n{: .datagrid #member_grid source=\"members\" }\n\n"
            "- [x] a line that counts something\n\n"
            "{= members.count } members.\n\n"
            "- [x] a button with a job\n\n"
            "[💸 Remind](#)\n{: .button #remind_btn }\n```python\nbutton.text = \"✅ Reminded\"\n```\n{: .onclick }\n\n"
            "- [x] a check that goes red before it goes green\n\n"
            "```gherkin\nFeature: The list shows members\n  Scenario: Rows are there\n    Given my page\n    :::python\n"
            "    self.grid: Datagrid = self.page.member_grid\n    :::\n    When the treasurer opens it\n    Then it shows rows\n    :::python\n"
            "    assert self.grid.rows, \"no rows yet\"\n    :::\n```\n{: .feature #my_check visible=\"true\" }\n")
    _serve_course_page(context, context.lesson_path, fix)


@when("the coordinator presses the call button {n:d} times")
def step_press_call(context, n):
    """The real button, as a person presses it: the form repaints a moment
    after each press (its row is derived asynchronously), so wait between."""
    btn = context.page.locator('.lc-mdpad-out [data-lc-id="call_btn"]').first
    btn.wait_for(state="attached", timeout=30_000)
    for _ in range(n):
        context.page.wait_for_timeout(800)
        btn.evaluate("e => e.click()")
    context.page.wait_for_timeout(1500)


@then('the form names "{family}"')
def step_form_names(context, family):
    import json
    form = context.page.locator('.lc-mdpad-out [data-lc-id="next_family"]').first
    got = json.loads(form.get_attribute("data-lc-value") or "{}").get("family")
    assert got == family, "the form names %r, expected %r" % (got, family)
