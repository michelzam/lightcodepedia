"""The x-ray verb's beats, driven the way a script line drives them (2026-11-04)."""
from behave import when, then
from playwright.sync_api import expect


@when('Doc does "xray" with "{arg}" on the part "{lc_id}"')
def step_xray_verb(context, arg, lc_id):
    context.page.wait_for_selector("[data-lc-id='%s']" % lc_id, timeout=25_000)
    ok = context.page.evaluate("""([id, arg]) => {
      const el = document.querySelector("[data-lc-id='" + id + "']");
      return window.lcVerbs.act('xray', el, arg === 'pipes' ? null : arg, {});
    }""", [lc_id, arg])
    assert ok, "the xray verb refused"
    context.page.wait_for_timeout(1500)


@when('the guide "{avatar_id}" is performing')
def step_guide_performing(context, avatar_id):
    # a tour in flight: the avatar's playing flag, the way the trigger sets it
    context.page.wait_for_function(
        "(id) => window._lcAvatars && window._lcAvatars[id]", arg=avatar_id, timeout=25_000)
    context.page.evaluate("(id) => { window._lcAvatars[id].playing = true; }", avatar_id)


@then("the x-ray shows one ghost and no pipes")
def step_lens_only(context):
    scene = context.page.locator("#lcx-scene")
    expect(scene).to_be_visible(timeout=10_000)
    shown, svg = context.page.evaluate("""() => {
      const scene = document.getElementById('lcx-scene');
      const ghosts = [...scene.children].filter(c => c.tagName !== 'svg' && !c.classList.contains('lcx-full') && c.style.display === 'block');
      const svg = scene.querySelector('.lcx-svg');
      return [ghosts.length, svg ? svg.style.display : 'absent'];
    }""")
    assert shown == 1, "the lens showed %d ghosts, the loupe is one" % shown
    assert svg == "none", "the lens drew pipes (svg display: %s)" % svg


@then('the x-ray scene never mentions "{keyword}"')
def step_scene_never(context, keyword):
    scene = context.page.locator("#lcx-scene")
    expect(scene).to_contain_text("Dataset", timeout=30_000)
    expect(scene).not_to_contain_text(keyword)
