"""One painter for code: the pad's fences, the .code cards, a feature's steps."""
from behave import when, then
from playwright.sync_api import expect


@then('the "{pad_id}" pad paints "{a}" and "{b}" as keywords')
def step_pad_sql(context, pad_id, a, b):
    piano = context.page.locator("[data-lc-id='%s'] .lc-mdpad-piano" % pad_id)
    expect(piano.locator(".md-kw").first).to_have_text(a, timeout=15_000)
    expect(piano.locator(".md-kw", has_text=b).first).to_be_attached()


@when('I open the first step code of the feature "{fid}"')
def step_open_impl(context, fid):
    card = context.page.locator(".lc-feature[data-lc-id='%s']" % fid)
    card.wait_for(timeout=15_000)
    impl = card.locator(".lc-feature-step-impl").first
    if not impl.evaluate("e => e.classList.contains('open')"):
        impl.evaluate("e => e.classList.add('open')")
    context.impl = impl


@then("that step code is painted on the gray")
def step_impl_painted(context):
    pre = context.impl.locator("pre.lc-md-paint")
    expect(pre).to_be_attached(timeout=10_000)
    assert pre.locator(".md-kw, .md-fn, .md-str").count() > 0, pre.inner_html()[:200]
    bg = pre.evaluate("e => getComputedStyle(e).backgroundColor")
    assert bg == "rgb(242, 244, 247)", "step code background is %s, not the cards' gray" % bg
