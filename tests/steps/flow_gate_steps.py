"""The mechanics module 02's flow lesson stands on.

Proven here before a word of the lesson exists, because the failure mode is
silent: a condition that never fires leaves a step shut for ever, the proof
goes red, and the learner is told they made a mistake they did not make.
"""
from behave import when, then


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
