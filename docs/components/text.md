# ✍️ Text — Markdown basics

Every page on this site is a plain text file written in Markdown[^md] — the lightweight format that turns `**bold**` into **bold** and `## Heading` into a big header. This page is your cheat sheet.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

There's one lightcodepedia twist: any `[^footnote]` reference becomes a hover/tap popover[^pop]. Try hovering or tapping the blue numbers above — like right now.

## 📐 Headings — structure your page

Three levels you'll actually use:

- `# Title` — the page's big `h1` heading (one per page).
- `## Section` — `h2`, also a **slide break** in 📽️ slides mode.
- `### Sub-section` — `h3`, just smaller. Not a slide break.

```markdown
# My Page Title

## First Section

### A sub-point inside that section
```

> Common confusion: students use `###` expecting it to create a new slide.
> Only `## h2` breaks slides. Worth repeating before the first presentation.
{: .speaker-note }

**Q:** You're building a 5-slide deck. Which heading level creates each new slide?

- [ ] `# h1` — the page title is slide 1, next `# h1` is slide 2.
- [x] `## h2` — the only heading level that starts a new slide.
- [ ] `### h3` — finer granularity is better.
- [ ] All of them. More `#` = more structure = more slides.
{: .quiz }

## ✨ Emphasis & inline marks

The six marks you'll use every day:

- `*italic*` or `_italic_` → *italic*
- `**bold**` → **bold**
- `` `inline code` `` → `inline code`
- `~~strikethrough~~` → ~~strikethrough~~
- `> quote` → a blockquote (see below)
- `[link text](url)` → a [link](https://example.com)

None of these need a blank line before or after — they work inline within a paragraph.

## 📋 Lists — bullets and numbers

**Bullets** — any of `-`, `*`, or `+` starts a list item:

```markdown
- first item
- second item
- third item
```

**Numbered** — the actual numbers don't matter; kramdown[^md] renumbers automatically:

```markdown
1. step one
1. step two
1. step three
```

Both render as you'd expect. Two-level nesting is fine; deeper nesting gets cramped in slides mode.

> In slide mode, every top-level `<li>` auto-fragments — one click per bullet.
> Tag the list `{: .nofragments }` if you want all items visible at once.
> See [📽️ Slides](/components/slides) for the full story.
{: .speaker-note }

**Q:** You type `1. step one` then `1. step two`. What numbers does the rendered page show?

- [ ] `1.` and `1.` — it renders exactly what you wrote.
- [x] `1.` and `2.` — kramdown renumbers automatically.
- [ ] It shows bullet points instead — kramdown ignores the numbers.
- [ ] Nothing renders — you need sequential numbers.
{: .quiz }

## 🔗 Links

Three patterns:

```markdown
[label](https://example.com)   external link
[label](/components/run)        another page on this site
[label](#section-heading-id)    anchor within this page
```

Internal links use a leading `/` — no domain needed. Anchor ids are the heading text lowercased with spaces replaced by hyphens: `## My Section` → `#my-section`.

## 💻 Code blocks

Three backticks, a language tag, the code, three backticks:

````markdown
```python
print("hello")
```
````

Common language tags: `python`, `yaml`, `json`, `markdown`, `liquid`, `csv`, `bash`.

To make a block **live** (editable and runnable), add `{: .run }` on the next line:

```python
print("hello, lightcodepedia")
```
{: .run rows="2" }

That `{: .run }` is an IAL[^ial] — see the IAL section below. It's how every component on this site gets activated.

**Q:** Which tag makes a fenced code block into a live Python editor?

- [ ] `{: .python }` — tells the page the language.
- [ ] `{: .live }` — obvious, descriptive.
- [x] `{: .run }` on the line right after the closing fence.
- [ ] A triple-star comment `***run***` inside the block.
{: .quiz }

## 📊 Tables

```markdown
| Column   | Notes                |
|----------|----------------------|
| short    | first column         |
| longer   | second column        |
```

Renders to:

| Column   | Notes                |
|----------|----------------------|
| short    | first column         |
| longer   | second column        |

Align columns with `:---` (left), `:---:` (center), `---:` (right) in the separator row.

Use a plain markdown table for ≤10 static rows. Use `{: .datagrid }` when students need to sort, filter, or scroll through many rows — see [📊 Datagrid](/components/datagrid).

## 💬 Blockquotes

```markdown
> This is a blockquote.
> It can span multiple lines.
> Each line starts with `> `.
```

> This is a blockquote.
> It can span multiple lines.
> Each line starts with `> `.

On this site, blockquotes tagged with `{: .speaker-note }` become presenter notes — hidden by default, visible when you press **N** in slide mode or add `?notes=1` to the URL.

## 📌 Footnotes — the hover-popover trick

This is the killer feature for tutorials. Write a term reference anywhere in your prose:

```markdown
The runner uses WebAssembly[^wasm] to run Python in the browser.
```

Then define it once (convention: at the bottom of the page):

```markdown
[^wasm]: **WebAssembly** — a binary format that runs near-native speed in
         every modern browser. No install, no server.
```

Without any extra work, lightcodepedia turns the little `[1]` link into a **hover/tap popover** containing the full definition. The reader never loses their place.

**Rules:**
1. Put `[^anyname]` right after the term in your prose — no space before the bracket.
2. Put `[^anyname]: definition` anywhere later in the file (convention: end of page).
3. The definition can include **bold**, *italic*, `code`, and links.
4. The same `[^anyname]` can appear multiple times — one definition serves all.

**What makes a good footnote definition:**
- Lead with `**Term**` then an em-dash, then the explanation.
- Keep it to 1–3 sentences. The popover is small.
- Definitions also print at the bottom of the page — useful for PDFs.

> Footnote popovers are one of the most-noticed features by new visitors.
> "Wait, did it just show me a definition? Without a page jump?" — yes, always.
{: .speaker-note }

## ⚙️ IAL — the power move

The pattern you'll see after plain markdown is the **IAL[^ial]**: a `{: ... }` line right after any block, attaching attributes (classes, ids, key-value pairs) to it. This is how every component on this site gets activated.

````markdown
```yaml
- name: Lucky
- name: Wanda
```
{: .datagrid id="dogs" }
````

Then `{: .form bound="dogs" }` on another block binds a form to that grid. The `.datagrid`, `.form`, `.run`, `.quiz`, `.agent` — all IAL.

**Rules:**
- Must be on its own line, immediately after the block (no blank line between).
- Multiple classes: `{: .class1 .class2 }`.
- Mix classes and key-value pairs: `{: .run id="demo" rows="4" }`.

**Q:** You write `{: .datagrid }` but there's a blank line between it and the YAML block. What happens?

- [x] The IAL doesn't attach — kramdown sees a new block. The grid never renders.
- [ ] It still works — kramdown is forgiving about blank lines.
- [ ] It renders as a form instead.
- [ ] The page compiles correctly but explodes at runtime.
{: .quiz }

## 💬 HTML comments

`<!-- hidden from readers -->` works and renders nothing. Good for draft notes, section markers, or reminders to your future self.

## 🏁 Cheat sheet

| You write | You get |
|---|---|
| `# T` | big `h1` with blue underline |
| `## S` | `h2`, also a slide break |
| `### s` | `h3` |
| `*x*` / `_x_` | *italic* |
| `**x**` | **bold** |
| `` `x` `` | inline `code` |
| `[t](url)` | link |
| `> q` | blockquote |
| `- / 1.` | list item |
| `\`\`\`py` | fenced code (Python) |
| `{: .class }` | IAL — attach attributes to block above |
| `[^x]` / `[^x]:` | footnote ref + definition (popover) |

---

**Q:** Which of these are TRUE about markdown on this site? (Pick all that apply.)

- [x] `## h2` is both a section heading and a slide break.
- [x] `[^name]` creates a hover/tap definition popover.
- [ ] `{: .datagrid }` must come before the YAML block.
- [x] The IAL must be on its own line immediately after the block — no blank line.
- [ ] Numbered lists must use sequential numbers or they won't render.
{: .quiz multi="true" }

[^md]: **Markdown** is a lightweight text format that converts to HTML — designed so the plain-text source is readable on its own. This site uses [kramdown](https://kramdown.gettalong.org/), a Ruby variant with extras: footnotes, IAL attribute lists, and task-list checkboxes.

[^pop]: **Footnote popover** — lightcodepedia's extension of kramdown's standard `[^name]` footnote syntax. Instead of jumping to the bottom of the page, the definition appears as a small popup/tooltip right where the `[1]` reference appears. Works on hover (desktop) and tap (mobile).

[^ial]: **IAL (Inline Attribute List)** — kramdown's `{: .class id="x" key="value" }` syntax. Placed on its own line right after a block, it attaches HTML attributes — ids, classes, data attributes — to that block. Every interactive component on this site (run, datagrid, form, quiz, agent, slides) is activated this way.

{% include backtotop.md %}
