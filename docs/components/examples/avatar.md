---
title: "Speaking Avatar — Overlay Instructor"
---

# 🗣️ Speaking Avatar

A speaking overlay character that narrates content while moving across the screen — and can **follow the elements it describes**: give a script line an `at:` selector and the avatar scrolls there, parks beside it, spotlights it, and speaks. Driven by **Web Speech API** (browser-native TTS) with an animated built-in face, any **Lottie** animation, a **Rive** state machine, or a recorded video character.

Press **▶ Play** to start, or click the character directly to toggle.

---

## 🙂 Prof. Light — the built-in face {#prof_light}

No Lottie needed: the default character blinks, and its mouth moves while it speaks. This one **follows the page** — watch it walk the sections below.

```yaml
name: "Prof. Light"
voice: en-US
script:
  - "Hi! I'm the built-in avatar — no animation file needed."
  - at: "#gatin_demo"
    say: "This is Gatin, my Lottie colleague. Anything Lottie can draw can be a character."
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

## 🧙 Aristotle — a recorded Memoji on a timed walk {#aristotle_demo}

The realism ceiling: a **recorded character** — Aristotle, an iPhone Memoji
with a real voice (and a Greek accent), one take. While the recording plays,
**timed cues** walk him to the components he describes — the peripatetic
school, on a web page. (`t:` values are tuned to the narration; adjust them
to your take. Cues can also drive slides: `slide: next`.)

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
        at: "#gatin_demo"
        say: "⏳ I'm a time-travaler!"
      - t: 20
        at: "#how_it_works"
        say: "😊 Happy learning!"
```
{: .avatar #aristotle_avatar size="180" }

[▶ Play](#)
{: .avatar-trigger target="aristotle_avatar" label-stop="⏹ Stop" }

---

## 🐱 Gatin — the cat instructor {#gatin_demo}

A bobbing cat character from the official [lottie-web demo repo](https://github.com/airbnb/lottie-web/tree/master/demo/gatin). Warm peach tones, swaying tail, blinking eyes.

```yaml
name: "Prof. Gatin"
path: wander
voice: en-US
lottie: "https://raw.githubusercontent.com/airbnb/lottie-web/master/demo/gatin/data.json"
script:
  - "Hello! I'm your virtual instructor."
  - "An object is a bundle of state and behavior."
  - "Lucky the dog has attributes — colour, weight, top speed."
  - "And methods — bark, run, wag_tail."
  - "State you can read. Behavior you can invoke."
  - "That's all an object is."
```
{: .avatar #gatin_avatar size="160" }

[▶ Play](#)
{: .avatar-trigger target="gatin_avatar" label-stop="⏹ Stop" }

---

## 🪢 Adrock — the rope-jumper {#adrock_demo}

An energetic character skipping rope — from the same official repo. Great for high-energy moments.

```yaml
name: "Adrock"
path: left
voice: en-US
lottie: "https://raw.githubusercontent.com/airbnb/lottie-web/master/demo/adrock/data.json"
script:
  - "Ready to jump in? Let's talk about methods."
  - "A method is a function that belongs to an object."
  - "lucky.run() — Lucky runs at his top speed."
  - "wanda.swim() — Wanda circles her bowl."
  - "Same idea. Different object. Different behavior."
```
{: .avatar #adrock_avatar size="150" }

[▶ Play](#)
{: .avatar-trigger target="adrock_avatar" label-stop="⏹ Stop" }

---

## 🚙 Riv — a Rive state-machine character {#rive_demo}

Lottie characters are **recordings** — they play, faster or slower. **Rive**
characters are **state machines**: idle/talk/blink states with runtime
*inputs* the narration drives live. A boolean input named like `talk` follows
the speech, a number input named like `mouth` follows the actual waveform
(vector lip-sync), and **trigger** inputs fire as each line starts. This demo
uses Rive's hello-world file (state machine `bumpy`) — its `bump` trigger
fires on every line, so the truck hits a pothole each time it "speaks". Swap
in any character from the [Rive community](https://rive.app/community/)
(Remix → download the `.riv`).

```yaml
name: "Riv"
path: right
voice: en-US
rive:
  url: "https://cdn.rive.app/animations/vehicles.riv"
  stateMachine: "bumpy"
script:
  - "I'm a Rive state machine — my bumps are an input, not a recording."
  - "Give your character a talk input and it follows the speech."
  - "A mouth number input even follows the waveform. Vector lip-sync."
```
{: .avatar #riv_avatar size="170" }

[▶ Play](#)
{: .avatar-trigger target="riv_avatar" label-stop="⏹ Stop" }

---

## How it works {#how_it_works}

| Attribute | Role |
|---|---|
| `script` | Lines the avatar speaks in order — a string, or `at:` + `say:` to walk to and spotlight the element the line describes |
| `audio` (per line) | URL of a pre-generated audio file — plays instead of browser TTS, and the mouth follows the real waveform (lip-sync) |
| `video` | A recorded character clip, or a list of fallbacks (alpha WebM first, mp4 second); lines with `video: true` play it with sound — real face, real lips, real voice |
| `transparent` | `true` + an alpha WebM source: the black background disappears and the character floats free (browsers without VP9-alpha fall back to the round crop) |
| `cues` (per recorded line) | `[{t, at, say, slide}]` — at `t` seconds into the recording, walk to `at`, change the caption to `say`, or drive slides (`slide: next/prev/start/exit`) — one take, choreographed |
| `path` | Fallback movement for untargeted lines: `left`, `center`, `right`, or `wander` |
| `voice` | BCP-47 tag — the **best-quality** matching browser voice is picked (neural/natural/premium ranked first) |
| `rate` / `pitch` | Speech tuning (defaults `0.95` / `1.05`) |
| `lottie` | URL to a Lottie JSON animation — or `{url, idle: [from,to], talk: [from,to]}` to loop **frame segments** per state (characters authored with idle + talking sequences switch properly instead of just changing tempo) |
| `rive` | URL to a `.riv` file — or `{url, stateMachine: "name"}`. The state machine's inputs are **auto-wired**: a boolean named like `talk` follows the speech, a number named like `mouth` follows the live waveform, triggers fire line by line |
| `size` | Bubble diameter in px (default: 140) |
| `autoplay` | `true` to start on page load |

The `{: .avatar-trigger target="id" }` IAL on any link wires it into a play/stop button. Multiple avatars on one page stagger automatically — they never stack.

## 🎬 Slide mode & studio mode

**In slide mode** (📽️), `at:` cues don't scroll — they **drive the deck**: the
avatar walks the presentation to the slide holding its target and discloses it
(fragments included). A narrated script over a slide deck is a self-running,
voice-over presentation.

**Studio mode** records it: `{: .avatar-studio target="id" }` on a link opens
the screen recorder **pre-configured for the avatar** — camera and mic off
(the avatar is the face and the voice), screen/tab audio on. Pick the tab,
recording starts, the page enters slide mode and the avatar plays — and when
the script completes, the recording stops, the deck exits, and the recorder's
review panel offers the **YouTube upload**. One take, from narration to
published video.

[🎬 Record Aristotle's tour](#)
{: .avatar-studio target="aristotle_avatar" }

A note on voices: browser TTS quality varies (Chrome's Google voices and Safari's enhanced voices sound best). For **studio quality that's identical for every visitor**, generate audio files once (any TTS studio — ElevenLabs, OpenAI TTS…), commit them under `/assets/audio/`, and give each script line an `audio:` URL — the avatar plays the file with real lip-sync and falls back to TTS where no file is given.

## 🎭 Finding better characters {#finding_characters}

Gatin and Adrock are from the 2016-era lottie-web demo folder — fine as proofs, dated as faces. Where to shop for an upgrade:

- **[LottieFiles free characters](https://lottiefiles.com/free-animations/characters)** — hundreds of thousands of free animations. Pick one → *Download → Lottie JSON* → commit it under `/assets/avatar/` and point `lottie:` at it (self-hosted = same-origin, no CORS worries, survives CDN changes). If the character was authored with idle **and** talking sequences, give the frame ranges as `idle:`/`talk:` segments and it switches states for real.
- **[Rive community](https://rive.app/community/)** — the genuinely *dynamic* tier: characters built as **state machines**. *Remix → Download .riv* → `rive: {url, stateMachine}`. Name an input `talk` (boolean) or `mouth` (number 0–100) in the Rive editor and the avatar drives it automatically — speech state and waveform lip-sync included, no code.
- **Remote URLs** also work when the host is CORS-open: any public file on `raw.githubusercontent.com` (sends `Access-Control-Allow-Origin: *`), e.g. the demo cat `https://raw.githubusercontent.com/airbnb/lottie-web/master/demo/gatin/data.json`.

The realism ladder, bottom to top: built-in SVG face → Lottie (canned loop) → Lottie with idle/talk segments → **Rive state machine with talk + mouth inputs** → recorded video character (Aristotle above).
