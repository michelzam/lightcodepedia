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
{: .prerequisite }

If the gate above is open, you've earned points on Tutorial 101 in this
browser. If it's closed — that *is* the demo: follow the link, answer a quiz,
come back.

## ✍️ How to write it

A list of links with the `{: .prerequisite }` IAL:

```markdown
- [🎓 Tutorial 101 — Explore](/tutorial101)
- [⚙️ Tutorial 102 — Compose](/tutorial102)
{: .prerequisite }
```

| Knob | Meaning |
|---|---|
| *(default)* | a page counts as done when the learner has earned **any** point there |
| `pass="80"` | require at least that percentage of the page's points |

- Scores come from the same store as the 🏅 score chip (quizzes and features,
  per browser, resettable from the chip's menu).
- The gate hides everything **after** it — put it near the top of the page.
- **🚀 This page unlocks** appears automatically at the bottom of any page that
  other pages declare as *their* prerequisite. Nothing to write — the learning
  graph assembles itself from the declarations.

## 🧠 Why

Prerequisites make the pedagogy explicit: pages state their assumptions, the
platform enforces them gently, and the reverse links turn every page into a
signpost. The learner is self-directed — with rails.
