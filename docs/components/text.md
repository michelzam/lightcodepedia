# ✍️ Text — Markdown basics

Every page on this site is a plain text file written in Markdown[^md] — the lightweight format that turns `**bold**` into **bold** and `## Heading` into a big header. This page is your cheat sheet and playground.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

There's one lightcodepedia twist: any `[^footnote]` reference becomes a hover/tap popover[^pop]. Try hovering the blue numbers above.

## ✏️ Try it live — edit and see

Type markdown on the left. See the rendered result on the right — instantly, as you type.

````markdown
## Hello, Markdown!

**Bold text** and *italic text* and `inline code`.

Inline *colour*{: .red} works in the live preview too.

- First bullet
- Second bullet
- Third bullet

1. Step one
1. Step two
1. Step three

| Name  | Age | Breed   |
|-------|-----|---------|
| Lucky |  3  | Beagle  |
| Wanda |  5  | Poodle  |

> A blockquote is just a line starting with `> `.

[Visit lightcodepedia](/)

```python
def greet(name):
    print(f"Hello, {name}!")
```
````
{: .mdpad rows="16" }

Try changing `**Bold**` to `**Loud**`. Add a new bullet. Break a table row. The preview updates on every keystroke — no server, just JavaScript[^marked] in the browser.

> Great opener for the first class: "Type your name in bold. Now make it a heading."
> The instant feedback loop lands faster than any explanation.
{: .speaker-note }

**Q:** You type `*hello*` in the editor. What appears in the preview?

- [ ] `*hello*` — the asterisks are displayed literally.
- [x] *hello* — italic text, asterisks consumed by the parser.
- [ ] A bullet point containing "hello".
- [ ] Nothing. The parser needs a page reload to see changes.
{: .quiz }

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

- [ ] `# h1` — each `# h1` is a new slide.
- [x] `## h2` — the only heading level that starts a new slide.
- [ ] `### h3` — finer granularity is better.
- [ ] All three. The more `#`, the more structure.
{: .quiz }

## ✨ Emphasis & inline marks

The six marks you'll use every day:

- `*italic*` or `_italic_` → *italic*
- `**bold**` → **bold**
- `` `inline code` `` → `inline code`
- `~~strikethrough~~` → ~~strikethrough~~
- `[link text](url)` → a [link](#)
- `> quote` → a blockquote (see below)

All of these work inside a paragraph — no blank lines needed around them.

## 🎨 Colour — tint a word

Markdown has no colour syntax, but lightcodepedia ships a few **colour classes** you apply with an IAL[^ial] — no HTML, no CSS to write. Wrap the word in `*…*` (the asterisks are just the carrier; the class shows it as plain colour):

- `*danger*{: .red}` → *danger*{: .red}
- `*success*{: .green}` → *success*{: .green}
- `*note*{: .blue}` → *note*{: .blue}
- `*warning*{: .amber}` → *warning*{: .amber}
- `*aside*{: .muted}` → *aside*{: .muted}
- `*highlight*{: .hl}` → *highlight*{: .hl} — a background mark

A whole phrase works too: `**the entire thing**{: .green}` → **the entire thing**{: .green}.

> Keep colour *meaningful*{: .blue} — red for caution, green for good — rather than decorative. A class is themeable and consistent; a hand-typed HTML colour is neither.
{: .speaker-note }

**Q:** How do you colour a word green without writing any HTML?

- [ ] `<span style="color:green">word</span>` in the markdown.
- [x] `*word*{: .green}` — an IAL colour class on an inline carrier.
- [ ] `{green}word{/green}` — a colour shortcode.
- [ ] You can't; markdown has no colour at all.
{: .quiz }

## 📋 Lists — bullets and numbers

**Bullets** — any of `-`, `*`, or `+` starts a list item:

```markdown
- first item
- second item
- third item
```

**Numbered** — the actual number values don't matter; kramdown renumbers automatically:

```markdown
1. step one
1. step two
1. step three
```

Two-level nesting is fine; deeper nesting gets cramped in slides mode.

> In slide mode, every top-level `<li>` auto-fragments — one click per bullet.
> Tag the list `{: .nofragments }` if you want all items visible at once.
{: .speaker-note }

**Q:** You write `1. step one` then `1. step two`. What numbers appear on the page?

- [ ] `1.` and `1.` — it renders exactly what you wrote.
- [x] `1.` and `2.` — kramdown renumbers automatically.
- [ ] Two bullet points — kramdown ignores the numbers.
- [ ] A parse error. You needed `2. step two`.
{: .quiz }

## 🔗 Links

Three patterns:

```markdown
[label](https://example.com)    external link
[label](/components/run)         another page on this site
[label](#section-heading-id)     anchor within this page
```

Internal links use a leading `/` — no domain needed. Anchor ids are the heading text lowercased with spaces replaced by hyphens: `## My Section` → `#my-section`.

## 💻 Code blocks

Three backticks, a language tag, the code, three more backticks:

````markdown
```python
print("hello")
```
````

Common language tags: `python`, `yaml`, `json`, `markdown`, `liquid`, `csv`, `bash`.

To make a block **live** (editable and runnable), add `{: .run }` on the very next line:

```python
print("hello, lightcodepedia")
```
{: .run rows="2" }

That `{: .run }` is an IAL[^ial] — see the IAL section below. It's how every interactive component on this site gets activated.

**Q:** Which line makes a fenced code block into a live Python editor?

- [ ] `{: .python }` — tells the page the language.
- [ ] `{: .live }` — descriptive and obvious.
- [x] `{: .run }` on the line right after the closing fence.
- [ ] A `# run` comment inside the block.
{: .quiz }

## 📊 Tables

```markdown
| Column   | Notes         |
|----------|---------------|
| short    | first column  |
| longer   | second column |
```

Renders to:

| Column   | Notes         |
|----------|---------------|
| short    | first column  |
| longer   | second column |

Align columns with `:---` (left), `:---:` (center), `---:` (right) in the separator row.

Use a plain markdown table for ≤10 static rows. Use `{: .datagrid }` when students need to sort, filter, or scroll through many rows — see [📊 Datagrid](/components/datagrid).

## 💬 Blockquotes

```markdown
> A blockquote starts with `> `.
> Multiple lines work fine.
```

> A blockquote starts with `> `.
> Multiple lines work fine.

On this site, blockquotes tagged `{: .speaker-note }` become presenter notes — hidden by default, visible when you press **N** in slide mode.

## 📌 Footnotes — the hover-popover trick

This is the killer feature for tutorials. Write a term reference anywhere in your prose:

```markdown
The runner uses WebAssembly[^wasm] to run Python in the browser.
```

Then define it once (convention: bottom of the page):

```markdown
[^wasm]: **WebAssembly** — a binary format that runs near-native speed
         in every modern browser. No install, no server.
```

Without any extra work, lightcodepedia turns the little number link into a **hover/tap popover** with the full definition — the reader never loses their place.

**Rules:**
1. Put `[^anyname]` right after the term — no space before the bracket.
2. Put `[^anyname]: definition` anywhere later in the file.
3. The definition supports full inline markdown: **bold**, *italic*, `code`, links.
4. The same `[^anyname]` can appear multiple times — one definition covers all.

> "The popover thing" is consistently the most-noticed feature by new visitors.
> "Wait — it showed me the definition without a page jump?" — let them discover it.
{: .speaker-note }

## ⚙️ IAL — the power move

The pattern you'll see most often after plain markdown is the **IAL[^ial]**: a `{: ... }` line right after any block that attaches attributes (classes, ids, key-value pairs) to it. This is how every component on this site gets activated.

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

**Q:** You write `{: .datagrid }` but leave a blank line between it and the YAML block. What happens?

- [x] The IAL doesn't attach — kramdown sees a new block. The grid never renders.
- [ ] It still works — kramdown is forgiving about blank lines.
- [ ] It renders as a form instead.
- [ ] The page compiles fine and explodes quietly at runtime.
{: .quiz }

## 💬 HTML comments

`<!-- hidden from readers -->` works and renders nothing. Use for draft notes or reminders to your future self.

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
| `- ` / `1.` | list item |
| <code>```python</code> | fenced code block |
| `*x*{: .red}` | *red* coloured word (also `.green .blue .amber .muted .hl`) |
| `{: .class }` | IAL — attach attributes to block above |
| `[^x]` / <code>[^x]:</code> | footnote ref + definition (popover) |

---

**Q:** Which of these are TRUE about markdown on this site? (Pick all that apply.)

- [x] `## h2` is both a section heading and a slide break.
- [x] `[^name]` creates a hover/tap definition popover.
- [ ] `{: .datagrid }` must come before the YAML block it wraps.
- [x] The IAL must be on its own line immediately after the block — no blank line.
- [ ] Numbered lists must use sequential numbers or they won't render.
{: .quiz multi="true" }

[^md]: **Markdown** is a lightweight text format that converts to HTML — designed so the plain-text source is readable on its own. This site uses [kramdown](https://kramdown.gettalong.org/), a Ruby variant with extras: footnotes, IAL attribute lists, and task-list checkboxes.

[^pop]: **Footnote popover** — lightcodepedia's extension of kramdown's standard `[^name]` footnote syntax. Instead of jumping to the bottom of the page, the definition appears as a small popup/tooltip right where the reference appears. Works on hover (desktop) and tap (mobile).

[^ial]: **IAL (Inline Attribute List)** — kramdown's `{: .class id="x" key="value" }` syntax. Placed on its own line right after a block, it attaches HTML attributes to that block. Every interactive component on this site is activated this way.

[^marked]: **marked.js** — a fast, lightweight JavaScript Markdown parser (~50 KB). Used here to render the live playground preview entirely in the browser. It handles CommonMark / GitHub-Flavored Markdown but not kramdown-specific extensions like IAL or footnotes.
