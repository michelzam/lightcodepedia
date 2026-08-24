"""Classroom 4: the onboarding desk — problem to solution, one click."""
from behave import then, when
from playwright.sync_api import expect


@then("both personas face each other")
def step_personas(context):
    cards = context.page.locator(".lc-persona")
    expect(cards.first).to_be_visible(timeout=30_000)
    assert cards.count() == 2, "expected 2 personas, got %d" % cards.count()
    expect(context.page.locator('[data-lc-id="p_instructor"]')).to_contain_text("one button")
    expect(context.page.locator('[data-lc-id="p_student"]')).to_contain_text("am I done")


@then("the pitch serves the instructor")
def step_pitch(context):
    pitch = context.page.locator('[data-lc-id="c4_pitch"]')
    expect(pitch).to_be_visible(timeout=20_000)
    expect(pitch).to_contain_text("Classroom 4")
    expect(pitch).to_contain_text("onboarding desk")
    # the FOR points at the persona, not its subtitle (Michel, 2026-08-24)
    expect(pitch).to_contain_text("The instructor")


@then("the impact map pulls its goal from the pitch")
def step_map(context):
    imap = context.page.locator('[data-lc-id="c4_map"]')
    expect(imap).to_be_visible(timeout=20_000)
    # goal omitted in the yaml — it must arrive from the pitch's benefit
    expect(imap).to_contain_text("one click invites the roster")
    expect(imap).to_contain_text("Invite-the-roster")


@then("the flow declares the one-click cast")
def step_flow_cast(context):
    strip = context.page.locator("#c4_flow .lc-ef-elements")
    expect(strip).to_be_visible(timeout=30_000)
    # the story tells the impact map — the x-ray pipes the two
    assert context.page.locator('#c4_flow[data-map="c4_map"]').count() == 1, \
        "the flow does not name its impact map"
    for ref in ("#c4_desk", "#c4_student", "GH.invite_roster",
                "Student[building]", "Invitation[sent]"):
        n = strip.locator('[data-el-ref="%s"]' % ref).count()
        assert n == 1, "cast misses %s (found %d)" % (ref, n)


@then("the desk and the join wizard wear their windows")
def step_windows(context):
    for bid, word in (("c4_desk", "Onboarding desk"), ("c4_student", "join wizard")):
        bar = context.page.locator('.lc-block-win[data-lc-id="%s"] .lc-win-title' % bid)
        expect(bar).to_be_visible(timeout=30_000)
        expect(bar).to_contain_text(word)
    # the desk's mission card holds THE one button, live singletons not specimens
    btn = context.page.locator(
        '[data-lc-inspector="c4_mission"] [data-card="gh"] button[data-m="simulate_invites"]')
    expect(btn).to_be_visible(timeout=45_000)
    # the join wizard is a MONITOR: identity comes from Canvas, nothing typable
    assert context.page.locator(
        '[data-lc-inspector="c4_student_view"][data-lc-ro]').count() == 1, \
        "the student view is editable"


@then("the model is backstage and the diagram shows the managers")
def step_model_diagram(context):
    model = context.page.locator('.lc-model[data-lc-id="c4_model"]')
    expect(model).to_be_hidden()
    assert "class Student" in (model.text_content() or ""), "model code missing"
    svg = context.page.locator(".lc-diagram svg").first
    expect(svg).to_be_visible(timeout=45_000)
    for word in ("Canvas", "GH", "invite roster", "seats"):
        expect(svg).to_contain_text(word, timeout=10_000)


@then("the HQ card links to classroom 4")
def step_hq_door(context):
    card = context.page.locator('.lc-block a[href*="classroom4"]')
    expect(card.first).to_be_visible(timeout=30_000)


@then("the invitations grid gains rows")
def step_invites_rows(context):
    expect(context.page.locator(
        '[data-lc-id="c4_invites"] tbody tr').first).to_be_visible(timeout=20_000)

# ── shared drivers (moved from classroom2/3 when those POCs retired) ─────────

@when("I run every embedded feature")
def step_run_all_features(context):
    cards = context.page.locator(".lc-feature")
    expect(cards.first).to_be_visible(timeout=30_000)
    n = cards.count()
    assert n >= 3, "expected the page's promises, found %d" % n
    for i in range(n):
        cards.nth(i).locator(".lc-feature-run").click()
        expect(cards.nth(i)).to_have_attribute("data-status", "passing", timeout=45_000)


@then("all embedded features pass")
def step_all_pass(context):
    cards = context.page.locator(".lc-feature")
    for i in range(cards.count()):
        expect(cards.nth(i)).to_have_attribute("data-status", "passing")


@when('I press "{verb}" on the "{elid}" inspector')
def step_press(context, verb, elid):
    context.page.locator(
        '[data-lc-inspector="%s"] [data-card] button[data-m="%s"]' % (elid, verb)).first.click()


@then('the "{grid_id}" grid shows "{who}" in "{state}"')
def step_state_cell(context, grid_id, who, state):
    row = context.page.locator('[data-lc-id="%s"] tbody tr' % grid_id).filter(has_text=who).first
    expect(row).to_contain_text(state, timeout=20_000)


# ── the REAL arms, network stubbed ───────────────────────────────────────────

from behave import given
import base64
import json as _json


def _author_key(context):
    context.page.add_init_script(
        "localStorage.setItem('lc_ed_pat','ghp_author');")


@given("a connected author key and a stubbed roster gate")
def step_stub_gate(context):
    _author_key(context)
    plan = (
        "Course 10954: 5 seat(s).\n\n"
        "ada@uwm.edu                            Ada Lovelace\n"
        "zik@uwm.edu                            Zik Newcomer\n\n"
        "Dry run - nothing was sent, nothing was stored.\n"
    )
    b64 = base64.b64encode(plan.encode()).decode()

    def gh(route):
        url = route.request.url
        if "/actions/workflows/" in url and route.request.method == "POST":
            route.fulfill(status=204, body="")
        elif "/commits/main/statuses" in url:
            route.fulfill(json=[{
                "context": "lc/roster-invite", "state": "success",
                "created_at": "2099-01-01T00:00:00Z", "description": "b" * 40}])
        elif "/git/blobs/" in url:
            route.fulfill(json={"content": b64, "encoding": "base64"})
        else:
            route.fulfill(status=404, json={"message": "not stubbed"})

    context.page.route("https://api.github.com/repos/**", gh)


@given("a connected author key and a stubbed org")
def step_stub_org(context):
    _author_key(context)

    def org(route):
        url = route.request.url
        if "/invitations" in url and "failed" not in url:
            route.fulfill(json=[{"email": "ada@uwm.edu", "login": None}])
        elif "/failed_invitations" in url:
            route.fulfill(json=[])
        elif "/members" in url:
            route.fulfill(json=[{"login": "linus"}])
        elif "/repos" in url:
            route.fulfill(json=[{
                "name": "build-ai-fall26-noor",
                "created_at": "2026-08-01T00:00:00Z",
                "pushed_at": "2026-08-20T00:00:00Z"}])
        else:
            route.fulfill(status=404, json={"message": "not stubbed"})

    context.page.route("https://api.github.com/orgs/**", org)


@when('I press the desk button "{bid}"')
def step_press_desk(context, bid):
    btn = context.page.locator('.lc-gate-btn[data-lc-id="%s"] button' % bid)
    expect(btn).to_be_visible(timeout=30_000)
    # the desk acts on the model — wait for the grid (the model ran) first
    expect(context.page.locator(
        '[data-lc-id="c4_roster"] tbody tr').first).to_be_visible(timeout=45_000)
    btn.click()


@then("the roster holds exactly {n:d} seats")
def step_roster_count(context, n):
    context.page.wait_for_function(
        "(n) => document.querySelectorAll('[data-lc-id=\"c4_roster\"] tbody tr').length === n",
        arg=n, timeout=20_000)
    # each seat is ONE line of the verdict — a mangled parse once swallowed
    # the whole plan into a single seat's name (Michel, 2026-08-24 screenshot)
    row = context.page.locator(
        '[data-lc-id="c4_roster"] tbody tr').filter(has_text="zik@uwm.edu").first
    expect(row).to_contain_text("Zik Newcomer")
    body = context.page.locator('[data-lc-id="c4_roster"] tbody')
    txt = body.text_content() or ""
    assert "Dry run" not in txt and "\\n" not in txt, \
        "the verdict leaked into a seat: %r" % txt[:200]
