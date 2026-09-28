"""The HQ map opens in the runner from the lab desk. The map itself is
served by a GitHub stub: the lab's real hq/index.md when it is on disk
(the lab), else the fixture under tests/fixtures (pedia, which carries no
hq/). Dates in the "last touched" list are rewritten by the scenario, so
the proof's verdict is the scenario's, never the calendar's."""
import datetime
import os
import re

from behave import given, when, then
from playwright.sync_api import expect

LAB = "michelzam/lightcodelab"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
MAP = os.path.join(ROOT, "hq", "index.md")
FIXTURE = os.path.join(ROOT, "tests", "fixtures", "hq_index.md")
TOPICS = ["engine.md", "cohorts.md", "partners.md"]


def _map_text(stale_topic=None, days=0):
    path = MAP if os.path.isfile(MAP) else FIXTURE
    with open(path, encoding="utf-8") as f:
        text = f.read()
    today = datetime.date.today()
    fresh = today.isoformat()
    old = (today - datetime.timedelta(days=days)).isoformat()

    def stamp(m):
        return m.group(1) + (old if m.group(2) == stale_topic else fresh) + '"'
    return re.sub(r'(topic:\s*(\w+),.*?last:\s*")\d{4}-\d{2}-\d{2}"', stamp, text)


def _serve(context, text):
    api = "https://api.github.com/repos/" + LAB

    context.hq_api_calls = []

    def handler(route):
        url = route.request.url
        context.hq_api_calls.append(url)
        if url.startswith(api + "/contents/hq/topics/") and url.endswith(".md") and os.path.isfile(
                os.path.join(ROOT, url[len(api + "/contents/"):])):
            # a real topic page from disk, when the lab is here
            with open(os.path.join(ROOT, url[len(api + "/contents/"):]), encoding="utf-8") as f:
                route.fulfill(status=200, content_type="text/plain; charset=utf-8", body=f.read())
            return
        if re.match(re.escape(api) + r"/contents/?(\?|$)", url):
            # the repo root: documents and folders, as GitHub lists them
            route.fulfill(status=200, json=[
                {"type": "file", "name": "CLAUDE.md", "path": "CLAUDE.md", "url": api + "/contents/CLAUDE.md"},
                {"type": "file", "name": "LAB.md", "path": "LAB.md", "url": api + "/contents/LAB.md"},
                {"type": "dir", "name": "courses", "path": "courses", "url": api + "/contents/courses"},
                {"type": "dir", "name": "hq", "path": "hq", "url": api + "/contents/hq"}])
            return
        if re.match(re.escape(api) + r"/contents/hq(\?|$)", url):
            route.fulfill(status=200, json=[
                {"type": "file", "name": "index.md", "path": "hq/index.md", "url": api + "/contents/hq/index.md"},
                {"type": "file", "name": "DECISION_REGISTER_20260718.md", "path": "hq/DECISION_REGISTER_20260718.md",
                 "url": api + "/contents/hq/DECISION_REGISTER_20260718.md"},
                {"type": "dir", "name": "topics", "path": "hq/topics", "url": api + "/contents/hq/topics"}])
            return
        if re.match(re.escape(api) + r"/contents/(CLAUDE|LAB)\.md|/contents/hq/DECISION", url):
            route.fulfill(status=200, content_type="text/plain", body="# A document\n\nOne line.\n")
            return
        if re.match(re.escape(api) + r"/contents/courses/[^?]*(\?|$)", url):
            route.fulfill(status=200, json=[
                {"type": "dir", "name": "module_0%d" % i, "path": "courses/micro_build_ai/module_0%d" % i,
                 "url": api + "/contents/courses/micro_build_ai/module_0%d" % i} for i in range(8)])
            return
        if url.startswith(api + "/contents/hq/index.md"):
            route.fulfill(status=200, content_type="text/plain; charset=utf-8", body=text)
            return
        if url.startswith(api + "/git/trees/"):
            # the folder takes one recursive tree census, then reads each page
            route.fulfill(status=200, json={"tree": [
                {"type": "blob", "path": "hq/topics/" + n} for n in TOPICS]})
            return
        if re.match(re.escape(api) + r"/contents/hq/topics(\?|$)", url):
            route.fulfill(status=200, json=[
                {"type": "file", "name": n, "path": "hq/topics/" + n,
                 "url": api + "/contents/hq/topics/" + n} for n in TOPICS])
            return
        if re.match(re.escape(api) + r"/contents/hq/topics/", url):
            route.fulfill(status=200, content_type="text/plain", body="# Topic\n\nA topic page.\n")
            return
        if re.match(re.escape(api) + r"(\?|$)", url):
            route.fulfill(status=200, json={"permissions": {"push": True}})
            return
        route.fulfill(status=404, json={"message": "hq stub"})

    context.page.route("https://api.github.com/**", handler)
    context.page.add_init_script("localStorage.setItem('lc_ed_pat','ghp_author');")


@given("the HQ map is served from the lab, touched today")
def step_map_fresh(context):
    _serve(context, _map_text())


@given('the HQ map is served from the lab, with "{topic}" last touched {days:d} days ago')
def step_map_stale(context, topic, days):
    _serve(context, _map_text(stale_topic=topic, days=days))


@then("the landing offers the HQ map in the runner")
def step_landing_door(context):
    a = context.page.locator("main a", has_text="Open the map").first
    expect(a).to_be_visible(timeout=10_000)
    href = a.get_attribute("href") or ""
    assert "run.html#src=gh:" + LAB + "/hq/index.md" in href, href


@then("the topic cards open in the runner")
def step_topic_cards(context):
    cards = context.page.locator('[data-lc-id="topic_cards"] a[href*="#src=gh:' + LAB + '/hq/topics/"]')
    expect(cards.first).to_be_visible(timeout=15_000)
    assert cards.count() == len(TOPICS), cards.count()


@then('the feature "{fid}" is green')
def step_feature_green(context, fid):
    card = context.page.locator('[data-lc-id="%s"]' % fid)
    expect(card).to_have_attribute("data-status", "passing", timeout=60_000)


@then('the feature "{fid}" is red and names "{what}"')
def step_feature_red_names(context, fid, what):
    card = context.page.locator('[data-lc-id="%s"]' % fid)
    expect(card).to_have_attribute("data-status", "failing", timeout=60_000)
    expect(card).to_contain_text(what)


@then('the shelf "{fid}" was listed from the repo root folder "{folder}"')
def step_shelf_root(context, fid, folder):
    expect(context.page.locator('[data-lc-id="%s"]' % fid)).to_be_attached(timeout=15_000)
    context.page.wait_for_timeout(1500)
    hits = [u for u in context.hq_api_calls if "/contents/" + folder in u]
    assert hits, "the shelf never asked for %s: %r" % (folder, context.hq_api_calls)
    assert not any("/contents//" in u or "/contents/hq/topics/" + folder in u or "/contents/hq/" + folder in u
                   for u in context.hq_api_calls), context.hq_api_calls


@then('the shelf "{fid}" opens "{path}" in the runner')
def step_shelf_opens(context, fid, path):
    card = context.page.locator('[data-lc-id="%s"] a[href*="#src=gh:%s/%s"]' % (fid, LAB, path))
    expect(card.first).to_be_visible(timeout=15_000)
