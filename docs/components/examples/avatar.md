---
title: "Speaking Avatar — Overlay Instructor"
---

# 🗣️ Speaking Avatar

A speaking overlay character that narrates content while moving across the screen. Driven by **Web Speech API** (browser-native TTS) and optionally a **Lottie** animation for the character.

Press **▶ Play** to start the demo, or click the character directly to toggle.

```yaml
name: "Prof. LC"
path: wander
voice: en-US
script:
  - "Hello! I'm your virtual instructor."
  - "An object is a bundle of state and behavior."
  - "Lucky the dog has attributes — colour, weight, top speed."
  - "And methods — bark, run, wag_tail."
  - "State you can read. Behavior you can invoke."
  - "That's all an object is."
```
{: .avatar #demo-avatar }

[▶ Play](#)
{: .avatar-trigger target="demo-avatar" label-stop="⏹ Stop" }

---

## With a Lottie character

Supply a `lottie` URL in the YAML to replace the default emoji face with a rich animation.
Any public Lottie JSON from [LottieFiles](https://lottiefiles.com) works.

```yaml
name: "Wanda"
path: left
voice: en-US
lottie: "https://assets2.lottiefiles.com/packages/lf20_myejiggj.json"
script:
  - "Hi! I'm Wanda."
  - "I live in a glass bowl and I swim in lazy circles."
  - "wanda.swim() — give it a try on the 3D playground."
```
{: .avatar #wanda-avatar }

[▶ Play](#)
{: .avatar-trigger target="wanda-avatar" label-stop="⏹ Stop" }

---

## How it works

| Attribute | Role |
|---|---|
| `script` | List of lines the avatar speaks in order |
| `path` | Movement pattern: `left`, `center`, `right`, or `wander` |
| `voice` | BCP-47 language tag (e.g. `en-US`, `fr-FR`) — picks the first matching browser voice |
| `lottie` | URL to a Lottie JSON animation (optional — defaults to 🗣️ emoji) |
| `autoplay` | `true` to start speaking on page load |

The `{: .avatar-trigger target="id" }` IAL on any link turns it into a play/stop button wired to the avatar with that `id`.

The component uses **only browser-native APIs** — no server required, no API key. Voice quality depends on the OS and browser.
