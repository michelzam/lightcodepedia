"""The public door: it must work with no account, no key, nothing stored."""
from behave import then, when
from playwright.sync_api import expect


@then("the shelter list shows {n:d} dogs")
def step_dogs(context, n):
    rows = context.page.locator(".ag-row, .lc-dg-table tbody tr")
    expect(rows.first).to_be_visible(timeout=20_000)
    assert rows.count() == n, "%d rows, expected %d" % (rows.count(), n)


@then("the fee chart is drawn")
def step_chart(context):
    chart = context.page.locator("#fee_chart svg, #fee_chart canvas, .lc-chart svg, .lc-chart canvas")
    expect(chart.first).to_be_visible(timeout=20_000)


@then("nothing on the page asked me to connect")
def step_no_key_wall(context):
    """The whole point of this page: a stranger sees the thing work before
    anyone asks them for anything."""
    body = context.page.locator("body").inner_text().lower()
    for wall in ("connect your key", "paste your key", "sign in to continue"):
        assert wall not in body, "the door asked for a credential: %r" % wall


@then('the proof is failing about "{who}"')
def step_proof_red(context, who):
    card = context.page.locator(".lc-feature").first
    expect(card).to_have_attribute("data-status", "failing", timeout=45_000)
    assert who in card.inner_text(), "the red message never named %s" % who


@then("the page offers the enrolment address")
def step_visitor_door(context):
    door = context.page.locator(".on_your_own").first
    expect(door).to_be_visible(timeout=10_000)
    expect(door).to_contain_text("build-ai@uwm.edu")


@then("the roster paragraph stays hidden")
def step_class_hidden(context):
    expect(context.page.locator(".in_class").first).to_be_hidden()


@then("the page tells me my invitation is coming to my university address")
def step_class_door(context):
    door = context.page.locator(".in_class").first
    expect(door).to_be_visible(timeout=10_000)
    expect(door).to_contain_text("uwm.edu")


@then("the page tells me to sign up with that same address")
def step_same_address(context):
    """Without this line they sign up on a personal Gmail, the invitation
    does not match, and the door looks broken."""
    txt = context.page.locator(".in_class").first.inner_text().lower()
    assert "same address" in txt, txt[:200]


@then("the page shows the way in when the mail never arrives")
def step_spam_recovery(context):
    """Spam eats invitations. The mail is a convenience, not the mechanism:
    a pending invitation can be accepted from the org's own page."""
    txt = " ".join(context.page.locator(".in_class").all_inner_texts()).lower()
    assert "/invitation" in txt, txt[:300]
    assert "expire" in txt, "nothing says an invitation can lapse: " + txt[:300]


@then("the enrolment address stays hidden")
def step_visitor_hidden(context):
    expect(context.page.locator(".on_your_own").first).to_be_hidden()


@then('the app is framed as a window titled "{title}"')
def step_framed(context, title):
    win = context.page.locator(".lc-runner-win").first
    expect(win).to_be_visible(timeout=20_000)
    expect(context.page.locator(".lc-win-title").first).to_contain_text(title)


@then("the fee cells accept a tap")
def step_cells_editable(context):
    cells = context.page.locator("td.lc-dg-edit")
    expect(cells.first).to_be_visible(timeout=20_000)
    assert cells.count() >= 3, "%d editable cells" % cells.count()


@when('I tap Nova\'s fee and type "{value}"')
def step_type_fee(context, value):
    cell = context.page.locator("tr", has_text="Nova").locator("td.lc-dg-edit").last
    cell.wait_for(state="visible", timeout=20_000)
    cell.click()
    context.page.keyboard.type(value)
    context.page.keyboard.press("Enter")
    context.page.wait_for_timeout(800)


@then("the dataset carries Nova's new fee")
def step_dataset_updated(context):
    got = context.page.evaluate(
        "() => (window.lcDatasets.dogs || []).filter(r => r.name === 'Nova')"
        "        .map(r => String(r.fee))[0]")
    assert got and got != "", "the edit never reached the dataset: %r" % got


@then("the page's own promise turns green")
def step_proof_green(context):
    context.page.evaluate(
        "document.querySelectorAll('.lc-feature').forEach("
        "  c => c.classList.remove('lc-feature-hidden'))")
    context.page.click(".lc-feature .lc-feature-run")
    expect(context.page.locator(".lc-feature").first).to_have_attribute(
        "data-status", "passing", timeout=45_000)


@when("I follow the cover's link into the game")
def step_cover_to_game(context):
    link = context.page.locator('a[href$="/courses/build_ai_start"]').first
    expect(link).to_be_visible(timeout=20_000)
    link.click()
    context.page.wait_for_url("**/courses/build_ai_start*", timeout=20_000)
    context.page.wait_for_load_state("networkidle")
