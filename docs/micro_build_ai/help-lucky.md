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

### 🗺️ The way to the park

```json
[
  { "lat": 43.0556, "lon": -87.8720, "label": "🌳 Lucky's park 🎾" }
]
```
{: .map height="280" zoom="14" }

### 🔍 Aim for the ball

The ball is **near the water** 💧. Slide **x** and **y** to aim — the hint updates
as you move:

```yaml
x: 20
y: 80
```
{: .form #hunt editable="true" sliders="x,y" min="0" max="100" step="5" title="Aim 🎯" }

```python
def _dist():
    x = hunt.x or 0
    y = hunt.y or 0
    return ((x - 70) ** 2 + (y - 30) ** 2) ** 0.5
def hint():
    d = _dist()
    if d <= 12: return "🎾 Found it! Lucky's got his ball!"
    if d < 30:  return "🔥 Warmer…"
    return "❄️ Cold — head for the water 💧"
```
{: .run silent="true" }

### {= hint() }
{: .nofragments }

**Where do lost things usually hide?**

- [x] where they were last seen
- [ ] somewhere brand new
- [ ] nowhere — they're just gone
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
