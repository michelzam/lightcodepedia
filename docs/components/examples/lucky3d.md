# 🐕🐠 Lucky & Wanda in 3D

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

## 🎙️ Narrated tour {#narrated_tour}

The guide is a **Rive state machine** — each script line can fire its inputs (`input: "bump"` here; give a dog character `bark`/`run` inputs and the same YAML makes Lucky's twin act out the lesson).

```yaml
name: "Riv"
voice: en-US
rive:
  url: "https://cdn.rive.app/animations/vehicles.riv"
  stateMachine: "bumpy"
script:
  - at: ".lc-scene3d"
    say: "Two objects: Lucky and Wanda. Their attributes are what you see."
  - say: "Call a method — bark, run — and behavior uses that state. Like this:"
    input: "bump"
  - at: "#narrated_tour"
    say: "State you can read. Behavior you can invoke. That's an object."
```
{: .avatar #lucky_guide size="150" }

[▶ Play the tour](#)
{: .avatar_trigger target="lucky_guide" label-stop="⏹ Stop" }
