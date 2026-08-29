import json

from behave import given, then, when
from playwright.sync_api import expect

# bound= regression net: the legacy editor binding is pinned by asserting on
# the REQUEST the agent sends (the augmented prompt must carry the editor's
# code) and on the Apply write-back. The expression form asserts the same
# request now carries the evaluated cell value instead.


@given('the recording model endpoint replies with a python fix "{code}"')
def step_recording_model(context, code):
    context.model_asks = []

    def fulfill(route):
        try:
            context.model_asks.append(route.request.post_data or "")
        except Exception:
            context.model_asks.append("")
        body = json.dumps({
            "choices": [{"message": {
                "content": "Try this:\n\n```python\n" + code + "\n```"}}],
            "usage": {"total_tokens": 7},
        })
        route.fulfill(status=200, content_type="application/json", body=body)

    context.page.route("**/chat/completions*", fulfill)


@when('I ask the "{agent_id}" agent "{prompt}"')
def step_ask_named_agent(context, agent_id, prompt):
    panel = context.page.locator('[data-lc-id="' + agent_id + '"]')
    panel.wait_for(state="attached", timeout=20_000)
    before = panel.locator(".lc-agent-log-entry").count()
    panel.locator(".lc-agent-prompt").fill(prompt)
    panel.locator(".lc-agent-send").click()
    # the visible panel is single-shot; the sitting's ledger appends
    expect(panel.locator(".lc-agent-log-entry")).to_have_count(
        before + 1, timeout=20_000)


@then('the model request carried the editor code "{snippet}"')
def step_request_carried(context, snippet):
    assert context.model_asks, "no model request was recorded"
    assert snippet in context.model_asks[-1], context.model_asks[-1][:600]


@when("I apply the agent's fix")
def step_apply_fix(context):
    btn = context.page.locator(".lc-agent-apply").first
    btn.wait_for(state="visible", timeout=10_000)
    btn.click()


@then('the "{run_id}" editor now holds "{code}"')
def step_editor_holds(context, run_id, code):
    ta = context.page.locator("#lc-pyrun-" + run_id + " .lc-pyrun-code")
    expect(ta).to_have_value(code, timeout=10_000)


@given('the model endpoint rejects with an array-wrapped 404 saying "{message}"')
def step_stub_array_error(context, message):
    body = json.dumps([{"error": {"code": 404, "message": message,
                                  "status": "NOT_FOUND"}}])
    context.page.route(
        "**/chat/completions*",
        lambda r: r.fulfill(status=404, content_type="application/json",
                            body=body))


@then('the desk relays "{message}"')
def step_desk_relays(context, message):
    status = context.page.locator('[data-lc-id="desk"] .lc-agent-status')
    expect(status).to_contain_text(message, timeout=15_000)


@given("this browser already spent AI energy today")
def step_energy_spent_today(context):
    """The day-quota verdict is believed only when OUR meter agrees —
    seed the meter so the wall is real, not a suspected spike."""
    context.page.add_init_script(
        "localStorage.setItem('lc_tokens', JSON.stringify("
        "{day: new Date().toISOString().slice(0,10), tokens: 1200, asks: 3}));")


@given('the model endpoint answers 429 saying "{message}"')
def step_stub_429(context, message):
    body = json.dumps([{"error": {"code": 429, "message": message,
                                  "status": "RESOURCE_EXHAUSTED"}}])
    context.page.route(
        "**/chat/completions*",
        lambda r: r.fulfill(status=429, content_type="application/json",
                            body=body))


# ── the energy key's life on a device ────────────────────────────────────
# Michel, 2026-08-05: the key had to be pasted again after every refresh.
# Storage was never the problem — three paths THREW A VALID KEY AWAY:
# a 403 at any desk, a 403 at the join door, and the door's network catch.
# These pin the survival rules, because a discarded key is invisible until
# a learner is asked for it again.

KEY_SLOT = "lc_ai_key_gemini"


@given('an energy key "{key}" is already saved on this device')
def step_key_preinstalled(context, key):
    context.page.add_init_script(
        "localStorage.setItem(%s, %s);" % (json.dumps(KEY_SLOT), json.dumps(key))
    )


@given('the model endpoint answers with status {status:d} saying "{message}"')
def step_stub_status(context, status, message):
    body = json.dumps([{"error": {"code": status, "message": message}}])
    context.page.route(
        "**/chat/completions*",
        lambda r: r.fulfill(status=status, content_type="application/json",
                            body=body))


@then("the energy key is still saved on this device")
def step_key_kept(context):
    # poll: the wipe happened inside the ask's promise chain, so a bare read
    # could pass simply by looking too early
    context.page.wait_for_timeout(700)
    got = context.page.evaluate("k => localStorage.getItem(k)", KEY_SLOT)
    assert got, "the key was thrown away — a 403 says nothing about the key itself"


@then("the energy key is gone from this device")
def step_key_dropped(context):
    context.page.wait_for_function(
        "k => localStorage.getItem(k) === null", arg=KEY_SLOT, timeout=15_000)


@then("the desk is still connected")
def step_desk_connected(context):
    panel = context.page.locator('[data-lc-id="desk"]')
    expect(panel.locator(".lc-agent-body")).to_be_visible(timeout=15_000)
    expect(panel.locator(".lc-agent-auth")).to_be_hidden(timeout=5_000)


@then("every desk on the page is connected")
def step_all_desks_connected(context):
    panels = context.page.locator(".lc-agent")
    n = panels.count()
    assert n, "no agent panel rendered"
    for i in range(n):
        expect(panels.nth(i).locator(".lc-agent-body")).to_be_visible(timeout=15_000)


@then('the desk asks for a key and explains "{needle}"')
def step_desk_asks_with_reason(context, needle):
    panel = context.page.locator('[data-lc-id="desk"]')
    expect(panel.locator(".lc-agent-auth")).to_be_visible(timeout=15_000)
    # the reason must be ON THE FORM: the chat status line it used to be
    # written to is hidden the moment the key is dropped
    msg = panel.locator(".lc-agent-authmsg")
    expect(msg).to_be_visible(timeout=10_000)
    expect(msg).to_contain_text(needle, timeout=5_000)


@then("course material for a tutor keeps the question and drops the answer")
def step_redaction(context):
    """Every page a tutor reads goes through this rule before it is sent. The
    options survive stripped of their [x]; the note that explains them does
    not, because that note IS the answer in prose."""
    out = context.page.evaluate(
        """() => window.lcRedactAnswers([
             '**Q:** Which part decides whether a card shows?',
             '',
             '- [ ] A form.',
             '- [x] A gate.',
             '- [ ] A query.',
             '',
             '  > The gate reads the date and opens the card.',
             '{: .quiz #which_quiz }'
           ].join('\\n'))""")
    assert out is not None, "the redaction rule is not exposed"
    assert "[x]" not in out and "[X]" not in out, out
    assert "The gate reads the date" not in out, out
    assert "Which part decides" in out, out
    assert "A gate." in out, out


@then("the day's ledger counted {n:d} question")
def step_ledger_count(context, n):
    got = context.page.evaluate("() => window.lcTokens && window.lcTokens.today()")
    assert got, "no ledger"
    assert got["asks"] == n, got
    assert got["tokens"] > 0, got


@then("the ledger's sentence warns that the free key is limited")
def step_ledger_line(context):
    line = context.page.evaluate("() => window.lcTokens.line()")
    assert "token" in line.lower(), line
    assert "limited" in line.lower(), line


@given('the model endpoint 503s once, then answers "{message}"')
def step_stub_503_then_ok(context, message):
    """A demand spike: the first call wobbles, the next one works."""
    state = {"n": 0}

    def fulfill(route):
        state["n"] += 1
        if state["n"] == 1:
            route.fulfill(status=503, content_type="application/json",
                          body=json.dumps({"error": {"code": 503,
                              "message": "The model is overloaded."}}))
        else:
            route.fulfill(status=200, content_type="application/json",
                          body=json.dumps({"choices": [
                              {"message": {"content": message},
                               "finish_reason": "stop"}]}))

    context.page.route("**/chat/completions*", fulfill)


@given("the learner also holds an openrouter key")
def step_hold_openrouter(context):
    context.page.add_init_script(
        "localStorage.setItem('lc_ai_key_openrouter','sk-or-test')")


@given('the model endpoint always 503s, but openrouter answers "{message}"')
def step_stub_503_forever_openrouter_ok(context, message):
    context.engine_calls = []

    def fulfill(route):
        context.engine_calls.append(route.request.url)
        if "openrouter.ai" in route.request.url:
            route.fulfill(status=200, content_type="application/json",
                          body=json.dumps({"choices": [
                              {"message": {"content": message},
                               "finish_reason": "stop"}]}))
        else:
            route.fulfill(status=503, content_type="application/json",
                          body=json.dumps({"error": {"code": 503,
                              "message": "The model is overloaded."}}))

    context.page.route("**/chat/completions*", fulfill)


@then('the desk answers "{message}"')
def step_desk_answers(context, message):
    bot = context.page.locator('[data-lc-id="desk"] .lc-agent-msg-bot')
    expect(bot).to_contain_text(message, timeout=30_000)


@then("the desk says which engine answered")
def step_desk_names_engine(context):
    status = context.page.locator('[data-lc-id="desk"] .lc-agent-status')
    expect(status).to_contain_text("openrouter.ai", timeout=15_000)


@then("the desk offers the other engine and names whose key pays")
def step_offer_shown(context):
    status = context.page.locator('[data-lc-id="desk"] .lc-agent-status')
    expect(status).to_contain_text("openrouter.ai", timeout=20_000)
    expect(status).to_contain_text("your spending", timeout=5_000)


@when("I accept the other engine")
def step_accept_fallback(context):
    context.page.click('[data-lc-id="desk"] .lc-agent-fallback-yes')


@when("I decline the other engine")
def step_decline_fallback(context):
    context.page.click('[data-lc-id="desk"] .lc-agent-fallback-no', timeout=20_000)
    context.page.wait_for_timeout(1500)


@then("no call reached the other engine")
def step_no_paid_call(context):
    hits = [u for u in getattr(context, "engine_calls", []) if "openrouter.ai" in u]
    assert not hits, "a paid engine was called without consent: %r" % hits
