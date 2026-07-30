import re

from behave import given, when, then
from playwright.sync_api import expect

# RT slides parity (slides.md lcSlidesRebuild + runner.md hook): a page-level
# runner render re-partitions its root into .lc-slide sections so Present and
# Reel work on RT-rendered courses. The gh: source is served by a stubbed
# contents API route; marked is shimmed via an init script so the scenario is
# hermetic (no CDN) and deterministic in CI and locally alike.


@given("a marked shim is preinstalled")
def step_marked_shim(context):
    # add_init_script runs before any page script, so lcLoadMarked's
    # window.marked short-circuit takes the shim and never touches the CDN.
    # It only needs to be faithful for the fixture: #/## headings + paragraphs.
    context.page.add_init_script(
        """window.marked = { parse: function (s) {
             return s.split(/\\n\\n+/).map(function (b) {
               b = b.trim();
               if (b.indexOf('## ') === 0) return '<h2>' + b.slice(3) + '</h2>';
               if (b.indexOf('# ')  === 0) return '<h1>' + b.slice(2) + '</h1>';
               var im = b.match(/^!\\[([^\\]]*)\\]\\(([^)]+)\\)$/);
               if (im) return '<img alt="' + im[1] + '" src="' + im[2] + '">';
               b = b.replace(/\\[([^\\]]*)\\]\\(([^)]+)\\)/g,
                             '<a href="$2">$1</a>');
               return b ? '<p>' + b + '</p>' : '';
             }).join('');
           } };"""
    )


@given('the GitHub contents API serves "{path}" with the document:')
def step_stub_contents_doc(context, path):
    body = context.text

    def fulfill(route):
        route.fulfill(status=200, content_type="text/plain; charset=utf-8",
                      body=body)
    context.page.route("**/api.github.com/repos/**/contents/" + path + "*", fulfill)
    context.page.route("**/raw.githubusercontent.com/**/" + path + "*", fulfill)
    context.page.route("**/raw.githubusercontent.com//main/" + path + "*", fulfill)


@then("the runner render partitions into {n:d} slides")
def step_runner_slides(context, n):
    expect(context.page.locator(".lc-run .lc-slide")).to_have_count(n, timeout=10_000)


@then("the page is in present mode")
def step_present_mode(context):
    expect(context.page.locator("body")).to_have_class(
        re.compile(r"lc-slides-active"), timeout=5_000
    )


@then('the active slide shows "{text}"')
def step_active_slide_shows(context, text):
    # VISIBLE, not just present: the page-load partition wraps /run's content
    # in an outer .lc-slide, and a display:none anywhere on that ancestor
    # chain blanks the screen while to_contain_text alone still passes.
    active = context.page.locator('.lc-run .lc-slide[data-active="true"]')
    expect(active).to_be_visible(timeout=5_000)
    expect(active).to_contain_text(text, timeout=5_000)


@then("the first rendered slide is visible")
def step_first_slide_visible(context):
    expect(context.page.locator(".lc-run .lc-slide").first).to_be_visible(timeout=5_000)


@when("I click the Reel option in the popup")
def step_click_reel_option(context):
    btn = context.page.locator("#lc-bl-reel-btn")
    expect(btn).to_be_visible(timeout=3_000)
    btn.click()
    context.page.wait_for_timeout(400)


@then('the page score key is "{key}"')
def step_score_key(context, key):
    got = context.page.evaluate("window.lcPageScores.norm(location.href)")
    assert got == key, f"score key {got!r}, expected {key!r}"


@then("a card href to that render produces the same score key")
def step_card_key_matches(context):
    page_key = context.page.evaluate("window.lcPageScores.norm(location.href)")
    card_key = context.page.evaluate(
        "window.lcPageScores.norm('run.html#src=gh:acme/demo/courses/demo/mod/index.md')"
    )
    assert card_key == page_key, f"card key {card_key!r} != page key {page_key!r}"


@given("a yaml shim declaring knowledge self is preinstalled")
def step_yaml_shim(context):
    # parseBot only needs the knowledge list out of the bot's yaml fence;
    # jsyaml itself lives on a CDN the sandbox blocks
    context.page.add_init_script(
        "window.jsyaml = { load: function () { return { knowledge: ['self'] } } };"
    )


@given('the counting GitHub contents API serves "{path}" as "{name}"')
def step_stub_counting(context, path, name):
    if not hasattr(context, "hits"):
        context.hits = {}
    context.hits[name] = 0

    def fulfill(route):
        context.hits[name] += 1
        route.fulfill(status=200, content_type="text/plain; charset=utf-8",
                      body="## Fragment\n\nBecause building beats watching.")
    context.page.route("**/api.github.com/repos/**/contents/" + path + "*", fulfill)
    context.page.route("**/raw.githubusercontent.com/**/" + path + "*", fulfill)
    context.page.route("**/raw.githubusercontent.com//main/" + path + "*", fulfill)


@when('I note the fragment hit count for "{name}"')
def step_note_hits(context, name):
    context.hits_before = context.hits.get(name, 0)


@when("I inject a tutor agent into the render root")
def step_inject_agent(context):
    context.page.evaluate(
        """() => {
            const root = document.querySelector('#lc-run');
            const p = document.createElement('p');
            p.className = 'agent';
            p.setAttribute('bot', 'tutor');
            p.textContent = 'Ask the tutor.';
            root.appendChild(p);
            window.lcUpgradeAgent(p);
        }"""
    )


@then('the fragment "{name}" is fetched again as tutor knowledge')
def step_fragment_refetched(context, name):
    # the page's own embed already fetched it once at render; the tutor's
    # knowledge assembly must fetch it AGAIN — that second hit is the proof
    for _ in range(40):
        if context.hits.get(name, 0) > context.hits_before:
            return
        context.page.wait_for_timeout(250)
    raise AssertionError(
        f"fragment {name!r}: {context.hits.get(name, 0)} hits, "
        f"expected more than {context.hits_before}"
    )
