"""Doc's pad verbs, driven the way a script line drives them."""
from behave import given, when, then
from playwright.sync_api import expect


def _ta(context, pad_id):
    return context.page.locator("[data-lc-id='%s'] .lc-mdpad-in" % pad_id)


def _act(context, verb, pad_id, arg=None, with_steps=False):
    try:
        context.page.wait_for_selector("[data-lc-id='%s'] .lc-mdpad-in" % pad_id, state="attached", timeout=20_000)
    except Exception:
        print("PAGE:", context.page.evaluate("document.body.innerText.slice(0, 600)"))
        raise
    ok = context.page.evaluate("""([verb, id, arg, withSteps]) => {
      const pad = document.querySelector("[data-lc-id='" + id + "']");
      const av = (window._lcAvatars || {}).guide;
      const ctx = { steps: (av && av.steps) || [] };
      return window.lcVerbs.act(verb, pad, arg, withSteps || verb === 'type' || verb === 'save' ? ctx : {});
    }""", [verb, pad_id, arg, with_steps])
    context.page.wait_for_timeout(2600 if verb in ("type", "replay", "moonwalk", "play") else 600)
    return ok


@when('Doc does "{verb}" with {n:d} on the "{pad_id}" pad')
def step_do_n(context, verb, n, pad_id):
    _act(context, verb, pad_id, n)


@when('Doc does "{verb}" on the "{pad_id}" pad with his steps')
def step_do_steps(context, verb, pad_id):
    _act(context, verb, pad_id, None, True)


@when('Doc does "{verb}" on the "{pad_id}" pad')
def step_do(context, verb, pad_id):
    _act(context, verb, pad_id)


@then("the \"{pad_id}\" pad holds '{text}' once")
def step_holds_once(context, pad_id, text):
    v = _ta(context, pad_id).input_value()
    assert v.count(text) == 1, "%r appears %d times in:\n%s" % (text, v.count(text), v)


@then("the \"{pad_id}\" pad holds '{text}'")
def step_holds(context, pad_id, text):
    expect(_ta(context, pad_id)).to_have_value(__import__("re").compile(__import__("re").escape(text)), timeout=5_000)


@then('the "{pad_id}" pad does not hold "{text}"')
def step_not_holds(context, pad_id, text):
    v = _ta(context, pad_id).input_value()
    assert text not in v, v


@given("the key is paired as the author's own")
def step_author_pair(context):
    context.page.add_init_script("localStorage.setItem('lc_ed_session', 'lc:author');")


@when('I click the trigger "{label}"')
def step_click_trigger(context, label):
    btn = context.page.get_by_text(label, exact=True).first
    btn.wait_for(timeout=15_000)
    context.page.wait_for_timeout(800)
    btn.click()
    context.page.wait_for_timeout(4000)


@then('the "{pad_id}" pad offers to keep it as "{line}"')
def step_offers(context, pad_id, line):
    inp = context.page.locator(".lc-mdpad-commentbar input")
    expect(inp).to_have_value(line, timeout=10_000)


@then('the bench received a commit titled "{title}"')
def step_commit_title(context, title):
    context.page.wait_for_timeout(1500)
    msgs = [c["message"] for c in context.bench_commits]
    assert title in msgs, "commits: %r" % msgs


def _film(context, pad_id):
    return context.page.evaluate("""(id) => {
      const w = document.querySelector("[data-lc-id='" + id + "']");
      return { on: w.hasAttribute('data-lc-replay'), frame: +(w.getAttribute('data-lc-frame') || -1) + 1,
               count: +(w.getAttribute('data-lc-frames') || 0) };
    }""", pad_id)


@then('the "{pad_id}" pad\'s film holds {n:d} frames')
def step_film_count(context, pad_id, n):
    f = _film(context, pad_id)
    assert f["on"] and f["count"] == n, f


@then('the "{pad_id}" pad\'s film ends on frame {n:d}')
def step_film_ends(context, pad_id, n):
    context.page.wait_for_function(
        "([id, n]) => { const w = document.querySelector(\"[data-lc-id='\" + id + \"']\");"
        " return w && !w.hasAttribute('data-lc-playing') && +(w.getAttribute('data-lc-frame')) + 1 === n; }",
        arg=[pad_id, n], timeout=10_000)


@then('the "{pad_id}" pad\'s film shows frame {n:d}')
def step_film_shows(context, pad_id, n):
    f = _film(context, pad_id)
    assert f["frame"] == n, f


@then('the "{pad_id}" pad\'s film is closed')
def step_film_closed(context, pad_id):
    f = _film(context, pad_id)
    assert not f["on"], f


@then('the check\'s step "{text}" is green')
def step_check_green(context, text):
    step = context.page.locator(".lc-feature-step", has_text=text).first
    expect(step.locator(".lc-feature-step-icon.pass")).to_be_attached(timeout=30_000)


@then('the "{pad_id}" pad is not held')
def step_not_held(context, pad_id):
    held = context.page.evaluate("(id) => document.querySelector(\"[data-lc-id='\" + id + \"']\")._lcHeld", pad_id)
    assert not held, held


@when('Doc types into the "{pad_id}" pad a step that forgets its decoration')
def step_type_bad(context, pad_id):
    context.page.wait_for_selector("[data-lc-id='%s'] .lc-mdpad-in" % pad_id, state="attached", timeout=20_000)
    context.page.evaluate("""(id) => {
      const pad = document.querySelector("[data-lc-id='" + id + "']");
      const steps = [
        { say: "a grid without its decoration",
          check: "a datagrid reads the reservations",
          lines: "[Families](#)" },
        { say: "a button",
          lines: "[Call](#)\\n{: .button }" }];
      window.lcVerbs.act('type', pad, 1, { steps });
      window.lcVerbs.act('type', pad, 2, { steps });
    }""", pad_id)
    context.page.wait_for_timeout(1500)


@then('the "{pad_id}" pad is held, saying "{text}"')
def step_held(context, pad_id, text):
    try:
        context.page.wait_for_function(
            "(id) => document.querySelector(\"[data-lc-id='\" + id + \"']\")._lcHeld", arg=pad_id, timeout=30_000)
    except Exception:
        print("DBG", context.page.evaluate("""(id) => { const w = document.querySelector("[data-lc-id='" + id + "']");
          return { val: w.querySelector('.lc-mdpad-in').value.slice(-300),
                   steps: [...document.querySelectorAll('.lc-feature-step')].map(s => (s.querySelector('.lc-feature-step-icon')||{}).className + ' ' + (s.textContent||'').slice(0,50)) }; }""", pad_id))
        raise
    held = context.page.evaluate("(id) => document.querySelector(\"[data-lc-id='\" + id + \"']\")._lcHeld", pad_id)
    assert held.startswith("🔴") and text in held, held
    context.held_message = held
