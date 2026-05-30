# 🔘 Button

A styled call-to-action link. Write a normal markdown link, add `{: .lc-btn }` inline after the closing bracket, and it renders as a button. Four color variants; works anywhere a link works.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 See it in action

[🚀 Get started](/components/run){: .lc-btn }
[Learn more](/components/text){: .lc-btn .lc-btn-secondary }
[✓ Done](/components/quiz){: .lc-btn .lc-btn-success }
[✗ Delete](#){: .lc-btn .lc-btn-danger }
[Outline](#){: .lc-btn .lc-btn-outline }

## 🛠️ How to make one

Add `{: .lc-btn }` **immediately** after the closing `]` of any markdown link — no space, no newline:

```markdown
[🚀 Get started](/components/run){: .lc-btn }
```

This is kramdown's **inline IAL** — it attaches the class directly to the `<a>` element.

**Q:** You write `[Go](#) {: .lc-btn }` with a space before `{:`. Does the button render?

- [ ] Yes — kramdown is flexible about spaces before inline IAL.
- [x] No — the inline IAL must immediately follow the `]` with no space at all.
- [ ] It attaches to the paragraph instead.
- [ ] It becomes an outline button — the space triggers a fallback style.
{: .quiz }

## 🎨 Variants

| You write | Result |
|---|---|
| `{: .lc-btn }` | Blue (primary) |
| `{: .lc-btn .lc-btn-secondary }` | Grey |
| `{: .lc-btn .lc-btn-success }` | Green |
| `{: .lc-btn .lc-btn-danger }` | Red |
| `{: .lc-btn .lc-btn-outline }` | Transparent with blue border |

## 🏁 Final exam

**Q:** Which markdown produces a green button linking to `/submit`?

- [ ] `[Submit](/submit){: .lc-btn-success }` — variant class only.
- [x] `[Submit](/submit){: .lc-btn .lc-btn-success }` — base class + variant.
- [ ] `[Submit](/submit){: .btn .btn-success }` — Bootstrap-style classes.
- [ ] Only the old `{% raw %}{% include button.md %}{% endraw %}` form produces colored buttons.
{: .quiz }

{% include backtotop.md %}
