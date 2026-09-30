# 🗺 HQ — the map

One page to start any session with. The pitch says what the lab is for,
the map says who it serves and through which topic, each leaf opens the
topic's page (state · doors · proof · rulings · next), and the proof below
turns red when a topic has not been touched for thirty days. Handoffs live
in the topic pages; the dated `HQ_HANDOFF_*.md` files are the archive.

```yaml
who: one educator-builder and the people he teaches, pitches and partners with
need: must resume any thread in minutes, on any device, without re-reading a month of notes
product: the HQ map
category: living handoff
benefit: every topic has one page, one proof and one next step
alternative: a growing handoff file per month
difference: the artifacts we teach with — pitch, map, proof — run the lab itself
```
{: .pitch #hq_pitch }

```yaml
impacts:
  - how: Ships the engine once, to pedia and npm, with the suite as the gate
    what: ⚙️ Engine — includes, bricks, rig, gates, share door
  - how: Publishes what the lab learns, papers and posters, PI in order
    what: 📣 Pedia and publications
  - how: Runs cohorts from Canvas to benches with one click per seat
    what: 🎓 Org courses and cohorts
  - how: Pitches to partners from an unlisted page and ships them bricks
    what: 🤝 Pitches and partners
  - how: Keeps protected courses in a vault, never rendered
    what: 🔒 Protected non-org courses
  - how: Offers open examples anyone can run
    what: 🐍 Open examples
  - how: Decides once and keeps the ruling
    what: 📜 Doctrine and decisions
  - how: Keeps the fleet healthy at zero cost
    what: 🩺 Ops — a11y, fleet, metrics, voice
    feature: hq_proof
```
{: .impact_map #hq_map pitch="hq_pitch" }

## 📂 Topics

One page each. Open a card: it runs in the runner with your author key.

[topics](topics)
{: .folder path="topics" cols="3" #topic_cards }

## 📂 The lab's root

Every document at the root and every folder with a front page, one card
each, opened in the runner: CLAUDE.md, LAB.md, LAUNCH.md, courses, pages…
Git is the version history; this is the index.

[root](/)
{: .folder path="/" cols="3" #root_cards }

## 🗄 This folder — the archive

The dated handoffs, the decision register, the drafts. Read when a topic
page points here, not before.

[hq](.)
{: .folder cols="3" #hq_cards }

## 🗓 Last touched

The one list a session updates before pushing: the date of the topic it
touched. Thirty days without a touch and the proof names the topic.

```yaml
- { topic: engine,       page: "topics/engine.md",       last: "2026-09-30" }
- { topic: pedia,        page: "topics/pedia.md",        last: "2026-09-27" }
- { topic: cohorts,      page: "topics/cohorts.md",      last: "2026-09-29" }
- { topic: partners,     page: "topics/partners.md",     last: "2026-09-29" }
- { topic: protected,    page: "topics/protected.md",    last: "2026-09-27" }
- { topic: examples,     page: "topics/examples.md",     last: "2026-09-27" }
- { topic: doctrine,     page: "topics/doctrine.md",     last: "2026-09-27" }
- { topic: ops,          page: "topics/ops.md",          last: "2026-09-27" }
```
{: .dataset #topics format="yaml" }

[Last touched](#)
{: .datagrid source="topics" rows="8" }

## 🧪 The map's own proof

```gherkin
Feature: The HQ map is current and consistent
  As the one who resumes a session
  I want the map to say when a topic went stale
  So that I never trust a handoff older than a month

  Scenario: Eight topics, none older than thirty days
    Given the map names its topics
    :::python
    self.topics = self.page.topics
    assert self.topics.count == 8, f"{self.topics.count} topics listed, the map draws 8"
    :::
    Then every topic was touched within thirty days
    :::python
    import time
    def day(iso):                       # civil date → days since 1970, no calendar module needed
        y, m, d = [int(x) for x in iso[:10].split("-")]
        y -= m <= 2
        era = y // 400
        yoe = y - era * 400
        doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
        return era * 146097 + yoe * 365 + yoe // 4 - yoe // 100 + doy - 719468
    today = int(time.time() // 86400)
    old = [t for t, d in zip(self.topics.values("topic"), self.topics.values("last"))
           if today - day(d) > 30]
    assert not old, f"stale, not touched for thirty days: {', '.join(old)}"
    :::
    And the pitch and the map agree
    :::python
    assert not self.page.hq_pitch.drifting, "the pitch drifts from what it reads"
    assert self.page.hq_map.pitch is not None, "the map reads no pitch"
    :::
```
{: .feature #hq_proof visible="true" status="pending" tags="hq,handoff" }

## 🧭 How a session uses this

1. Open this map. Read the topic page you will touch. Nothing else.
2. Work. Rulings that would surprise a stranger go to the topic's rulings,
   dated, five lines at most; the rest is in git.
3. Before pushing: update the topic's **state** and **next**, and its date
   in the list above. Run the proofs.
