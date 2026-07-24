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


@when("the published results are from a run long before this build")
def step_seed_stale_results(context):
    # drive the real dataset the board binds to: an all-green summary whose run
    # stamp is years old. Green numbers + ancient stamp is exactly the lie.
    context.page.evaluate(
        """() => window.lcSetDataset('ux_summary', [{
             features: 19, scenarios: 146, steps: 794,
             features_failed: 0, scenarios_failed: 0, steps_failed: 0,
             run: '2020-01-01T00:00Z'
           }])"""
    )
    context.page.wait_for_timeout(300)


@then("the totals stat says the results are stale")
def step_stat_stale(context):
    chip = context.page.locator(".lc-stat[data-bind='ux_summary']").first
    expect(chip).to_contain_text("stale", timeout=8_000)
    expect(chip).to_have_class(__import__("re").compile(r"\blc-stat-stale\b"), timeout=8_000)


@when('I open the accordion section "{title}"')
def step_open_accordion_titled(context, title):
    summary = context.page.locator(
        ".lc-accordion details summary", has_text=title
    ).first
    summary.wait_for(state="visible", timeout=15_000)
    summary.click()
    context.page.wait_for_timeout(800)  # lazy markdown render + upgrades
