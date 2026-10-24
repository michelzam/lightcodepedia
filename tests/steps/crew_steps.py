import json

from behave import given, then, when
from playwright.sync_api import expect

T = 20_000


@given("the AI answers as Rey and Chuck, Rey wrong the first time")
def step_stub_crew_ai(context):
    """Rey (the reader) says home first, then met once Chuck's words come back;
    Chuck (the checker), with the row, disagrees with home and agrees with met."""
    context.crew_asks = []

    def answer(route):
        body = json.loads(route.request.post_data or "{}")
        system = body["messages"][0]["content"]
        user = body["messages"][1]["content"]
        context.crew_asks.append({"system": system, "user": user})
        if "AGREE or DISAGREE" in system:
            text = "DISAGREE — the row says asked: no visit yet" if "The verdict: home" in user else "AGREE — one stage at a time"
        else:
            text = "VERDICT: met" if "disagreed" in user else "VERDICT: home"
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


@then('the crew "{cid}" sorted "{family}" as "{stage}" in {tries:d} tries')
def step_crew_sorted(context, cid, family, stage, tries):
    rows = [r for r in _rows(context, cid + ".sorted") if r.get("family") == family]
    assert rows, "no stage for %s in %r" % (family, _rows(context, cid + ".sorted"))
    assert rows[0]["next_stage"] == stage and int(rows[0]["tries"]) == tries, rows[0]


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
    assert "no visit yet" in reads[1]["user"], reads[1]["user"]


@then("Rey read the words only, and Chuck checked them against the row")
def step_row_to_checker(context):
    reads = [a for a in context.crew_asks if "AGREE or DISAGREE" not in a["system"]]
    checks = [a for a in context.crew_asks if "AGREE or DISAGREE" in a["system"]]
    assert reads and all('"stage"' not in a["user"] for a in reads), reads
    assert checks and '"stage":"asked"' in checks[0]["user"], checks[0]["user"]





@then('the crew "{cid}" shows its {n:d} messages, none sorted yet')
def step_crew_upfront(context, cid, n):
    context.page.wait_for_function("([id, n]) => ((window.lcDatasets || {})[id] || []).length === n", arg=[cid + ".sorted", n], timeout=T)
    rows = _rows(context, cid + ".sorted")
    assert all(r.get("next_stage") == "" for r in rows), rows
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
        text = "AGREE — one stage at a time" if "AGREE or DISAGREE" in system else "VERDICT: met"
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


@then('the proof "{fid}" can be read on the page')
def step_proof_seen(context, fid):
    card = context.page.locator(".lc-feature[data-lc-id='" + fid + "']")
    expect(card).to_be_visible(timeout=T)
    expect(card.locator(".lc-feature-run")).to_be_visible(timeout=T)


@then('the proof "{fid}" wears the tag "{tag}"')
def step_proof_tag(context, fid, tag):
    expect(context.page.locator(".lc-feature[data-lc-id='" + fid + "'] .lc-feature-tag", has_text=tag).first).to_be_visible(timeout=T)


@then('the crew "{cid}" shows its desk, {state}')
def step_crew_desk(context, cid, state):
    crew = _crew(context, cid)
    expect(crew.locator(".lc-crew-head .lc-agent-key")).to_be_visible(timeout=T)
    ring = crew.locator(".lc-agent-auth")
    if state == "open":
        expect(ring).to_be_visible(timeout=T)
        expect(ring.locator(".lc-agent-ring-row").first).to_be_visible(timeout=T)
    else:
        expect(ring).to_be_hidden(timeout=T)


@given("an energy key is saved on this device, and its engine cannot be reached")
def step_engine_unreachable(context):
    context.page.add_init_script("localStorage.setItem('lc_ai_key_gemini', 'AIza-crew-test');")
    context.page.route("**/chat/completions*", lambda r: r.abort())


@then('the crew "{cid}" says "{text}"')
def step_crew_says(context, cid, text):
    expect(_crew(context, cid).locator(".lc-crew-status")).to_contain_text(text, timeout=T)


@then("the page has one guide, docked small in its corner")
def step_one_docked_guide(context):
    hosts = context.page.locator(".lc-avatar-host")
    n = hosts.count()
    docked = context.page.locator(".lc-avatar-host.lc-avatar-docked").count()
    assert n >= 1 and docked == n, "%d guides on the page, %d docked: a guide floats in the page" % (n, docked)






@then('the crew "{cid}" says why "{family}" went "{stage}": "{why}"')
def step_crew_why(context, cid, family, stage, why):
    rows = [r for r in _rows(context, cid + ".sorted") if r.get("family") == family]
    assert rows and rows[0].get("next_stage") == stage and rows[0].get("why") == why, rows
    grid = context.page.locator(".lc-datagrid[data-bind='" + cid + ".sorted'] tbody tr", has_text=family).first
    expect(grid).to_contain_text(why, timeout=T)


@then('the crew "{cid}" shows its tokens as an agent does: "{text}"')
def step_crew_usage(context, cid, text):
    expect(_crew(context, cid).locator(".lc-agent-usage")).to_contain_text(text, timeout=T)


@then('the run\'s event flow "{fid}" tells "{beats}"')
def step_flow_tells(context, fid, beats):
    """beats, in order, separated by " / " — each the text of a chip; the last an event."""
    flow = context.page.locator(".lc-event-flow[data-lc-id='" + fid + "']")
    expect(flow.locator(".lc-ef-step").first).to_be_attached(timeout=T)
    chips = flow.locator(".lc-ef-step").evaluate_all("els => els.map(e => [e.getAttribute('data-kind'), e.textContent.trim()])")
    texts = [t for _, t in chips]
    at = 0
    for b in beats.split(" / "):
        hit = next((i for i in range(at, len(texts)) if b in texts[i]), None)
        assert hit is not None, "the flow never says %r after chip %d: %r" % (b, at, texts)
        at = hit + 1
    assert chips[at - 1][0] == "event", "the last beat %r is a %s, not an event (orange)" % (texts[at - 1], chips[at - 1][0])



@then('the crew "{cid}" shows its bounds: {tries:d} tries, a budget of {budget:d}')
def step_crew_bounds(context, cid, tries, budget):
    crew = _crew(context, cid)
    expect(crew.locator(".lc-crew-step[data-bound='tries'] b")).to_have_text(str(tries), timeout=T)
    expect(crew.locator(".lc-crew-step[data-bound='budget'] b")).to_have_text(str(budget), timeout=T)


@when('I press "{sign}" on the {bound} of the crew "{cid}" {n:d} times')
def step_crew_step(context, sign, bound, cid, n):
    b = _crew(context, cid).locator(".lc-crew-step[data-bound='%s'] button[data-d='%s']" % (bound, "1" if sign == "+" else "-1"))
    for _ in range(n):
        b.click()


@then('the gauge of the crew "{cid}" reads "{text}", {level}')
def step_crew_gauge(context, cid, text, level):
    g = _crew(context, cid).locator(".lc-crew-gauge")
    expect(g).to_contain_text(text, timeout=T)
    expect(g).to_have_attribute("data-level", level, timeout=T)


@then('the crew "{cid}" shows the engine\'s 🔋 asks left, as an agent does')
def step_crew_quota(context, cid):
    q = _crew(context, cid).locator(".lc-agent-quota")
    expect(q).to_be_visible(timeout=T)
    expect(q).to_contain_text("🔋", timeout=T)


@then('the accordion section "{title}" comes before the grid "{gid}"')
def step_section_before_grid(context, title, gid):
    expect(context.page.locator(".lc-datagrid[data-lc-id='" + gid + "']")).to_be_attached(timeout=T)
    ok = context.page.evaluate("""([t, id]) => {
        const g = document.querySelector(".lc-datagrid[data-lc-id='" + id + "']");
        const h = [...document.querySelectorAll(".lc-accordion details summary")].find(e => e.textContent.includes(t));
        return !!(g && h && (h.compareDocumentPosition(g) & Node.DOCUMENT_POSITION_FOLLOWING));
    }""", [title, gid])
    assert ok, "the section %r is not above the grid %r" % (title, gid)


@then('picking "{who}" in the grid "{gid}", the form "{fid}" shows its {what}')
def step_form_worker(context, who, gid, fid, what):
    context.page.locator(".lc-datagrid[data-lc-id='" + gid + "'] tbody tr", has_text=who).first.click()
    form = context.page.locator("[data-lc-id='" + fid + "']")
    expect(form).to_contain_text(what, timeout=T)


@then('the asks of the crew "{cid}" add up to its gauge: {n:d}')
def step_crew_asks_sum(context, cid, n):
    rows = _rows(context, cid + ".sorted")
    total = sum(int(r.get("asks") or 0) for r in rows)
    assert total == n == int(_crew(context, cid).get_attribute("data-asks") or 0), (total, n, rows)
    expect(_crew(context, cid).locator(".lc-crew-gauge")).to_contain_text("%d of" % n)
    expect(context.page.locator(".lc-datagrid[data-bind='" + cid + ".sorted'] thead th", has_text="Asks")).to_have_count(1, timeout=T)



@then('the 🔑 of the crew "{cid}" is marked, its keys folded')
def step_crew_key_marked(context, cid):
    crew = _crew(context, cid)
    expect(crew.locator(".lc-agent-auth")).to_be_hidden(timeout=T)
    expect(crew.locator(".lc-crew-head .lc-agent-key")).to_have_class(__import__("re").compile(r"\blc-agent-key-alert\b"), timeout=T)


@when('I press the 🔑 of the crew "{cid}"')
def step_crew_key_press(context, cid):
    _crew(context, cid).locator(".lc-crew-head .lc-agent-key").click()
