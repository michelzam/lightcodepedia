"""🚀 Ship — the author-designed deployment component.

The bay is a PUBLIC repo (or a folder inside one, bay="owner/repo/base").
These steps stub both sides of a ship: the source repo the assignment
renders from, and the bay's contents API + raw host. PUTs are captured so
the scenario can assert exactly what crossed the wire — the discipline of
rt_save, applied to deployment.
"""
import json

from behave import given, when, then
from playwright.sync_api import expect


@given("I am signed in with a course key")
def step_course_key(context):
    context.page.add_init_script("localStorage.setItem('lc_ed_pat','ghp_stub');")


@given('the bench HEAD commit is "{sha}"')
def step_head_commit(context, sha):
    body = json.dumps([{"sha": sha}])

    def fulfill(route):
        route.fulfill(status=200, content_type="application/json", body=body)
    context.page.route("**/api.github.com/repos/**/commits*", fulfill)


@given("the bay accepts writes")
def step_bay_accepts(context):
    """Capture every PUT to the bay; GET of a not-yet-written path 404s the
    way a fresh bay would. The manifest is served from what ship PUT there,
    so the manifest assertion reads what actually crossed the wire."""
    context.bay_puts = {}

    def handle(route):
        req = route.request
        path = req.url.split("/contents/", 1)[1].split("?")[0]
        if req.method == "PUT":
            context.bay_puts[path] = json.loads(req.post_data or "{}")
            return route.fulfill(status=201, content_type="application/json",
                                 body=json.dumps({"content": {"path": path}}))
        if path in context.bay_puts:
            import base64
            raw = context.bay_puts[path].get("content", "")
            return route.fulfill(status=200, content_type="text/plain; charset=utf-8",
                                 body=base64.b64decode(raw).decode("utf-8"))
        return route.fulfill(status=404, content_type="application/json",
                             body='{"message":"Not Found"}')
    context.page.route("**/api.github.com/repos/acme/bay/contents/**", handle)


@given('the bay manifest points "{app}" at "{sha}" with entry "{entry}"')
def step_bay_manifest(context, app, sha, entry):
    body = json.dumps({app: {"sha": sha, "entry": entry, "files": [entry]}})

    def fulfill(route):
        route.fulfill(status=200, content_type="application/json", body=body)
    context.page.route("**/raw.githubusercontent.com/acme/bay/**/manifest.json*", fulfill)


@given("the bay has no manifest")
def step_bay_no_manifest(context):
    def fulfill(route):
        route.fulfill(status=404, content_type="text/plain", body="404")
    context.page.route("**/raw.githubusercontent.com/acme/bay/**/manifest.json*", fulfill)


@given('the bay serves "{path}" with the document')
@given('the bay serves "{path}" with the document:')
def step_bay_serves(context, path):
    body = context.text

    def fulfill(route):
        route.fulfill(status=200, content_type="text/plain; charset=utf-8", body=body)
    context.page.route("**/api.github.com/repos/acme/bay/contents/" + path + "*", fulfill)
    context.page.route("**/raw.githubusercontent.com/acme/bay/**/" + path.split("/")[-1] + "*", fulfill)


@then("the ship button is disarmed with a reason")
def step_ship_disarmed(context):
    btn = context.page.locator(".lc-ship button").first
    expect(btn).to_be_visible(timeout=15_000)
    expect(btn).to_be_disabled()
    reason = context.page.locator(".lc-ship .lc-ship-status").first
    assert reason.inner_text().strip(), "a disarmed button must say why"


@when("I press the ship button")
def step_press_ship(context):
    btn = context.page.locator(".lc-ship button").first
    expect(btn).to_be_enabled(timeout=15_000)
    btn.click()
    context.page.wait_for_timeout(1500)


@then('the bay received "{path}"')
def step_bay_received(context, path):
    assert path in context.bay_puts, \
        "bay got %r" % (sorted(context.bay_puts.keys()),)


@then('the bay manifest now points "{app}" at "{sha}"')
def step_manifest_updated(context, app, sha):
    puts = {p: b for p, b in context.bay_puts.items() if p.endswith("manifest.json")}
    assert puts, "no manifest was written: %r" % (sorted(context.bay_puts.keys()),)
    import base64
    body = json.loads(base64.b64decode(list(puts.values())[0]["content"]).decode("utf-8"))
    assert app in body and body[app]["sha"] == sha, body


@then("the ship button reports the shipped link")
def step_ship_reports(context):
    status = context.page.locator(".lc-ship .lc-ship-status").first
    expect(status).to_contain_text("Shipped", timeout=15_000)
    link = context.page.locator(".lc-ship .lc-ship-status a").first
    href = link.get_attribute("href") or ""
    assert "#src=gh:acme/bay/" in href, href


@then('the ship embed renders "{text}"')
def step_ship_embed_renders(context, text):
    inner = context.page.locator(".lc-runner-embed .lc-run").first
    expect(inner).to_contain_text(text, timeout=20_000)


@then("the ship embed says nothing is shipped yet")
def step_ship_embed_waiting(context):
    status = context.page.locator(".lc-runner-embed .lc-run-status").first
    expect(status).to_contain_text("othing shipped yet", timeout=20_000)
