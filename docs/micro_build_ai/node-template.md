# 🧭 Node template — how every chapter is built

*This page is the **author's skeleton** for a BUILD-AI chapter. Copy it to start
a new chapter, then replace the placeholder text. It's also a reading aid: every
chapter follows this exact shape, so you always know where you are.*

Each chapter tells one turn of the **moonwalk** and discloses it in the
**three-unity** rhythm — **one place, one action, one unit of time**. The order
below is the order on the page.

## 📚 Author note — a chapter is internally a `KnowledgeNode`

*For authors only — do **not** disclose this class to learners early.* Each
chapter is modelled as a `KnowledgeNode` (a real class in the
[component model](/components/model)); its state machine is the path the learner
walks: `locked → discovering` *(place)* `→ designing` *(action)* `→ specifying`
*(time)* `→ mastered`.

> **Objects before classes.** Learners play with each chapter as an *object*
> first. The shared `KnowledgeNode` class is revealed only in a later "Design"
> chapter, once objects feel familiar — keep it out of the early chapters, the
> catalog, and the front page.
{: .speaker-note }

[KnowledgeNode](#)
{: .diagram scope="KnowledgeNode" }

Hold **⌥ Option / Alt** and hover a chapter's widgets to x-ray them against this
model.

---

## 🎯 The goal — from the future

> *Open with the destination, not the foundations.* One short, vivid paragraph:
> what this module lets you (or Lucky) **do**, and **why it matters** — framed
> from where things are heading. The learner should want it before they
> understand it.

*Author note — `Why: from the future`. The feature already exists; we reveal it
top-down. Keep it to 3–4 lines.*

## 🧱 Before you start

> *Prerequisites = "the reveal you just saw."* One line linking back to the
> previous module (none for M1 — just curiosity). No formal prerequisites ever.

---

## 🐾 Discover — *Unity of place* (runtime: interaction first)

> *Behavior before architecture.* Put the **live, working** thing in front of
> the learner and let them act as a **user** — click, type, select, watch state
> change. **No code or model yet.** Use real components: `.form`, `.datagrid`,
> `.map`, `.chart`, `.run`. Lucky 🐕 is the concrete instance here — a specific
> pet, never an abstract "Object." (*Bottom-up: instances before models.*)

## 🔧 Design — *Unity of action* (structure emerges)

> *Now open the same thing up.* A new action — "Design" — reveals that the
> screen you used, the **model** behind it, and the **code/config** are three
> **synchronized views of one thing**. On Lightcodepedia this is literally the
> **X-ray** (⌥-hover any widget) and the editor's **Diagram** tab. Show the
> structure; don't make them write it yet. (*Outside-in: behavior before inner design.*)

## 📜 Specs — *Unity of time* (evidence-based, and they were there all along)

> *The twist.* Reveal the **specification / features** that were silently
> driving the thing from the very first click. Show the **promises it keeps** as
> examples that must pass (tests), turned into **living documentation**. The
> verified feature becomes a **reusable building block** for the next module.
> *The specs were there all along — you just discover them last.*

---

## 📌 Key concepts

> *Recap the 3–6 ideas this module taught, in plain language — one line each.*
> This is the learner's takeaway card, and it's exactly what the quiz below
> tests. Mirror the wording so the quiz feels fair.

> *Glossary by footnote — every new term gets a `[^term]` at first use, defined
> at the foot of the page.* kramdown collects them into a **Definitions** section
> (with hover popovers via `footnote_tips`), so each chapter builds its own
> glossary for free. Then close the chapter with a **"decoded"** table mapping
> the story's metaphors to that official vocabulary — story first, words last.
{: .speaker-note }

- **Concept 1** — one-line plain-language definition.
- **Concept 2** — …
- **Concept 3** — …

## 🎲 Test yourself

> *3–4 `.quiz` questions, one per key concept above.* Mark the right answer with
> `[x]`. Completing quizzes earns **karma** automatically (see below).

````
**Q:** A question that checks Concept 1.

- [ ] A plausible-but-wrong option
- [x] The correct option
- [ ] Another distractor
- [ ] Another distractor
{: .quiz }
````

## 🤖 Ask Ari

> *Ari is the guide.* Lead with a short curated Q&A (works even before a key, and
> seeds the questions learners actually ask). Then drop a **live Ari panel** —
> learners get their key in [onboarding](/micro_build_ai/onboarding), so by the
> time they reach any node, Ari can really answer. Brand it with `title: Ari`
> and `icon: 🐾`, and tailor the `system:` prompt to this node's moment.

**"Why did we use the app before learning how it works?"**
Because behavior is easier to grasp than architecture — you build intuition
first, then we explain the machinery underneath.

**"I'm stuck — where do I look?"**
Re-read the **Key concepts** card above; each line maps to one quiz question.

```yaml
title: Ari
icon: 🐾
system: |
  You are Ari, an Aristotelian pair-lightcoder for the BUILD-AI course.
  Warm, brief, Socratic. Start from the goal; offer one small next step.
  Tailor this line to the node's moment. Keep answers under ~120 words.
intro: "Ask me anything about this node."
placeholder: "Why does this matter?"
```
{: .agent id="ari_node" }

No key yet? [Get one →](/micro_build_ai/onboarding)

## ⭐ Your karma

> *No code needed — the platform tracks it.* Every quiz you pass adds **karma**,
> saved in your browser (`localStorage`). It carries across modules and counts
> toward your **BUILD-AI credential**. Nothing to sign up for; clear your
> browser data and it resets.

## ➡️ Next — one layer deeper

> *Link forward to the next module (the next reusable block), plus a way back to
> the map.*

```
### 🔜 Continue
[Next module →](#)

### 🗺️ The map
[Back to the journey](/micro_build_ai/)
```
{: .cards cols="2" }
