# ✍️ Text — Markdown basics

Every page on this site is just markdown[^md]. This page is your reference: the handful of symbols you'll use 95 % of the time, plus the lightcodepedia twist on footnotes that turns definitions into hover-popovers (try hovering or tapping any little blue number you see — like the one right after "markdown" up there).

## Headings

Three levels you'll actually use, with a side effect specific to this site:

- `# Title` — the page's `h1`, shown big with a blue underline.
- `## Section` — `h2`, also a slide break in 📽️ slides mode[^slides].
- `### Sub-section` — `h3`, just smaller. Not a slide break.

Source:

```markdown
# Page title

## A section

### A sub-section
```

## Emphasis & inline marks

- `*italic*` → *italic*
- `**bold**` → **bold**
- `` `inline code` `` → `inline code`
- `~~strikethrough~~` → ~~strikethrough~~
- `> quote` → blockquote (see below)

## Lists

Bullets — any of `-`, `*`, `+` start one:

```markdown
- first
- second
- third
```

Numbered — actual numbers don't matter, kramdown renumbers:

```markdown
1. step one
1. step two
1. step three
```

Two-level nesting is OK; deeper gets cramped in slides mode.

## Links

```markdown
[label](https://example.com)        external
[label](datagrid)                    another page on this site
[label](#section-id)                 anchor within this page
```

## Code blocks

Three backticks, a language, the code, three backticks:

````markdown
```python
print("hello")
```
````

Highlighting is automatic; languages we use a lot: `python`, `yaml`, `json`, `markdown`, `liquid`.

To make the block **live** (Python you can run), add the `.run` IAL[^ial] on the next line:

```python
print("hello, lightcodepedia")
```
{: .run rows="2" }

That's all it takes. See [Run](/components/run) for the full story.

## Tables

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

Alignment with `:---`, `:---:`, `---:` in the separator row.

## Blockquotes

```markdown
> A blockquote is just one or more lines starting with `> `.
> Useful for asides and pulled phrases.
```

> A blockquote is just one or more lines starting with `> `.
> Useful for asides and pulled phrases.

## Footnotes — and the popover trick

This is the killer feature for tutorials. Kramdown gives you footnotes for free:

```markdown
The slides engine reads each kramdown IAL[^ial] on the page.

[^ial]: **Inline Attribute List** — kramdown syntax that attaches
        attributes to the *preceding* block, e.g. `{: .datagrid }`.
```

Without any extra work, lightcodepedia turns the little number link into a **hover/tap popover** containing the full footnote — so readers see the definition right where the term appears, without losing their spot. The actual "Definitions" section still appears at the bottom of the page for printing and for the "list of all terms" use case.

**How to write a footnote:**
1. Put `[^anyname]` right after the term in your prose. No spaces.
2. Put `[^anyname]: the definition` somewhere later (convention: at the bottom of the page).
3. The definition can include **bold**, *italic*, `code`, lists, links — full markdown.
4. The same `[^anyname]` can appear multiple times in the page; one definition serves all of them.

**Best practice for definitions:**
- Lead with `**Term**` then an em-dash, then the explanation.
- Keep it to 1–3 sentences. The popover is small.
- If you need a paragraph, write a paragraph; kramdown handles multi-line footnotes by indenting continuation lines.

## kramdown IAL — applying attributes

The pattern you'll see most after plain markdown is the IAL[^ial]: a `{: ... }` line right after a block to attach attributes (an id, classes, key-value pairs) to it. This is what activates every component on the site:

```markdown
```yaml
- name: Lucky
- name: Wanda
```
{: .datagrid id="dogs" }
```

Then `{: .form bound="dogs" }` on another block binds a form to that grid. See [Datagrid](/components/datagrid) and [Form](/components/form) for the full menu of attributes.

## Comments — for student-builder eyes only

`<!-- like this -->` HTML comments work and aren't rendered. Kramdown also has its own `{::comment} ... {:/}` syntax. Use either to leave notes for your future self without cluttering the page.

## Cheat sheet

| You write       | You get                                |
|-----------------|----------------------------------------|
| `# T`           | big `h1` with blue underline           |
| `## S`          | `h2`, also a slide break               |
| `### s`        | `h3`                                   |
| `*x*` / `_x_`   | *italic*                               |
| `**x**`         | **bold**                               |
| `` `x` ``       | inline `code`                          |
| `[t](url)`      | link                                   |
| `![alt](url)`   | image                                  |
| `> q`           | blockquote                             |
| `- / 1.`        | list                                   |
| ```` ```py ```` | fenced code (python)                   |
| `{: .class }`   | IAL — attach attributes to block above |
| `[^x] / [^x]:`  | footnote ref + definition (popover)    |

---

[^md]: **Markdown** is a lightweight text format that converts to HTML — designed so the source itself stays human-readable. Lightcodepedia uses [kramdown](https://kramdown.gettalong.org/), a variant with extras like footnotes and the IAL.

[^slides]: **Slides** — every page on this site can be presented as a deck by clicking the 📽️ button at the bottom-left. `## h2` headings become slide breaks; bullets fragment. See [Slides](/components/slides).

[^ial]: **Inline Attribute List** — kramdown's `{: .class id="x" key="value" }` syntax, placed on its own line right after a block, attaches HTML attributes to that preceding block. The site's components (run, datagrid, form, slides) are all activated this way.

{% include backtotop.md %}
