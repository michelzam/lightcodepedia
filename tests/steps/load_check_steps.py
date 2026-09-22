"""🧠 Cognitive load check in the editor's ♿ Audit tab (load_check.feature)."""
import re

from behave import given, when, then
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


@given('the commits API names the page\'s last commit "{message}"')
def step_commits_api(context, message):
    import json as _json
    context.page.route(re.compile(r"https://api\.github\.com/repos/[^/]+/[^/]+/commits\?.*"),
                       lambda r: r.fulfill(status=200, content_type="application/json",
                                           body=_json.dumps([{"sha": "abc1234def5678", "commit": {"message": message + "\n\nmore"}}])))


@when('the load rule "{rule}" is set to {value:d}')
def step_set_rule(context, rule, value):
    context.page.evaluate("([r, v]) => { window.lcLoadRules[r] = v; }", [rule, value])


@then('clicking the section row "{section}" outlines that section on the page')
def step_click_section(context, section):
    row = context.page.locator('#ed-load-list .ed-a11y-row[data-kind="load-section"]', has_text=section).first
    expect(row).to_be_visible(timeout=5_000)
    row.click()
    lit = context.page.locator(".markdown-body h2.ed-a11y-outline")
    expect(lit).to_have_count(1, timeout=5_000)
    expect(lit).to_contain_text(section)


@then('the history grid marks "{col}" as improved on the latest run, its headers explained')
def step_grid_improved(context, col):
    grid = context.page.locator("#ed-load-hist .ed-load-grid")
    expect(grid).to_be_visible(timeout=5_000)
    heads = grid.locator("thead th")
    names = heads.all_text_contents()
    assert col in names, names
    assert all(t for t in [heads.nth(i).get_attribute("title") for i in range(heads.count())]), "a header without a tooltip"
    i = names.index(col)
    cell = grid.locator("tbody tr").first.locator("td").nth(i)
    expect(cell).to_have_class(re.compile(r"\bbetter\b"))
    expect(cell).to_have_text("0")


@then('the latest version\'s tooltip names the commit "{message}"')
def step_sha_tooltip(context, message):
    sha = context.page.locator("#ed-load-hist tbody tr").first.locator(".ed-load-sha")
    expect(sha).to_have_attribute("title", re.compile(re.escape(message)), timeout=10_000)
