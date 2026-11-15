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


# ── a new voice id (Michel, 2026-11-15) ───────────────────────────────────
# A page that had voiced once held the id for the visit: a Shift-click went
# straight to generating with the OLD voice, and a phone had no Shift at all.

@given('the voice prompt answers "{vid}"')
def step_voice_prompt(context, vid):
    context.voice_asked = []

    def answer(dialog):
        if "voice id" in dialog.message:
            context.voice_asked.append(dialog.default_value)
            dialog.accept(vid)
        else:
            dialog.accept(dialog.default_value)

    context.page.on("dialog", answer)


@when('I click "{label}" with Shift held')
def step_shift_click(context, label):
    context.page.get_by_text(label).first.click(modifiers=["Shift"])


@when('I click the voices button "{label}"')
def step_plain_click(context, label):
    context.page.get_by_text(label).first.click()


@when("the studio has committed {n:d} voice manifest")
@when("the studio has committed {n:d} voice manifests")
def step_wait_manifests(context, n):
    for _ in range(60):
        if len(context.vox_puts) >= n:
            return
        context.page.wait_for_timeout(250)
    raise AssertionError("the studio committed %d manifest(s), not %d" % (len(context.vox_puts), n))


@when("I change the guide's voice from its menu")
def step_change_voice(context):
    context.page.click("#guide_seed")
    item = context.page.get_by_text("🎙️ Change voice")
    expect(item).to_be_visible(timeout=5_000)
    item.click()


@then('the voice prompt offered "{vid}" to replace')
def step_prompt_offered(context, vid):
    assert context.voice_asked, "the voice id was never asked"
    assert context.voice_asked[-1] == vid, "the prompt offered %r" % context.voice_asked[-1]


@then('the last manifest voices "{line}" with "{vid}"')
def step_last_manifest_voice(context, line, vid):
    body = _json.loads(context.vox_puts[-1])
    man = _json.loads(_b64.b64decode(body["content"]).decode("utf-8"))
    files = set()
    for ids in man.values():
        for lines in ids.values():
            files |= set(lines.values())
    h = hashlib.sha1(("%s|eleven_multilingual_v2|%s" % (vid, line)).encode()).hexdigest()[:16]
    assert "lc-%s.mp3" % h in files, "%r is not voiced with %r — files: %r" % (line, vid, sorted(files))


@then('this browser remembers the voice "{vid}"')
def step_remembers_voice(context, vid):
    got = context.page.evaluate("() => localStorage.getItem('lc_11_voice')")
    assert got == vid, "this browser holds the voice %r" % got


@given("every line's audio is in the repo but not yet on the site")
def step_audio_in_repo_only(context):
    # the site's copy: not published yet (Pages still rebuilding)
    context.page.route(
        "**/assets/audio/lc-*.mp3",
        lambda route, *a: route.fulfill(status=404, body=b""),
    )
    # the repo's copy: committed a minute ago (registered last → wins)
    context.page.route(
        "**/api.github.com/repos/acme/demo/contents/docs/assets/audio/lc-*.mp3",
        lambda route, *a: route.fulfill(status=200, content_type="application/json",
                                        body='{"sha":"in-repo"}'),
    )


@given("ElevenLabs calls are counted")
def step_count_eleven(context):
    context.eleven_calls = []

    def fulfill(route, *a):
        context.eleven_calls.append(route.request.url)
        route.fulfill(status=200, content_type="audio/mpeg", body=b"\xff\xe3\x18\xc4" + bytes(20))

    context.page.route("**/api.elevenlabs.io/**", fulfill)


@then("ElevenLabs was called {n:d} times")
def step_eleven_called(context, n):
    assert len(context.eleven_calls) == n, "ElevenLabs was called %d time(s): %r" % (
        len(context.eleven_calls), context.eleven_calls)


@then('the guide says "{text}"')
def step_guide_says(context, text):
    expect(context.page.locator(".lc-guide-hello", has_text=text).first).to_be_visible(timeout=10_000)


@when("I open the guide's menu")
def step_open_guide_menu(context):
    context.page.click("#guide_seed")
    context.page.wait_for_timeout(800)   # the ownership answer is async


@then('the guide\'s menu has no "{label}"')
def step_menu_has_no(context, label):
    assert context.page.get_by_text(label, exact=True).count() == 0, "%r is in the menu" % label
