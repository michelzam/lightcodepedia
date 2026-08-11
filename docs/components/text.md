# ✍️ Text

Every page on this site is a plain text file written in Markdown[^md] — the lightweight format that turns `**bold**` into **bold** and `## Heading` into a big header. This page is your cheat sheet and playground.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

There's one lightcodepedia twist: any `[^footnote]` reference becomes a hover/tap popover[^pop]. Try hovering the blue numbers above.

**Where definitions live:** anywhere on the page — the natural home is
**collected at the end of the file**, even when the references sit inside
block fences or embedded fragments. The page settles everything into ONE
list with a single, reading-order numbering (no restarting at 1 per block),
rendered where the definitions were authored, with no injected title — add
your own heading if you want one. The same concept slug defined twice
collapses into one entry (first definition wins).

## ✏️ Try it live — edit and see

Read the result on the **left**, type the markdown on the **right** — instantly, as you type. The rendered page is what you are making, so it takes the reading position; the source sits beside it.

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
{: .mdpad #playground rows="16" }

Try changing `**Bold**` to `**Loud**`. Add a new bullet. Break a table row. The preview updates on every keystroke — no server, just JavaScript[^marked] in the browser.

### 🔧 Knobs

| Attribute | What it does |
|---|---|
| `rows="14"` | Editor height in text rows (default 12) |
| `save="true"` | Adds a 💾 **Save** button that commits the block straight back to the page source — no x-ray, no page editor |
| `save="cv.md"` | The **two-repo contract**: the fence stays the author's seed; the reader's copy persists in *their own* connected repo — relative lands beside the lesson, `/my/cv.md` at the bench root — see below |
| `#id` | Optional — names the pad for X-ray |

**About `save="true"`:** the button appears only when a save could actually work — you are connected, the page has a source file, and that source is not read-only. Otherwise it is disabled and says which of the three is missing, rather than failing after the click. It writes through the same path the x-ray **Keep** uses, so a block is committed one way, not two.

**About `save="<path>"` — same page, two repos:** a course page can carry the author's material *and* a place for the reader's work, stored apart. The fence text is only the **starter**; the first 💾 creates the file in the reader's own repo, and from then on the pad opens with *their* text (marked "✓ yours"). **↺ Start over** brings the starter back on screen — the saved file survives until the next 💾. Because seed and saved copy are different files in different repos, the author can republish the page forever and never touch anyone's work; there is exactly one writer per file, so conflicts cannot exist.

**🕘 Versions — the history is already there.** Every 💾 is a commit in the reader's own repo, so a saved pad can show its whole past: **🕘 Versions** lists each save, **compare** diffs it against what the pad holds now (added lines green, removed red), and **bring back** drops an older draft into the editor. Restoring is not a rollback — the next 💾 is simply another commit, so nothing is ever lost. The button appears once a file exists to have a history. The **first** 💾 keeps the author's starter as a version first — labelled *the lesson's starter*, never passed off as your own draft — so your opening change has a before.

**The spelling picks the shelf.** A relative path (`cv.md`, `../shared/notes.md`) resolves against the *lesson's own folder* — the full course path, so the reader's bench mirrors the course tree and two courses never collide, and a teacher browsing a bench finds each contribution beside the lesson that produced it. A leading slash (`/my/cv.md`) means the bench root — for the personal files that outlive one lesson. On a plain site page (no rendered lesson) relative falls back to the root.

Try it — this pad keeps its text at `/my/scratch.md` in *your* connected repo (the button explains itself if you aren't connected yet):

````markdown
## My scratch space
Whatever you write here is **yours** — saved in your repo, not this page's.
````
{: .mdpad #my_scratch save="/my/scratch.md" rows="8" }

### 📏 Ask the pad questions

Give the pad an `#id` and a `.feature` on the same page can **grade what the
learner typed** — the preview is the document being made, and these read it:

| Property | What it answers |
|---|---|
| `rendered` | all the preview's text, one string |
| `source` | what the learner actually typed — for criteria about *how* the markdown is written |

A named pad also **publishes** `{source}` as a live cell scope: `{=cv1.source}` in prose, in a `visible=` gate, or wired into an agent via `bound="{=cv1.source}"` — always the current text, debounced.
| `titles` | the `#` lines (a page opens with exactly one) |
| `sections` | the `##` lines — the real structure |
| `bolds` | every **bold** phrase |
| `italics` | every *italic* phrase |
| `bullets` | every bulleted (unordered) list item |
| `numbered` | every numbered (ordered) list item — where rank matters |
| `links` | every link's text |
| `images` | how many images made it in |

Plus `this_year()` — the year on the reader's own clock, so a rubric can
demand a date *from the future* without any code in the page. Together they
turn acceptance criteria into a self-grading rubric: seed the pad red,
let the learner type it green.

```gherkin
Feature: A markdown block becomes a live editor and preview
  As a lowcoder
  I want to type markdown and see it render as I type
  So that I can learn and draft with instant feedback

  Scenario: The block upgrades into a live preview pad
    Given the live editor above
    :::python
    self.pad: Mdpad = self.page.playground
    :::
    When the page has upgraded it
    Then it is a visible editor and preview
    :::python
    assert self.pad.visible
    :::

  Scenario: The pad answers questions about the document being made
    Given the same live editor
    :::python
    self.pad: Mdpad = self.page.playground
    :::
    When a rubric reads its preview
    Then structure, emphasis, lists and links are all countable
    :::python
    assert "Hello, Markdown!" in self.pad.sections, self.pad.sections
    assert any("Bold" in b for b in self.pad.bolds), self.pad.bolds
    assert any("italic" in i for i in self.pad.italics), self.pad.italics
    assert len(self.pad.bullets) >= 3, len(self.pad.bullets)
    assert len(self.pad.numbered) >= 3, len(self.pad.numbered)
    assert self.pad.source.count("1. Step") >= 3, "the demo numbers lazily - all 1."
    assert len(self.pad.links) >= 1, self.pad.links
    assert self.pad.images == 0, self.pad.images
    assert this_year() >= 2026, this_year()
    :::
```
{: .feature tags="code" status="passing" }

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

"Themeable" is literal: the site's text, link and border colours are named
**tokens** defined once, and the **👁️ High contrast** toggle (bottom-left
pill → Display) swaps that one palette site-wide — every page, every
component, your colour classes included. Author with classes and the theme
does the rest; hardcode a hex and you've opted that word out of it.

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
> "Wait — it showed me the definition without a page jump?" — discover it for yourself.
{: .speaker-note }

## ⚙️ IAL — the power move

The pattern you'll see most often after plain markdown is the **IAL[^ial]**: a `{: ... }` line right after any block that attaches attributes (classes, ids, key-value pairs) to it. This is how every component on this site gets activated.

````markdown
```yaml
- name: Lucky
- name: Wanda
```
{: .datagrid #dogs }
````

Then `{: .form bound="dogs" }` on another block binds a form to that grid. The `.datagrid`, `.form`, `.run`, `.quiz`, `.agent` — all IAL.

**Rules:**
- Must be on its own line, immediately after the block (no blank line between).
- Multiple classes: `{: .class1 .class2 }`.
- Mix classes and key-value pairs: `{: .run #demo rows="4" }`.

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

[^ial]: **IAL (Inline Attribute List)** — kramdown's `{: .class #x key="value" }` syntax. Placed on its own line right after a block, it attaches HTML attributes to that block. Every interactive component on this site is activated this way.

[^marked]: **marked.js** — a fast, lightweight JavaScript Markdown parser (~50 KB). Used here to render the live playground preview entirely in the browser. It handles CommonMark / GitHub-Flavored Markdown but not kramdown-specific extensions like IAL or footnotes.
