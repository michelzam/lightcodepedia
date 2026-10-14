from behave import then
from playwright.sync_api import expect

# {: .feature src="other.md#proof" } — a lesson's proof, borrowed by a later
# page. It arrives AFTER the render (a second file is read), so wait for it.


@then('the proof "{fid}" arrives from the other page')
def step_proof_arrives(context, fid):
    card = context.page.locator('.lc-feature[data-lc-id="%s"]' % fid)
    card.wait_for(state="attached", timeout=20_000)
    expect(card.locator(".lc-feature-run")).to_have_count(1)


@then('the page says, in one line, "{text}"')
def step_one_line_error(context, text):
    err = context.page.locator(".lc-feature-embed-err").first
    expect(err).to_contain_text(text, timeout=20_000)
    said = err.inner_text()
    assert "\n" not in said.strip() and "Traceback" not in said, said
