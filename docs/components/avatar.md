# 🧑‍🏫 Avatar

A speaking **overlay character** — Prof. LC — that narrates a page: it **walks**
from element to element, **spotlights** what it's describing, and **speaks**
each line. The voice is the browser's speech synthesis, a studio audio file, or
a recorded video face. It's the platform's *guide engine*: tutorials, guided
tours — and the player behind the [🎬 demo](/components/demo)'s **▶ Replay**.

**This page is the tutorial** — press ▶ Play and let it show you.

## 👀 Try it now

[▶ Play](#)
{: .avatar_trigger #avatar_go target="prof" }

[🎙️ Generate voices](#)
{: .avatar_voices target="prof" }

```yaml
voice: en-US
bot: doc
face:
  zoom: 1.2
script:
  - "Hello! I'm Doc — I narrate pages, line by line."
  - at: avatar_playground
    say: "I walk to the element I'm describing, and spotlight it."
  - at: avatar_go
    say: "That button started me — it stops me too. Click me to do the same."
  - "Scripts can also play studio audio, or a recorded video of a real face."
```
{: .avatar #prof dock="true" size="115" }

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
  - at: some_widget
    say: "This grid is editable — click a cell."
```
{: .avatar #guide }

[▶ Play](#)
{: .avatar_trigger target="guide" label-stop="⏹ Stop" }
````

## 📜 Script lines

A line is a plain string (the character wanders) or an object:

| Key | What it does |
|---|---|
| `at:` | The **id** of the component (or heading) to walk to — scroll there, park beside it, **spotlight** it |
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
| `elevenlabs` | An ElevenLabs voice id (or `{ voice, model }`) — playback auto-finds each line's pre-generated studio file and falls back to TTS; see 🎙️ below |
| `bot` | A bot name (`docs/bots/…`) — the docked guide gains **💬 Ask**: questions answered by that bot on the learner's own PAT, and the answer is *performed* — the guide walks to the components it mentions while speaking. It only ever walks, points and talks — never acts |
| `dock="true"` | Dock this avatar as the page's **guide**: a small face in the bottom-right corner, zero moves away — tap it for ▶ play tour · next · ⏹ stop. The full character stays hidden until it performs; right-click (long-press) on it opens the same verbs beside it (this page docks Doc) |
| `face` | Make the built-in character look like **you** — see 🪞 below |

Without `lottie`/`rive`/`video`, the built-in **Prof. LC** face is used — round
professor glasses, expressive brows (they lift while speaking), a bow tie; it
blinks, breathes, its eyes *and head* turn toward the spotlighted element, and
its mouth follows the voice. Fully procedural — new text never needs new assets.

## 🪞 Make it you

Every feature of the built-in face is a knob (all keys optional; without
`face:` you get the classic Prof. LC — which is what this page's Doc wears,
compact via `zoom`). An author-lookalike example:

```yaml
face:
  skin: "#e2a87e"       # head colour
  glasses: square       # round · square · none
  beard: "#e8e4de"      # goatee + mustache colour, or none
  brows: "#4a3b30"      # eyebrow colour
  hair: none            # none · sides · full  (+ hair_color)
  wear: shirt           # bow · shirt · none   (+ wear_color)
  head: oval            # round · oval
  zoom: 1.2             # enlarge features only — pair with size="115"
  blush: false
```

It stays a friendly caricature, not a photo — the animations (blink, brow
lift, head turn, lip sync) work identically on every combination. For a real
face, use `video:` (a recorded clip) or a `rive:` character.

## 🎬 Studio — record the narrated walk

[🎥 Studio](#)`{: .avatar_studio target="guide" }` opens the
[screen recorder](/components/recorder), plays the avatar over the page (or the
[slides](/components/slides) deck), stops when the script ends, and offers the
YouTube upload — a narrated video of the page, produced by the page itself.

A `pick` trigger (`{: .avatar_trigger pick target="guide" }`) plays a **local**
video file as the character — in-memory only, never uploaded or committed.

## 🎙️ Studio voices from text — no recording (ElevenLabs)

Browser TTS is the zero-setup default; for **studio quality that still needs no
recording**, generate the audio **from the script text**, straight from the
page. Put a generate button next to any avatar (there's a live one at the top
of this page):

````markdown
[🎙️ Generate voices](#)
{: .avatar_voices target="guide" }
````

Click it. It asks (**first time only** — both are remembered on this device,
like your ✏️ editor connection, and reused silently after that;
**Shift-click** the button whenever you want to change them): your
**ElevenLabs voice id** and your **API key**. Then, per script line, it:

1. **generates** the missing audio (ElevenLabs, called from *your* browser),
2. lets you **hear it immediately**,
3. **commits** the mp3s *and the page's voice manifest* to the repo via the
   ✏️ editor's PAT — and the manifest is how playback **wires itself**: no
   fence config, no `audio:` keys, nothing to edit. Lines without a generated
   file simply fall back to TTS.

- **Change a line → click again**: files are content-addressed (hash of
  voice + text), so only changed lines are regenerated and billed; everything
  unchanged is cached forever — and stale audio can never play against new
  text.
- **Your own voice**: clone it once on elevenlabs.io (included in paid plans) —
  every new text then speaks as *you*, never recorded again.
- **Visitors are never involved**: they get plain static mp3 files — no API,
  no key, none of your credits.
- Optional: pin the voice in content with `elevenlabs: <voice_id>` in the
  fence (playback then computes filenames even without the manifest).
- Prefer the terminal (bulk pages, CI)? `ELEVENLABS_API_KEY=sk_… node
  packages/gen-audio.mjs docs/your-page.md --voice <voice_id>` — identical
  file naming and manifest, interchangeable with the button.

## 💬 Ask — questions, answered in place

With `bot: doc` on the fence, the docked guide's menu gains **💬 Ask**. Type a
question; it goes to [the bot](/components/agent) — Doc's persona plus this
page's own material — on **your PAT and your free credits** (first ask pastes
it once, kept in memory only). The answer comes back **performed**: Doc walks
to each component his reply mentions, spotlights it, and speaks the step.

- The guide **never acts** — he walks, points and talks. Changing things stays
  yours (and will always ask first, when that day comes).
- One question at a time for now — conversation memory is a later stage.
- A component the reply names wrongly is simply spoken, not walked — a wrong
  answer can never break the page.
- **Connected to the ✏️ editor?** Your PAT is reused silently — no re-pasting;
  agents and the guide share one token per page.
- **No guide on a page?** The mode pill (bottom-left) has a **🧑‍🏫 Guide**
  toggle: it summons the generic companion on any page, remembered on your
  device — no tour there, but 💬 Ask still knows the page it stands on.
  Authored guides always take precedence.
- **📌 Keep & voice (authors).** When the ✏️ editor is connected, the guide's
  menu offers to **keep** the answer that just played: its steps are appended
  to this page's tour (committed like any edit, the question credited as
  *"You might wonder: …"*), and the new lines are **voiced** with your
  ElevenLabs voice on the spot. Learners' real questions grow the course —
  and a kept answer never costs anyone credits again. If the page's fence
  can't be located unambiguously, the keep aborts — it can never corrupt a
  page.

## 🤝 With the demo — ▶ Replay

The [🎬 demo](/components/demo) records a learner's actions; its **▶ Replay**
compiles that trace into an avatar script and hands it to this engine:
Prof. LC re-walks the learner's path, spotlights each
widget they touched, re-applies their edits live, and narrates. Same character,
two jobs: **guide** on the way in, **witness** on the way back.

## ⚠️ Good to know

- **Voices vary by device** — browser TTS quality differs; set `voice` to your
  page's language, use `voice: off` for silence, or record real audio/video for
  studio quality.
- **Autoplay needs sound permission** on some browsers — the trigger click is
  the reliable start.
- The spotlight is an amber outline on the `at:` element. Point `at:` any
  component's **id** — forms, quizzes, grids and headings all resolve, wherever
  the platform placed them.

## 🔗 Related

```
/components/demo
/components/recorder
/components/slides
```
{: .related }
