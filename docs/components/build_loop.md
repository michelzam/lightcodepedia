# 🔁 Build Loop

A slowly turning hex hive. Agents walk the ring, blocks flow from station to
station changing colour as they go, and finished apps rise off the core and
orbit above it. One continuous cycle — the mechanics of building with AI, at
altitude.

Drag to turn it, scroll to zoom, hover a pod to preview it — and **click a pod
to pin a legend that stays attached to it** while the hive keeps turning.
Click again, or the ×, to close it. Pin as many as you like and compare.

```
Need: every build starts with someone's problem
Design: turn the need into something you can hold
Blocks: snap the working parts together
AI: bring in the partner that thinks with you
Ship: put it in someone's hands
Learn: what you shipped starts the next loop
```
{: .build_loop height="470" }

## Writing one

One station per line, `Label: what happens there`. Three to eight lines — the
ring lays itself out, picks the colours, and spaces the traffic.

````
```
Need: every build starts with someone's problem
Design: turn the need into something you can hold
Blocks: snap the working parts together
AI: bring in the partner that thinks with you
Ship: put it in someone's hands
Learn: what you shipped starts the next loop
```
{: .build_loop height="470" }
````

## Attributes

| Attribute | Default | What it does |
|---|---|---|
| `height` | `460` | stage height in pixels |
| `speed` | `1` | global animation rate |
| `spin` | `true` | auto-rotate the hive; `"false"` starts it still |
| `agents` | `5` | figures circulating the ring, `0`–`10` |

## Reading it

| What you see | What it means |
|---|---|
| The ring | the loop never ends — shipping starts the next turn |
| Blocks changing colour mid-gap | each station transforms the work it passes on |
| Agents walking | people move the work; the loop does not run itself |
| The core | the one thing every station turns around |
| Cards orbiting above | what the loop produces, staying in orbit — used, not filed |
| A pinned legend | the one station you are thinking about, kept in view as it moves |

## Verbs — what a narrator can do to it

The loop registers presentation verbs, so an avatar can drive it *while it
talks*: turn the hive to face a station, pin its legend, and leave it pinned
as the tour moves on. The avatar walks to that station's chip first, so it
is standing beside the thing it is describing.

| Verb | `with:` | What happens |
|---|---|---|
| `look_at` | station label | eases the hive round until that station faces the viewer |
| `pin` | station label | attaches its legend, and leaves it attached |
| `unpin` | label, or nothing | closes one legend, or all of them |
| `spin` | `on` / `off` / nothing | auto-rotation; bare `spin` toggles |
| `recentre` | — | back to the opening framing |

These are **view state only**. Nothing here can change content, a score or an
answer — a consequential action simply has no verb to call, which is how
"the tutor never acts" stays structural rather than a promise.

```yaml
name: "Hive"
voice: en-US
script:
  - at: ".lc-build-loop"
    say: "This is one build loop. Six stations, and the work never stops moving."
  - do: spin
    with: "off"
    say: "Let me hold it still for a second."
  - do: look_at
    with: "Need"
    say: "Every turn starts here — someone has a problem worth solving."
  - do: pin
    with: "Need"
    say: "I'll leave that one open so you can keep it in view."
  - do: look_at
    with: "AI"
    say: "Four stations on, AI joins as a partner — not as the whole build."
  - do: pin
    with: "AI"
    say: "Notice both legends stay stuck to their pods as we move."
  - do: unpin
    say: "Clear those."
  - do: spin
    with: "on"
    say: "And the loop keeps turning. Shipping is what starts the next one."
```
{: .avatar #loop_guide size="150" }

[▶ Play the tour](#)
{: .avatar_trigger target="loop_guide" label-stop="⏹ Stop" }

## Inside an accordion

This is how the BUILD-AI course page carries it: folded away until a learner
opens it, so the page stays light and nothing renders until it is asked for.

`````
### 🔁 A folded loop

Same component, one fold down.

```
Ask: what is actually needed
Make: build the smallest working thing
Check: put it in front of someone
```
{: .build_loop height="360" agents="3" }
`````
{: .accordion }

## Notes

Hover is not the only way in: the coloured chips under the stage preview a
station on hover or focus and pin it on click, so the whole scene is reachable
from the keyboard. Tapping a pod pins it on a touch screen. Pinned legends are
HTML, not geometry — they stay crisp at any zoom and their text can be selected. A visitor
with `prefers-reduced-motion` gets the hive still — turnable and readable,
but not moving on its own. The loop stops rendering entirely when it scrolls
out of view.

Three stations is the floor, eight the ceiling. Past that the ring gets
crowded and the labels start to collide — which is a good sign you have a
second loop, not a longer one.
