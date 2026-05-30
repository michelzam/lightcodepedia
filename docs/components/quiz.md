# 🧪 Quiz

Turn any bullet list into an interactive question with one IAL[^ial]. Click an option to see if you got it right. Works inline on a normal page and as a slide of its own in 📽️ slides mode.

## Single-choice — `[x]` syntax (recommended)

The natural way: use GitHub-style task-list markers. `[x]` is the correct answer, `[ ]` is wrong.

```markdown
**Q:** What does `## h2` do on this site?

- [ ] Bolds the text
- [x] Starts a new slide
- [ ] Makes the text smaller
- [ ] Centers the heading
{: .quiz }
```

Renders to:

**Q:** What does `## h2` do on this site?

- [ ] Bolds the text
- [x] Starts a new slide
- [ ] Makes the text smaller
- [ ] Centers the heading
{: .quiz }

Click any option. Wrong pick → red ✗ + the right answer flashes green. Click again to retry.

## Single-choice — `correct="N"` syntax (equivalent)

Same quiz written with the explicit attribute form. 1-indexed, plain bullets:

```markdown
- Bolds the text
- Starts a new slide
- Makes the text smaller
- Centers the heading
{: .quiz correct="2" }
```

Pick whichever feels natural per quiz. They produce identical behavior.

## Per-option explanations

Nest a `>` blockquote under any option (with blank lines around it — kramdown's nesting rule) for a one-line explanation that appears after the option is graded:

```markdown
- [ ] Bolds the text

  > That would be `**bold**`.

- [x] Starts a new slide

  > Right — `## h2` is the slide break.

- [ ] Makes the text smaller

  > That would be smaller `<h3>` and friends.
{: .quiz }
```

Renders to:

- [ ] Bolds the text

  > That would be `**bold**`.

- [x] Starts a new slide

  > Right — `## h2` is the slide break.

- [ ] Makes the text smaller

  > That would be smaller `<h3>` and friends.
{: .quiz }

The explanation styles green for the correct option, red for a wrong-clicked one. You can write full markdown inside the blockquote (code spans, **bold**, links).

## Multi-select — square checkboxes

Add `multi="true"` and `[x]` on every correct option. The visual marker shifts to **☐ / ☑** to signal "pick all that apply", and a **Check** button appears below:

```markdown
**Q:** Which of these are vegetables?

- [ ] Apple
- [x] Carrot
- [ ] Steak
- [x] Spinach
{: .quiz multi="true" }
```

Renders to:

**Q:** Which of these are vegetables?

- [ ] Apple
- [x] Carrot
- [ ] Steak
- [x] Spinach
{: .quiz multi="true" }

Toggle each ☐ to ☑, hit **Check**. Missed-correct and wrong-selected both get ✗; only fully matching picks pass.

## Page-level score

Once you've answered at least one quiz on the page, a small **🏆 N/M** badge appears at the bottom-right (above the ✏️ pencil). Tap it for a per-quiz breakdown. The score is **session-only** — refresh clears it. No grades are reported anywhere.

`.run` blocks with `expected="…"` count toward the score too (see below).

## Code-as-answer — `.run expected="…"`

Add `expected="…"` to a `.run` block and the runner compares the printed output to the expected string after every ▶ Run. Match → ✓ in the status. Mismatch → ✗ with the expected value.

```python
print("hello")
```
{: .run rows="2" expected="hello" }

The runner above is graded: get the print right, score it. Edit and retry until the expected matches.

## Knobs

| Attribute | Description |
|---|---|
| `correct="N"` | Single-choice answer (1-indexed) |
| `correct="N,M,…"` | Multi-select answers (1-indexed, comma-separated) |
| `multi="true"` | Enables multi-select mode + Check button + checkbox visuals |
| `[x]` / `[ ]` | GitHub task-list sugar — replaces `correct=` when used |
| nested `>` blockquote | Per-option explanation, shown after grading |
| `id="…"` on the list | Used for the score-popover label; auto-generated if missing |

## Inside slides mode

Quizzes work as slides of their own with no extra syntax. The slide engine skips click-to-advance over quiz options, so students can pick without skipping ahead.

## Two more for the road

**Q:** Which kramdown syntax adds a footnote popover?

- [x] `[^name]` / `[^name]: …`
- [ ] `<abbr title="…">`
- [ ] {% raw %}`{% include def.md term="…" %}`{% endraw %}
- [ ] `### Definitions`
{: .quiz }

**Q:** Which of these become slide breaks in 📽️ mode?

- [ ] `# h1`
- [x] `## h2`
- [ ] `### h3`
- [ ] `#### h4`
{: .quiz multi="true" }

## Limits of v1 — still

Future asks if you hit them:

- **No per-attempt log**, just a snapshot of current correctness per quiz. Re-answering correctly after a wrong pick counts as correct.
- **No persistence** across reloads. Easy to add via localStorage if you want; ask.
- **No fill-in-the-blank widget.** `.run expected="…"` is the working substitute — students write code to produce specific output.

[^ial]: **Inline Attribute List** — kramdown's `{: .class key="value" }` syntax, placed on its own line right after a block (here: a bullet list), attaches attributes to that block. See [Text](/components/text).

{% include backtotop.md %}
