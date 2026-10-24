import json

from behave import given, then, when
from playwright.sync_api import expect

T = 20_000


@given("the AI answers as Rey and Chuck, Rey wrong the first time")
def step_stub_crew_ai(context):
    """Rey (the reader) says PAY first, then VISIT once Chuck's words come back;
    Chuck (the checker) disagrees with PAY and agrees with VISIT."""
    context.crew_asks = []

    def answer(route):
        body = json.loads(route.request.post_data or "{}")
        system = body["messages"][0]["content"]
        user = body["messages"][1]["content"]
        context.crew_asks.append({"system": system, "user": user})
        if "AGREE or DISAGREE" in system:
            text = "DISAGREE — no visit is booked for Biscuit" if "The verdict: PAY" in user else "AGREE — a visit first"
        else:
            text = "VERDICT: VISIT" if "disagreed" in user else "VERDICT: PAY"
        route.fulfill(status=200, content_type="application/json",
                      body=json.dumps({"choices": [{"message": {"content": text}}],
                                       "usage": {"prompt_tokens": 9, "completion_tokens": 3, "total_tokens": 12}}))
    context.page.route("**/chat/completions*", answer)


def _crew(context, cid):
    return context.page.locator(".lc-crew[data-lc-id='" + cid + "']")


@when('I press ▶ Run on the crew "{cid}"')
def step_run_crew(context, cid):
    btn = _crew(context, cid).locator(".lc-crew-run")
    expect(btn).to_be_enabled(timeout=T)
    btn.click()


@then('the crew "{cid}" is done')
def step_crew_done(context, cid):
    expect(_crew(context, cid)).to_have_attribute("data-state", "done", timeout=T)


def _rows(context, ds):
    return context.page.evaluate("id => (window.lcDatasets || {})[id] || []", ds)


@then('the crew "{cid}" sorted "{family}" as "{lane}" in {tries:d} tries')
def step_crew_sorted(context, cid, family, lane, tries):
    rows = [r for r in _rows(context, cid + ".sorted") if r.get("family") == family]
    assert rows, "no lane for %s in %r" % (family, _rows(context, cid + ".sorted"))
    assert rows[0]["lane"] == lane and int(rows[0]["tries"]) == tries, rows[0]


@then('the crew "{cid}" asked the AI {n:d} times')
def step_crew_asks(context, cid, n):
    got = int(_crew(context, cid).get_attribute("data-asks") or 0)
    assert got == n, "%d AI asks, expected %d" % (got, n)


@then('the crew\'s log shows "{who}" saying "{text}"')
def step_crew_log(context, who, text):
    rows = _rows(context, "desk.log")
    assert any(r.get("who") == who and text in str(r.get("out")) for r in rows), rows


@then("Rey's second ask carried Chuck's words")
def step_second_ask(context):
    reads = [a for a in context.crew_asks if "AGREE or DISAGREE" not in a["system"]]
    assert len(reads) == 2, reads
    assert "no visit is booked" in reads[1]["user"], reads[1]["user"]





@then('the crew "{cid}" shows its {n:d} messages, none sorted yet')
def step_crew_upfront(context, cid, n):
    context.page.wait_for_function("([id, n]) => ((window.lcDatasets || {})[id] || []).length === n", arg=[cid + ".sorted", n], timeout=T)
    rows = _rows(context, cid + ".sorted")
    assert all(r.get("lane") == "" for r in rows), rows
    expect(context.page.locator(".lc-datagrid[data-bind='" + cid + ".sorted'] tbody tr")).to_have_count(n, timeout=T)


@then('the crew "{cid}" spent {n:d} tokens, {k:d} on each AI step')
def step_crew_tokens(context, cid, n, k):
    got = int(_crew(context, cid).get_attribute("data-tokens") or 0)
    assert got == n, "%d tokens, expected %d" % (got, n)
    steps = [r for r in _rows(context, cid + ".log") if r.get("kind") in ("reader", "checker")]
    assert steps and all(int(r.get("tokens")) == k for r in steps), steps
    expect(_crew(context, cid).locator(".lc-crew-status")).to_contain_text(str(n) + " tokens")


@then('the grid of the crew "{cid}" has "{who}" selected')
def step_crew_selected(context, cid, who):
    expect(context.page.locator(".lc-datagrid[data-bind='" + cid + ".sorted'] tr.lc-dg-selected")).to_contain_text(who, timeout=T)


@when('I press the trigger of the avatar "{aid}"')
def step_press_trigger(context, aid):
    context.page.locator("[target='" + aid + "'], [data-target='" + aid + "']").first.click()



@given("a Groq key is saved on this device, and Groq has retired the preset model")
def step_groq_retired(context):
    """Michel, 2026-10-23, on his phone: Rey's ask came back "The model `llama-3…` … not
    accessible". The service names what it serves at /models; the healed model answers."""
    context.page.add_init_script("localStorage.setItem('lc_ai_key_groq', 'gsk-crew-test');")
    context.crew_models = []

    def chat(route):
        body = json.loads(route.request.post_data or "{}")
        context.crew_models.append(body.get("model"))
        if body.get("model") == "llama-3.3-70b-versatile":
            return route.fulfill(status=400, content_type="application/json", body=json.dumps({"error": {
                "message": "The model `llama-3.3-70b-versatile` has been decommissioned and is no longer accessible.",
                "type": "invalid_request_error", "code": "model_decommissioned"}}))
        system = body["messages"][0]["content"]
        text = "AGREE — a visit first" if "AGREE or DISAGREE" in system else "VERDICT: VISIT"
        route.fulfill(status=200, content_type="application/json", body=json.dumps({
            "choices": [{"message": {"content": text}}], "usage": {"total_tokens": 10}}))
    context.page.route("**/api.groq.com/**/chat/completions*", chat)
    context.page.route("**/api.groq.com/**/models*", lambda r: r.fulfill(status=200, content_type="application/json",
        body=json.dumps({"data": [{"id": "llama-3.1-8b-instant"}, {"id": "openai/gpt-oss-120b"}]})))


@then('the crew healed onto "{model}"')
def step_crew_healed(context, model):
    assert "llama-3.3-70b-versatile" in context.crew_models, context.crew_models
    assert context.crew_models[-1] == model, context.crew_models


@then('the grid "{gid}" keeps its text at one size on a phone')
def step_grid_text_size(context, gid):
    got = context.page.evaluate("""id => { const g = document.querySelector(".lc-datagrid[data-lc-id='" + id + "']");
        if (!g) return 'no grid';
        const cs = getComputedStyle(g);
        return cs.getPropertyValue('-webkit-text-size-adjust') || cs.getPropertyValue('text-size-adjust') || cs.webkitTextSizeAdjust || ''; }""", gid)
    assert got == "100%", "the grid's text-size-adjust is %r: a phone may enlarge its long columns" % got
