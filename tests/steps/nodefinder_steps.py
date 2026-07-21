from behave import given, when, then
from playwright.sync_api import expect

# 1×1 transparent PNG — the site probe only needs a loadable image
PNG = (b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
       b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
       b"\x00\x00\x05\x00\x01\r\n-\xb3\x00\x00\x00\x00IEND\xaeB`\x82")


@given('a stubbed fork "{user}" whose site is live')
def step_fork_live(context, user):
    context.node_stub = {"user": user, "repo": True, "site": True}


@given('a stubbed fork "{user}" whose site is not live')
def step_fork_dark(context, user):
    context.node_stub = {"user": user, "repo": True, "site": False}


@given('a stubbed missing fork "{user}"')
def step_fork_missing(context, user):
    context.node_stub = {"user": user, "repo": False, "site": False}


def _routes(context):
    st = context.node_stub
    u = st["user"]

    def repo_route(route):
        if st["repo"]:
            route.fulfill(status=200, json={"name": "lightcodepedia"})
        else:
            route.fulfill(status=404, json={"message": "Not Found"})

    context.page.route("https://api.github.com/repos/%s/lightcodepedia" % u, repo_route)

    def deploy_route(route):
        # a live site has github-pages deployments; a dark fork has none
        route.fulfill(status=200, json=[{"id": 1}] if st["site"] else [])

    context.page.route(
        "https://api.github.com/repos/%s/lightcodepedia/deployments*" % u, deploy_route)

    def img_route(route):
        if st["site"]:
            route.fulfill(status=200, content_type="image/png", body=PNG)
        else:
            route.fulfill(status=404, body="")

    context.page.route("https://%s.github.io/lightcodepedia/assets/lab.jpg*" % u, img_route)
    context.page.route(
        "https://%s.github.io/lightcodepedia/" % u,
        lambda r: r.fulfill(status=200, content_type="text/html",
                            body="<h1>LightNode home</h1>"))


@when('I visit the node "{handle}"')
def step_visit_node(context, handle):
    _routes(context)
    context.page.goto(context.base_url + "/" + handle, wait_until="domcontentloaded")


@then('I land on the "{user}" LightNode')
def step_landed(context, user):
    # poll the URL rather than wait_for_url: the router's location.replace is
    # a cross-origin navigation, and failing here should REPORT where we are
    for _ in range(40):
        if user + ".github.io" in context.page.url:
            return
        context.page.wait_for_timeout(250)
    raise AssertionError("stayed on " + context.page.url)


@then("the router explains the site is not switched on")
def step_not_switched_on(context):
    expect(context.page.locator("body")).to_contain_text("switched on", timeout=10_000)


@then("the router invites to start a LightNode")
def step_invites(context):
    expect(context.page.locator("body")).to_contain_text("start yours", timeout=10_000)
