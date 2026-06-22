# 🧪 Quiz

Turn any bullet list into an interactive question with one line of markup. Students click to answer; wrong picks show ✗ immediately but the correct answer stays hidden until they find it — a treasure hunt, not an answer key.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 🎯 Try one now

**Q:** What does `## h2` do on this site?

- [ ] Makes the text a bit bigger than `### h3`.
- [x] Starts a new slide in 📽️ slide mode.
- [ ] Centers the heading.
- [ ] Nothing special — it's just a regular heading.
{: .quiz }

Click any option. Wrong answer? You see a red ✗ on that pick. The correct answer stays hidden. Find it yourself — that's the point.

> Before students click, ask them to predict aloud. "What do you think happens when you click a wrong answer?"
> The treasure-hunt behavior surprises everyone — most expect the answer to be revealed immediately.
{: .speaker-note }

```gherkin
Feature: A task list becomes an interactive quiz
  As a lowcoder
  I want a bullet list with [x]/[ ] markers to grade clicks
  So that learners self-check with no backend

  Scenario: Picking an option reveals a verdict on it
    Given a single-select quiz on this page
    :::python
    self.quiz = None
    for q in Object._all(".lc-quiz"):
        if q._attr("multi") != "true":
            self.quiz = Quiz(q._el)
            break
    assert self.quiz is not None, "no single-select quiz found"
    self.opts = self.quiz._qq("li")
    :::
    When nothing has been clicked yet
    Then the quiz is ungraded
    :::python
    assert not self.quiz.graded
    :::
    When I pick the first option
    :::python
    self.quiz.pick(0)
    :::
    Then that option is revealed as right or wrong
    :::python
    first = self.opts[0]._el
    assert first.classList.contains("lc-quiz-correct") or first.classList.contains("lc-quiz-wrong")
    assert self.quiz.graded
    :::
```
{: .feature tags="learn" status="passing" }

## 🛠️ How to make a quiz

Write a bullet list with `[x]` on the correct answer and `[ ]` on the wrong ones. Add `{: .quiz }` on the very next line.

```markdown
**Q:** Which IAL[^ial] activates the Python runner?

- [ ] `{: .run-python }`
- [x] `{: .run }`
- [ ] `{: .python }`
- [ ] `{: .exec }`
{: .quiz }
```

Renders to:

**Q:** Which IAL activates the Python runner?

- [ ] `{: .run-python }`
- [x] `{: .run }`
- [ ] `{: .python }`
- [ ] `{: .exec }`
{: .quiz }

The `[x]` / `[ ]` syntax is identical to GitHub's task-list checkboxes — no new syntax to learn.

> The IAL must be directly after the last list item (or its nested blockquote).
> A blank line before `{: .quiz }` breaks attachment silently.
> You'd see a plain bullet list with no click behavior — the most common gotcha.
{: .speaker-note }

**Q:** You added `{: .quiz }` but clicking the options does nothing. What's the most likely cause?

- [ ] The quiz widget needs `multi="true"` to work.
- [x] There's a blank line between the last list item and `{: .quiz }` — the IAL didn't attach.
- [ ] You used `[x]` but the correct syntax is `[X]` (capital X).
- [ ] Quizzes only work in slide mode. You're in scroll mode.
{: .quiz }

## ✏️ Per-option explanations

Nest a `>` blockquote under any list item to add an explanation that appears after that option is graded.

```markdown
- [ ] Bolds the text.

  > That would be `**bold**`.

- [x] Starts a new slide.

  > Right — `## h2` is the slide break in 📽️ mode.

- [ ] Makes the text smaller.

  > That's `### h3` — smaller, but not a slide break.
{: .quiz }
```

Renders to:

- [ ] Bolds the text.

  > That would be `**bold**`.

- [x] Starts a new slide.

  > Right — `## h2` is the slide break in 📽️ mode.

- [ ] Makes the text smaller.

  > That's `### h3` — smaller, but not a slide break.
{: .quiz }

The explanation styles green for the correct pick, red for a wrong one. Full markdown works inside the blockquote: `code`, **bold**, links.

## ☑️ Multi-select — "pick all that apply"

Add `multi="true"` and mark every correct option with `[x]`. The visual shifts to square **☐ / ☑** checkboxes and a **Check** button appears. Wrong-selected picks get ✗ after Check, but **missed correct answers stay hidden** — same treasure-hunt rule.

```markdown
**Q:** Which of these are valid Python loop types? (Pick all that apply.)

- [x] `for`
- [ ] `repeat`
- [x] `while`
- [ ] `loop`
{: .quiz multi="true" }
```

Renders to:

**Q:** Which of these are valid Python loop types? (Pick all that apply.)

- [x] `for`
- [ ] `repeat`
- [x] `while`
- [ ] `loop`
{: .quiz multi="true" }

Toggle each ☐ to ☑, hit **Check**. Re-toggle and re-check until you've found every correct answer.

**Q:** A student clicks **Check** and only `for` is marked ✓. They haven't found `while` yet. What does the quiz show?

- [x] ✗ on their wrong picks; the missed correct answer (`while`) stays hidden.
- [ ] All correct answers are revealed so you can learn.
- [ ] The quiz resets and they start over.
- [ ] A confetti explosion. They found one — celebrate the partial win.
{: .quiz }

## 📊 Page-level score 🏆

Once you've answered at least one quiz on the page, a small **🏆 N/M** badge appears at the top-right. Tap it for a per-quiz breakdown. The score is **session-only** — refresh clears it. No grades are reported anywhere.

`.run` blocks with `expected="…"` count toward the score too: match the expected output → ✓.

```python
print("hello")
```
{: .run rows="2" expected="hello" }

The runner above is graded. Edit it to print something else — the score badge updates.

> For a live demo: walk through the score badge after answering a few quizzes on this page.
> "Notice how it updated? That's your personal tally — nobody else sees it, and it resets on refresh."
{: .speaker-note }

## 🔧 Knobs

| Attribute | What it does |
|---|---|
| `[x]` / `[ ]` | Marks correct / wrong answers inline — recommended |
| `correct="N"` | Equivalent to `[x]` — 1-indexed position of the correct answer |
| `correct="N,M,…"` | Multi-select correct answers (1-indexed, comma-separated) |
| `multi="true"` | Enables multi-select mode: checkboxes + Check button |
| nested `>` blockquote | Per-option explanation, shown after grading |
| `id="…"` | Label in the 🏆 score popover; auto-generated if omitted |

**Q:** You have a 3-option quiz where option 2 is correct. Which IAL is equivalent to using `[x]` on option 2?

- [ ] `{: .quiz correct="option-2" }`
- [x] `{: .quiz correct="2" }` — 1-indexed position
- [ ] `{: .quiz answer="2" }`
- [ ] `{: .quiz position="2" }`
{: .quiz }

## 🎭 Inside slides mode

Quizzes work inside slides with no extra syntax. The slide engine **does not advance the deck** when you click a quiz option — so students answer without skipping to the next slide. The slide picker shows a colored dot for each slide with a quiz: 🔵 untried, 🟠 attempted, 🟢 all correct.

## 🏁 Final exam — boss level

**Q:** Which of these are TRUE about quizzes? (Pick all that apply.)

- [x] `[x]` marks the correct answer; `[ ]` marks wrong ones.
- [x] Blank line before `{: .quiz }` silently breaks the widget.
- [ ] `multi="true"` reveals all correct answers when Check is clicked.
- [x] `.run expected="…"` blocks count toward the 🏆 score.
- [ ] The score is saved to localStorage and persists across reloads.
{: .quiz multi="true" }

**Q:** A student clicks three wrong answers in a row. What has the quiz revealed so far?

- [ ] All wrong answers are revealed — they'd see three red ✗ items.
- [x] Only the three items they actually clicked get ✗. Unclicked wrong answers stay neutral.
- [ ] The quiz gives up and reveals the correct answer after three wrong tries.
- [ ] The page refreshes. Three strikes, you're out.
{: .quiz }

**Q:** It's a treasure-hunt quiz. There are 4 options. You've clicked 3 wrong ones (all ✗). How many clicks to finish?

- [x] Exactly one — the only remaining option must be the correct one.
- [ ] Four — you need to re-click everything to confirm.
- [ ] Zero — three ✗ means the quiz gives up and grades itself.
- [ ] Unknowable. The quiz keeps the secret forever.
{: .quiz }

## ⚠️ Limits of v1

- **No per-attempt log.** Re-answering correctly after a wrong pick counts as correct in the score. It's a learning tool, not an exam platform.
- **No persistence.** Score clears on refresh. Ask if you want localStorage persistence.
- **No fill-in-the-blank.** Use `.run expected="…"` as the substitute — students write code to produce the expected output.

[^ial]: **IAL (Inline Attribute List)** — kramdown's `{: .class key="value" }` syntax, placed on its own line right after a block, attaches HTML attributes to it. See [✍️ Text](/components/text).
