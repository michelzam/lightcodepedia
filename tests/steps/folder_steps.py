import base64
import json
import re

from behave import given, when, then
from playwright.sync_api import expect

# The .folder shelf on a runner render enumerates via the GitHub contents
# API; these steps stub the listing, the raw page bodies, and the write
# endpoints (PUT/DELETE) so the trash flow can be asserted end to end.


@given('the folder "{dirpath}" is empty')
def step_stub_empty_folder(context, dirpath):
    step_stub_folder(context, dirpath, "")


@given('the folder "{dirpath}" serves pages "{names}"')
def step_stub_folder(context, dirpath, names):
    files = []
    for n in names.split(","):
        n = n.strip()
        if not n:
            continue
        files.append({
            "type": "file", "name": n, "path": dirpath + "/" + n,
            "download_url": "https://raw.example.org/" + dirpath + "/" + n,
            "url": "https://api.github.com/repos/acme/demo/contents/" + dirpath + "/" + n,
        })
    listing = json.dumps(files)

    def serve_dir(route):
        route.fulfill(status=200, content_type="application/json", body=listing)

    def serve_raw(route):
        name = route.request.url.split("/")[-1]
        route.fulfill(status=200, content_type="text/plain",
                      body="# " + name.replace(".md", "").strip("_").title())

    context.page.route(
        "**/api.github.com/repos/**/contents/" + dirpath, serve_dir)
    context.page.route("**/raw.example.org/**", serve_raw)


@given('the folder file "{path}" accepts moves')
def step_stub_move_endpoints(context, path):
    context.moved_to = []
    body = base64.b64encode(b"# Alpha\n").decode()

    def handle(route):
        req = route.request
        if req.method == "GET":
            route.fulfill(status=200, content_type="application/json",
                          body=json.dumps({"content": body, "sha": "abc123"}))
        elif req.method == "DELETE":
            route.fulfill(status=200, content_type="application/json", body="{}")
        else:
            route.continue_()

    def handle_put(route):
        if route.request.method == "PUT":
            context.moved_to.append(
                route.request.url.split("/contents/")[-1])
            route.fulfill(status=201, content_type="application/json", body="{}")
        else:
            route.continue_()

    context.page.route("**/api.github.com/repos/**/contents/" + path, handle)
    context.page.route("**/api.github.com/repos/**/contents/**/_trash/**", handle_put)


@when("the page enters X-ray mode")
def step_enter_xray(context):
    context.page.evaluate("window.lcMode.set('xray')")
    context.page.wait_for_timeout(500)


@then('the shelf shows a card for "{title}"')
def step_shelf_shows(context, title):
    expect(context.page.locator(".lc-card", has_text=title).first)\
        .to_be_visible(timeout=10_000)


@then('the shelf hides "{title}" and every writing affordance')
def step_shelf_read_posture(context, title):
    expect(context.page.locator(".lc-card", has_text=title)).to_have_count(0)
    assert context.page.locator("[data-newpage]").count() == 0, "➕ New leaked into read posture"
    assert context.page.locator(".lc-card-gear").count() == 0, "⚙️ gear leaked into read posture"


@then("the shelf offers New and a gear on each file card")
def step_shelf_workbench(context):
    expect(context.page.locator("[data-newpage]")).to_be_visible(timeout=10_000)
    assert context.page.locator(".lc-card-gear").count() >= 2, "gears missing on file cards"
    # the workbench talks filenames: the real name sits before each gear
    expect(context.page.locator(".lc-card-fname", has_text="alpha.md").first)\
        .to_be_visible(timeout=5_000)


@then("the empty shelf offers no New button")
def step_empty_read(context):
    expect(context.page.get_by_text("No pages in")).to_be_visible(timeout=10_000)
    assert context.page.locator("[data-newpage]").count() == 0, "➕ New leaked into the read empty state"


@then("the empty shelf offers a New button")
def step_empty_workbench(context):
    expect(context.page.locator("[data-newpage]")).to_be_visible(timeout=10_000)


@when('I trash the "{title}" card')
def step_trash_card(context, title):
    card = context.page.locator(".lc-card", has_text=title).first
    context.page.once("dialog", lambda d: d.accept())
    card.locator(".lc-card-gear").click()
    card.locator("[data-act='trash']").click()
    context.page.wait_for_timeout(1000)


@then('the file was moved to "{prefix}"')
def step_moved_prefix(context, prefix):
    # the trash flow now writes TWO files (the born _trash/index.md, then
    # the moved file) — assert on whichever carries the prefix + suffix
    assert context.moved_to, "no move (PUT) request was issued"
    hits = [u for u in context.moved_to if u.startswith(prefix)]
    assert hits, context.moved_to
    if "_trash/" in prefix:
        assert any("_deleted_" in u for u in hits), context.moved_to


@then("the trash folder was born with its index")
def step_trash_born_with_index(context):
    # every folder is its index.md — _trash included, from its first use
    assert any(u.endswith("_trash/index.md") for u in context.moved_to), \
        context.moved_to


@given("the viewer can push to the repo")
def step_can_push(context):
    context.page.route(
        "**/api.github.com/repos/acme/demo",
        lambda r: r.fulfill(status=200, content_type="application/json",
                            body=json.dumps({"permissions": {"push": True}})))


@given("the viewer cannot push to the repo")
def step_cannot_push(context):
    context.page.route(
        "**/api.github.com/repos/acme/demo",
        lambda r: r.fulfill(status=200, content_type="application/json",
                            body=json.dumps({"permissions": {"push": False}})))


@given('the folder "{dirpath}" lists pages "{names}" plus subfolder "{sub}" with files "{tree}"')
def step_stub_folder_with_subdir(context, dirpath, names, sub, tree):
    step_stub_folder(context, dirpath, names)
    subdir = {
        "type": "dir", "name": sub, "path": dirpath + "/" + sub,
        "url": "https://api.github.com/repos/acme/demo/contents/" + dirpath + "/" + sub,
    }
    files = []
    for n in names.split(","):
        n = n.strip()
        if not n:
            continue
        files.append({
            "type": "file", "name": n, "path": dirpath + "/" + n,
            "download_url": "https://raw.example.org/" + dirpath + "/" + n,
            "url": "https://api.github.com/repos/acme/demo/contents/" + dirpath + "/" + n,
        })
    listing = json.dumps(files + [subdir])
    # LIFO: this listing (with the subdir) shadows the plain one
    context.page.route(
        "**/api.github.com/repos/**/contents/" + dirpath,
        lambda r: r.fulfill(status=200, content_type="application/json", body=listing))
    context.page.route(
        "**/api.github.com/repos/**/contents/" + dirpath + "/" + sub,
        lambda r: r.fulfill(status=200, content_type="application/json", body="[]"))
    blobs = [{"type": "blob", "path": dirpath + "/" + sub + "/" + f.strip()}
             for f in tree.split(",") if f.strip()]
    blobs += [{"type": "blob", "path": f2["path"]} for f2 in files]
    # real repos interleave tree entries — the move autocomplete feeds on them
    dirs = {dirpath, dirpath + "/" + sub}
    for b in blobs:
        parts = b["path"].split("/")[:-1]
        for i in range(1, len(parts) + 1):
            dirs.add("/".join(parts[:i]))
    blobs = [{"type": "tree", "path": d} for d in sorted(dirs)] + blobs
    context.page.route(
        "**/api.github.com/repos/**/git/trees/**",
        lambda r: r.fulfill(status=200, content_type="application/json",
                            body=json.dumps({"tree": blobs})))


@then('the subfolder card shows the census "{count}"')
def step_subfolder_census(context, count):
    chip = context.page.locator(".lc-card-fcount", has_text=count)
    expect(chip.first).to_be_visible(timeout=10_000)


@then('the shelf shows no card for "{title}"')
def step_shelf_no_card(context, title):
    context.page.wait_for_timeout(400)
    assert context.page.locator(".lc-card", has_text=title).count() == 0, \
        title + " leaked into the read posture"


@when('I tap the gear on the "{title}" card')
def step_tap_gear(context, title):
    card = context.page.locator(".lc-card", has_text=title).first
    card.locator(".lc-card-gear").tap()


@then("the card menu is open")
def step_card_menu_open(context):
    expect(context.page.locator(".lc-folder-menu")).to_be_visible(timeout=5_000)
    expect(context.page.locator("[data-act='trash']")).to_be_visible(timeout=2_000)


@then("the subfolder card offers a gear")
def step_subdir_gear(context):
    card = context.page.locator(".lc-card[data-dirpath]").first
    expect(card.locator(".lc-card-gear")).to_be_visible(timeout=5_000)


@when('I choose "{act}" on the "{title}" card')
def step_choose_menu_act(context, act, title):
    card = context.page.locator(".lc-card", has_text=title).first
    card.locator(".lc-card-gear").click()
    context.page.locator("[data-act='" + act + "']").click()


@then('the page URL carries "{a}" and "{b}"')
def step_url_carries(context, a, b):
    context.page.wait_for_function(
        "([a, b]) => location.href.includes(a) && location.href.includes(b)",
        arg=[a, b], timeout=10_000)


@given('moves into "{dest}" are accepted')
def step_accept_moves_into(context, dest):
    if not hasattr(context, "moved_to"):
        context.moved_to = []

    def handle_put(route):
        if route.request.method == "PUT":
            context.moved_to.append(route.request.url.split("/contents/")[-1])
            route.fulfill(status=201, content_type="application/json", body="{}")
        else:
            route.continue_()

    context.page.route("**/api.github.com/repos/**/contents/" + dest + "/**", handle_put)


@then('the destination autocomplete offers "{path}"')
def step_autocomplete_offers(context, path):
    expect(context.page.locator(".lc-folder-move input")).to_be_visible(timeout=5_000)
    context.page.wait_for_function(
        "(p) => Array.from(document.querySelectorAll('#lc-move-dirs option'))"
        ".some(o => o.value === p)",
        arg=path, timeout=10_000)


@when('I move it to "{dest}"')
def step_do_move(context, dest):
    context.moved_to = []
    inp = context.page.locator(".lc-folder-move input")
    inp.fill(dest)
    context.page.locator("[data-go]").click()
    context.page.wait_for_timeout(1000)


@given("course pages serve raw markdown")
def step_serve_raw_pages(context):
    def fulfill(route):
        name = route.request.url.split("/")[-1].replace(".md", "")
        route.fulfill(status=200, content_type="text/plain",
                      body="# " + name.title() + "\n\nSome prose.\n")
    # registered FIRST in the scenario: later, more specific routes win
    context.page.route(
        "**/api.github.com/repos/**/contents/courses/demo/mod/**", fulfill)


@then("the course map draws at least {n:d} nodes")
def step_course_map_nodes(context, n):
    context.page.wait_for_function(
        "(n) => document.querySelectorAll('.lc-sitemap svg .lc-sm-node circle').length >= n",
        arg=n, timeout=15_000)


@given('the subfolder "{dirpath}" carries an index with one quiz')
def step_subdir_index_quiz(context, dirpath):
    doc = "# Week One\n\n**Q:** Ready?\n\n- [x] Yes\n- [ ] No\n{: .quiz }\n"
    listing = json.dumps([{
        "type": "file", "name": "index.md", "path": dirpath + "/index.md",
        "download_url": "https://raw.example.org/" + dirpath + "/index.md",
        "url": "https://api.github.com/repos/acme/demo/contents/" + dirpath + "/index.md",
    }])
    context.page.route(
        "**/api.github.com/repos/**/contents/" + dirpath,
        lambda r: r.fulfill(status=200, content_type="application/json", body=listing))
    context.page.route(
        "**/raw.example.org/" + dirpath + "/index.md",
        lambda r: r.fulfill(status=200, content_type="text/plain", body=doc))


@then('the folder card score chip reads "{score}"')
def step_folder_score_chip(context, score):
    card = context.page.locator(".lc-card[data-dirpath]").first
    expect(card.locator(".lc-card-score")).to_contain_text(score, timeout=10_000)


@when("I tap the empty shelf's New button")
def step_tap_empty_new(context):
    context.new_dialog = []
    def on_dialog(d):
        context.new_dialog.append(d.message)
        d.dismiss()
    context.page.once("dialog", on_dialog)
    btn = context.page.locator("[data-newpage]")
    expect(btn).to_be_visible(timeout=10_000)
    btn.tap()
    context.page.wait_for_timeout(600)


@then("the New dialog opens")
def step_new_dialog_opened(context):
    assert context.new_dialog, "the lens swallowed the tap — no New dialog"
    assert "New page or folder" in context.new_dialog[0], context.new_dialog[0]


@given('new files land in "{dirpath}"')
def step_accept_new_files(context, dirpath):
    context.created = []

    def handle(route):
        if route.request.method == "PUT":
            context.created.append(route.request.url.split("/contents/")[-1])
            route.fulfill(status=201, content_type="application/json", body="{}")
        else:
            route.continue_()

    context.page.route(
        "**/api.github.com/repos/**/contents/" + dirpath + "/*.md", handle)


@when('I create a new page named "{name}"')
def step_create_named(context, name):
    context.page.once("dialog", lambda d: d.accept(name))
    btn = context.page.locator("[data-newpage]")
    expect(btn).to_be_visible(timeout=10_000)
    btn.click()
    context.page.wait_for_timeout(1200)


@then('the file "{path}" was created')
def step_file_created(context, path):
    assert context.created, "no create request was issued"
    assert context.created[0] == path, context.created[0]


@given('the folder "{dirpath}" lists "{name}" whose raw token is stale')
def step_stub_stale_raw(context, dirpath, name):
    """The listing is fine; only the download_url token has expired — the
    exact shape of a cached private-repo listing."""
    listing = [{
        "type": "file", "name": name, "path": dirpath + "/" + name,
        "download_url": "https://raw.githubusercontent.com/acme/demo/main/"
                        + dirpath + "/" + name + "?token=EXPIRED",
    }]
    body = ("# \U0001F43E Adoption Day\n\nA story from the future.\n\n"
            "```gherkin\nFeature: Proof\n  Scenario: ok\n    Given a thing\n```\n"
            "{: .feature status=\"pending\" tags=\"data\" }\n")

    context.page.route(
        "**/api.github.com/repos/**/contents/" + dirpath,
        lambda r: r.fulfill(status=200, content_type="application/json",
                            body=json.dumps(listing)))
    # the authenticated per-file read works…
    context.page.route(
        "**/api.github.com/repos/**/contents/" + dirpath + "/" + name,
        lambda r: r.fulfill(status=200, content_type="text/plain", body=body))
    # …while the stale raw token does not
    context.page.route("**/raw.githubusercontent.com/**token=EXPIRED*",
                       lambda r: r.fulfill(status=404, body="Not Found"))
    # the page hosting the shelf
    index_md = "# Module\n\n[Browse](#)\n{: .folder }\n"
    context.page.route(
        "**/api.github.com/repos/**/contents/" + dirpath + "/index.md",
        lambda r: r.fulfill(status=200, content_type="text/plain", body=index_md))
    context.page.route("**/raw.githubusercontent.com/**/index.md*",
                       lambda r: r.fulfill(status=200, content_type="text/plain",
                                           body=index_md))


@given("a stubbed private repo whose raw tokens have expired")
def step_expired_raw(context):
    # the failure shape from the field: the API answers fine, but
    # raw.githubusercontent 404s because the token baked into a cached
    # listing has aged out
    INDEX = "# \U0001f44b 00\u00b7Welcome\n\n\U0001f3d7 Skills ready to build.\n"
    SHELF = "# Shelf\n\n[modules](#)\n{: .folder path=\"courses\" open=\"runner\" }\n"

    def handler(route):
        url = route.request.url
        if "/contents/" in url:
            path = url.split("/contents/", 1)[1].split("?")[0]
            if path.endswith("shelf.md"):
                route.fulfill(status=200, content_type="text/plain", body=SHELF)
            elif path.endswith("index.md"):
                route.fulfill(status=200, content_type="text/plain", body=INDEX)
            elif path.endswith(".md"):
                route.fulfill(status=200, content_type="text/plain", body="# Page\n")
            else:
                route.fulfill(status=200, json=[
                    {"type": "dir", "name": "module_00", "path": path + "/module_00",
                     "url": "https://api.github.com/repos/acme/private/contents/"
                            + path + "/module_00"},
                    {"type": "file", "name": "index.md",
                     "path": path + "/module_00/index.md",
                     "download_url": "https://raw.githubusercontent.com/expired/index.md",
                     "url": "https://api.github.com/repos/acme/private/contents/"
                            + path + "/module_00/index.md"},
                ])
            return
        if re.search(r"/repos/[^/]+/[^/]+$", url):
            route.fulfill(status=200, json={"permissions": {"push": False}})
            return
        route.fulfill(status=404, json={"message": "stub"})

    context.page.route("https://api.github.com/**", handler)
    context.page.route("https://raw.githubusercontent.com/**",
                       lambda r: r.fulfill(status=404, body="Not Found"))
    context.page.add_init_script(
        "localStorage.setItem('lc_ed_pat','ghp_stub');"
        "localStorage.setItem('lc_ed_repo','acme/private');")


@when("I open a shelf listing that repo")
def step_open_private_shelf(context):
    context.page.goto(
        context.base_url + "/run.html#src=gh:acme/private/courses/shelf.md",
        wait_until="domcontentloaded")
    context.page.wait_for_selector(".lc-cards .lc-card", timeout=20_000)


@then("the subfolder card shows the index's own title")
def step_subdir_title(context):
    card = context.page.locator(".lc-cards .lc-card").first
    expect(card).to_contain_text("00\u00b7Welcome", timeout=10_000)
    expect(card).to_contain_text("Skills ready to build", timeout=5_000)
