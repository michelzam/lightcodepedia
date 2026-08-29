import base64 as _b64
import hashlib
import json as _json

from behave import given, then, when
from playwright.sync_api import expect

# The 🎙️ studio, on a page the learner WALKED to. The docked seed lives on
# <body>, so an in-frame hop swaps the lesson under it while the seed stays —
# and the seed was born holding the first page's guide. The studio then voiced
# the page the learner LEFT and filed it under the page they were ON (410
# module_01, Michel 2026-08-29: three pages carrying one page's twelve
# recordings, two of them speaking robot).
#
# The whole flow is stubbed: an already-present mp3 (HEAD 200) takes the
# studio's cached path, so no ElevenLabs call is needed to reach the manifest
# commit — which is the fact under test.


@given("a voice key is in this browser")
def step_voice_key(context):
    context.page.add_init_script(
        "try { localStorage.setItem('lc_11_key', 'bdd-voice-key');"
        "      localStorage.setItem('lc_11_voice', 'bdd-voice-id'); } catch (e) {}"
    )


@given("every line's audio is already in the repo")
def step_audio_cached(context):
    """HEAD 200 on any studio file → the cached path, no synthesis needed."""
    context.page.route(
        "**/assets/audio/lc-*.mp3",
        lambda route, *a: route.fulfill(status=200, content_type="audio/mpeg",
                                        body=b"\xff\xe3\x18\xc4" + bytes(20)),
    )


@given("the voice manifest is watched")
def step_watch_manifest(context):
    context.vox_puts = []

    def fulfill(route, *a):
        req = route.request
        if req.method == "PUT":
            context.vox_puts.append(req.post_data or "")
            route.fulfill(status=200, content_type="application/json",
                          body='{"content":{"sha":"new-sha"}}')
            return
        route.fulfill(status=404, content_type="application/json", body="{}")

    context.page.route("**/api.github.com/repos/**/contents/docs/assets/audio/vox.json*",
                       fulfill)


@when('I walk to the next lesson through "{label}"')
def step_walk(context, label):
    context.page.click("#lc-run a:has-text('%s')" % label)
    context.page.wait_for_function(
        "() => { const r = document.querySelector('#lc-run[data-lc-src-path]');"
        "        return r && /02_/.test(r.dataset.lcSrcPath); }",
        timeout=10_000,
    )
    context.page.wait_for_timeout(1200)   # the render's avatars register


@when("I record the guide's voices")
def step_record(context):
    context.page.click("#guide_seed")
    voices = context.page.get_by_text("🎙️ Voices")
    expect(voices).to_be_visible(timeout=5_000)
    voices.click()


def _manifest(context):
    for _ in range(40):
        for body in context.vox_puts:
            try:
                payload = _json.loads(body)
                return _json.loads(_b64.b64decode(payload["content"]).decode("utf-8"))
            except Exception:
                continue
        context.page.wait_for_timeout(250)
    raise AssertionError("the studio committed no voice manifest")


@then('the recordings filed under "{slug}" are of "{line}"')
def step_filed_under(context, slug, line):
    man = _manifest(context)
    assert slug in man, "manifest holds %r, not %r" % (list(man), slug)
    keys = set()
    for lines in man[slug].values():
        keys |= set(lines)
    want = hashlib.sha1(line.encode()).hexdigest()[:16]
    assert want in keys, ("%r is not among the %d recording(s) filed under %r"
                          % (line, len(keys), slug))


@then('no recording is of "{line}"')
def step_no_recording_of(context, line):
    man = _manifest(context)
    stray = hashlib.sha1(line.encode()).hexdigest()[:16]
    for slug, ids in man.items():
        for lines in ids.values():
            assert stray not in lines, (
                "%r was recorded under %r — the page the learner left" % (line, slug))
