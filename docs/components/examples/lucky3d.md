---
title: "Lucky & Wanda — 3D Object Playground"
---

# 🐕🐠 Lucky & Wanda in 3D! Pour Véronique & Jean

The same two objects you met in [Tutorial 101](/tutorial101) — but alive. Every **attribute** you edit changes what you see. Every **method** you call makes them behave. That's all an object is: state you can read, behavior you can invoke.

**Try it:** change Lucky's `colour`, drag `weight_kg`, then call `lucky.run()` and watch his `top_speed_kmh` matter.

```yaml
lucky:
  colour: Black
  weight_kg: 28
  top_speed_kmh: 40
  adopted: true
wanda:
  colour: Orange
  weight_kg: 0.03
  top_speed_kmh: 6
  adopted: false
```
{: .scene3d height="440" }

## 🧠 What just happened?

| You did | In object terms |
|---|---|
| Picked a colour | `lucky.colour = "Golden"` — an **attribute assignment**, the object re-renders |
| Dragged weight\_kg | same attribute, *continuous* value — state drives appearance |
| Clicked `bark()` | a **method call** — behavior that uses the object's own state |
| Clicked `run()` | the animation speed comes from `top_speed_kmh` — methods read attributes |
| Ticked adopted | a **boolean** attribute with a visible consequence (collar / castle) |

The YAML forms in [Tutorial 101](/tutorial101) and these 3D bodies are **the same objects** — one shows the state as text, the other as behavior. Alt-hover any component on this site (or use 📽️ → X-ray on mobile) to see this structure everywhere.
