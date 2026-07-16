# 🧑‍🏫 Avatar

A speaking **overlay character** — Prof. LC — that narrates a page: it **walks**
from element to element, **spotlights** what it's describing, and **speaks**
each line. The voice is the browser's speech synthesis, a studio audio file, or
a recorded video face. It's the platform's *guide engine*: tutorials, guided
tours — and the player behind the [🎬 demo](/components/demo)'s **▶ Replay**.

**This page is the tutorial** — press ▶ Play and let it show you.

## 👀 Try it now

[▶ Play](#)
{: .avatar-trigger #avatar_go target="prof" }

```yaml
voice: en-US
script:
  - "Hello! I'm Prof. LC — I narrate pages, line by line."
  - at: '[data-lc-id="avatar_playground"]'
    say: "I walk to the element I'm describing, and spotlight it."
  - at: "#avatar_go"
    say: "That button started me — it stops me too. Click me to do the same."
  - "Scripts can also play studio audio, or a recorded video of a real face."
```
{: .avatar #prof }

```yaml
dog: Lucky
treats: 3
```
{: .form #avatar_playground editable="true" title="A widget to visit" }

## 🛠️ How to make one

A YAML fence holds the config + script; a trigger link plays/stops it:

````markdown
```yaml
voice: en-US
script:
  - "Hello! Let's explore this page together."
  - at: "#some_widget"
    say: "This grid is editable — click a cell."
```
{: .avatar #guide }

[▶ Play](#)
{: .avatar-trigger target="guide" label-stop="⏹ Stop" }
````

## 📜 Script lines

A line is a plain string (the character wanders) or an object:

| Key | What it does |
|---|---|
| `at:` | CSS selector — scroll there, park beside it, **spotlight** it |
| `say:` | The line — spoken, and shown in the speech bubble |
| `audio:` | URL of a pre-recorded audio file — plays instead of TTS; the mouth follows the real waveform |
| `video:` | `true` / URL — play the recorded character clip **with sound** for this line (real face, real voice) |
| `cues:` | Inside one recorded take: `[{ t: seconds, at:, say:, slide: next\|prev\|start\|exit }]` — fire as the clip crosses each time |
| `input:` | Drive a Rive character's state machine — `"bark"` fires that trigger, `{ run: true, speed: 7 }` sets inputs |
| `pause:` | Seconds to hold after the line (default 0.5) |
| `step:` | `true` forces a stop at this line; `false` chains on even in step mode |

## 🔧 Knobs

In the YAML (or as attributes on the block):

| Knob | What it does |
|---|---|
| `voice` | BCP-47 tag (`fr-FR`) — the best-quality matching browser voice is picked. Default: the page's language (**en-US**). **`off`** = silent: the bubble shows each line, dwells, moves on |
| `rate` / `pitch` | TTS tuning (defaults 0.95 / 1.05) |
| `path` | Where untargeted lines park: `left` · `center` · `right` · `wander` |
| `autoplay` | `true` starts on page load |
| `step` | `true` = step-by-step: each click plays **one** line and waits (▶ Start → Next → ↺ Replay) |
| `size` | Pixel size of the character bubble (attribute, default 140) |
| `lottie` | A Lottie JSON URL — or `{ url, idle: [from,to], talk: [from,to] }` frame segments |
| `rive` | A `.riv` URL or `{ url, stateMachine }` — inputs named like *talk*/*mouth* are auto-wired to the narration |
| `video` | A recorded clip URL (or `[webm-alpha, mp4]` fallbacks) — the character *is* the video |
| `transparent` | `true` + an alpha WebM: the face floats free, no round crop |

Without `lottie`/`rive`/`video`, the built-in **Prof. LC** face is used — round
professor glasses, expressive brows (they lift while speaking), a bow tie; it
blinks, breathes, its eyes *and head* turn toward the spotlighted element, and
its mouth follows the voice. Fully procedural — new text never needs new assets.

## 🎬 Studio — record the narrated walk

[🎥 Studio](#)`{: .avatar-studio target="guide" }` opens the
[screen recorder](/components/recorder), plays the avatar over the page (or the
[slides](/components/slides) deck), stops when the script ends, and offers the
YouTube upload — a narrated video of the page, produced by the page itself.

A `pick` trigger (`{: .avatar-trigger pick target="guide" }`) plays a **local**
video file as the character — in-memory only, never uploaded or committed.

## 🤝 With the demo — ▶ Replay

The [🎬 demo](/components/demo) records a learner's actions; its **▶ Replay**
compiles that trace into an avatar script and hands it to this engine
(`window.lcAvatarPlay`): Prof. LC re-walks the learner's path, spotlights each
widget they touched, re-applies their edits live, and narrates. Same character,
two jobs: **guide** on the way in, **witness** on the way back.

## ⚠️ Good to know

- **Voices vary by device** — browser TTS quality differs; set `voice` to your
  page's language, use `voice: off` for silence, or record real audio/video for
  studio quality.
- **Autoplay needs sound permission** on some browsers — the trigger click is
  the reliable start.
- The spotlight is an amber outline on the `at:` element; any CSS selector works.
  Platform components are addressable as `[data-lc-id="your_id"]` (a form's DOM
  id is prefixed, so the plain `#id` only works for headings and raw elements).

## 🔗 Related

```
/components/demo
/components/recorder
/components/slides
```
{: .related }
