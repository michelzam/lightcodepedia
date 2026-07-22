import json
import re

from behave import given, when, then
from playwright.sync_api import expect

LAB = "michelzam/lightcodelab"
RAW = "https://api.github.com/_raw/"
LESSON = "# Intro lesson\n\nA first lesson on the shelf.\n"


def _routes(context):
    variables = getattr(context, "node_vars", None)

    def handler(route):
        url = route.request.url
        if "/actions/variables" in url:
            # node variables: per-node configuration, owner-readable only
            if variables is None:
                route.fulfill(status=404, json={"message": "Not Found"})
            else:
                route.fulfill(status=200, json={"variables": variables})
            return
        if url.startswith(RAW):
            route.fulfill(status=200, content_type="text/plain", body=LESSON)
            return
        m = re.search(r"/contents/(.+?)(?:\?|$)", url)
        if m:
            folder = m.group(1)
            route.fulfill(status=200, json=[
                {"type": "file", "name": "intro.md", "path": folder + "/intro.md",
                 "download_url": RAW + folder + "/intro.md",
                 "url": "https://api.github.com/none"},
            ])
            return
        route.fulfill(status=404, json={"message": "stub"})

    context.page.route("https://api.github.com/**", handler)


@given('a stubbed lab tree where COURSE_PATH is "{val}"')
def step_stub_tree_vars(context, val):
    context.node_vars = [{"name": "COURSE_PATH", "value": val}]


@given("a stubbed lab tree with no node variables")
def step_stub_tree_novars(context):
    context.node_vars = None


@when("I open the material page without a key")
def step_open_material_bare(context):
    context.page.goto(context.base_url + "/lab/material", wait_until="domcontentloaded")
    context.page.wait_for_selector(".lc-cards", timeout=10_000)
    context.page.wait_for_timeout(800)


@when("I open the material page")
def step_open_material(context):
    _routes(context)
    context.page.add_init_script(
        "localStorage.setItem('lc_ed_pat','ghp_author');"
        "localStorage.setItem('lc_ed_repo','" + LAB + "');")
    context.page.goto(context.base_url + "/lab/material", wait_until="domcontentloaded")
    context.page.wait_for_selector(".lc-cards .lc-card[data-url]", timeout=10_000)


@then("the shelf asks for the author key")
def step_shelf_locked(context):
    expect(context.page.locator(".lc-cards").first).to_contain_text("author key", timeout=8000)


@then('a "{folder}" card opens in the runner')
def step_card_runner(context, folder):
    card = context.page.locator('.lc-cards .lc-card[data-url*="%s/intro.md"]' % folder).first
    expect(card).to_be_visible(timeout=8000)
    href = card.locator("a").first.get_attribute("href") or ""
    assert "run.html#src=gh:" + LAB + "/" + folder + "/intro.md" in href, href
    expect(card).to_contain_text("Intro lesson")


@then("the topbar offers the HQ door")
def step_hq_door(context):
    link = context.page.locator("#lc-topbar .lc-links a", has_text="HQ").first
    expect(link).to_be_visible(timeout=8000)
    assert "/lab/" in (link.get_attribute("href") or "")


@when("I open the HQ landing")
def step_open_hq(context):
    context.page.goto(context.base_url + "/lab/", wait_until="domcontentloaded")
    context.page.wait_for_timeout(1200)


@then("the landing offers doors to classroom and material")
def step_hq_cards(context):
    body = context.page.locator("main")
    expect(body.locator("a", has_text="Open the classroom").first).to_be_visible(timeout=10_000)
    expect(body.locator("a", has_text="Open the shelf").first).to_be_visible()


@then("the topbar menu lists the classroom and the shelf")
def step_lab_menu(context):
    links = context.page.locator("#lc-topbar .lc-links")
    expect(links.locator("a", has_text="Classroom").first).to_be_visible(timeout=8000)
    expect(links.locator("a", has_text="Material").first).to_be_visible()
