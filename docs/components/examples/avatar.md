---
---

# 🗣️ Speaking Avatar

A speaking overlay character that narrates content and **follows the elements it describes**: give a script line an `at:` selector and the avatar scrolls there, parks beside it, spotlights it, and speaks. Three character tiers below — the built-in face, a recorded video, a live state machine.

Press **▶ Play**, or click a character directly to toggle.

---

## 🙂 Prof. Light — the built-in face {#prof_light}

Zero assets: blinks, eyes track the spotlight, the mouth moves while speaking. This one **walks the page**.

```yaml
name: "Prof. Light"
voice: en-US
script:
  - "Hi! I'm the built-in avatar — no animation file needed."
  - at: "#rive_demo"
    say: "This is Riv — a state machine, not a recording."
  - at: "#how_it_works"
    say: "And this table explains every attribute. See you there!"
  - at: "#aristotle_demo"
    say: "(Aristotle's real voice — my mouth follows its waveform)"
    audio: /assets/audio/aristotle_voice_8s.m4a
```
{: .avatar #prof_avatar }

[▶ Play](#)
{: .avatar-trigger target="prof_avatar" label-stop="⏹ Stop" }

---

## 🪜 Step-by-step — you click for the next line {#step_demo}

Add `step="true"` and the avatar **waits between lines**: each click on the trigger
(or the character) speaks the next line and stops. The button reads
**▶ Start → Next → (n/total) → ↺ Replay**. Ideal for live walk-throughs and
screen recordings, where you set the pace and sync narration to what you're doing.

```yaml
name: "Step Guide"
voice: en-US
script:
  - "Click Next — I wait for you between every line."
  - at: "#how_it_works"
    say: "Now we're at the attribute table. Click again when you're ready…"
  - at: "#finding_characters"
    say: "…and now down here. You set the pace — perfect for recording."
```
{: .avatar #step_avatar step="true" }

[▶ Start](#)
{: .avatar-trigger target="step_avatar" label-stop="⏹ Stop" }

---

## 🧙 Aristotle — a recorded Memoji on a timed walk {#aristotle_demo}

The realism ceiling: a **recorded character** — an iPhone Memoji with a real
voice, one take. **Timed cues** walk him to the components he describes while
the recording plays. (`t:` values are tuned to the narration; cues can also
drive slides: `slide: next`.)

```yaml
name: "Aristotle"
video:
  - /assets/avatar/aristotle_alpha.webm
  - /assets/avatar/aristotle.mp4
transparent: true
script:
  - say: "Hi, I'm Aristotle, considered by some father of modern science."
    video: true
    cues:
      - t: 0
        at: "#aristotle_avatar"
      - t: 5
        say: "I look smart, isn't it?"
      - t: 10
        at: "#rive_demo"
        say: "⏳ I'm a time-travaler!"
      - t: 20
        at: "#how_it_works"
        say: "😊 Happy learning!"
```
{: .avatar #aristotle_avatar size="180" step="true"}

[▶ Play](#)
{: .avatar-trigger target="aristotle_avatar" label-stop="⏹ Stop" }

---

## 🔒 Runtime video — a secret clip that never touches the repo {#runtime_video}

**For a secret video, use 📁 Choose a local file** (below). The browser reads it
straight off your disk into an **in-memory blob** and plays it as the avatar —
**never uploaded, never committed, never even typed**, gone when you close the
tab. **With sound**, and a VP9-alpha `.webm` keeps its transparency. Nothing
about the clip reaches GitHub. *(`file:///Users/…` paths can't be used directly —
browsers block a page from reading your disk; the picker is exactly how you hand
one over, privately.)*

**Only for a clip you're fine publishing**, the form also accepts a URL — a
served `/assets/clip.mp4`, any direct `.mp4/.webm` link, or an unlisted
**YouTube** link (which autoplays **muted**). For your secret recording: use the
picker, not a URL.

Both routes end at `button.page.secret_avatar.video(url)`; cues fire by real
playback time. Set it, **fold** the panel, press ▶ Play.

````
### !🔗 Video source — *set off-camera, then fold*
```yaml
video_url: ""
```
{: .form #secret_src editable="true" title="Private video URL" }

[📼 Load video](#)
{: .button #load_secret_video }

```python
def on_click(button):
    u = (button.page.secret_src.data.video_url or "").strip()
    if u:
        button.page.secret_avatar.video(u)
```
{: .onclick }
````
{: .accordion }

[📁 Choose a local video…](#)
{: .avatar-trigger target="secret_avatar" pick="video" }

**Your planned cues live on the `video: true` line, under `cues:`.** Each fires at
its `t:` (seconds *into the clip*, by real playback time) and can change the
**bubble** (`say:`), **walk** the avatar to an element (`at:`), **hold** a beat then
resume on its own (`pause:` seconds), or **stop until you click ▶** (`step: true`).
Author the timeline once — it runs the same for a local file, a direct URL, or YouTube:

```yaml
name: "Aristotle"
transparent: true
script:
  # ONE recorded take = your local clip. cues: choreograph it by the clip's OWN
  # playback time — t: is seconds INTO the video, not wall-clock.
  - say: "Loaded from my disk — my cues run off the clip's own timeline."
    video: true                      # source = the file you picked (or a URL)
    cues:
      - t: 0                         # 0.0 s in …
        at: "#runtime_video"         #   walk to & spotlight this element
        say: "t: is seconds into the clip"   #   set the speech bubble
      - t: 4                         # 4 s — just swap the caption
        say: "💬 a fresh bubble, no narration cut"
      - t: 8                         # 8 s — stroll elsewhere, mid-clip
        at: "#how_it_works"
        say: "I can move while the video keeps playing"
      - t: 12                        # 12 s — freeze, then resume by myself
        say: "⏸ holding 3 s… then I carry on"
        pause: 3                     #   pause the clip 3 s after this cue
      - t: 18                        # 18 s — wait for a human
        say: "👉 click ▶ to continue"
        step: true                   #   stop here until you press ▶
      - t: 24
        say: "😊 last beat — happy recording!"
```
{: .avatar #secret_avatar size="180" step="true" }

[▶ Play](#)
{: .avatar-trigger target="secret_avatar" label-stop="⏹ Stop" }

---

## 🚙 Riv — a Rive state-machine character {#rive_demo}

A Rive character is a **state machine with inputs**, not a recording — and the
script **drives the inputs**: `input: "bump"` fires the trigger named `bump`
exactly when that line is spoken. Inputs named `talk` (boolean) or `mouth`
(number) are driven automatically — speech state and waveform lip-sync. This
demo is Rive's hello-world (state machine `bumpy`, one trigger); swap in any
character from the [Rive community](https://rive.app/community/).

```yaml
name: Riv
path: right
voice: en-US
rive:
  url: https://cdn.rive.app/animations/vehicles.riv
  stateMachine: bumpy
script:
- say: Watch the road — this bump is scripted.
  at: "#aristotle_avatar"
  input: bump
  audio: /assets/audio/riv_avatar/line_01.wav
- say: Name an input 'talk' and your character follows the speech.
  audio: /assets/audio/riv_avatar/line_02.wav
  at: "#rive_demo"
- say: A 'mouth' number input even follows the universal waveform.
  at: "#how_it_works"
  audio: /assets/audio/riv_avatar/line_03.wav
```
{: .avatar #riv_avatar size="170" }

[▶ Play](#)
{: .avatar-trigger target="riv_avatar" label-stop="⏹ Stop" }

---

## How it works {#how_it_works}

| Attribute | Role |
|---|---|
| `script` | Lines spoken in order — a string, or `at:` + `say:` to walk to and spotlight an element |
| `audio` (per line) | Pre-generated audio file — plays instead of TTS, mouth follows the real waveform |
| `video` | Recorded character clip (list = fallbacks, alpha WebM first); lines with `video: true` play it with sound |
| `transparent` | `true` + alpha WebM: the background disappears, the character floats free |
| `cues` (per recorded line) | `[{t, at, say, input, slide}]` — choreograph one take: at `t` seconds walk, caption, drive states or slides |
| `input` (per line or cue) | Drive the Rive state machine: `"bark"` fires that trigger, `{run: true, speed: 7}` sets boolean/number inputs |
| `rive` | `.riv` URL or `{url, stateMachine}` — inputs named `talk`/`mouth` are auto-driven by the speech |
| `lottie` | Lottie JSON URL or `{url, idle: [from,to], talk: [from,to]}` frame segments |
| `path` | Movement for untargeted lines: `left`, `center`, `right`, `wander` |
| `voice`, `rate`, `pitch` | TTS tuning — best-quality matching browser voice is picked |
| `size` / `autoplay` | Bubble diameter in px (140) / start on page load |
| `step` | `"true"`: step-by-step — each click on the trigger (or character) speaks the next line and stops (`▶ Start → Next → ↺ Replay`) |

`{: .avatar-trigger target="id" }` on any link makes a play/stop button. Multiple avatars stagger automatically. Add the **`pick`** knob — `{: .avatar-trigger target="id" pick="video" }` — and the same trigger instead opens a local file picker: the chosen video plays as the avatar from an in-memory blob (with sound), never uploaded or committed.

**Runtime source** — `Page().<avatar>.video(url)` (e.g. from a button `on_click`) sets the clip at runtime, so a private URL never lives in the repo: a direct `.mp4/.webm` plays through the avatar's `<video>` (alpha + frame-accurate cues), an unlisted **YouTube** link plays through its embed with a shim so the same cues still fire. See [🔒 Runtime video](#runtime_video) above.

## 🎬 Slide mode & studio mode

**In slide mode** (📽️), `at:` cues drive the deck: the avatar walks the presentation to the slide holding its target and discloses it. **Studio mode** records it all: `{: .avatar-studio target="id" }` opens the screen recorder pre-configured (camera/mic off, tab audio on), recording starts, slides enter, the avatar plays — and on the last word the recording stops and the review panel offers the **YouTube upload**.

[🎬 Record Aristotle's tour](#)
{: .avatar-studio target="aristotle_avatar" }

## 🎭 Characters & voices {#finding_characters}

- **Characters**: the [Rive community](https://rive.app/community/) (Remix → download the `.riv`; name inputs `talk`/`mouth` in their editor and the avatar drives them — plus your own inputs via `input:`). Lottie characters from [LottieFiles](https://lottiefiles.com/free-animations/characters) work too — self-host the JSON under `/assets/avatar/`.
- **Your own voice, cloned locally**: [VoiceClone Studio](https://github.com/GeorgesZam/voice_cloning_local) (Chatterbox TTS) speaks any text as *you* from a 10–20 s sample. `tools/gen_voice_lines.py` runs it over a whole page — one wav per script line under `/assets/audio/<avatar_id>/`, YAML rewired with `--write`; `--lang fr` for the multilingual model. Clone only voices you have the right to clone.

```
pip install chatterbox-tts torchaudio
python3 tools/gen_voice_lines.py docs/components/examples/avatar.md \
    --ref my_voice.m4a --avatar riv_avatar --write
```
