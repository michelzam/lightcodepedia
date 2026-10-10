"""A paged datagrid: its title bar, and a page turn the detail form follows."""
from behave import when, then
from playwright.sync_api import expect


@then('the "{gid}" grid\'s title bar reads "{text}"')
def step_title(context, gid, text):
    bar = context.page.locator("[data-lc-id='%s'] .lc-dg-titlebar" % gid)
    expect(bar).to_have_text(text, timeout=15_000)


@then('the form shows "{text}"')
def step_form_shows(context, text):
    expect(context.page.locator(".lc-form").first).to_contain_text(text, timeout=10_000)


@when('I turn the "{gid}" grid to its next page')
def step_next_page(context, gid):
    btn = context.page.locator("[data-lc-id='%s'] .lc-dg-pages button" % gid).last
    expect(btn).to_have_text("→", timeout=15_000)
    btn.click()
    context.page.wait_for_timeout(300)


@then('the "{gid}" grid has "{text}" selected')
def step_selected(context, gid, text):
    row = context.page.locator("[data-lc-id='%s'] tr.lc-dg-selected" % gid)
    expect(row).to_contain_text(text, timeout=5_000)
