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

The ball 🎾 is **near the water** 💧. Slide **x** and **y** — it moves toward the
target 🎯:

```yaml
x: 20
y: 80
```
{: .form #hunt editable="true" sliders="x,y" min="0" max="100" step="5" title="Aim 🎯" }

```python
def _row(val, tgt):
    n = 12
    b = min(n - 1, max(0, round((val or 0) / 100 * (n - 1))))
    t = min(n - 1, max(0, round(tgt / 100 * (n - 1))))
    return "".join("🎾" if i == b else ("🎯" if i == t else "▫️") for i in range(n))
def x_row(): return _row(hunt.x, 70)
def y_row(): return _row(hunt.y, 30)
def hint():
    d = (((hunt.x or 0) - 70) ** 2 + ((hunt.y or 0) - 30) ** 2) ** 0.5
    return "🎾 Found it!" if d <= 10 else ("🔥 warmer…" if d < 30 else "❄️ cold")
```
{: .run silent="true" }

x&nbsp;&nbsp;{= x_row() }
y&nbsp;&nbsp;{= y_row() }

**{= hint() }**

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
