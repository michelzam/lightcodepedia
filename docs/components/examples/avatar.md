---
title: "Speaking Avatar — Overlay Instructor"
---

# 🗣️ Speaking Avatar

A speaking overlay character that narrates content while moving across the screen. Driven by **Web Speech API** (browser-native TTS) and a **Lottie** animation for the character.

Press **▶ Play** to start, or click the character directly to toggle.

---

## 🐱 Gatin — the cat instructor

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
{: .avatar #gatin-avatar }

[▶ Play](#)
{: .avatar-trigger target="gatin-avatar" label-stop="⏹ Stop" }

---

## 🪢 Adrock — the rope-jumper

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
{: .avatar #adrock-avatar size="150" }

[▶ Play](#)
{: .avatar-trigger target="adrock-avatar" label-stop="⏹ Stop" }

---

## How it works

| Attribute | Role |
|---|---|
| `script` | Lines the avatar speaks in order |
| `path` | Movement: `left`, `center`, `right`, or `wander` |
| `voice` | BCP-47 tag — picks the first matching browser voice |
| `lottie` | URL to a Lottie JSON animation |
| `size` | Bubble diameter in px (default: 120) |
| `autoplay` | `true` to start on page load |

The `{: .avatar-trigger target="id" }` IAL on any link wires it into a play/stop button.

**Working Lottie sources (CORS-open via `raw.githubusercontent.com`):**

- 🐱 Gatin cat — `https://raw.githubusercontent.com/airbnb/lottie-web/master/demo/gatin/data.json`
- 🪢 Adrock rope-jumper — `https://raw.githubusercontent.com/airbnb/lottie-web/master/demo/adrock/data.json`
- 🏃 Jumping character — `https://raw.githubusercontent.com/airbnb/lottie-web/master/demo/happy2016/data.json`

Any public JSON on `raw.githubusercontent.com` works — it sends `Access-Control-Allow-Origin: *`.
