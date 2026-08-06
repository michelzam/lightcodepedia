from behave import then, when
from playwright.sync_api import expect

# The volunteer rubric (module_01): an mdpad the acceptance criteria can
# grade. Red first is part of the contract — the wall-of-text seed MUST
# fail, or the rubric is decoration, not evidence.


@then("the embedded feature ends red")
def step_feature_ends_red(context):
    # the failing badge appears only when the MicroPython run finished and
    # at least one step assertion raised — a crash or a hang never gets here
    expect(
        context.page.locator(".lc-feature .lc-feature-badge-failing").first
    ).to_be_visible(timeout=45_000)


@then("the step error blames the engine, not the learner")
def step_error_blames_engine(context):
    err = context.page.locator(".lc-feature-step-err").first
    expect(err).to_be_visible(timeout=15_000)
    text = err.inner_text()
    # It used to read "a newer engine" and tell the reader to publish. Michel
    # published, nothing changed, and the message had sent him chasing a fix
    # that was never the problem (2026-08-05). The contract now: say plainly it
    # is not the learner, name whose bug it is, prescribe nothing.
    assert "Not you" in text, text
    assert "page's bug" in text, text
    assert "newer engine" not in text and "publish" not in text.lower(), \
        "the message is prescribing a publish again: " + text
    # the technical cause stays visible for authors, in parentheses
    assert "attribute" in text, text


@when("I retype the pad with")
@when("I retype the pad with:")
def step_retype_pad(context):
    # fill() replaces the textarea's value and fires the input event — the
    # same path a typing learner takes, so the preview re-renders live
    ta = context.page.locator(".lc-mdpad-in").first
    ta.wait_for(state="visible", timeout=15_000)
    ta.fill(context.text)
