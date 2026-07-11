---
title: "Help Lucky"
---

# 🐾 Help Lucky find his ball

Lucky lost his ball at the park 🎾. Let's help him find it!

## 🥇 First — just help him

### 🪧 He needs a sign

Lucky can't read many words, so keep it big:

````
# 🐾 ➡️ 🌳
### 🎾 **PARK!** ☀️
````
{: .block }

### 🌳 Throw the ball in the park

Slide to move the ball 🎾 onto the park 🌳 — then hit **Fetch**, and Lucky runs for it!

```yaml
lat: 43.045
lon: -87.885
```
{: .form #hunt editable="true" sliders="lat:43.04:43.07:0.002,lon:-87.90:-87.85:0.002" title="Where to throw 🎾" }

```
label,lat,lon
🌳 Lake Park,43.055,-87.872
```
{: .map bind="hunt" bindicon="🎾" fetch="🐕" target="43.055,-87.872" radius="0.004" zoom="14" height="340" }

**What makes a good throw?**

- [x] line up **both** sliders on the park
- [ ] just one slider is enough
- [ ] Lucky fetches from anywhere
{: .quiz }

## 🥈 Then — change things

Make Lucky's sign your own, and pick where he's headed. Everything updates **live**:

### ✏️ The sign

Type on the left, watch it change on the right:

```markdown
# 🐾 ➡️ 🌳
### 🎾 **PARK!** ☀️
```
{: .mdpad rows="7" }

### 🎚️ The destination

```yaml
place: Lake Park
emoji: 🌳
```
{: .form #dest editable="true" options="place=Lake Park|Riverside Park|Estabrook Park" title="Destination" }

Lucky's off to **{= dest.place or 'the park' }** {= dest.emoji or '🌳' }!

*Play all you like — nothing can break, and nothing's saved yet.*

## 🥉 Keep it — make it real

**Reload the page.** 😮 Your sign and destination snapped right back to default —
your changes are **gone**.

That's the deal: you can play and change anything, but to **keep** your work — and
let other people see it — you need your own place to save it. That's the *only*
reason to sign up: to make your changes stick.

[🔒 Save my changes — set me up →](/micro_build_ai/onboarding){: .button }

```
### 🏠 Back
[The journey](/micro_build_ai/)
```
{: .cards cols="1" }
