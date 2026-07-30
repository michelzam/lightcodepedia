# 🖼 Frame flags

When an LMS embeds a LightCode page in an iframe, **the host owns navigation**.
Canvas drives module 1, then exercise 2, from its own pages — so the page inside
the frame must not offer a way out. These four URL flags decide how much of the
platform a learner gets, per page, with no build and no separate "kiosk" build.

## 👀 Try it now

Add them to the iframe `src`:

```
https://lightcodepedia.org/courses/build_ai/m1?focus=1&editable=1&open=/courses/*
```

| Flag | Default | What it does |
|---|---|---|
| `focus=1` | off | menu bar **stays, read-only** — context, not a door. `.related` goes |
| `editable=0` / `=1` | on (off when embedded) | the page editor, independent of focus |

`editable=0` closes **every** editing door: the pill's ✏️ Edit item, the
⌥E hotkey, x-ray's Keep — and the drawer itself as the final gate, whatever
route was tried.
| `navigable=0` / `=1` | **off under focus**, on otherwise | internal links live in-frame, or neutralised |
| `open=a,b` | — | glob allowlist: matching internal links open in a **new tab** |
| `embed=true` | off | the older, blunter mode — hides the bar and the page title entirely |

The flags are orthogonal. `focus=1&editable=1` gives a learner a page they can
work in and save from, but cannot wander off. `focus=1&navigable=1` keeps the
links live — useful for a multi-page exercise the host wants to hand over
wholesale.

## 🎓 Side by side

`open` is how a learner reads the course and works the exercise at the same
time: the host frames the bench with `open=/courses/*`, so a link into the
course opens in its own tab instead of replacing the bench. Two windows, one on
each half of the screen — the browser can place a new window, only the OS can
tile it.

## ⚠️ Good to know

- **External links are never touched.** They were never a way out of the module.
- A neutralised link still **reads as text** — the page doesn't look broken, it
  just isn't a door. The guard is delegated, so it also covers cards, folders
  and anything the runtime renders later.
- The frame keeps its **own history**, so a swipe-back inside the iframe can
  still move within pages the learner already visited.
- Flags are **URL-level, not security**. A learner who opens the page directly
  gets the full platform. This shapes attention, it does not enforce a boundary.

```gherkin
Feature: The host decides how much platform a learner gets
  As an educator whose LMS drives the sequence
  I want the embedded page to offer no way out of the exercise
  So that a learner stays where the course put them

  Scenario: Focus keeps the bar for context but not for navigation
    Given a page framed with focus on
    When the learner looks at the menu bar
    Then it is there, showing where they are
    And nothing in it responds to a press

  Scenario: A focused page can still be worked in
    Given a page framed with focus on and editable on
    When the learner opens the editor and saves
    Then the change is written, and they are still on the same page

  Scenario: Allowed links open beside the work, not over it
    Given a page framed with focus on and the course path allowed
    When the learner follows a link into the course
    Then it opens in a new tab
    And the exercise is still there, untouched, in the first one

  Scenario: Everything else stops being a door
    Given a page framed with focus on
    When the learner presses a link that leaves the page
    Then nothing navigates, and the text stays readable
```
{: .feature tags="ui,learn" status="pending" }

## 🔗 Related

```
/components/embed_page
/components/menu
/components/folder
```
{: .related }
