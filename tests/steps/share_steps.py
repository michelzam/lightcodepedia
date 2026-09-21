"""🔗 Share unlisted — the owner's row in the account menu (rt_share.feature)."""
import base64 as _b64
import json as _json
import re

from behave import given, when, then
from playwright.sync_api import expect

LAB = "michelzam/lightcodelab"
CONTENTS = "**/api.github.com/repos/" + LAB + "/contents/"


def _puts(context):
    if not hasattr(context, "share_puts"):
        context.share_puts = []      # (method, path, body)
    return context.share_puts


def _serve_share_files(context):
    """every PUT/DELETE under docs/share/ is recorded and answered 200"""
    puts = _puts(context)

    def fulfill(route):
        req = route.request
        if req.method in ("PUT", "DELETE"):
            puts.append((req.method, req.url.split("/contents/", 1)[1].split("?")[0], req.post_data or ""))
            route.fulfill(status=200, content_type="application/json",
                          body='{"content":{"sha":"new"},"commit":{"sha":"c"}}')
            return
        route.fulfill(status=404, content_type="application/json", body="{}")
    context.page.route(CONTENTS + "docs/share/**", fulfill)


@given("the lab's share folder is empty")
def step_share_empty(context):
    _serve_share_files(context)
    context.page.route(CONTENTS + "docs/share",
                       lambda r: r.fulfill(status=404, content_type="application/json", body="{}"))


@given('the lab\'s share folder already holds "{src}" under "{sid}"')
def step_share_holds(context, src, sid):
    _serve_share_files(context)
    name = src.split("/")[-1]
    folder = "docs/share/" + sid
    context.page.route(CONTENTS + "docs/share",
                       lambda r: r.fulfill(status=200, content_type="application/json",
                                           body=_json.dumps([{"type": "dir", "name": sid, "path": folder}])))
    context.page.route(CONTENTS + folder,
                       lambda r: r.fulfill(status=200, content_type="application/json",
                                           body=_json.dumps([{"type": "file", "name": name, "path": folder + "/" + name, "sha": "old-sha"}])))
    doc = "---\nlc_share_of: " + src + "\n---\n# old copy\n"

    def file_route(route):
        if route.request.method == "GET":
            route.fulfill(status=200, content_type="application/json",
                          body=_json.dumps({"content": _b64.b64encode(doc.encode()).decode(), "sha": "old-sha"}))
            return
        _puts(context).append((route.request.method, folder + "/" + name, route.request.post_data or ""))
        route.fulfill(status=200, content_type="application/json", body='{"content":{"sha":"new"}}')
    context.page.route(CONTENTS + folder + "/" + name, file_route)


@given('the lab serves "{path}" with the document')
@given('the lab serves "{path}" with the document:')
def step_lab_serves(context, path):
    doc = context.text
    context.share_src_dir = path.rsplit("/", 1)[0]

    def fulfill(route):
        route.fulfill(status=200, content_type="application/json",
                      body=_json.dumps({"content": _b64.b64encode(doc.encode()).decode(), "sha": "src-sha"}))
    context.page.route(CONTENTS + path, fulfill)


@given('the lab serves the files "{a}" and "{b}" beside it')
def step_lab_serves_files(context, a, b):
    def serve(payload):
        return lambda r: r.fulfill(status=200, content_type="application/json",
                                   body=_json.dumps({"content": _b64.b64encode(payload).decode(), "sha": "f"}))
    for name in (a, b):
        context.page.route(CONTENTS + context.share_src_dir + "/" + name, serve(("bytes of " + name).encode()))


def _open_account_menu(context):
    btn = context.page.locator("#lc-user-btn")
    expect(btn).to_be_visible(timeout=10_000)
    btn.click()
    context.page.wait_for_function(
        "() => document.getElementById('lc-user-drop').classList.contains('open')", timeout=5_000)


@when("I choose Share unlisted in my account menu")
def step_choose_share(context):
    _open_account_menu(context)
    row = context.page.locator("#lc-ud-share")
    expect(row).to_be_visible(timeout=10_000)
    row.click()




@then('the share dialog offers a link, an iframe and a QR code for "{tail}"')
def step_dialog(context, tail):
    url = context.page.locator(".lc-share .lc-share-url")
    expect(url).to_be_visible(timeout=15_000)
    pat = re.compile(r"^" + re.escape(context.base_url) + r"/share/" +
                     (re.escape(tail) if "/" in tail else r"[0-9a-f]{12}/" + re.escape(tail)) + r"$")
    expect(url).to_have_value(pat)
    link = url.input_value()
    context.share_link = link
    expect(context.page.locator(".lc-share .lc-share-iframe")).to_have_value(re.compile(r'<iframe src="' + re.escape(link) + '"'))
    expect(context.page.locator(".lc-share .lc-share-qr")).to_have_attribute("data-lc-text", link)


@then('the page was copied to the share folder with "{a}" and "{b}"')
def step_copied(context, a, b):
    sid = context.share_link.split("/share/")[1].split("/")[0]
    paths = {p: body for m, p, body in _puts(context) if m == "PUT"}
    page = "docs/share/" + sid + "/qr.md"
    assert page in paths, paths.keys()
    content = _b64.b64decode(_json.loads(paths[page])["content"]).decode()
    assert content.startswith("---\nlc_share_of: docs/components/qr.md\n---\n# QR page"), content
    for name in (a, b):
        assert "docs/share/" + sid + "/" + name in paths, paths.keys()


@then('the share was refreshed in place under "{sid}"')
def step_refreshed(context, sid):
    hits = []
    for _ in range(40):
        hits = [(p, body) for m, p, body in _puts(context) if m == "PUT" and p == "docs/share/" + sid + "/qr.md"]
        if hits:
            break
        context.page.wait_for_timeout(250)
    assert hits, [p for _, p, _ in _puts(context)]
    body = _json.loads(hits[-1][1])
    assert body.get("sha") == "old-sha", body       # an update, not a second copy
    assert "QR page, edited" in _b64.b64decode(body["content"]).decode()
    assert not [p for m, p, _ in _puts(context) if m == "PUT" and sid not in p], "a second folder was created"


@when("I press Unshare")
def step_unshare(context):
    context.page.locator(".lc-share .lc-share-off").click()


@then('the share folder "{sid}" was emptied')
def step_emptied(context, sid):
    for _ in range(40):
        if any(m == "DELETE" and p == "docs/share/" + sid + "/qr.md" for m, p, _ in _puts(context)):
            expect(context.page.locator(".lc-share .lc-share-status")).to_contain_text("Unshared", timeout=5_000)
            return
        context.page.wait_for_timeout(250)
    raise AssertionError("no DELETE reached the share folder: " + str([(m, p) for m, p, _ in _puts(context)]))


@given('the lab hides "{path}" from this key')
def step_lab_hides(context, path):
    for p in (path, path.replace(".md", "/index.md")):
        context.page.route(CONTENTS + p,
                           lambda r: r.fulfill(status=404, content_type="application/json", body='{"message":"Not Found"}'))


@then('the share dialog says the key cannot see "{repo}"')
def step_dialog_no_access(context, repo):
    st = context.page.locator(".lc-share .lc-share-status")
    expect(st).to_contain_text("Your key cannot see " + repo, timeout=15_000)
    expect(st).to_contain_text("Contents read and write")


@then("the share dialog says the page is not shared")
def step_not_shared(context):
    expect(context.page.locator(".lc-share .lc-share-status")).to_contain_text("Not shared", timeout=15_000)
    expect(context.page.locator(".lc-share .lc-share-go")).to_be_visible()
    assert not context.page.locator(".lc-share .lc-share-off").is_visible()


@then("the share dialog says the page is shared")
def step_is_shared(context):
    expect(context.page.locator(".lc-share .lc-share-status")).to_contain_text("Shared", timeout=15_000)
    expect(context.page.locator(".lc-share .lc-share-refresh")).to_be_visible()
    expect(context.page.locator(".lc-share .lc-share-off")).to_be_visible()


@when("I press Share")
def step_press_share(context):
    btn = context.page.locator(".lc-share .lc-share-go")
    expect(btn).to_be_enabled(timeout=15_000)
    btn.click()


@when("I press Refresh")
def step_press_refresh(context):
    btn = context.page.locator(".lc-share .lc-share-refresh")
    expect(btn).to_be_enabled(timeout=15_000)
    btn.click()


@then("the page reads as a shared page of Lightcodepedia")
def step_reader_chrome(context):
    expect(context.page.locator("html")).to_have_class(re.compile(r"\blc-shared\b"), timeout=10_000)
    brand = context.page.locator("#lc-topbar .lc-brand")
    expect(brand).to_have_attribute("href", "https://lightcodepedia.org/")
    for sel in ("#lc-start-pill", "#lc-user-pill", ".lc-slides-fab", ".lc-edit-fab"):
        assert not context.page.locator(sel).first.is_visible(), sel + " shows on a shared page"
    hrefs = context.page.evaluate("() => Array.from(document.querySelectorAll('#lc-topbar .lc-links a')).map(a => a.href)")
    assert hrefs and all(h.startswith("https://lightcodepedia.org/") for h in hrefs), hrefs
