---
---
# 🎨 Custom class

Components cover most needs — but when you want your *own* look, you can define a **custom CSS class** and attach it to any block with an IAL tag, exactly the way every component activates. The components are just someone else's classes; here you make your own.

## 👀 See it in action

<style>
.highlight-box {
  background: #fffbea;
  border-left: 4px solid #f59e0b;
  padding: 0.8em 1em;
  border-radius: 6px;
}
</style>

This paragraph wears a custom class — a warm callout box you defined yourself, in two lines of plain text.
{: .highlight-box }

## 🛠️ How to make one

Two steps:

**1. Define the class once**, in a small `<style>` block (CSS is the one bit of markup that's fair game — it's presentation, not logic):

````html
<style>
.highlight-box {
  background: #fffbea;
  border-left: 4px solid #f59e0b;
  padding: 0.8em 1em;
  border-radius: 6px;
}
</style>
````

**2. Attach it** to any paragraph, list, heading, or fenced block with an IAL tag on the very next line — the same `{: .class }` syntax `{: .qr }` and `{: .datagrid }` use:

````markdown
This paragraph wears a custom class.
{: .highlight-box }
````

That's the whole trick. The only difference between `.highlight-box` and `.datagrid` is that *you* decided what `.highlight-box` means.

## 💡 Tips

- **Stack classes**: `{: .highlight-box .center }` attaches both.
- **Tweak a component**: stack your class onto a built-in — `{: .datagrid .compact }` — to restyle it without touching the component.
- **Reuse**: define the class once near the top of the page, attach it as many times as you like.
- **Site-wide**: for a class you want on *every* page, add it to the site's CSS instead of a per-page `<style>`.

> A favourite classroom moment: "The components are someone else's classes — now make your own." It demystifies the entire `{: .x }` syntax in a single step.
{: .speaker-note }

**Q:** How do you attach a custom class `.note` to a paragraph?

- [ ] Wrap the paragraph in `<div class="note">`.
- [x] Put `{: .note }` on the line right after the paragraph.
- [ ] Add `class: note` to the page's front matter.
- [ ] Prefix the paragraph with `.note:`.
{: .quiz }
