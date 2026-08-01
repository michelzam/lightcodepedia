# 📋 Prerequisite

Declare what a learner should master **before** this page. The platform checks
their recorded score on each linked page: all met → a slim green line; anything
missing → a gate that sends them there and folds the rest of the page away
(with an honest *show anyway* escape). And it works **both ways**: every page
automatically recommends, at its bottom, the pages it unlocks — so learners
always know where they came from and where they can go next.

## 👀 See it in action

This very page requires Tutorial 101:

- [🎓 Tutorial 101 — Explore](/tutorial101)
{: .prerequisite pass="100" escape="true"}

If the gate above is open, you've earned points on Tutorial 101 in this
browser. If it's closed — that *is* the demo: follow the link, answer a quiz,
come back.

```gherkin
Feature: A page that knows what must come first
  As an author
  I want to declare what a learner should master before this page
  So that nobody lands here lost, and everybody knows where to go next

  Scenario: An unmet prerequisite gates the page
    Given a page requiring a lesson the learner has not scored on
    When they open it
    Then a gate sends them to that lesson and folds the rest away
    And an escape is offered only when the author asked for one

  Scenario: A met prerequisite gets out of the way
    Given a learner who has earned points on every required lesson
    When they open the page
    Then the gate is a slim green line, and the page reads normally

  Scenario: The link points both ways
    Given a lesson that another page requires
    When the learner finishes it
    Then that lesson shows where they can go next
```
{: .feature tags="learn" status="pending" }

## ✍️ How to write it

A list of links with the `{: .prerequisite }` IAL:

```markdown
- [🎓 Tutorial 101 — Explore](/tutorial101)
- [⚙️ Tutorial 102 — Compose](/tutorial102)
{: .prerequisite }
```

| Knob | Meaning |
|---|---|
| *(default)* | **mastery**: every point on each linked page — and **no way through** |
| `pass="50"` | relax it: that percentage of the page's points is enough |
| `escape="true"` | offer a *show it anyway* hatch (off by default) |
| `escape="Peek anyway"` | same hatch, in your own words |

**Why those defaults.** A gate that opens on one lucky point isn't a
prerequisite, and a gate anyone can wave away teaches that gates are
decoration. So the platform asks for everything and offers no door —
and the *author* decides, per page, whether to soften either. Relax the
bar where the next page only needs a taste of the last one; open a door
where a curious reader deserves one.

- Scores come from the same store as the 🏅 score chip (quizzes and features,
  per browser, resettable from the chip's menu).
- **Works in courses too**: on a runner render (bench, vault), a relative
  link means "my sibling page" and the gate checks that page's own score —
  the key names the content, never the runner.
- The gate hides everything **after** it — put it near the top of the page.
- **🚀 This page unlocks** appears automatically at the bottom of any page that
  other pages declare as *their* prerequisite. Nothing to write — the learning
  graph assembles itself from the declarations.

## 🧠 Why

Prerequisites make the pedagogy explicit: pages state their assumptions, the
platform enforces them gently, and the reverse links turn every page into a
signpost. The learner is self-directed — with rails.
