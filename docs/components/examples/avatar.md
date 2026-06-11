---
title: "Speaking Avatar — Overlay Instructor"
---

# 🗣️ Speaking Avatar

A speaking overlay character that narrates content while moving across the screen — and can **follow the elements it describes**: give a script line an `at:` selector and the avatar scrolls there, parks beside it, spotlights it, and speaks. Driven by **Web Speech API** (browser-native TTS) with an animated built-in face, or any **Lottie** animation.

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
```
{: .avatar #prof_avatar }

[▶ Play](#)
{: .avatar-trigger target="prof_avatar" label-stop="⏹ Stop" }

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

## How it works {#how_it_works}

| Attribute | Role |
|---|---|
| `script` | Lines the avatar speaks in order — a string, or `at:` + `say:` to walk to and spotlight the element the line describes |
| `path` | Fallback movement for untargeted lines: `left`, `center`, `right`, or `wander` |
| `voice` | BCP-47 tag — the **best-quality** matching browser voice is picked (neural/natural/premium ranked first) |
| `rate` / `pitch` | Speech tuning (defaults `0.95` / `1.05`) |
| `lottie` | URL to a Lottie JSON animation — omit it for the built-in animated face |
| `size` | Bubble diameter in px (default: 140) |
| `autoplay` | `true` to start on page load |

The `{: .avatar-trigger target="id" }` IAL on any link wires it into a play/stop button. Multiple avatars on one page stagger automatically — they never stack.

A note on voices: quality is the browser's, not ours — Chrome's Google voices and Safari's enhanced voices sound best, and the same page sounds different per browser. For studio-quality narration, a cloud TTS with a user-supplied key (the agent component's pattern) would be the next step.

**Working Lottie sources (CORS-open via `raw.githubusercontent.com`):**

- 🐱 Gatin cat — `https://raw.githubusercontent.com/airbnb/lottie-web/master/demo/gatin/data.json`
- 🪢 Adrock rope-jumper — `https://raw.githubusercontent.com/airbnb/lottie-web/master/demo/adrock/data.json`
- 🏃 Jumping character — `https://raw.githubusercontent.com/airbnb/lottie-web/master/demo/happy2016/data.json`

Any public JSON on `raw.githubusercontent.com` works — it sends `Access-Control-Allow-Origin: *`.
