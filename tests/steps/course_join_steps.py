import json
import re

from behave import given, when, then
from playwright.sync_api import expect


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
        if re.search(r"/repos/[^/]+/[^/]+/contents/", url) and method == "GET":
            if st.get("vault_ok"):
                route.fulfill(status=200, json={"name": "index.md", "sha": "s"})
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
