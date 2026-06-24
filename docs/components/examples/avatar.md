---
title: "Speaking Avatar — Overlay Instructor"
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

`{: .avatar-trigger target="id" }` on any link makes a play/stop button. Multiple avatars stagger automatically.

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
