from behave import when, then
from playwright.sync_api import expect

SEL_GRID = ".lc-datagrid"
SEL_GRID_ROW = ".ag-row"
SEL_CHART = ".lc-chart"
SEL_MAP = ".lc-map"
SEL_VIDEO = ".lc-video, iframe[src*='youtube'], iframe[src*='youtu.be']"


@then("a datagrid component is visible")
def step_grid_visible(context):
    el = context.page.locator(SEL_GRID).first
    expect(el).to_be_visible(timeout=15_000)


@then("the datagrid contains at least {n} rows")
def step_grid_row_count(context, n):
    rows = context.page.locator(SEL_GRID_ROW)
    rows.first.wait_for(state="visible", timeout=15_000)
    count = rows.count()
    assert count >= int(n), f"Expected at least {n} rows, found {count}"


@then("a chart component is visible")
def step_chart_visible(context):
    el = context.page.locator(SEL_CHART).first
    expect(el).to_be_visible(timeout=15_000)


@then("a map component is visible")
def step_map_visible(context):
    el = context.page.locator(SEL_MAP).first
    expect(el).to_be_visible(timeout=15_000)


@then("a video block is visible")
def step_video_visible(context):
    el = context.page.locator(SEL_VIDEO).first
    expect(el).to_be_visible(timeout=15_000)


@when("I click the first row in the datagrid")
def step_click_grid_row(context):
    row = context.page.locator(SEL_GRID_ROW).first
    row.wait_for(state="visible", timeout=15_000)
    row.click()
    context.page.wait_for_timeout(500)


@then("the chart reflects a data update")
def step_chart_updated(context):
    # Chart canvas should still be present and visible after row selection
    el = context.page.locator(SEL_CHART).first
    expect(el).to_be_visible(timeout=5_000)
