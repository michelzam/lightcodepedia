# 🚀 Ship

Deployment as a **course element**. The author writes a ship button into an
assignment page; the learner's own key copies the named files into a public
**bay**, under a folder named `app_sha` — immutable, provenance-pinned,
enumerable per assignment. A runner embed with `src="ship:<app>"` then
renders the deployed copy on the same page: the proof that deployment
worked is the app itself, live, not a success message.

```
[Ship it](#)
{: .ship app="adoption_day" files="_app_dogs.md, dogs.yaml" bay="owner/bay_repo/bays" }

[My shipped app](#)
{: .runner src="ship:adoption_day" bay="owner/bay_repo/bays" title="" }
```
{: .code }

## 🎛️ Knobs

| Knob | Meaning |
|---|---|
| `app` | the assignment's name, chosen by the author — it prefixes every deploy folder, so submissions are enumerable by construction |
| `files` | exactly what ships, comma-separated, relative to the page — the author decides the blast radius, never the learner in the moment |
| `bay` | `owner/repo` or `owner/repo/base` — a **public** repo (or folder in one) that receives the deploys and holds the `manifest.json` ledger |
{: .wide_first }

## 📐 How it holds together

- **Capability is placement.** No `.ship` on a page, no shipping. The author
  activates the assignment by writing the component — and disarms every
  classroom at once by removing it.
- **The gate is the author's too.** Put `{: .prerequisite features="true" }`
  at the top of the assignment page and the learner cannot reach the button
  until the page's checks run green. One job per component: prerequisite
  gates, feature proves, ship copies, runner shows.
- **Public means public.** The bay is "anyone with the link" tier;
  protection is unguessability — the sha in the folder name, nothing
  listing or indexing it. The button says so before anyone presses it.
- **`ship:` resolves keyless.** The embed reads the bay's manifest raw, with
  no key at all — what it renders is exactly what a stranger with the link
  would see. Before the first ship it waits politely instead of erroring.

## 👀 The button, disarmed

On this built page there is no rendered course around the button and no
learner key, so it shows its honest disarmed state — each missing piece
names itself:

[Ship it](#)
{: .ship app="demo_dogs" files="_demo.md" bay="michelzam/lightcodepedia/bays" }

```gherkin
Feature: A dead control explains itself
  As a learner meeting a disarmed ship button
  I want it to say exactly why it will not fire
  So that I never wonder whether the page is broken

  Scenario: The disarmed button names its reason
    Given the ship button above
    :::python
    self.box: Object = Object._all(".lc-ship")[0]
    :::
    When the page has rendered
    Then the button is disabled and the status says why
    :::python
    btn = Object._all(".lc-ship button")[0]
    assert btn._get("disabled") is not None, "button should be disarmed here"
    text: str = Object._all(".lc-ship-status")[0]._text()
    assert len(text.strip()) > 10, text
    :::
```
{: .feature #ship_disarmed tags="ui" status="passing" }

## 📲 A real deployed app, live

This window resolves `ship:demo_dogs` through a real bay's manifest —
keyless, on this public page, exactly as a learner's shipped PoC would:

[Demo dogs, deployed](#)
{: .runner src="ship:demo_dogs" bay="michelzam/lightcodepedia/bays" title="" }

The full flow — armed button, files crossing to the bay, the manifest
ledger, the `ship:` embed filling — is proven end to end in
`tests/features/ship.feature`, with both sides of the wire stubbed.

[in this folder](.)
{: .folder parent="true" }
