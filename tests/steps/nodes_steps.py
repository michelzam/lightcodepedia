from behave import then
from playwright.sync_api import expect

# The page calls the GitHub API unauthenticated; rate-limited responses log
# "Failed to load resource" console errors in CI, so nodes scenarios assert
# rendering, not console silence.


@then("the LightNode network map is visible")
def step_nodes_map_visible(context):
    expect(context.page.locator("#lc-nodes-svg")).to_be_visible(timeout=15_000)


@then('the "{dataset_id}" bound grid shows at least {n:d} rows')
def step_bound_grid_rows(context, dataset_id, n):
    rows = context.page.locator(
        ".lc-datagrid[data-bind='" + dataset_id + "'] tbody tr"
    )
    # the dataset is fetched remotely — wait until the nth row exists
    expect(rows.nth(n - 1)).to_be_visible(timeout=20_000)


@when('I open the accordion section "{title}"')
def step_open_accordion_titled(context, title):
    summary = context.page.locator(
        ".lc-accordion details summary", has_text=title
    ).first
    summary.wait_for(state="visible", timeout=15_000)
    summary.click()
    context.page.wait_for_timeout(800)  # lazy markdown render + upgrades
