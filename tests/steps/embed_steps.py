import base64
import re

from behave import given, when, then
from playwright.sync_api import expect

# a real 1×1 PNG, so blob-URL images genuinely decode
PNG_1PX = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8"
    "z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)

# Folder-relative {: .embed } (widgets.md): a container carrying
# data-lc-src-path for a file OUTSIDE docs/ makes embeds resolve against that
# file's folder via the GitHub contents API. The API is stubbed with a
# Playwright route (same approach the classroom suite uses), so the scenarios
# assert the RESOLUTION — which URL the widget asks for — not GitHub itself.


@given('the GitHub contents API serves "{path}" with "{content}"')
def step_stub_contents(context, path, content):
    def fulfill(route):
        route.fulfill(status=200, content_type="text/plain; charset=utf-8",
                      body=content)
    context.page.route("**/api.github.com/repos/**/contents/" + path + "*", fulfill)
    context.page.route("**/raw.githubusercontent.com/**/" + path + "*", fulfill)
    context.page.route("**/raw.githubusercontent.com//main/" + path + "*", fulfill)


@when('I inject an embed of "{href}" rendered from "{src_path}"')
def step_inject_based_embed(context, href, src_path):
    context.page.evaluate(
        """([href, srcPath]) => {
            /* the based branch needs a builder key; any value satisfies the
               stubbed route */
            localStorage.setItem('lc_ed_pat', 'bdd-test-key');
            /* marked comes from a CDN on demand; a one-line shim keeps the
               scenario hermetic when it isn't already loaded */
            if (!window.marked) window.marked = { parse: function (s) {
              return '<p>' + s.replace(/^#+\\s*/gm, '') + '</p>'; } };
            const host = document.createElement('div');
            host.id = 'lc-embed-bdd';
            host.setAttribute('data-lc-src-path', srcPath);
            host.setAttribute('data-lc-src-repo', 'acme/demo-course');
            host.innerHTML = '<p class="embed"><a href="' + href + '">frag</a></p>';
            document.querySelector('.markdown-body').appendChild(host);
            window.lcScanElement(host);
        }""",
        [href, src_path],
    )


@then('the injected embed shows "{text}"')
def step_embed_shows(context, text):
    expect(context.page.locator("#lc-embed-bdd .lc-embed")).to_contain_text(
        text, timeout=10_000
    )


@given('the GitHub contents API serves the image "{path}"')
def step_stub_image(context, path):
    def fulfill(route):
        # reality-faithful: with Accept raw, GitHub answers with its OWN media
        # type, not image/png — the engine must type the blob itself or the
        # <img> may refuse to decode. A friendly image/png here would hide it.
        route.fulfill(status=200, content_type="application/vnd.github.v3.raw",
                      body=PNG_1PX)
    # both fetch forms: the contents API and raw.githubusercontent (the
    # engine tries raw first for bot/knowledge reads, API as fallback)
    context.page.route("**/api.github.com/repos/**/contents/" + path + "*", fulfill)
    context.page.route("**/raw.githubusercontent.com/**/" + path + "*", fulfill)
    context.page.route("**/raw.githubusercontent.com//main/" + path + "*", fulfill)


@given("a builder key is connected")
def step_builder_key(context):
    # before navigation: the runner reads the key at render time (page load)
    context.page.add_init_script(
        "try { localStorage.setItem('lc_ed_pat', 'bdd-test-key'); } catch (e) {}"
    )


@then("the injected embed shows an image from a blob URL")
def step_embed_blob_image(context):
    img = context.page.locator("#lc-embed-bdd .lc-embed img")
    expect(img).to_have_attribute("src", re.compile(r"^blob:"), timeout=10_000)
    expect(img).to_be_visible(timeout=5_000)


@then("the runner's image resolves to a blob URL")
def step_runner_blob_image(context):
    img = context.page.locator(".lc-run img")
    expect(img).to_have_attribute("src", re.compile(r"^blob:"), timeout=10_000)
    expect(img).to_be_visible(timeout=5_000)


@then("the runner's image decodes from the site")
def step_runner_site_image(context):
    img = context.page.locator(".lc-run img")
    expect(img).to_have_attribute(
        "src", re.compile(r"/courses/AI-Builders\.png$"), timeout=10_000
    )
    # decoded for REAL — a 404 or a text ghost leaves naturalWidth at 0,
    # which is exactly the "green tests, broken screen" gap to close
    context.page.wait_for_function(
        "() => { var i = document.querySelector('.lc-run img');"
        "        return i && i.naturalWidth > 0; }",
        timeout=10_000,
    )


@when('I inject a sized embed of "{href}" height "{h}" rendered from "{src_path}"')
def step_inject_based_embed_h(context, href, h, src_path):
    context.page.evaluate(
        """([href, h, srcPath]) => {
            localStorage.setItem('lc_ed_pat', 'bdd-test-key');
            const host = document.createElement('div');
            host.id = 'lc-embed-bdd';
            host.setAttribute('data-lc-src-path', srcPath);
            host.setAttribute('data-lc-src-repo', 'acme/demo-course');
            host.innerHTML = '<p class="embed" height="' + h + '"><a href="' + href + '">banner</a></p>';
            document.querySelector('.markdown-body').appendChild(host);
            window.lcScanElement(host);
        }""",
        [href, h, src_path],
    )


@then("the injected embed shows the site image 400px tall")
def step_embed_site_image_h(context):
    img = context.page.locator("#lc-embed-bdd .lc-embed img")
    # site path, NOT a sibling lookup and NOT a blob — the exact module_00 case
    expect(img).to_have_attribute(
        "src", re.compile(r"/courses/AI-Builders\.png$"), timeout=10_000
    )
    context.page.wait_for_function(
        "() => { var i = document.querySelector('#lc-embed-bdd img');"
        "        return i && i.naturalWidth > 0 && i.offsetHeight === 400; }",
        timeout=10_000,
    )


@then("the injected embed upgrades the quiz component")
def step_embed_quiz_upgraded(context):
    # the regression: {: .quiz } stayed literal text and checkboxes dead
    expect(context.page.locator("#lc-embed-bdd .lc-quiz")).to_have_count(
        1, timeout=10_000
    )
    literal = context.page.evaluate(
        "document.getElementById('lc-embed-bdd').textContent.includes('{: .quiz')"
    )
    assert not literal, "the IAL marker still renders as literal text"
