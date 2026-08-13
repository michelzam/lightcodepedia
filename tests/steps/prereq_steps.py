import json

from behave import given, then
from playwright.sync_api import expect

# The prerequisite gate on runner renders: scores live under gh:owner/repo/…
# content keys (score.md's canon), and the gate must read exactly those.


@given('the learner has mastered "{key}"')
def step_seed_full(context, key):
    # every point on that page — what the default (pass=100) demands
    _seed(context, {key: {"won": 3, "total": 3}})


@given('the learner has earned some points on "{key}"')
def step_seed_partial(context, key):
    # 2/3: enough for a relaxed gate, not for mastery
    _seed(context, {key: {"won": 2, "total": 3}})


@given('the learner has earned points on "{key}"')
def step_seed_score(context, key):
    _seed(context, {key: {"won": 3, "total": 3}})


def _seed(context, obj):
    seed = json.dumps(obj)
    context.page.add_init_script(
        "try { localStorage.setItem('lc_scores', %s); } catch (e) {}"
        % json.dumps(seed)
    )


@then('a prerequisite gate offers "{title}"')
def step_gate_offers(context, title):
    gate = context.page.locator(".lc-prereq")
    expect(gate).to_be_visible(timeout=10_000)
    expect(gate.locator("a", has_text=title)).to_be_visible(timeout=5_000)


@then('the gated content "{text}" is hidden')
def step_gated_hidden(context, text):
    expect(context.page.get_by_text(text)).to_be_hidden(timeout=10_000)


@then("the prerequisites are met")
def step_prereq_met(context):
    expect(context.page.locator(".lc-prereq-met")).to_be_visible(timeout=10_000)


@then('the gated content "{text}" is visible')
def step_gated_visible(context, text):
    expect(context.page.get_by_text(text)).to_be_visible(timeout=10_000)


@then("nothing below the gate is visible")
def step_nothing_below(context):
    # give every late upgrader (dataset → grid, fence → block, quiz) time to
    # replace its element, then demand the page body is still gone
    context.page.wait_for_timeout(2500)
    leaked = context.page.evaluate(
        """() => {
            const gate = document.querySelector('.lc-prereq');
            if (!gate) return ['no gate'];
            const out = [];
            let n = gate.nextElementSibling;
            while (n) {
              const cs = getComputedStyle(n);
              if (cs.display !== 'none' && n.offsetParent !== null)
                out.push(n.className || n.tagName);
              n = n.nextElementSibling;
            }
            return out;
        }"""
    )
    assert not leaked, "visible below a locked gate: %s" % leaked


@when("I show the page anyway")
def step_show_anyway(context):
    context.page.locator(".lc-prereq [data-show]").click()


@then("no escape hatch is offered")
def step_no_escape(context):
    n = context.page.locator(".lc-prereq [data-show]").count()
    assert n == 0, "the gate offered a way through when the author gave none"


@then('the escape hatch reads "{label}"')
def step_escape_label(context, label):
    expect(context.page.locator(".lc-prereq [data-show]")).to_have_text(
        label, timeout=10_000)


@then('"{title}" is still a link I can follow')
def step_met_is_link(context, title):
    link = context.page.locator(".lc-prereq-met a, .lc-prereq li.ok a", has_text=title).first
    expect(link).to_be_visible(timeout=15_000)
    href = link.get_attribute("href") or ""
    assert href and href != "#", f"the met prerequisite leads nowhere: {href!r}"


# ── features="true": the proofs count too ───────────────────────────────────
@given('the learner turned "{feature}" green on "{key}"')
def step_seed_feature_green(context, feature, key):
    _seed_features(context, {key + "#" + feature: {"status": "passing"}})


@given('the learner left "{feature}" red on "{key}"')
def step_seed_feature_red(context, feature, key):
    _seed_features(context, {key + "#" + feature: {"status": "failing"}})


def _seed_features(context, obj):
    """Merge, so a scenario can seed one green and one red."""
    try:
        have = context._feat_seed or {}
    except (AttributeError, KeyError):
        have = {}
    have.update(obj)
    context._feat_seed = have
    context.page.add_init_script(
        "try { localStorage.setItem('lc_features', %s); } catch (e) {}"
        % json.dumps(json.dumps(have))
    )


@then('"{title}" leads back through the runner to "{path}"')
def step_prereq_link_healed(context, title, path):
    link = context.page.locator(".lc-prereq-met a, .lc-prereq a", has_text=title).first
    href = link.get_attribute("href") or ""
    assert "#src=gh:" in href, "a raw markdown href cannot be opened by the site: %r" % href
    assert href.endswith("/" + path), href
