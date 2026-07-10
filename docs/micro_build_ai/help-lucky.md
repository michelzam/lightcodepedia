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

### 🔍 Where's the ball?

Clues: it's **yellow**, **small**, and Lucky last saw it **near the water** 💧.
Tell him where to look, then hit **Find**:

```yaml
where: ""
```
{: .form #hunt editable="true" title="Look where?" }

[🔍 Find it](#)
{: .button #find }

```python
def on_click(button):
    where = (Page().hunt.data.where or "").lower()
    tries = int(Store.get("build_ai.hunt.tries") or 0)
    if "water" in where or "pond" in where or "lake" in where:
        Store.set("build_ai.hunt.found", True)
        Store.set("build_ai.hunt.points", int(Store.get("build_ai.hunt.points") or 0) + 10)
    else:
        Store.set("build_ai.hunt.tries", tries + 1)
```
{: .onclick }

🐕 Not there… Lucky keeps sniffing by the **water** 💧. Try again!
{: visible="= build_ai.hunt.tries and not build_ai.hunt.found" }

🎾 **Found it!** +10 exploration points — you're at **{= build_ai.hunt.points or 0 }**. Lucky's over the moon!
{: visible="= build_ai.hunt.found" }

**Quick one — where do lost things usually hide?**
{: visible="= build_ai.hunt.found" }

- [x] where they were last seen
- [ ] somewhere brand new
- [ ] nowhere — they're just gone
{: .quiz visible="= build_ai.hunt.found" }

## 🥈 Then — make it yours

No account, nothing to install — your changes just stick, right here in your browser.

### ✏️ Change the sign

Type on the left, watch it change on the right:

```markdown
# 🐾 ➡️ 🌳
### 🎾 **PARK!** ☀️
```
{: .mdpad rows="7" }

### 🎚️ Set the destination

Pick where Lucky's headed — the line below follows you:

```yaml
place: Lake Park
emoji: 🌳
```
{: .form #dest editable="true" title="Destination" }

Lucky's off to **{= dest.place or 'the park' }** {= dest.emoji or '🌳' }!

## 🥉 Finally — make it real

You changed Lucky's sign and picked his spot — and it stuck! But only **here**, in
your browser. Want to **keep it for real** and let other people use it too?

That's the moment you get your own place to save — and *only* now, because *now*
there's a real reason.

[🔑 Set up to save →](/micro_build_ai/onboarding){: .button }

```
### 🏠 Back
[The journey](/micro_build_ai/)
```
{: .cards cols="1" }
