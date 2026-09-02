import json
import re

from behave import given, when, then
from playwright.sync_api import expect


HUB = {"name": "build-ai-fall26", "is_template": True, "fork": False,
       "default_branch": "main", "updated_at": "2026-07-01T00:00:00Z"}
# last term's session, still standing in the org and touched more recently
# than this one — the shape that paired a teacher with the wrong bench
OLD_HUB = {"name": "build-ai-summer26", "is_template": True, "fork": False,
           "default_branch": "main", "updated_at": "2026-08-30T00:00:00Z"}
OLD_BENCH = "uwm-build-ai/build-ai-summer26-zamm-student"
BENCH = "build-ai-fall26-zamm-student"
BAY = BENCH + "-bay"


def _stub(context):
    st = getattr(context, "join_stub", {"vault_ok": False})

    def handler(route):
        req = route.request
        url, method = req.url, req.method
        if url.endswith("/user") and method == "GET":
            # the page reads the scope header cross-origin — it must be exposed,
            # exactly as the real GitHub API exposes it
            route.fulfill(status=200, json={"login": "zamm-student"},
                          headers={"X-OAuth-Scopes": "repo",
                                   "Access-Control-Expose-Headers": "X-OAuth-Scopes"})
            return
        if re.search(r"/user/memberships/orgs/", url) and method == "PATCH":
            st["vault_ok"] = True          # accepting the invite grants the team read
            route.fulfill(status=200, json={"state": "active"})
            return
        if re.search(r"/orgs/[^/]+/repos", url) and method == "GET":
            # hub discovery: the session template is visible once enrolled
            hubs = []
            if st.get("vault_ok"):
                hubs = [OLD_HUB, HUB] if st.get("last_term") else [HUB]
            route.fulfill(status=200, json=hubs)
            return
        if re.search(r"/orgs/[^/]+/repos", url) and method == "POST":
            # the wizard creating the learner's public bay with their own key
            body = json.loads(req.post_data or "{}")
            st["bay"] = True
            context.bay_created = body
            route.fulfill(status=201, json={"name": body.get("name", "")})
            return
        # ── the bay (public sister of the bench) — before BENCH: its name
        #    CONTAINS the bench name, so the bench block would swallow it ──
        if BAY in url:
            if method == "GET":
                if st.get("bay"):
                    route.fulfill(status=200, json={"name": BAY})
                else:
                    route.fulfill(status=404, json={"message": "Not Found"})
                return
        if re.search(r"/repos/[^/]+/[^/]+/contents/", url) and method == "GET" and BENCH not in url:
            if st.get("vault_ok"):
                route.fulfill(status=200, json={"name": "index.md", "sha": "s"})
            else:
                route.fulfill(status=404, json={"message": "Not Found"})
            return
        # ── the bench (org-owned fork of the hub) ─────────────────────────
        if BENCH in url:
            if "/compare/" in url and method == "GET":
                route.fulfill(status=200, json={"ahead_by": st.get("behind", 0)})
                return
            if url.endswith("/merge-upstream") and method == "POST":
                st["behind"] = 0
                route.fulfill(status=200, json={"message": "fast-forwarded"})
                return
            if "/contents/index.md" in url and method == "GET":
                if st.get("bench") and not st.get("no_index"):
                    route.fulfill(status=200, json={"name": "index.md", "sha": "s"})
                else:
                    route.fulfill(status=404, json={"message": "Not Found"})
                return
            if method == "GET":
                if st.get("bench"):
                    route.fulfill(status=200, json={"name": BENCH, "default_branch": "main"})
                else:
                    route.fulfill(status=404, json={"message": "Not Found"})
                return
        if url.endswith("/forks") and method == "POST":
            # the wizard must never fork — that is the desk's act (A′)
            context.fork_posted = url
            st["bench"] = True
            route.fulfill(status=202, json={"name": BENCH})
            return
        if re.search(r"/repos/[^/]+/[^/]+$", url) and method == "GET":
            # repo metadata: visible exactly when the learner has vault access
            if st.get("vault_ok"):
                route.fulfill(status=200, json={"name": "uwm-build-ai-vault"})
            else:
                route.fulfill(status=404, json={"message": "Not Found"})
            return
        route.fulfill(status=404, json={"message": "stub"})

    context.page.route("https://api.github.com/**", handler)


@when('I open the content door "{path}"')
def step_open_door(context, path):
    context.page.goto(context.base_url + path, wait_until="domcontentloaded")
    # the runner's own load never settles in the offline rig — the door's
    # job ends at the address bar, so commit is the moment to judge
    context.page.wait_for_url(lambda u: "/run.html" in u and "#src=" in u,
                              timeout=15_000, wait_until="commit")


@then('the runner is asked for "{target}"')
def step_door_target(context, target):
    assert context.page.url.endswith(
        "#src=gh:uwm-build-ai/uwm-build-ai-vault/" + target), \
        "the door forwarded to %s" % context.page.url


@then("the runner carries the baked learner flags")
def step_door_flags(context):
    url = context.page.url
    for piece in ("focus=1", "crumb=BUILD-AI",
                  "open=gh%3Auwm-build-ai%2Fuwm-build-ai-vault%2Fcourses%2F*"):
        assert piece in url, "missing %s in %s" % (piece, url)
    # editable is NOT baked: it would override the frame's own read-only rule
    assert "editable=" not in url, "the door still declares editable: %s" % url


def _edit_pill(context):
    """The pill's ✏️ Edit — the one door into edit mode on a framed page."""
    context.page.wait_for_selector("#lc-bl-edit-btn", state="attached", timeout=10_000)
    context.page.wait_for_timeout(2200)   # syncEditDoors settles after the render
    return context.page.evaluate(
        "() => { const b = document.getElementById('lc-bl-edit-btn');"
        "        return { disabled: !!b.disabled, title: b.title || '' }; }")


@then("the edit door is closed, and it says why")
def step_edit_door_closed(context):
    st = _edit_pill(context)
    assert st["disabled"], "the ✏️ Edit item is still live on a course page in the frame"
    assert "course" in st["title"].lower(), \
        "a disabled door must name its reason, got %r" % st["title"]


@then("the edit door is open")
def step_edit_door_open(context):
    st = _edit_pill(context)
    assert not st["disabled"], "an explicit editable=1 was ignored: %r" % st["title"]


@then("the landing wears the learner chrome, not the platform")
def step_door_chrome(context):
    # the URL said the right thing once and the page still wore the full
    # platform (Michel's mac, 2026-08-25) — so judge the CHROME itself:
    # crumb mode on the root, the topbar's menu links gone
    context.page.wait_for_timeout(800)
    root_cls = context.page.evaluate("document.documentElement.className")
    assert "lc-crumb-mode" in root_cls, "no crumb mode: %r" % root_cls
    links = context.page.locator("#lc-topbar .lc-links")
    if links.count():
        expect(links.first).to_be_hidden()


@then("no retired pencil floats over the lesson")
def step_no_pencil(context):
    # The ✏️ FAB was retired for the pill + ⌥E, but a leftover rule showed it
    # again whenever a frame said editable=1 — which every door bakes — so the
    # Canvas view of 410 wore a pencil (Michel, 2026-08-30). It stays in the
    # DOM as the editor's presence marker; it must never be on screen.
    fab = context.page.locator("#ed-fab")
    if fab.count():
        expect(fab.first).to_be_hidden()


@given("a stubbed GitHub that accepts the key with repo scope")
def step_stub_key(context):
    context.join_stub = {"vault_ok": False}


@given("the learner can read the vault")
def step_stub_vault_ok(context):
    context.join_stub["vault_ok"] = True


def _open(context, stored=False):
    if not hasattr(context, "join_stub"):
        context.join_stub = {"vault_ok": False}
    _stub(context)
    if stored:
        context.page.add_init_script("localStorage.setItem('lc_ed_pat','ghp_stored');")
    context.page.goto(context.base_url + "/courses/join", wait_until="domcontentloaded")
    context.page.wait_for_selector(".lc-join .lcj-step", timeout=10_000)
    context.page.wait_for_timeout(600)


@when("I open the course wizard")
def step_open_wizard(context):
    _open(context)


@when("I open the course wizard with a stored key")
def step_open_wizard_stored(context):
    _open(context, stored=True)


@when("I confirm I have an account")
def step_have_account(context):
    context.page.click('.lc-join [data-a="have"]')
    context.page.wait_for_timeout(200)


@when('I paste the course key "{key}" and check it')
def step_paste_key(context, key):
    context.page.fill(".lc-join .lcj-key", key)
    context.page.click('.lc-join .lcj-course button[type="submit"]')
    context.page.wait_for_timeout(1200)


@when("I check my access")
def step_check_access(context):
    context.page.click('.lc-join [data-a="checkaccess"]')
    context.page.wait_for_timeout(600)


def _cls(context, n):
    return context.page.locator('.lc-join .lcj-step[data-n="%s"]' % n).get_attribute("class") or ""


@then("join step 1 is active and steps 2 and 3 are off")
def step_fresh_state(context):
    assert "on" in _cls(context, 1).split(), _cls(context, 1)
    assert "off" in _cls(context, 2).split() and "off" in _cls(context, 3).split()


@then("join steps 1 and 2 are done and step 3 is active")
def step_key_done(context):
    # the key check advances states after a short success pause — poll, don't race
    context.page.wait_for_selector('.lc-join .lcj-step[data-n="3"].on', timeout=6000)
    assert "ok" in _cls(context, 1).split() and "ok" in _cls(context, 2).split()


@then("the wizard says the learner is in")
def step_is_in(context):
    expect(context.page.locator('.lc-join [data-m="3"]')).to_contain_text("You’re in", timeout=6000)


@then("the wizard offers no way out of setup")
def step_no_exit(context):
    """No door into the course, no door into the bench — a five-step setup
    that hands out exits at step 3 loses learners before their AI key."""
    context.page.wait_for_timeout(600)
    hrefs = context.page.eval_on_selector_all(
        ".lc-join a", "els => els.map(e => (e.getAttribute('href') || '') + '|' + e.textContent.trim())")
    stray = [h for h in hrefs if "/run.html" in h.split("|")[0]]
    assert not stray, "the wizard still opens the runner from inside setup: %r" % stray


@then("the wizard guides to the invitation, not an error dump")
def step_guided(context):
    txt = context.page.locator('.lc-join [data-m="3"]').inner_text()
    assert "invitation" in txt.lower(), txt
    assert "404" not in txt and "HTTP" not in txt, txt


@when("I accept my invitation in the wizard")
def step_accept_invite(context):
    context.page.click('.lc-join [data-a="accept"]')
    context.page.wait_for_timeout(900)


# ── step 4: the bench ──────────────────────────────────────────────────

@given("my bench exists and is {n:d} updates behind the hub")
def step_bench_exists(context, n):
    context.join_stub["bench"] = True
    context.join_stub["behind"] = n


@then("the bench step says the teacher's desk builds it")
def step_bench_is_desks(context):
    expect(context.page.locator('.lc-join [data-m="4"]')).to_contain_text(
        "your teacher’s desk builds it", timeout=8000)
    assert context.page.locator('.lc-join [data-a="fork"]').count() == 0, \
        "the retired Create-my-bench button is back"


@then("my bench shows up to date with the hub")
def step_bench_current(context):
    expect(context.page.locator('.lc-join [data-m="4"]')).to_contain_text("up to date", timeout=8000)


@then("the bench shows {n:d} updates to sync")
def step_bench_behind(context, n):
    expect(context.page.locator('.lc-join [data-m="4"]')).to_contain_text("%d update" % n, timeout=8000)
    expect(context.page.locator('.lc-join [data-a="sync"]')).to_be_visible()


@when("I sync my bench")
def step_sync_bench(context):
    context.page.click('.lc-join [data-a="sync"]')
    context.page.wait_for_timeout(800)


@when('I open the course door "{query}" with a stored key')
def step_open_door(context, query):
    if not hasattr(context, "join_stub"):
        context.join_stub = {"vault_ok": False}
    _stub(context)
    context.page.add_init_script("localStorage.setItem('lc_ed_pat','ghp_stored');")
    context.page.goto(context.base_url + "/courses/join" + query, wait_until="domcontentloaded")
    context.page.wait_for_timeout(600)


@then("I am forwarded into my bench")
def step_forwarded(context):
    for _ in range(40):
        if "run.html#src=gh:uwm-build-ai/" + BENCH + "/index.md" in context.page.url:
            return
        context.page.wait_for_timeout(250)
    raise AssertionError("stayed on " + context.page.url)


@then("the bench step explains the session is not visible")
def step_session_not_visible(context):
    expect(context.page.locator('.lc-join [data-m="4"]')).to_contain_text("isn’t visible", timeout=8000)


@given("my bench has no index yet")
def step_bench_no_index(context):
    context.join_stub["no_index"] = True


@then("the bench step invites a refresh")
def step_invites_refresh(context):
    expect(context.page.locator('.lc-join [data-m="4"]')).to_contain_text("Refresh", timeout=8000)
    expect(context.page.locator('.lc-join [data-a="sync"]')).to_be_visible()


@given("the energy provider accepts the key")
def step_energy_ok(context):
    context.page.route(
        "**/generativelanguage.googleapis.com/**/models*",
        lambda r: r.fulfill(status=200, content_type="application/json",
                            body='{"data": []}'))


@given("the energy provider rejects the key")
def step_energy_bad(context):
    context.page.route(
        "**/generativelanguage.googleapis.com/**/models*",
        lambda r: r.fulfill(status=401, content_type="application/json",
                            body='{"error": "invalid key"}'))


@when('I paste the energy key "{key}" and check it')
def step_paste_energy_key(context, key):
    box = context.page.locator(".lcj-ekey")
    box.wait_for(state="attached", timeout=15_000)
    # the step may still be folded if earlier checks are mid-flight — the
    # form handler is live either way; make it visible the way a learner
    # who reached step 5 sees it
    context.page.wait_for_function(
        "() => { var s = document.querySelector('.lcj-step[data-n=\"5\"]');"
        "        return s && !s.classList.contains('off'); }", timeout=15_000)
    box.fill(key)
    context.page.locator(".lcj-energy button[type=submit]").click()


@then("the energy step confirms the key works and will follow the learner")
def step_energy_confirmed(context):
    m = context.page.locator('[data-m="5"]')
    expect(m).to_contain_text("key works", timeout=10_000)
    expect(m).to_contain_text("follows you", timeout=5_000)


@then("the energy step reports the rejection with the status code")
def step_energy_rejected(context):
    m = context.page.locator('[data-m="5"]')
    expect(m).to_contain_text("rejected", timeout=10_000)
    expect(m).to_contain_text("401", timeout=5_000)


@given('an old author connection points at "{repo}"')
def step_stale_connection(context, repo):
    # the teacher's browser: a connection left over from an earlier life —
    # exactly the repo the learner's key was never meant to cover
    context.page.add_init_script(
        "localStorage.setItem('lc_ed_repo', '" + repo + "');"
    )


@then("the connected repo is my bench")
def step_pair_completed(context):
    # give the wizard's bench resolution a beat to land
    context.page.wait_for_timeout(600)
    repo = context.page.evaluate("() => localStorage.getItem('lc_ed_repo')")
    assert repo and repo.endswith("/" + BENCH), (
        "connection still points at %r — the pair was never completed" % repo)


@then("the course key is asked through a named credential form")
def step_key_form_contract(context):
    # the browser files a password under the USERNAME next to it; without one
    # it steals whatever text it saw last on the page ("Milwaukee", a grid
    # cell, became a credential in the field). The contract: a real form,
    # autocomplete on, a readonly lc-course-key identity beside the key.
    form = context.page.locator(".lc-join form.lcj-course")
    expect(form).to_be_attached(timeout=10_000)
    assert form.get_attribute("autocomplete") == "on"
    user = form.locator('input[autocomplete="username"]')
    expect(user).to_have_value("lc-course-key")
    assert user.get_attribute("readonly") is not None
    key = form.locator('input[type="password"]')
    assert key.get_attribute("autocomplete") == "current-password"


# ── the energy key survives everything except a real rejection ───────────
# Michel, 2026-08-05: the key had to be pasted again after every refresh.
# The door saved it ONLY on a clean 200, so a website-restricted key (403)
# or a blocked road (fetch rejected) discarded a key that was perfectly
# good. Only 400/401 — the provider saying the key itself is wrong — may
# throw one away.

ENERGY_SLOT = "lc_ai_key_gemini"


@given("the energy provider will not let us test the key")
def step_energy_forbidden(context):
    context.page.route(
        "**/generativelanguage.googleapis.com/**/models*",
        lambda r: r.fulfill(
            status=403, content_type="application/json",
            body='{"error": {"message": "Requests from referer are blocked."}}'))


@given("the energy provider cannot be reached at all")
def step_energy_unreachable(context):
    # abort = no HTTP answer ever arrives, an ad-blocker's view of the world
    context.page.route(
        "**/generativelanguage.googleapis.com/**/models*",
        lambda r: r.abort())


@then("the energy step says the key is saved but untested")
def step_energy_saved_untested(context):
    m = context.page.locator('[data-m="5"]')
    expect(m).to_contain_text("Key saved", timeout=10_000)
    # VISIBLE, not merely present: marking the step done folds its body away,
    # and this is the one message a learner actually has to read
    expect(m).to_be_visible(timeout=5_000)


@then("the energy key is on this device")
def step_energy_key_present(context):
    context.page.wait_for_function(
        "k => !!localStorage.getItem(k)", arg=ENERGY_SLOT, timeout=10_000)


@then("no energy key is on this device")
def step_energy_key_absent(context):
    # settle first: a save would land inside the check's promise chain, so
    # reading straight away could pass by being early rather than by being right
    context.page.wait_for_timeout(1200)
    got = context.page.evaluate("k => localStorage.getItem(k)", ENERGY_SLOT)
    assert not got, "a rejected key was saved: " + str(got)


@given('an energy key "{key}" is on this device')
def step_energy_key_seeded(context, key):
    context.page.add_init_script(
        "localStorage.setItem(%s, %s);" % (json.dumps(ENERGY_SLOT), json.dumps(key))
    )


@then("the energy step is already done")
def step_energy_step_done(context):
    step = context.page.locator('.lcj-step[data-n="5"]')
    expect(step).to_have_class(re.compile(r"\bok\b"), timeout=15_000)
    expect(context.page.locator('[data-m="5"]')).to_contain_text(
        "already saved", timeout=10_000)


@then("no repository was created by the wizard")
def step_no_repo_created(context):
    """The wizard only reads and syncs. Bays are the console's act, and
    since A′ the bench fork is the desk's — the wizard asks for neither."""
    context.page.wait_for_timeout(800)
    assert getattr(context, "bay_created", None) is None, \
        "the wizard created a repo: %r" % (context.bay_created,)
    assert getattr(context, "fork_posted", None) is None, \
        "the wizard forked a bench: %r" % (context.fork_posted,)


# ── one bench per SESSION: last term's is never inherited ───────────────────

@given("last term's session is still in the org")
def step_last_term_hub(context):
    """Its hub was touched more recently than this term's — the wizard used
    to take that as "the session" (Michel, 2026-08-31)."""
    context.join_stub["last_term"] = True


@given("this device is still paired to last term's bench")
def step_stale_pairing(context):
    if not hasattr(context, "join_stub"):
        context.join_stub = {"vault_ok": False}
    context.page.add_init_script(
        "localStorage.setItem('lc_ed_repo','%s');"
        "localStorage.setItem('lc_ed_session','build-ai-summer26');"
        "localStorage.setItem('lc_ed_pat','ghp_stored');" % OLD_BENCH)


@given("this device carries a pairing from before the stamp")
def step_unstamped_pairing(context):
    """The state every device was in until 2026-09-01: a bench, no session.
    The page cannot ask the address either — a cached door serves no hub."""
    if not hasattr(context, "join_stub"):
        context.join_stub = {"vault_ok": False}
    context.page.add_init_script(
        "localStorage.setItem('lc_ed_repo','%s');"
        "localStorage.setItem('lc_ed_pat','ghp_stored');" % OLD_BENCH)


@when("I open a saving lesson with no session in its address")
def step_open_bare_lesson(context):
    context.page.goto(context.base_url + "/components/datagrid",
                      wait_until="domcontentloaded")
    context.page.wait_for_selector('[data-lc-id="repair_me"] .lc-dg-save',
                                   timeout=20_000)
    context.page.wait_for_timeout(400)


@then("the keep button is armed")
def step_keep_armed(context):
    """A page that names no class has nothing to contradict — the bench the
    device was given still saves, exactly as before the session rule."""
    keep = context.page.locator('[data-lc-id="repair_me"] .lc-dg-save').first
    expect(keep).to_be_enabled(timeout=20_000)
    t = context.page.evaluate("() => window.lcBench.target(document.body)")
    assert t.get("repo") == OLD_BENCH, t


@when('I open a saving lesson framed for "{session}"')
def step_open_framed_lesson(context, session):
    """A course page carries the session in its address — the door bakes it —
    and holds a grid that saves into the bench."""
    context.page.goto(context.base_url + "/components/datagrid?hub=" + session,
                      wait_until="domcontentloaded")
    context.page.wait_for_selector('[data-lc-id="repair_me"] .lc-dg-save',
                                   timeout=20_000)
    context.page.wait_for_timeout(400)


@then('the bench step names the session "{session}"')
def step_bench_names_session(context, session):
    m = context.page.locator('.lc-join [data-m="4"]')
    expect(m).to_contain_text(session, timeout=20_000)
    assert "summer26" not in (m.text_content() or ""), \
        "the wizard reached for last term: %r" % m.text_content()


@then("this device is paired to no bench")
def step_no_pairing(context):
    repo = context.page.evaluate("() => localStorage.getItem('lc_ed_repo') || ''")
    assert not repo, "still paired to %s" % repo


@then("the keep button says the bench for this session is not paired")
def step_keep_refuses(context):
    keep = context.page.locator('[data-lc-id="repair_me"] .lc-dg-save').first
    expect(keep).to_be_disabled(timeout=20_000)
    title = keep.get_attribute("title") or ""
    assert "build-ai-fall26" in title and "paired" in title, title
    t = context.page.evaluate(
        "() => window.lcBench.target(document.body)")
    assert not t.get("repo"), "a page of this session reached last term's bench"
