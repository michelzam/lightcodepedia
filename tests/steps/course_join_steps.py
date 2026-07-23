import json
import re

from behave import given, when, then
from playwright.sync_api import expect


HUB = {"name": "build-ai-fall26", "is_template": True, "fork": False,
       "default_branch": "main", "updated_at": "2026-07-01T00:00:00Z"}
BENCH = "build-ai-fall26-zamm-student"


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
            route.fulfill(status=200, json=[HUB] if st.get("vault_ok") else [])
            return
        if re.search(r"/repos/[^/]+/[^/]+/contents/", url) and method == "GET":
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
            if method == "GET":
                if st.get("bench"):
                    route.fulfill(status=200, json={"name": BENCH, "default_branch": "main"})
                else:
                    route.fulfill(status=404, json={"message": "Not Found"})
                return
        if url.endswith("/forks") and method == "POST":
            st["bench"] = True             # fork lands in the org as the bench
            route.fulfill(status=202, json={"name": BENCH})
            return
        if re.search(r"/repos/[^/]+/[^/]+$", url) and method == "GET":
            # repo metadata: visible exactly when the student has vault access
            if st.get("vault_ok"):
                route.fulfill(status=200, json={"name": "uwm-build-ai-vault"})
            else:
                route.fulfill(status=404, json={"message": "Not Found"})
            return
        route.fulfill(status=404, json={"message": "stub"})

    context.page.route("https://api.github.com/**", handler)


@given("a stubbed GitHub that accepts the key with repo scope")
def step_stub_key(context):
    context.join_stub = {"vault_ok": False}


@given("the student can read the vault")
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
    context.page.click('.lc-join [data-a="checkkey"]')
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


@then("the wizard says the student is in")
def step_is_in(context):
    expect(context.page.locator('.lc-join [data-m="3"]')).to_contain_text("You’re in", timeout=6000)


@then("the open-course door points at the vault entry")
def step_door(context):
    a = context.page.locator(".lc-join [data-open] a")
    expect(a).to_be_visible(timeout=6000)
    href = a.get_attribute("href") or ""
    assert "run.html#src=gh:uwm-build-ai/uwm-build-ai-vault/courses/micro_build_ai/index.md" in href, href


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


@then("the bench step offers the fork")
def step_offers_fork(context):
    expect(context.page.locator('.lc-join [data-a="fork"]')).to_be_visible(timeout=8000)


@when("I fork my bench")
def step_fork_bench(context):
    context.page.click('.lc-join [data-a="fork"]')
    context.page.wait_for_timeout(1500)


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


@then("the bench door opens in the runner")
def step_bench_door(context):
    a = context.page.locator(".lc-join [data-bench] a")
    expect(a).to_be_visible(timeout=6000)
    href = a.get_attribute("href") or ""
    assert "run.html#src=gh:uwm-build-ai/" + BENCH + "/index.md" in href, href
    assert "github.com/" not in href, href


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
