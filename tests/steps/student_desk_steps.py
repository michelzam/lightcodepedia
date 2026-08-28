"""The triptych desk: switchboard into Navigate360, PAWS and Canvas."""
import base64
import json

from behave import given, then, when
from playwright.sync_api import expect

FACTS = [
    {"name": "Lovelace, Ada", "email": "ada@uwm.edu", "canvas_id": 111,
     "sis": "123", "score": 88, "grade": "A", "last_activity": "2026-08-20",
     "hours": 12.5},
    {"name": "Newcomer, Zik", "email": "zik@uwm.edu", "canvas_id": 222,
     "sis": "456", "score": None, "grade": "", "last_activity": "",
     "hours": 0},
]


def _key(context):
    context.page.add_init_script("localStorage.setItem('lc_ed_pat','ghp_author');")


@given("a connected author key on the triptych")
def step_tri_key(context):
    _key(context)


@given("a connected author key and a stubbed facts gate")
def step_tri_gate(context):
    _key(context)
    b64 = base64.b64encode(json.dumps(FACTS).encode()).decode()

    def gh(route):
        url = route.request.url
        if "/actions/workflows/" in url and route.request.method == "POST":
            route.fulfill(status=204, body="")
        elif "/commits/main/statuses" in url:
            route.fulfill(json=[{
                "context": "lc/student-facts", "state": "success",
                "created_at": "2099-01-01T00:00:00Z", "description": "c" * 40}])
        elif "/git/blobs/" in url:
            route.fulfill(json={"content": b64, "encoding": "base64"})
        else:
            route.fulfill(status=404, json={"message": "not stubbed"})

    context.page.route("https://api.github.com/repos/**", gh)


@then("the triptych offers fetch, card and roster")
def step_tri_stands(context):
    expect(context.page.locator("[data-lc-id='tri_desk'] button")).to_be_visible(timeout=20_000)
    expect(context.page.locator(".lc-tri-card")).to_be_visible()
    expect(context.page.locator(".lc-tri-card")).to_contain_text("Fetch the roster")


@then("the HQ card links to the triptych")
def step_tri_hq(context):
    context.page.goto(context.base_url + "/lab/", wait_until="domcontentloaded")
    expect(context.page.locator('a[href*="/lab/students"]').first).to_be_visible(timeout=20_000)


@when("I press the triptych fetch button")
def step_tri_fetch(context):
    context.page.click("[data-lc-id='tri_desk'] button")
    context.page.wait_for_timeout(1500)


@when('I pick "{who}" in the triptych roster')
def step_tri_pick(context, who):
    row = context.page.locator(
        "[data-lc-id='tri_roster'] tbody tr").filter(has_text=who).first
    row.click()
    context.page.wait_for_timeout(400)


@then('the card shows the canvas facts "{score}" and "{when_}"')
def step_tri_facts(context, score, when_):
    card = context.page.locator(".lc-tri-card")
    expect(card).to_contain_text("Lovelace", timeout=10_000)
    expect(card).to_contain_text(score)
    expect(card).to_contain_text(when_)


@then('the "{sys}" launcher aims at "{piece}"')
def step_tri_aim(context, sys, piece):
    href = context.page.get_attribute(
        ".lc-tri-card [data-sys='%s']" % sys, "href") or ""
    assert piece in href, "%s launcher: %s" % (sys, href)


@when('I type "{eab}" as the Navigate id')
def step_tri_type_eab(context, eab):
    box = context.page.locator(".lc-tri-card [data-eab]")
    box.fill(eab)
    box.press("Enter")
    context.page.wait_for_timeout(300)


@then("the Navigate id is kept in this browser only")
def step_tri_eab_kept(context):
    kept = context.page.evaluate("localStorage.getItem('lc_eab_ids')") or ""
    assert "8679020" in kept, kept
