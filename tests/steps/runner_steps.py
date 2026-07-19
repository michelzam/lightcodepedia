import re
from behave import when, then
from playwright.sync_api import expect


@when('I open the runner page on "{src}"')
def step_open_runner(context, src):
    context.page.goto(context.base_url + "/run#src=" + src, wait_until="domcontentloaded")


@when("I wait for the runner to render")
def step_wait_render(context):
    # the status note hides when the render pipeline completes
    context.page.wait_for_selector(".lc-runner .lc-run-status", state="hidden", timeout=20_000)
    context.page.wait_for_timeout(400)


@then('the runner shows a heading "{text}"')
def step_heading(context, text):
    expect(context.page.locator("#lc-run h1", has_text=text)).to_be_visible()


@then("the runner shows bold text")
def step_bold(context):
    expect(context.page.locator("#lc-run strong").first).to_be_visible()


@then('the runner contains a "{sel}" element')
def step_contains(context, sel):
    expect(context.page.locator("#lc-run " + sel).first).to_be_visible(timeout=10_000)


@then('the rendered block mentions "{text}"')
def step_block_text(context, text):
    assert text in context.page.locator("#lc-run .lc-block").first.inner_text()


@then("the runner reports it could not load")
def step_error(context):
    # the status is visible immediately ("Loading…"); wait for the fetch to
    # actually 404 and the message to change — on a deployed CDN the round-trip
    # is not instant, so asserting on visibility alone races (was flaky red)
    status = context.page.locator(".lc-runner .lc-run-status")
    expect(status).to_contain_text(
        re.compile("could not load|is private", re.I), timeout=15_000
    )


@then("a rendered component carries an editable source snapshot")
def step_rt_snapshot(context):
    # the runner auto-ids fences and snapshots them pre-upgrade, so xray edits
    # the verbatim markdown source (backticks intact), not the rendered text
    got = context.page.evaluate(
        """() => {
          var el = document.querySelector('#lc-run [data-lc-id]');
          if (!el) return { ok: false, why: 'no data-lc-id wrapper' };
          var snap = window.lcSourceOf && window.lcSourceOf(el.getAttribute('data-lc-id'));
          return { ok: !!snap && snap.indexOf('Lucky') >= 0, why: (snap || '').slice(0, 60) };
        }"""
    )
    assert got["ok"], got["why"]


@then("footnote refs and their definitions render, none left raw")
def step_rt_footnotes(context):
    # marked has no footnote syntax; the client pipeline (lcClientFootnotes)
    # must emit the kramdown shape — datagrid.md has 3 live refs, one nested
    # inside another definition's body
    got = context.page.evaluate(
        """() => ({
          sups: document.querySelectorAll('#lc-run sup[id^=fnref] a.footnote').length,
          notes: document.querySelectorAll('#lc-run div.footnotes li[id^=fn]').length,
          raw: document.getElementById('lc-run').innerText.match(/\\[\\^[^\\]]+\\]:/g) || []
        })"""
    )
    assert got["sups"] >= 3 and got["notes"] >= 3 and not got["raw"], got
