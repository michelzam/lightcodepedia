from behave import then, when

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
