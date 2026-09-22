"""🧠 Cognitive load check in the editor's ♿ Audit tab (load_check.feature)."""
import re

from behave import when, then
from playwright.sync_api import expect


@when("I press the editor's load check")
def step_press_load(context):
    btn = context.page.locator("#ed-load-run")
    expect(btn).to_be_visible(timeout=15_000)
    btn.click()
    expect(context.page.locator(".ed-load-cards")).to_be_visible(timeout=15_000)


def _card(context, name):
    return context.page.locator('.ed-load-card[data-score="%s"]' % name)


@then('the load card "{name}" reads "{text}" and warns')
def step_card_warns(context, name, text):
    card = _card(context, name)
    expect(card).to_contain_text(text)
    expect(card).to_have_attribute("data-verdict", "warn")


@then('the load card "{name}" reads "{text}" and passes')
def step_card_passes(context, name, text):
    card = _card(context, name)
    expect(card).to_contain_text(text)
    expect(card).to_have_attribute("data-verdict", "ok")


@then('the load card "{name}" reads "{text}" and says "{delta}"')
def step_card_delta(context, name, text, delta):
    card = _card(context, name)
    expect(card).to_contain_text(text)
    expect(card.locator(".ed-load-delta")).to_contain_text(delta)


@then('the load rows name "{label}"')
def step_load_rows(context, label):
    rows = context.page.locator('#ed-load-list .ed-a11y-row[data-kind="load"]')
    texts = [t.replace("\n", " ") for t in rows.all_text_contents()]
    assert any(re.sub(r"\s+", " ", t).startswith(label) for t in texts), texts


@then('the load rules are listed, "{rule}" set to "{value}"')
def step_load_rules(context, rule, value):
    table = context.page.locator("#ed-load-rules table")
    expect(table).to_be_attached()
    row = table.locator("tr", has_text=rule).first
    expect(row.locator("b")).to_have_text(value)


@when("the page moves to a new version without the loose form")
def step_new_version(context):
    # the author saved a version without the form: the file has a new sha
    context.page.evaluate("""() => {
        const el = document.querySelector('[data-lc-id="loose"]'); if (el) el.remove();
        window.lcEdSha = 'v2-after-edit';
    }""")


@then("the load history remembers {n:d} runs")
def step_history(context, n):
    hist = context.page.locator("#ed-load-hist summary")
    expect(hist).to_contain_text("%d runs" % n, timeout=5_000)
