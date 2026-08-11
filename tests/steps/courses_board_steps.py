import base64
import json

from behave import given, when, then
from playwright.sync_api import expect

LAB = "michelzam/lightcodelab"
VAULT = "acme/acme-vault"
COURSE = "demo"


def _tree(paths, prefix):
    return {"tree": [{"type": "blob", "path": prefix + p, "sha": "sha-" + p}
                     for p in paths]}


@given('the board\'s lab holds "{a}" "{b}" "{c}" "{d}"')
def step_lab_holds(context, a, b, c, d):
    context.board_lab = [a, b, c, d]


@given('the board\'s vault holds "{a}"')
def step_vault_holds(context, a):
    context.board_vault = [a]


@when("I open the material board")
def step_open_board(context):
    lab = _tree(context.board_lab, "courses/%s/" % COURSE)
    vault = _tree(context.board_vault, "courses/%s/" % COURSE)
    cfg = "vault: %s\npath: courses\n" % VAULT

    def handler(route, request=None):
        url = route.request.url
        if "/contents/courses/%s/__course.yml" % COURSE in url:
            # the board asks for it raw
            route.fulfill(status=200, content_type="text/plain", body=cfg)
        elif "/contents/courses" in url:
            route.fulfill(status=200, json=[{"name": COURSE, "type": "dir"}])
        elif "/repos/%s/git/trees" % LAB in url:
            route.fulfill(status=200, json=lab)
        elif "/repos/%s/git/trees" % VAULT in url:
            route.fulfill(status=200, json=vault)
        else:
            route.fulfill(status=404, json={"message": "stub"})

    context.page.route("https://api.github.com/**", handler)
    context.page.add_init_script(
        "localStorage.setItem('lc_ed_pat','ghp_author');"
        "localStorage.setItem('lc_ed_repo','%s');" % LAB)
    context.page.goto(context.base_url + "/lab/material", wait_until="domcontentloaded")
    context.page.wait_for_timeout(2500)


@then('the course reads "{state}"')
def step_course_state(context, state):
    got = context.page.evaluate(
        "() => ((window.lcDatasets || {}).lc_courses || []).map(r => r.state)")
    assert state in (got or []), "board says %r, expected %r" % (got, state)
