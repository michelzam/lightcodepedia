# 🔘 Button

A styled call-to-action link. Write a normal markdown link, add `{: .button }` inline after the closing bracket, and it renders as a button. Four color variants; works anywhere a link works.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 See it in action

[🚀 Get started](/components/run){: .button }
[Learn more](/components/text){: .button .button-secondary }
[✓ Done](/components/quiz){: .button .button-success }
[✗ Delete](#){: .button .button-danger }
[Outline](#){: .button .button-outline }

## 🛠️ How to make one

Add `{: .button }` **immediately** after the closing `]` of any markdown link — no space, no newline:

```markdown
[🚀 Get started](/components/run){: .button }
```

This is kramdown's **inline IAL** — it attaches the class directly to the `<a>` element.

**Q:** You write `[Go](#) {: .button }` with a space before `{:`. Does the button render?

- [ ] Yes — kramdown is flexible about spaces before inline IAL.
- [x] No — the inline IAL must immediately follow the `]` with no space at all.
- [ ] It attaches to the paragraph instead.
- [ ] It becomes an outline button — the space triggers a fallback style.
{: .quiz }

## 🎨 Variants

| You write | Result |
|---|---|
| `{: .button }` | Blue (primary) |
| `{: .button .button-secondary }` | Grey |
| `{: .button .button-success }` | Green |
| `{: .button .button-danger }` | Red |
| `{: .button .button-outline }` | Transparent with blue border |

## 🏁 Final exam

**Q:** Which markdown produces a green button linking to `/submit`?

- [ ] `[Submit](/submit){: .button-success }` — variant class only.
- [x] `[Submit](/submit){: .button .button-success }` — base class + variant.
- [ ] `[Submit](/submit){: .btn .btn-success }` — Bootstrap-style classes.
- [ ] Only the old `{% raw %}{% include button.md %}{% endraw %}` form produces colored buttons.
{: .quiz }
