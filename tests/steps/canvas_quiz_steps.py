"""The Canvas quiz desk: a stubbed Canvas + specs served as the lab repo's own."""
import json

from behave import given, when, then
from playwright.sync_api import expect

HOST = "https://canvas.test"
COURSE = "4242"

CLEAN = """# 05 \u00b7 Basement \u2014 check
{: .canvas_quiz anchors="reservations, met, Diallo" }

### The four words

Your reservations list shows 14 rows and the check names five families. Which fix?

- [ ] Add WHERE home = '' so the dogs not yet home stay listed

  > Diallo met Scout already; the call is done.

- [x] Add WHERE met = '' so families who never met a dog stay

  > Nine rows left \u2014 the ones still waiting for a call.

- [ ] Sort the grid by met and hide the rows already filled

  > The view would look right while the question stayed wrong.

- [ ] Remove those five families from the reservations data

  > Their reservations are real; the data is not what is wrong.

{: .quiz }

### values vs count

Why does the check read values("met") from to_call rather than count?

- [x] It reads inside the rows, so the check can name the five

  > Which is why the red message could name them.

- [ ] It runs faster than count on a query bound to a set

  > Speed is not the question with fourteen rows.

- [ ] It is required when a feature card carries a grades knob

  > The grades knob decides who awards the colour.

- [ ] It works on datasets, while count works on queries only

  > Both work on both.

{: .quiz }
"""

TELLS = """# Tempting
{: .canvas_quiz anchors="reservations" }

### The tell

In the reservations list, which fix makes the check green?

- [ ] Sort the grid

  > no

- [ ] Delete the rows

  > no

- [x] **Add `WHERE met = ''` so the list keeps only the families still waiting**

  > yes

- [ ] Call them all

  > no

{: .quiz }
"""

GENERIC = """# Generic
{: .canvas_quiz anchors="reservations, Diallo" }

### sql

What does the SQL WHERE clause do?

- [x] It filters the rows a query returns

  > yes

- [ ] It sorts the rows a query returns

  > no

- [ ] It joins two tables on a column

  > no

{: .quiz }
"""


def _stub(context, spec_text, existing=None):
    context.canvas_posts = []
    context.spec_text = spec_text
    # the desk's PAGE and its SPEC both come through the contents API — the
    # path says which is which
    page_md = (
        "# Canvas desk\n\n"
        "[Canvas quiz desk](#)\n"
        '{: .canvas_quiz #m05 course="' + COURSE + '" host="' + HOST + '" '
        'spec="hq/quizzes/demo.md" }\n')

    def contents(route):
        body = spec_text if "quizzes/" in route.request.url else page_md
        route.fulfill(status=200, content_type="text/plain", body=body)

    context.page.route("https://api.github.com/repos/**/contents/**", contents)

    quizzes = existing if existing is not None else [
        {"id": 7, "title": "Something else", "published": True, "question_count": 3}]

    def canvas(route):
        req = route.request
        if req.method == "GET" and "/quizzes" in req.url:
            route.fulfill(status=200, content_type="application/json", body=json.dumps(quizzes))
        else:
            context.canvas_posts.append(req.url)
            route.fulfill(status=200, content_type="application/json",
                          body=json.dumps({"id": 99}))

    context.page.route(HOST + "/api/v1/**", canvas)
    context.page.add_init_script(
        "localStorage.setItem('lc_ed_pat','ghp_author');"
        "localStorage.setItem('lc_canvas_key','1234~stub');")


@given("a stubbed Canvas course")
def step_canvas_course(context):
    context.canvas_existing = None


@given('the spec "{path}" is the module 05 quiz')
def step_spec_clean(context, path):
    _stub(context, CLEAN, context.canvas_existing)


@given('the spec "{path}" has a key that is longest and bold')
def step_spec_tells(context, path):
    _stub(context, TELLS)


@given('the spec "{path}" asks a generic SQL question')
def step_spec_generic(context, path):
    _stub(context, GENERIC)


@given("the course already holds that quiz, published, with questions")
def step_course_has_published(context):
    _stub(context, CLEAN, [{"id": 12, "title": "05 · Basement — check",
                            "published": True, "question_count": 5}])


@when("I open the canvas desk for that spec")
def step_open_desk(context):
    """Rendered through the runner, so the block carries the stub's host and
    course — the lab page itself ships with no course id on purpose."""
    context.page.goto(
        context.base_url + "/run.html#src=gh:michelzam/lightcodelab/docs/lab/canvas_desk.md",
        wait_until="domcontentloaded")
    context.page.locator(".lc-cq").first.wait_for(timeout=20_000)


@when("I open the canvas desk with its inspection grids")
def step_open_desk_grids(context):
    """The __quiz folder page's shape: the desk plus a questions grid, a
    bound form, and a master-filtered options grid over its datasets."""
    page_md = (
        "# Canvas desk\n\n"
        "[Canvas quiz desk](#)\n"
        '{: .canvas_quiz #m05 spec="hq/quizzes/demo.md" }\n\n'
        "[questions](#)\n"
        '{: .datagrid #m05q bind="m05_questions" rows="6" }\n\n'
        "```yaml\n```\n"
        '{: .form bound="m05q" title="Question" }\n\n'
        "[options](#)\n"
        '{: .datagrid #m05o bind="m05_options" master="m05q" filter="q=q" rows="10" }\n\n'
        "```yaml\n```\n"
        '{: .form bound="m05o" title="Option" }\n')

    def contents(route):
        body = context.spec_text if "quizzes/" in route.request.url else page_md
        route.fulfill(status=200, content_type="text/plain", body=body)

    context.page.route("https://api.github.com/repos/**/contents/**", contents)
    context.page.goto(
        context.base_url + "/run.html#src=gh:michelzam/lightcodelab/docs/lab/canvas_desk.md",
        wait_until="domcontentloaded")
    context.page.locator(".lc-cq").first.wait_for(timeout=20_000)


@then("the questions grid lists the spec's questions")
def step_grid_questions(context):
    # the runner road renders the light table, the lab road AG — accept both
    grid = context.page.locator(
        '[data-lc-id="m05q"] .ag-row, [data-lc-id="m05q"] .lc-dg-table tbody tr')
    expect(grid.first).to_be_visible(timeout=20_000)
    assert grid.count() >= 1, "no question rows"


@then("the options grid carries a marked key")
def step_grid_key(context):
    cell = context.page.locator(
        '[data-lc-id="m05o"] .ag-cell, [data-lc-id="m05o"] .lc-dg-table td').filter(has_text="✅")
    expect(cell.first).to_be_visible(timeout=20_000)


@then("the options grid shows only the first question's options")
def step_options_first(context):
    rows = context.page.locator('[data-lc-id="m05o"] .lc-dg-table tbody tr')
    expect(rows.first).to_be_visible(timeout=20_000)
    n = context.page.evaluate("(window.lcDatasets.m05_options||[]).filter(o=>o.q===1).length")
    assert rows.count() == n, "%d rows for %d q1 options" % (rows.count(), n)


@when("I select the second question row")
def step_select_q2(context):
    context.page.locator('[data-lc-id="m05q"] .lc-dg-table tbody tr').nth(1).click()
    context.page.wait_for_timeout(400)


@then("the options grid shows only the second question's options")
def step_options_second(context):
    n = context.page.evaluate("(window.lcDatasets.m05_options||[]).filter(o=>o.q===2).length")
    rows = context.page.locator('[data-lc-id="m05o"] .lc-dg-table tbody tr')
    assert rows.count() == n, "%d rows for %d q2 options" % (rows.count(), n)


@then("the bound form shows the second question")
def step_form_q2(context):
    name = context.page.evaluate("(window.lcDatasets.m05_questions||[])[1].name")
    form = context.page.locator(".lc-form")
    expect(form.first).to_be_visible(timeout=10_000)
    assert name in form.first.text_content(), "form does not carry %r" % name


@then("the option form follows into the second question's options")
def step_option_form_follows(context):
    """The master moved, so the option form must show a q2 option — never a
    leftover from q1 (the detail republishes its first row on master change)."""
    why = context.page.evaluate(
        "(window.lcDatasets.m05_options||[]).filter(o=>o.q===2)[0].why")
    form = context.page.locator('.lc-form[data-bound="m05o"], .lc-form:has(.lc-form-name:text("Option"))').last
    expect(form).to_be_visible(timeout=10_000)
    assert why in form.text_content(), "option form does not carry a q2 option"


@when("I press the quiz desk's {label} button")
def step_press(context, label):
    sel = {"Lint": '[data-a="lint"]', "Read Canvas": '[data-a="read"]',
           "Push": '[data-a="push"]'}[label]
    context.page.click(".lc-cq " + sel)
    context.page.wait_for_timeout(1200)


@then("the desk reports no tells")
def step_no_tells(context):
    expect(context.page.locator(".lc-cq-msg")).to_contain_text("no tells", timeout=10_000)


@then("the push button is offered")
def step_push_offered(context):
    expect(context.page.locator('.lc-cq [data-a="push"]')).to_be_enabled(timeout=8_000)


@then("the desk names the longest-option tell")
def step_longest(context):
    expect(context.page.locator(".lc-cq-msg")).to_contain_text("longest option", timeout=10_000)


@then("the desk names the decoration tell")
def step_decoration(context):
    expect(context.page.locator(".lc-cq-msg")).to_contain_text("bold/code/emoji")


@then("the push button stays out of reach")
def step_push_blocked(context):
    expect(context.page.locator('.lc-cq [data-a="push"]')).to_be_disabled()


@then("the desk says the question names nothing from the module")
def step_generic_named(context):
    expect(context.page.locator(".lc-cq-msg")).to_contain_text(
        "names nothing from the module", timeout=10_000)


@then("the desk lists the course's quizzes")
def step_lists(context):
    expect(context.page.locator(".lc-cq-list")).to_contain_text("Something else", timeout=10_000)


@then("the desk refuses to touch the published quiz")
def step_refuses(context):
    expect(context.page.locator(".lc-cq-msg")).to_contain_text("Unpublish", timeout=10_000)
    assert not [u for u in context.canvas_posts if "questions" in u], \
        "it wrote questions into a published quiz: %r" % context.canvas_posts
