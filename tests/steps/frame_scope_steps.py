from behave import then, when
from playwright.sync_api import expect

# Frame flags define the SCOPE a host (Canvas, any LMS) grants. These steps
# click a real internal link and inspect where the learner actually lands —
# same tab or new, flags kept or lost.


def _first_internal_link(page, prefix=""):
    # a link that leaves this page but stays on this site — the folder-card
    # case in miniature
    return page.evaluate(
        """(prefix) => {
            const here = location.pathname;
            const as = Array.from(document.querySelectorAll('a[href]'));
            /* SITE-canonical compare: the lab is served under a project base
               (/lightcodelab), pedia at the domain root. Matching raw
               pathnames finds a "/components/" link on one and nothing on
               the other — the same suite, two verdicts. Strip the base, the
               way the frame guard itself does. */
            const base = window.lcBase || '';
            const strip = p => (base && p.indexOf(base + '/') === 0)
                                 ? p.slice(base.length) : p;
            const hereP = strip(here);
            for (const a of as) {
              if (a.target === '_blank' || a.hasAttribute('download')) continue;
              const h = a.getAttribute('href') || '';
              if (!h || h.startsWith('#')) continue;
              let u;
              try { u = new URL(a.href, location.href); } catch (e) { continue; }
              if (u.origin !== location.origin) continue;
              const p = strip(u.pathname);
              if (p === hereP) continue;
              if (prefix && p.indexOf(prefix) !== 0) continue;
              return a.href;
            }
            return null;
        }""",
        prefix,
    )


@when("I follow the first internal link")
def step_follow_internal(context):
    _follow(context, "")


@when('I follow the first internal link to "{prefix}"')
def step_follow_internal_prefix(context, prefix):
    _follow(context, prefix)


def _follow(context, prefix):
    href = _first_internal_link(context.page, prefix)
    assert href, "no internal link to %r on the page" % (prefix or "anywhere")
    context.lc_url_before = context.page.url
    context.lc_pages_before = len(context.page.context.pages)
    context.page.evaluate(
        """(href) => {
            const a = Array.from(document.querySelectorAll('a[href]'))
              .find(x => x.href === href);
            a.click();
        }""",
        href,
    )
    context.page.wait_for_timeout(1200)


@then('the page I land on still carries "{flag}"')
def step_landed_with_flag(context, flag):
    url = context.page.url
    assert flag in url, "landed on %s — %s missing" % (url, flag)


@then("the page I land on carries no frame flags")
def step_landed_clean(context):
    url = context.page.url
    for k in ("focus=", "navigable=", "editable=", "open="):
        assert k not in url, "unframed page grew a flag: %s" % url


@then("no second tab was opened")
def step_no_new_tab(context):
    n = len(context.page.context.pages)
    assert n == context.lc_pages_before, "a new tab appeared (%d → %d)" % (
        context.lc_pages_before, n)


@then('a second tab was opened carrying "{flag}"')
def step_new_tab_with_flag(context, flag):
    pages = context.page.context.pages
    assert len(pages) > context.lc_pages_before, "no new tab was opened"
    assert flag in pages[-1].url, "new tab is %s — %s missing" % (
        pages[-1].url, flag)


@then("I actually left the page I was on")
def step_actually_moved(context):
    # a neutralised link leaves the URL untouched — which would let a
    # "flags still there" assertion pass without any navigation at all
    assert context.page.url != context.lc_url_before, \
        "still on %s — the link never navigated" % context.page.url


@when("I follow the first folder card link")
def step_follow_card(context):
    # the learner's actual gesture: a tap on a card, not on whatever link the
    # page happens to expose first. Cards arrive async — wait for the gallery.
    card = context.page.locator(".lc-card h3 a").first
    card.wait_for(state="visible", timeout=20_000)
    context.lc_url_before = context.page.url
    context.lc_pages_before = len(context.page.context.pages)
    card.click()
    context.page.wait_for_timeout(1500)


@then('the crumb reads "{course}" then "{module}" then "{page}"')
def step_crumb(context, course, module, page):
    """The trail is filled by whoever knows: the page title comes from the
    render, the module's title from its own index.md, read once."""
    crumb = context.page.locator("#lc-crumb")
    expect(crumb).to_contain_text(module, timeout=20_000)
    expect(crumb).to_contain_text(page, timeout=20_000)
    brand = context.page.locator("#lc-topbar .lc-brand")
    expect(brand).to_contain_text(course, timeout=10_000)
    assert not brand.get_attribute("href"), "the brand still navigates away"


@then("the menu links are gone")
def step_no_menu(context):
    links = context.page.locator("#lc-topbar .lc-links")
    assert links.count() == 0 or not links.first.is_visible(), "the menu is still offered"


@then("the runner never names the file")
def step_no_file_chip(context):
    bar = context.page.locator(".lc-run-bar")
    assert bar.count() == 0 or not bar.first.is_visible(), "the source chip is still shown"


@then("no Up pill is offered")
def step_no_up(context):
    context.page.wait_for_timeout(1200)
    assert context.page.locator(".lc-folder-up-pill").count() == 0, "Up is still there"


@then("an Up pill is offered")
def step_up(context):
    expect(context.page.locator(".lc-folder-up-pill").first).to_be_visible(timeout=15_000)


@then("my face is shown")
def step_face_shown(context):
    chip = context.page.locator("#lc-user-btn")
    chip.wait_for(state="visible", timeout=10_000)


@then("tapping it opens nothing")
def step_chip_inert(context):
    context.page.locator("#lc-user-btn").click()
    context.page.wait_for_timeout(300)
    assert not context.page.evaluate(
        "document.getElementById('lc-user-drop').classList.contains('open')"
    ), "the framed learner got the full account menu"


@then("the trail sits left and the meters sit right, before my face")
def step_two_groups(context):
    """Michel, 2026-08-13: "justify left module and page names, then justify
    right the global score and AI/GH PAT credits left"."""
    context.page.evaluate("window.lcCrumbScore && window.lcCrumbScore('12/20')")
    context.page.wait_for_timeout(200)
    geo = context.page.evaluate("""() => {
      const box = s => { const el = document.querySelector(s);
        if (!el) return null; const r = el.getBoundingClientRect();
        return { left: Math.round(r.left), right: Math.round(r.right), w: Math.round(r.width) }; };
      return { crumb: box('#lc-crumb'), meta: box('#lc-crumb-meta'),
               pill: box('#lc-user-pill'), door: box('#lc-start-pill'),
               scoreInMeta: !!document.querySelector('#lc-crumb-meta .lc-crumb-score'),
               inner: window.innerWidth };
    }""")
    assert geo["scoreInMeta"], "the score is not in the right-hand group (%r)" % geo
    assert geo["meta"] and geo["meta"]["w"] > 0, "the meters are not shown (%r)" % geo
    assert geo["crumb"]["right"] <= geo["meta"]["left"], \
        "the trail is not left of the meters (%r)" % geo
    # last in the row is the face when signed in, the sign-in door when not
    last = geo["pill"] if geo["pill"]["w"] else geo["door"]
    if last["w"]:
        assert geo["meta"]["right"] <= last["left"] + 1, \
            "the meters are not just before the account chip (%r)" % geo
    else:
        assert geo["meta"]["right"] >= geo["inner"] - 40, \
            "the meters are not right-justified (%r)" % geo
    # left-justified: the trail starts near the brand, not floated to the middle
    assert geo["crumb"]["left"] < geo["inner"] / 2, "the trail drifted right (%r)" % geo


@then("the module name leads to the module's own cover")
def step_module_is_a_door(context):
    """Read-only was never about being stuck: going UP to the module you are
    already inside stays inside the course (Michel, 2026-08-13)."""
    link = context.page.locator("#lc-crumb a.lc-crumb-mod")
    expect(link).to_have_count(1, timeout=15_000)
    href = link.get_attribute("href") or ""
    assert href.endswith("/index.md"), "the module name points at %r" % href


@then("the page begins right under the bar")
def step_no_canyon(context):
    """Michel, 2026-08-13, on the Canvas view: "00 welcome is way too low"."""
    gap = context.page.evaluate("""() => {
      const bar = document.getElementById('lc-topbar').getBoundingClientRect();
      const h = document.querySelector('#lc-run h1, #lc-run h2, main h1');
      return h ? Math.round(h.getBoundingClientRect().top - bar.bottom) : null;
    }""")
    assert gap is not None, "no heading to measure"
    assert gap <= 40, "the page starts %dpx below the bar" % gap


@then("the about bubble credits the content, the platform and the AI")
def step_about_bubble(context):
    chip = context.page.locator("#lc-crumb-meta .lc-meter-about")
    expect(chip).to_have_count(1, timeout=15_000)
    tip = chip.get_attribute("title") or ""
    for want in ("content:", "platform:", "AI:"):
        assert want in tip, "the about bubble says %r" % tip
    assert chip.evaluate("el => getComputedStyle(el).cursor") == "default", \
        "the bubble looks clickable, and it does nothing yet"
