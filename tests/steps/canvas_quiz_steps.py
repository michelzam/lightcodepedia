"""The Canvas quiz desk: a stubbed Canvas + specs served as the lab repo's own."""
import json

from behave import given, when, then
from playwright.sync_api import expect

HOST = "https://canvas.test"
COURSE = "4242"

CLEAN = """
title: "05 · Basement — check"
anchors: [reservations, met, Diallo]
questions:
  - name: The four words
    text: "Your reservations list shows 14 rows and the check names five families. Which fix?"
    answers:
      - text: "Add WHERE home = '' so the dogs not yet home stay listed"
        why: "Diallo met Scout already; the call is done."
      - text: "Add WHERE met = '' so families who never met a dog stay"
        correct: true
        why: "Nine rows left — the ones still waiting for a call."
      - text: "Sort the grid by met and hide the rows already filled"
        why: "The view would look right while the question stayed wrong."
      - text: "Remove those five families from the reservations data"
        why: "Their reservations are real; the data is not what is wrong."
  - name: values vs count
    text: "Why does the check read values(\\"met\\") from to_call rather than count?"
    answers:
      - text: "It reads inside the rows, so the check can name the five"
        correct: true
        why: "Which is why the red message could name them."
      - text: "It runs faster than count on a query bound to a set"
        why: "Speed is not the question with fourteen rows."
      - text: "It is required when a feature card carries a grades knob"
        why: "The grades knob decides who awards the colour."
      - text: "It works on datasets, while count works on queries only"
        why: "Both work on both."
"""

TELLS = """
title: "Tempting"
anchors: [reservations]
questions:
  - name: The tell
    text: "In the reservations list, which fix makes the check green?"
    answers:
      - text: "Sort the grid"
      - text: "Delete the rows"
      - text: "**Add `WHERE met = ''` so the list keeps only the families still waiting**"
        correct: true
      - text: "Call them all"
"""

GENERIC = """
title: "Generic"
anchors: [reservations, Diallo]
questions:
  - name: sql
    text: "What does the SQL WHERE clause do?"
    answers:
      - text: "It filters the rows a query returns"
        correct: true
      - text: "It sorts the rows a query returns"
      - text: "It joins two tables on a column"
"""


def _stub(context, spec_text, existing=None):
    context.canvas_posts = []
    # the desk's PAGE and its SPEC both come through the contents API — the
    # path says which is which
    page_md = (
        "# Canvas desk\n\n"
        "[Canvas quiz desk](#)\n"
        '{: .canvas_quiz #m05 course="' + COURSE + '" host="' + HOST + '" '
        'spec="hq/quizzes/demo.yaml" }\n')

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
