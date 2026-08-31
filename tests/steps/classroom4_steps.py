"""Classroom 4: the onboarding desk — problem to solution, one click."""
from behave import then, when
from playwright.sync_api import expect


@then("both personas face each other")
def step_personas(context):
    cards = context.page.locator(".lc-persona")
    expect(cards).to_have_count(2, timeout=30_000)
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
    expect(imap).to_contain_text("Invite button, gated")


@then("the flow declares the one-click cast")
def step_flow_cast(context):
    # the cast strip is STRUCTURE, not ink — attached for x-ray and
    # proofs, never shown to the reader (Michel, 2026-08-25)
    strip = context.page.locator("#c4_flow .lc-ef-elements")
    expect(strip).to_be_attached(timeout=30_000)
    expect(strip).to_be_hidden()
    # the story tells the impact map — the x-ray pipes the two
    assert context.page.locator('#c4_flow[data-map="c4_map"]').count() == 1, \
        "the flow does not name its impact map"
    for ref in ("#c4_desk", "#c4_student", "Desk.plan", "Desk.sync",
                "Student[invited]", "Student[building]"):
        n = strip.locator('[data-el-ref="%s"]' % ref).count()
        assert n == 1, "cast misses %s (found %d)" % (ref, n)


@then("the desk and the join wizard wear their windows")
def step_windows(context):
    for bid, word in (("c4_desk", "Onboarding desk"), ("c4_student", "join wizard")):
        bar = context.page.locator('.lc-block-win[data-lc-id="%s"] .lc-win-title' % bid)
        expect(bar).to_be_visible(timeout=30_000)
        expect(bar).to_contain_text(word)
    # the mission card IS the Desk instance — its verbs are the buttons
    btn = context.page.locator(
        '[data-lc-inspector="c4_mission"] [data-card="desk"] button[data-m="plan"]')
    expect(btn).to_be_visible(timeout=45_000)
    # the join wizard is a MONITOR: identity comes from Canvas, nothing typable
    assert context.page.locator(
        '[data-lc-inspector="c4_student_view"][data-lc-ro]').count() == 1, \
        "the student view is editable"


@then("the model is backstage and the diagram shows the desk")
def step_model_diagram(context):
    model = context.page.locator('.lc-model[data-lc-id="c4_model"]')
    expect(model).to_be_hidden()
    assert "class Student" in (model.text_content() or ""), "model code missing"
    svg = context.page.locator(".lc-diagram svg").first
    expect(svg).to_be_visible(timeout=45_000)
    for word in ("Desk", "Student", "plan", "sync", "roster"):
        expect(svg).to_contain_text(word, timeout=10_000)


@then('the desk offers exactly the verbs "{verbs}"')
def step_only_verbs(context, verbs):
    # proofs-only muscle (_simulate) must never wear a button here
    got = context.page.evaluate(
        """() => Array.from(document.querySelectorAll(
             '[data-lc-inspector="c4_mission"] [data-card="desk"] button[data-m]'))
             .map(b => b.getAttribute('data-m'))""")
    want = [v.strip() for v in verbs.split(",")]
    assert sorted(got) == sorted(want), "desk offers %r" % got


@when('I click the "{kind}" legend chip on "{flow_id}"')
def step_click_legend(context, kind, flow_id):
    context.page.click("#%s [data-lk='%s']" % (flow_id, kind))
    context.page.wait_for_timeout(150)


@then('the "{flow_id}" flow shows its "{kind}" notes')
def step_flow_kind_shown(context, flow_id, kind):
    expect(context.page.locator(
        "#%s .lc-ef-step[data-kind='%s']" % (flow_id, kind)).first
    ).to_be_visible(timeout=15_000)


@then('the "{flow_id}" flow hides its "{kind}" notes')
def step_flow_kind_hidden(context, flow_id, kind):
    expect(context.page.locator(
        "#%s .lc-ef-step[data-kind='%s']" % (flow_id, kind)).first
    ).to_be_hidden()


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
        "Org uwm-build-ai: 4 member(s).\n\n"
        "Skipped:\n"
        "   \u00b7  mk@karmicsoft.com                   already invited (2026-08-24)\n\n"
        "To invite: 3\n"
        "   ada@uwm.edu                            Ada Lovelace\n"
        "   zik@uwm.edu                            Zik Newcomer\n"
        "   ENONAIVI@UWM.EDU                       Onaivi, Emmanuel\n\n"
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


@given("a stubbed org")
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
            route.fulfill(json=[{"login": "zik"}])
        elif "/repos" in url:
            route.fulfill(json=[
                {"name": "build-ai-fall26-zik",
                 "created_at": "2026-08-01T00:00:00Z",
                 "pushed_at": "2026-08-20T00:00:00Z"},
                # the bench's public bay twin — must NOT become a student
                {"name": "build-ai-fall26-zik-bay",
                 "created_at": "2026-08-01T00:00:00Z",
                 "pushed_at": "2026-08-21T00:00:00Z"}])
        else:
            route.fulfill(status=404, json={"message": "not stubbed"})

    context.page.route("https://api.github.com/orgs/**", org)


@then('the "{verb}" verb on the "{elid}" inspector is enabled')
def step_verb_enabled(context, verb, elid):
    btn = context.page.locator(
        '[data-lc-inspector="%s"] [data-card] button[data-m="%s"]' % (elid, verb)).first
    expect(btn).to_be_visible(timeout=45_000)
    expect(btn).to_be_enabled(timeout=15_000)


@then('the "{verb}" verb on the "{elid}" inspector is disabled')
def step_verb_disabled(context, verb, elid):
    btn = context.page.locator(
        '[data-lc-inspector="%s"] [data-card] button[data-m="%s"]' % (elid, verb)).first
    expect(btn).to_be_visible(timeout=45_000)
    expect(btn).to_be_disabled()


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



@then("no bay twin became a student")
def step_no_bay_phantom(context):
    txt = context.page.locator('[data-lc-id="c4_roster"] tbody').text_content() or ""
    assert "bay" not in txt, "a -bay repo minted a phantom seat: %r" % txt[:200]


@then("no seat is named after a skip reason")
def step_no_reason_names(context):
    txt = context.page.locator('[data-lc-id="c4_roster"] tbody').text_content() or ""
    assert "already invited" not in txt, \
        "a skip reason became a name: %r" % txt[:200]


@given("an org where ada accepts between two syncs")
def step_stub_org_acceptance(context):
    context.c4_syncs = {"n": 0}

    def org(route):
        url = route.request.url
        if "/invitations" in url and "failed" not in url:
            context.c4_syncs["n"] += 1
            first = context.c4_syncs["n"] <= 1
            route.fulfill(json=[{"email": "ada@uwm.edu", "login": None}] if first else [])
        elif "/failed_invitations" in url:
            route.fulfill(json=[])
        elif "/members" in url:
            first = context.c4_syncs["n"] <= 1
            route.fulfill(json=[{"login": "zik"}] if first
                          else [{"login": "zik"}, {"login": "adalove"}])
        elif "/repos" in url:
            route.fulfill(json=[])
        else:
            route.fulfill(status=404, json={"message": "not stubbed"})

    context.page.route("https://api.github.com/orgs/**", org)


@given("an org where guest zara is invited by hand and then accepts")
def step_stub_org_guest(context):
    context.c4_syncs = {"n": 0}

    def org(route):
        url = route.request.url
        if "/invitations" in url and "failed" not in url:
            context.c4_syncs["n"] += 1
            first = context.c4_syncs["n"] <= 1
            route.fulfill(json=[{"email": "zara@ext.org", "login": None}] if first else [])
        elif "/failed_invitations" in url:
            route.fulfill(json=[])
        elif "/members" in url:
            first = context.c4_syncs["n"] <= 1
            route.fulfill(json=[] if first else [{"login": "zaralove"}])
        elif "/repos" in url:
            route.fulfill(json=[])
        else:
            route.fulfill(status=404, json={"message": "not stubbed"})

    context.page.route("https://api.github.com/orgs/**", org)


@then('the "{grid_id}" grid shows "{who}" with login "{login}"')
def step_login_cell(context, grid_id, who, login):
    row = context.page.locator(
        '[data-lc-id="%s"] tbody tr' % grid_id).filter(has_text=who).first
    expect(row).to_contain_text(login, timeout=20_000)


@given("a bench factory that records what it builds")
def step_stub_factory(context):
    context.c4_built = []

    def org_side(route):
        # the reconciler's org-level acts: the session team and the bay
        url = route.request.url
        m = route.request.method
        if m == "PUT" and "/teams/" in url and "/memberships/" in url:
            context.c4_built.append(("team", url.rsplit("/", 1)[-1]))
            route.fulfill(status=200, json={"state": "active"})
        elif m == "POST" and url.rstrip("/").endswith("/repos"):
            body = _json.loads(route.request.post_data or "{}")
            context.c4_built.append(("bay", body.get("name", "")))
            route.fulfill(status=201, json={"name": body.get("name", "")})
        else:
            route.fallback()   # the org facts stub handles the rest

    context.page.route("https://api.github.com/orgs/**", org_side)

    def repos(route):
        url = route.request.url
        m = route.request.method
        # a bench is a FORK of the hub (register §18) — a /generate template
        # copy finds no answer here and the scenario goes red
        if m == "POST" and url.rstrip("/").endswith("/forks"):
            body = _json.loads(route.request.post_data or "{}")
            context.c4_built.append(("fork", body.get("name", "")))
            route.fulfill(status=202, json={"full_name": "x"})
        elif m == "GET" and url.rstrip("/").endswith("-bay"):
            # no bay yet — the reconciler must create it
            route.fulfill(status=404, json={"message": "Not Found"})
        elif m == "GET" and any(url.rstrip("/").endswith("/" + b)
                                for k, b in context.c4_built if k == "fork"):
            # the bridge polls the fresh fork until it answers
            route.fulfill(status=200, json={"name": url.rsplit("/", 1)[-1]})
        elif m == "PUT" and "/collaborators/" in url:
            context.c4_built.append(("grant", url.rsplit("/", 1)[-1] + "@" + url.split("/repos/")[1].split("/")[1]))
            route.fulfill(status=204, body="")
        else:
            route.fallback()   # the roster gate's own stub handles the rest

    context.page.route("https://api.github.com/repos/**", repos)


@given("a bench factory where the bench already stands")
def step_stub_factory_exists(context):
    context.c4_built = []

    def org_side(route):
        url = route.request.url
        m = route.request.method
        if m == "PUT" and "/teams/" in url and "/memberships/" in url:
            context.c4_built.append(("team", url.rsplit("/", 1)[-1]))
            route.fulfill(status=200, json={"state": "active"})
        elif m == "POST" and url.rstrip("/").endswith("/repos"):
            body = _json.loads(route.request.post_data or "{}")
            context.c4_built.append(("bay", body.get("name", "")))
            route.fulfill(status=201, json={"name": body.get("name", "")})
        else:
            route.fallback()

    context.page.route("https://api.github.com/orgs/**", org_side)

    def repos(route):
        url = route.request.url
        m = route.request.method
        if m == "POST" and url.rstrip("/").endswith("/forks"):
            # the name already stands — GitHub says 403, NOT "exists"
            route.fulfill(status=403, json={"message": "Name already exists on this account"})
        elif m == "GET" and url.rstrip("/").endswith("-bay"):
            route.fulfill(status=404, json={"message": "Not Found"})
        elif m == "GET" and "/repos/" in url and url.rstrip("/").endswith("-adalove"):
            # the bench itself answers — this is what acquits the key
            route.fulfill(status=200, json={"name": url.rsplit("/", 1)[-1]})
        elif m == "PUT" and "/collaborators/" in url:
            context.c4_built.append(("grant", url.rsplit("/", 1)[-1]))
            route.fulfill(status=204, body="")
        else:
            route.fallback()

    context.page.route("https://api.github.com/repos/**", repos)


@then('the factory teamed "{login}" and built the bay "{bay}"')
def step_factory_kit(context, login, bay):
    def done():
        return ("team", login) in context.c4_built and \
               ("bay", bay) in context.c4_built
    for _ in range(40):
        if done():
            return
        context.page.wait_for_timeout(250)
    raise AssertionError("factory log: %r" % context.c4_built)


@then('the factory built "{bench}" and granted "{login}"')
def step_factory_built(context, bench, login):
    def done():
        return ("fork", bench) in context.c4_built and \
               any(k == "grant" and v.startswith(login + "@") for k, v in context.c4_built)
    for _ in range(40):
        if done():
            return
        context.page.wait_for_timeout(250)
    raise AssertionError("factory log: %r" % context.c4_built)


@given("an org whose members wear their names")
def step_stub_org_names(context):
    _author_key(context)

    def org(route):
        url = route.request.url
        if "/invitations" in url and "failed" not in url:
            route.fulfill(json=[])
        elif "/failed_invitations" in url:
            route.fulfill(json=[])
        elif "/members" in url:
            route.fulfill(json=[{"login": "Emmanuel-Onaivi"}, {"login": "egbas"}])
        elif "/repos" in url:
            route.fulfill(json=[{
                "name": "build-ai-fall26-Emmanuel-Onaivi",
                "created_at": "2026-08-01T00:00:00Z",
                "pushed_at": "2026-08-20T00:00:00Z"}])
        else:
            route.fulfill(status=404, json={"message": "not stubbed"})

    context.page.route("https://api.github.com/orgs/**", org)
