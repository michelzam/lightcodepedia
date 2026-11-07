"""The editable model (steps_runtime.md modelEditor) — Michel, 2026-11-06, Python
Module 11: "the python editors can define classes with states, colors, emojis, and
allow UI components to follow". Since 2026-11-06 it is the pad (pyrun.md) in apply
mode — Michel: "it should not create new components without asking permission"."""
from behave import given, when, then
from playwright.sync_api import expect


def _editor(context, mid):
    return context.page.locator("#lc-pyrun-%s textarea.lc-pyrun-code" % mid)


@when('in the model editor "{mid}" I replace')
def step_model_editor_replace(context, mid):
    old, new = [part.strip("\n") for part in context.text.split("\n⇩\n")]
    ta = _editor(context, mid)
    expect(ta).to_be_visible(timeout=15_000)
    code = ta.input_value()
    assert old in code, "not in the editor: " + old
    ta.fill(code.replace(old, new, 1))


@when('I apply the model editor "{mid}"')
def step_model_editor_apply(context, mid):
    context.page.locator("#lc-pyrun-%s .lc-pyrun-run" % mid).click()


@then('the model editor "{mid}" says "{text}"')
def step_model_editor_says(context, mid, text):
    expect(context.page.locator("#lc-pyrun-%s .lc-pyrun-out" % mid)).to_contain_text(text, timeout=15_000)


@then('the cards "{iid}" offer the command "{verb}"')
def step_cards_offer(context, iid, verb):
    expect(context.page.locator("[data-lc-id='%s'] button[data-m='%s']" % (iid, verb)).first).to_be_attached(timeout=15_000)


@then('the cards "{iid}" show the state "{state}"')
def step_cards_state(context, iid, state):
    expect(context.page.locator("[data-lc-id='%s']" % iid).first).to_contain_text(state, timeout=15_000)


@given('this browser kept an old edit of the model "{mid}" on "{src}": "{code}"')
def step_kept_old_edit(context, mid, src, code):
    key = "lc_model_edit:" + src + ":" + mid
    context.page.add_init_script("try { localStorage.setItem(%r, %r); } catch (e) {}" % (key, code.replace('\\"', '"')))


@then('the model editor "{mid}" holds "{text}"')
def step_editor_holds(context, mid, text):
    ta = _editor(context, mid)
    expect(ta).to_be_visible(timeout=15_000)
    assert text in ta.input_value(), ta.input_value()[:300]


@then('the model editor "{mid}" does not hold "{text}"')
def step_editor_not_holds(context, mid, text):
    assert text not in _editor(context, mid).input_value()


@then('the model editor "{mid}" offers "{text}"')
def step_editor_offers(context, mid, text):
    expect(context.page.locator("#lc-pyrun-%s .lc-pyrun-status" % mid)).to_contain_text(text, timeout=10_000)


@then('the cards "{iid}" have no button "{verb}"')
def step_cards_no_button(context, iid, verb):
    expect(context.page.locator("[data-lc-id='%s'] .lc-ins-card" % iid).first).to_be_visible(timeout=15_000)
    assert context.page.locator("[data-lc-id='%s'] button[data-m='%s']" % (iid, verb)).count() == 0


@then('the console of "{iid}" reads "{text}"')
def step_console_reads(context, iid, text):
    expect(context.page.locator("[data-lc-console='%s']" % iid).first).to_contain_text(text, timeout=10_000)


@then('the model editor "{mid}" is the pad: ▶ Apply, ↺, a gutter, coloured code')
def step_editor_is_the_pad(context, mid):
    """One Python editor on the site (Michel, 2026-11-06): the editable model wears
    the pad's gutter, Prism colours and bar — ▶ Apply where ▶ Run stands."""
    root = context.page.locator("#lc-pyrun-%s" % mid)
    expect(root).to_be_visible(timeout=15_000)
    expect(root.locator(".lc-pyrun-run")).to_have_text("▶ Apply")
    expect(root.locator(".lc-pyrun-reset")).to_be_visible()
    expect(root.locator(".lc-pyrun-gutter-inner")).to_contain_text("2")
    expect(root.locator(".lc-pyrun-hl .token.keyword").first).to_be_attached(timeout=15_000)


@then('the diagram draws the package "{pkg}" holding "{classes}"')
def step_diagram_package(context, pkg, classes):
    """The author's classes cluster under their fence's id, the file they live in
    (Michel, 2026-11-06: "the package name should not be kore, but swiftsip")."""
    svg = context.page.locator(".lc-diagram svg").first
    expect(svg).to_be_visible(timeout=40_000)
    labels = svg.locator("g.cluster text").all_text_contents()
    assert any(pkg in t for t in labels), "no package %r among the clusters: %r" % (pkg, labels)
    assert not any("kore" in t for t in labels), "the framework's kore package is drawn: %r" % labels
    for cls in [c.strip() for c in classes.split(",")]:
        expect(svg.locator("g.node title", has_text=cls).first).to_be_attached(timeout=20_000)
