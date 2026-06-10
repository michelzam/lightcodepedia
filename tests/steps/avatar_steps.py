import re
from behave import when, then
from playwright.sync_api import expect


def _host(context, avatar_id):
    """The fixed overlay element the include appends to <body>."""
    return context.page.locator("#lc-avatar-" + avatar_id)


def _trigger(context, avatar_id):
    return context.page.locator("[data-avt-target='" + avatar_id + "']").first


@then('the avatar overlay "{avatar_id}" is visible')
def step_overlay_visible(context, avatar_id):
    expect(_host(context, avatar_id)).to_be_visible(timeout=15_000)


@when('I click the avatar trigger for "{avatar_id}"')
def step_click_trigger(context, avatar_id):
    # the trigger is a no-op until the avatar has registered itself
    expect(_host(context, avatar_id)).to_be_visible(timeout=15_000)
    trig = _trigger(context, avatar_id)
    trig.wait_for(state="visible", timeout=15_000)
    trig.click()
    context.page.wait_for_timeout(300)


@then('the avatar trigger for "{avatar_id}" shows the stop label')
def step_trigger_stop_label(context, avatar_id):
    expect(_trigger(context, avatar_id)).to_have_class(
        re.compile(r"playing"), timeout=5_000
    )


@then('the avatar "{avatar_id}" is in the "{state}" state')
def step_avatar_state(context, avatar_id, state):
    expect(_host(context, avatar_id)).to_have_attribute(
        "data-state", state, timeout=5_000
    )
