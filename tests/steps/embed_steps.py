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


def _refuse(route):
    """What GitHub answers a key it no longer accepts."""
    route.fulfill(status=401, content_type="application/json",
                  body='{"message":"Bad credentials"}')


@given("the GitHub contents API refuses the key")
def step_refuse_api(context):
    # registered after the serving routes, so it wins for the API only —
    # raw keeps answering, which is the whole point of the fallback
    context.page.route("**/api.github.com/repos/**/contents/**", _refuse)


@given("the raw file host refuses the key too")
def step_refuse_raw(context):
    context.page.route("**/raw.githubusercontent.com/**", _refuse)


@when('I inject a public-site embed of "{href}" with a stale key')
def step_inject_site_embed(context, href):
    """A plain site node — no data-lc-src-path — read with a refused key.

    The reported bug is a PUBLIC site (pedia): the private lab has no keyless
    route by design, so the public case is declared explicitly rather than
    inherited from whichever site the suite runs against.
    """
    context.page.evaluate(
        """(href) => {
            localStorage.setItem('lc_ed_pat', 'stale-key');
            window.lcRepoPrivate = false;
            if (!window.marked) window.marked = { parse: function (s) {
              return '<p>' + s.replace(/^#+\\s*/gm, '') + '</p>'; } };
            const host = document.createElement('div');
            host.id = 'lc-embed-bdd';
            host.innerHTML = '<p class="embed"><a href="' + href + '">frag</a></p>';
            document.querySelector('.markdown-body').appendChild(host);
            window.lcScanElement(host);
        }""",
        href,
    )


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


@when('I inject an image embed of "{href}" width "{w}" align "{al}" rendered from "{src_path}"')
def step_inject_floated_embed(context, href, w, al, src_path):
    context.page.evaluate(
        """([href, w, al, srcPath]) => {
            const host = document.createElement('div');
            host.id = 'lc-embed-bdd';
            host.setAttribute('data-lc-src-path', srcPath);
            host.setAttribute('data-lc-src-repo', 'acme/demo-course');
            host.innerHTML = '<p class="embed" width="' + w + '" align="' + al
              + '"><a href="' + href + '">pic</a></p>'
              + '<p>Wrapping text follows the picture.</p>';
            document.querySelector('.markdown-body').appendChild(host);
            window.lcScanElement(host);
        }""",
        [href, w, al, src_path],
    )


@then("the injected embed floats right at 40% width")
def step_embed_floats(context):
    img = context.page.locator("#lc-embed-bdd .lc-embed img")
    expect(img).to_be_visible(timeout=10_000)
    # the container floats (text wraps), the image takes the relative width
    context.page.wait_for_function(
        "() => { var c = document.querySelector('#lc-embed-bdd .lc-embed');"
        "        var i = c && c.querySelector('img');"
        "        return c && getComputedStyle(c).float === 'right'"
        "            && i && i.style.width === '40%'; }",
        timeout=10_000,
    )


@given('the external image "{url}" is served')
def step_stub_external_image(context, url):
    context.page.route(url, lambda r: r.fulfill(
        status=200, content_type="image/jpeg", body=PNG_1PX))


@then("the injected embed hotlinks the external image")
def step_embed_external_image(context):
    img = context.page.locator("#lc-embed-bdd .lc-embed img")
    # the URL must survive untouched — no rebase, no sibling lookup, no blob
    expect(img).to_have_attribute(
        "src", re.compile(r"^https://pics\.example\.org/hero\.jpg$"),
        timeout=10_000,
    )
    expect(img).to_be_visible(timeout=5_000)


@when('I inject an ambient image embed of "{href}" rendered from "{src_path}"')
def step_inject_ambient_embed(context, href, src_path):
    context.page.evaluate(
        """([href, srcPath]) => {
            const host = document.createElement('div');
            host.id = 'lc-embed-bdd';
            host.setAttribute('data-lc-src-path', srcPath);
            host.setAttribute('data-lc-src-repo', 'acme/demo-course');
            host.innerHTML = '<p class="embed" effect="ambient"><a href="'
              + href + '">banner</a></p>';
            document.querySelector('.markdown-body').appendChild(host);
            window.lcScanElement(host);
        }""",
        [href, src_path],
    )


@then("the injected embed animates ambiently")
def step_embed_ambient(context):
    img = context.page.locator("#lc-embed-bdd .lc-embed-ambient img")
    expect(img).to_be_visible(timeout=10_000)
    # a REAL animation, not just a class: the computed name must resolve
    context.page.wait_for_function(
        "() => { var i = document.querySelector('#lc-embed-bdd .lc-embed-ambient img');"
        "        return i && getComputedStyle(i).animationName === 'lc-ambient'; }",
        timeout=10_000,
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


@then('the injected embed shows a block card with "{text}"')
def step_embed_block_card(context, text):
    # the fence + {: .block } must become a rendered card, not a literal
    # code listing — module_00's packaged sections depend on it
    card = context.page.locator("#lc-embed-bdd .lc-block")
    expect(card).to_be_visible(timeout=10_000)
    expect(card).to_contain_text(text, timeout=5_000)


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

@when('I inject a forced image embed of "{href}" rendered from "{src_path}"')
def step_inject_forced_image_embed(context, href, src_path):
    context.page.evaluate(
        """([href, srcPath]) => {
            const host = document.createElement('div');
            host.id = 'lc-embed-bdd';
            host.setAttribute('data-lc-src-path', srcPath);
            host.setAttribute('data-lc-src-repo', 'acme/demo-course');
            host.innerHTML = '<p class="embed" image="true"><a href="' + href
              + '">api pic</a></p>';
            document.querySelector('.markdown-body').appendChild(host);
            window.lcScanElement(host);
        }""",
        [href, src_path],
    )


@then("the injected embed shows an image, not an iframe")
def step_embed_forced_image(context):
    img = context.page.locator("#lc-embed-bdd img")
    expect(img).to_be_visible(timeout=10_000)
    assert context.page.locator("#lc-embed-bdd iframe").count() == 0, \
        "the URL-API image was iframed"



# ── {: .video }: addressable, privacy-first, and drivable by an avatar ────
# The manim recaps are SILENT on purpose so the avatar is the only soundtrack.
# That only works if the page can reach the player, which needs three things
# the component did not do: keep the author's id, ask for the command channel
# (enablejsapi), and be delegated autoplay. A postMessage cannot be tested
# against real YouTube from here — what IS tested is that the exact documented
# command leaves the page aimed at the right frame.

def _video(context, vid):
    el = context.page.locator(f'iframe[data-lc-id="{vid}"]')
    el.wait_for(state="attached", timeout=15_000)
    return el


@then('the video "{vid}" is an addressable frame')
def step_video_addressable(context, vid):
    el = _video(context, vid)
    assert el.get_attribute("id") == vid, "the id did not survive the upgrade"
    assert "lc-video" in (el.get_attribute("class") or "")


@then('the video "{vid}" is served from the nocookie host')
def step_video_nocookie(context, vid):
    src = _video(context, vid).get_attribute("src") or ""
    assert "youtube-nocookie.com/embed/" in src, src
    assert "rel=0" in src, "a lesson clip must not offer strangers' videos: " + src


@then('the video "{vid}" can be commanded and may autoplay')
def step_video_commandable(context, vid):
    el = _video(context, vid)
    src = el.get_attribute("src") or ""
    allow = el.get_attribute("allow") or ""
    assert "enablejsapi=1" in src, "no command channel: " + src
    assert "autoplay" in allow, (
        "autoplay is not delegated, so a play command reaches a player that "
        "cannot obey it: allow=" + allow)


@when("I record what the video frame is told")
def step_record_postmessages(context):
    # stand in front of the frame's contentWindow.postMessage so the command
    # is captured instead of vanishing across the origin boundary
    context.page.evaluate("""() => {
        window.__lcSent = [];
        document.querySelectorAll('iframe.lc-video').forEach(function (f) {
          var cw = f.contentWindow;
          if (!cw) return;
          try {
            Object.defineProperty(f, 'contentWindow', {
              configurable: true,
              get: function () {
                return { postMessage: function (msg) { window.__lcSent.push(String(msg)); } };
              }
            });
          } catch (e) { window.__lcSentError = String(e); }
        });
      }""")


@given('the avatar verb "{verb:w}" fires at "{vid:w}"')
@when('the avatar verb "{verb:w}" fires at "{vid:w}"')
def step_verb_fires(context, verb, vid):
    context.page.evaluate(
        """([v, id]) => window.lcVerbs.act(v, document.querySelector('[data-lc-id="' + id + '"]'))""",
        [verb, vid])
    context.page.wait_for_timeout(300)


@given('the avatar verb "{verb:w}" fires at "{vid:w}" with "{arg}"')
@when('the avatar verb "{verb:w}" fires at "{vid:w}" with "{arg}"')
def step_verb_fires_arg(context, verb, vid, arg):
    context.page.evaluate(
        """([v, id, a]) => window.lcVerbs.act(v, document.querySelector('[data-lc-id="' + id + '"]'), a)""",
        [verb, vid, arg])
    context.page.wait_for_timeout(300)


def _sent(context):
    return context.page.evaluate("() => window.__lcSent || []")


@then('the player was told to "{func:w}"')
def step_player_told(context, func):
    sent = _sent(context)
    assert any(func in s for s in sent), f"{func} not among {sent}"


@then('the player was told to "{first:w}" and then "{second:w}"')
def step_player_told_order(context, first, second):
    sent = _sent(context)
    idx = [i for i, s in enumerate(sent) if first in s]
    jdx = [i for i, s in enumerate(sent) if second in s]
    assert idx and jdx, f"expected both {first} and {second}, got {sent}"
    assert min(idx) < min(jdx), f"{first} must come before {second}: {sent}"


@then('the verb "{verb:w}" points at the video "{vid:w}"')
def step_verb_subject(context, verb, vid):
    got = context.page.evaluate(
        """([v, id]) => {
             var el = document.querySelector('[data-lc-id="' + id + '"]');
             var s = window.lcVerbs.target(v, el);
             return s ? (s.getAttribute('data-lc-id') || s.tagName) : null;
           }""", [verb, vid])
    assert got == vid, f"the avatar would stand at {got!r}, not the video"
