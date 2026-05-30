# 🧪 Quiz

Turn any bullet list into an interactive question with one IAL[^ial]. Click an option to see if you got it right. Works inline on a normal page and as a slide of its own in 📽️ slides mode.

## Single-choice (immediate feedback)

Source:

```markdown
**Q:** What does `## h2` do on this site?

- Bolds the text
- Starts a new slide
- Makes the text smaller
- Centers the heading
{: .quiz correct="2" }
```

Renders to:

**Q:** What does `## h2` do on this site?

- Bolds the text
- Starts a new slide
- Makes the text smaller
- Centers the heading
{: .quiz correct="2" }

Click any option. Wrong pick gets ✗ in red and the right answer flashes green. Click again to retry.

## Multi-select (Check to grade)

Add `multi="true"` and list multiple correct positions in `correct=`:

```markdown
**Q:** Which of these are vegetables?

- Apple
- Carrot
- Steak
- Spinach
{: .quiz multi="true" correct="2,4" }
```

Renders to:

**Q:** Which of these are vegetables?

- Apple
- Carrot
- Steak
- Spinach
{: .quiz multi="true" correct="2,4" }

Click each option to toggle selection. Hit **Check** to grade. Wrong-selected and missed-correct items both get ✗; only fully-correct picks get ✓. Click an option again to reset and retry.

## How `correct=` works

- **1-indexed.** First option is `1`, second is `2`, etc.
- **Comma-separated for multi.** `correct="1,3,5"` accepts three correct picks.
- **Whitespace tolerated.** `correct="1, 3, 5"` is the same.
- **Out-of-range silently ignored.** `correct="0"` or `correct="99"` just means "no correct answer matches" — useful while drafting.

## Inside slides mode

Quizzes work as slides of their own with no extra syntax. The slide engine knows not to advance the deck on quiz clicks — students can pick options without skipping ahead.

A slide-friendly pattern:

```markdown
## Quick check

**Q:** Which IAL turns a list into a quiz?

- `{: .runnable }`
- `{: .quiz }`
- `{: .test }`
{: .quiz correct="2" }
```

The whole thing fits a single slide; click-to-advance is suppressed on the quiz, so the student has to answer (or hit `→` / picker) to move on.

## Knobs

| Attribute | Description |
|---|---|
| `correct="N"` | Single-choice answer (1-indexed) |
| `correct="N,M,…"` | Multi-select answers (1-indexed, comma-separated) |
| `multi="true"` | Enables multi-select mode + Check button |

## Limits of v1

Not in this version — easy to add later if you want them:

- **Per-option explanations.** Currently when wrong, the right answer flashes; that's the only feedback. Inline explanations (`"x is wrong because…"`) would need a per-item IAL convention; deferred until needed.
- **Scoring across multiple quizzes.** Each quiz is independent — no page-level or session-level score yet.
- **Code-as-answer / fill-in-the-blank.** Pair a `.run` runner with a question instead — let students try the code and see what `print()` says.

## Try a few

**Q:** Which kramdown syntax adds a footnote popover?

- `[^name]` / `[^name]: …`
- `<abbr title="…">`
- {% raw %}`{% include def.md term="…" %}`{% endraw %}
- `### Definitions`
{: .quiz correct="1" }

**Q:** Which of these become slide breaks in 📽️ mode?

- `# h1`
- `## h2`
- `### h3`
- `#### h4`
{: .quiz multi="true" correct="2" }

[^ial]: **Inline Attribute List** — kramdown's `{: .class key="value" }` syntax, placed on its own line right after a block (here: a bullet list), attaches attributes to that block. See [Text](/components/text).

{% include backtotop.md %}
