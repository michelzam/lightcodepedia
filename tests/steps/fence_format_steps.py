"""A data fence's own format word decides how its rows are read."""
from behave import then
import re
from playwright.sync_api import expect


@then('the "{gid}" grid shows the cell "{text}"')
def step_grid_cell(context, gid, text):
    cell = context.page.locator("[data-lc-id='%s'] td, [data-lc-id='%s'] .ag-cell" % (gid, gid)).filter(has_text=re.compile(r"^\s*" + re.escape(text) + r"\s*$"))
    expect(cell.first).to_be_visible(timeout=15_000)
