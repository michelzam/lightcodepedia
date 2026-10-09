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

### 🎯 Focus — the caret's block, on both sides

Put the caret in a block on the right and that block **pulses** on the left,
so a learner changing a line sees where the change lands. With
`piano="true"` the source pane bands consecutive blocks in two shades and
marks the caret's block in a third; with `numbers="true"` a gutter numbers
the lines. Both off by default, both pure rendering: the text is untouched.

`````
# Sam, volunteer coordinator

Answers families without guessing. Three years at the shelter.

## Skills

- Talks to people
- Reads the data
- Writes the page
`````
{: .mdpad #cv_focus piano="true" numbers="true" rows="10" }

```gherkin
Feature: The caret's block shows on both sides of the pad
  As a learner editing a page
  I want the block I am in to light up in the preview
  So that I see where my change lands before I make it

  Scenario: The caret in a paragraph pulses that paragraph, and the piano marks it
    Given the piano pad above
    :::python
    self.pad: Mdpad = self.page.cv_focus
    :::
    When the caret lands in the second block
    :::python
    self.pad.caret = self.pad.source.index("Three years")
    :::
    Then the preview pulses that block and the piano marks it
    :::python
    assert self.pad.focus == 1, self.pad.focus
    assert self.pad.focused is not None, "nothing pulsed"
    assert "Three years" in self.pad.focused._el.textContent
    keys = self.pad.keys
    assert keys[0].startswith("k0") and keys[1].startswith("k1"), keys
    assert keys[1].endswith(" now") and not keys[0].endswith(" now"), keys
    :::

  Scenario: A heading is found by its words, and the gutter counts the lines
    Given the piano pad above
    :::python
    self.pad: Mdpad = self.page.cv_focus
    :::
    When the caret lands on the Skills heading
    :::python
    self.pad.caret = self.pad.source.index("## Skills") + 3
    :::
    Then the pulse is on that heading
    :::python
    assert self.pad.focus == 2, self.pad.focus
    assert self.pad.focused._el.tagName.lower() == "h2", self.pad.focused._el.tagName
    assert self.pad.focused._el.textContent.strip() == "Skills"
    :::
    And the gutter numbers every source line once
    :::python
    n = len(self.pad.source.split("\n"))
    assert self.pad.numbers == list(range(1, n + 1)), self.pad.numbers
    :::
```
{: .feature #focus_proof tags="ui" visible="true" status="passing" }

### 🎞 Replay — watch the document grow

A pad saved to the bench keeps every version (🕘). **🎞 Replay** plays them
as frames: the lesson's starter first, then each save in order. The source
pane becomes a **diff pane** with the usual cues — `+` green where a line
came, `−` red where one went, the signs in a gutter so a copied selection is
clean text — the block that changed pulses in the preview,
and a slider is the cursor. ▶ plays forward, ◀ plays backward (the
moonwalk), `replay="0.8"` sets the seconds per frame. Read-only: nothing is
written, and ■ Stop puts the editor back exactly as it was. The button sits
at the head of the **🕘 Versions** list — one place for the history — and
every row of that list can be clicked to show that one version the same
way; the list follows the replay, lighting the row of the frame on screen.
Folding the list stops the replay. While it plays, the pad keeps the size it
had — on a phone at most a screen's worth — and the preview scrolls to the
change rather than growing with the frame. It needs a connected bench, so it
shows here only with your key.

### 🔧 Knobs

| Attribute | What it does |
|---|---|
| `rows="14"` | Editor height in text rows (default 12) |
| `piano="true"` | The **piano**: consecutive blocks banded in two shades of the source pane, the caret's block in a third — see *Focus* below |
| `numbers="true"` | A line number per source line in a gutter; wrapped lines keep one number. Off by default |
| `replay="1.5"` | Seconds per frame when 🎞 **Replay** plays the saved versions (default 1.5). The button sits at the head of 🕘 **Versions**; any row of that list, clicked, shows that version |
| `comment="true"` | 💾 **Save…** asks for one line — what you just did — and the line names the version in 🕘 Versions. An empty line keeps nothing |
| `save="true"` | Adds a 💾 **Save** button that commits the block straight back to the page source — no x-ray, no page editor |
| `save="cv.md"` | The **two-repo contract**: the fence stays the author's seed; the reader's copy persists in *their own* connected repo — relative lands beside the lesson, `/my/cv.md` at the bench root — see below |
| `decorations="true"` | The preview renders the way the site does: block decorations apply and component fences come alive — see below |
| `save="<path>"` **+** `decorations="true"` | An **app screen**: the pad is a page of the learner's own app, so the preview wears app chrome — a title bar mirroring the page's `#` line (the file's name until there is one) |
| `layout="rows"` | Preview **above** the source instead of beside it — for a landscape document (a story in colour) that half a pane would squeeze. Default: side by side |
| `#id` | Optional — names the pad for X-ray |

**About `save="true"`:** the button appears only when a save could actually work — you are connected, the page has a source file, and that source is not read-only. Otherwise it is disabled and says which of the three is missing, rather than failing after the click. It writes through the same path the x-ray **Keep** uses, so a block is committed one way, not two.

**About `save="<path>"` — same page, two repos:** a course page can carry the author's material *and* a place for the reader's work, stored apart. The fence text is only the **starter**; the first 💾 creates the file in the reader's own repo, and from then on the pad opens with *their* text (marked "✓ yours"). **↺ Start over** brings the starter back on screen — the saved file survives until the next 💾. Because seed and saved copy are different files in different repos, the author can republish the page forever and never touch anyone's work; there is exactly one writer per file, so conflicts cannot exist.

**🕘 Versions — the history is already there.** Every 💾 is a commit in the reader's own repo, so a saved pad can show its whole past: **🕘 Versions** lists each save, **compare** diffs it against what the pad holds now (added lines green, removed red), and **bring back** drops an older draft into the editor. Restoring is not a rollback — the next 💾 is simply another commit, so nothing is ever lost. The button appears once a file exists to have a history. The **first** 💾 keeps the author's starter as a version first — labelled *the lesson's starter*, never passed off as your own draft — so your opening change has a before.

**The spelling picks the shelf.** A relative path (`cv.md`, `../shared/notes.md`) resolves against the *lesson's own folder* — the full course path, so the reader's bench mirrors the course tree and two courses never collide, and a teacher browsing a bench finds each contribution beside the lesson that produced it. A leading slash (`/my/cv.md`) means the bench root — for the personal files that outlive one lesson. On a plain site page (no rendered lesson) relative falls back to the root.

**The author's sandbox.** When the connection is the author's own — their source repo, paired by hand in the editor, not a class — every saved copy goes under `__sandbox/` in that repo, same path below it. The author can walk their own lesson, save, repair, and never rewrite the material; the dunder folder never travels, never publishes. A learner's pairing is a bench, so nothing changes for them.

Try it — this pad keeps its text at `/my/scratch.md` in *your* connected repo (the button explains itself if you aren't connected yet):

````markdown
## My scratch space
Whatever you write here is **yours** — saved in your repo, not this page's.
````
{: .mdpad #my_scratch save="/my/scratch.md" rows="8" }

**Say what you did.** Add `comment="true"` and the button reads **💾 Save…** —
the ellipsis promises a question. One line, *what did you just do?*, and
that line becomes the version's name in 🕘 Versions: a diary of your work
instead of twelve identical saves. An empty line keeps nothing. Buttons that
would do nothing are off: 💾 until something changed, ↺ while the pad already
holds the starter; and 🕘 Versions shows whether it is open.

````markdown
## Diary
Each save, one line about the step you just took.
````
{: .mdpad #my_diary save="/my/diary.md" comment="true" rows="5" }

```gherkin
Feature: A save can carry one line about what was done
  As a learner keeping my pages in my own space
  I want each save to be named by what I just did
  So that my versions read as a diary, not a count

  Scenario: The button promises the question
    Given the diary pad above
    :::python
    self.save: Object = Object._all("[data-lc-id='my_diary'] ~ .lc-mdpad-bar .lc-mdpad-save")[0]
    self.reset: Object = Object._all("[data-lc-id='my_diary'] ~ .lc-mdpad-bar .lc-mdpad-reset")[0]
    :::
    When the pad asks for a comment
    Then the save button reads Save with an ellipsis
    :::python
    assert self.save.text.strip() == "💾 Save…", f"button reads {self.save.text!r}"
    :::
    And start over is off while the pad holds the starter
    :::python
    assert self.reset._el.disabled, "↺ is on, yet the pad holds the lesson's starter"
    :::
```
{: .feature tags="ui" status="pending" }

### 🎨 Decorations — the page, not only the text

By default the preview shows the **text**: headings, bold, lists, inline
*colour*{: .red}. Add `decorations="true"` and it shows the **page** —
every `{: … }` line works as it does on the site. A `{: .red }` under a
paragraph tints it, and a fenced block followed by `{: .pitch }` or
`{: .cards }` turns into the live component. A résumé grows into a page
that pitches its author:

`````markdown
## Ana Diaz
*Data analyst*{: .blue} — Milwaukee

Open to internships from June.
{: .green }

```yaml
who: hiring managers
need: must turn messy spreadsheets into decisions
product: Ana Diaz
category: junior data analyst
benefit: clean data and one chart that answers the question
alternative: a generic résumé
difference: every claim links to a page that runs
```
{: .pitch }

```
### 🐍 Python
pandas, matplotlib, notebooks

### 🛢️ SQL
joins, window functions, PostgreSQL

### 📊 Dashboards
one question, one chart
```
{: .cards cols="3" }

[✉️ Write to Ana](mailto:ana@example.org)
{: .button }
`````
{: .mdpad #cv_deco decorations="true" rows="18" }

Change `product:` to your own name, or break the `{: .cards }` line, and
watch the component leave and come back. The source is painted to match:
a decoration line sits on its own lighter band with the **class** in blue,
the **#id** in pink and each **knob** green-and-orange; a fence and its
body are muted; headings, links and emphasis have their colours. Every pad
paints this way, with or without decorations. The preview waits for a short
pause in your typing before it rebuilds, so a component is not rebuilt
on every key. The pad also reports which components are alive:
`components` lists them by kind.

**Every decoration is a library component.** Nothing is invented for the
pad. Any component's own example, typed into a decorated pad, comes alive.
That is the whole library, proven by the suite:

| for | decorations |
|---|---|
| layout | `.block` `.blocks` `.cards` `.grid` `.accordion` `.carousel` `.scrollable` |
| story | `.pitch` `.persona` `.impact_map` `.event_flow` `.feature` |
| data | `.chart` `.datagrid` `.query` `.record` `.map` `.qr` |
| interaction | `.quiz` `.radio` `.form` `.dropdown` `.menu` `.button` `.run` `.code` `.pytutor` `.agent` `.embed-page` `.prerequisite` `.build_loop` |
| words | `{: .red }` `{: .green }` `{: .blue }`, inline or under a paragraph |

Two have nothing to show in a preview, by design. `.dataset` is data
without a face: it feeds a chart or a grid in the same pad. `.avatar`
belongs to the page, not to a document. A `.prerequisite` gates only the
preview, never the page around the pad.

## 🔌 Wires — and when they break

A decorated pad is a small page: a dataset feeds a grid through
`source=`, a form follows a grid through `master=`, an agent reads an
editor through `bound=`. Those are wires, and the preview draws them
honestly. Delete the dataset fence below, or rename its id, and watch:

`````markdown
```
name,legs
Rex,4
Tweety,2
```
{: .dataset #pets }

[Pets](#)
{: .datagrid source="pets" }
`````
{: .mdpad #wires_pad decorations="true" rows="10" }

The preview's model is what the text declares, nothing more: a dataset the
pad no longer writes leaves the page's registry with the render — no save,
no reload. A wire to an id the page does not have is drawn as such: the
block wears a dashed frame naming the missing id, and one chip over the
preview counts them. Save stays what it is, persistence.

```gherkin
Feature: A wire to nothing is drawn broken
  As a learner wiring a grid to a dataset
  I want a deleted or renamed id to break visibly, at once
  So that I fix the wire instead of trusting rows that are no longer there

  Scenario: The dataset fence is deleted — the grid loses its rows and names the missing id
    Given the wires pad, whole
    :::python
    self.pad: Mdpad = self.page.wires_pad
    self.was = self.pad.source
    assert self.pad.broken == [], self.pad.broken
    :::
    When the dataset fence is deleted from the pad
    :::python
    self.pad.source = "[Pets](#)\n{: .datagrid source=\"pets\" }"
    :::
    Then the registry no longer holds the dataset
    :::python
    assert "pets" not in [str(k) for k in js.Object.keys(js.window.lcDatasets)], "pets survived its fence"
    :::
    And the grid's block is drawn broken, naming the source
    :::python
    assert self.pad.broken == ["source «pets»"], self.pad.broken
    :::

  Scenario: beside= works in the pad, and the caret still finds its block
    Given the wires pad, whole, with a chart beside the grid
    :::python
    self.pad: Mdpad = self.page.wires_pad
    self.pad.source = self.was
    self.pad.source = self.was + '\n\n[Legs](#)\n{: .chart source="pets" type="bar" x="name" y="legs" beside="true" }'
    :::
    Then the grid and the chart share one row, and no wire is broken
    :::python
    rows = Object._all('[data-lc-id="wires_pad"] .lc-blocks[data-lc-beside]')
    assert len(rows) == 1 and int(rows[0]._el.children.length) == 2, len(rows)
    assert self.pad.broken == [], self.pad.broken
    :::
    And the caret on the chart's line lights the chart, not the grid
    :::python
    self.pad.caret = len(self.pad.source) - 1
    lit = Object._all('[data-lc-id="wires_pad"] .lc-mdpad-focus')
    assert len(lit) == 1, len(lit)
    el = lit[0]._el
    assert el.parentNode.hasAttribute("data-lc-beside"), "the focus missed the row"
    assert el.isSameNode(el.parentNode.lastElementChild), "the focus lit the grid, not the chart"
    self.pad.source = self.was
    :::

  Scenario: The id is renamed — the old wire breaks on the spot
    Given the wires pad, whole again
    :::python
    self.pad: Mdpad = self.page.wires_pad
    self.pad.source = self.was
    assert self.pad.broken == [], self.pad.broken
    :::
    When the dataset is renamed and the grid is not
    :::python
    self.pad.source = self.was.replace("#pets", "#cats")
    :::
    Then the wire to the old id is broken
    :::python
    assert self.pad.broken == ["source «pets»"], self.pad.broken
    :::
    And wiring the grid to the new id mends it
    :::python
    self.pad.source = self.was.replace("#pets", "#cats").replace('source="pets"', 'source="cats"')
    assert self.pad.broken == [], self.pad.broken
    self.pad.source = self.was
    :::
```
{: .feature tags="code" status="passing" }

```gherkin
Feature: Decorations turn the pad's preview into a page
  As a learner writing my résumé
  I want my decorations to show in the preview as on the site
  So that my résumé can carry a pitch and cards, not only text

  Scenario: Block decorations and components render in the preview
    Given the résumé pad
    :::python
    self.pad: Mdpad = self.page.cv_deco
    :::
    When the preview has rendered the page
    Then the pitch and the cards are live components
    :::python
    assert "pitch" in self.pad.components, self.pad.components
    assert "cards" in self.pad.components, self.pad.components
    :::
    And the decoration lines are not left as text
    :::python
    assert "{:" not in self.pad.rendered, "a {: } line leaked into the preview"
    :::
    And a plain link-button counts as a component too
    :::python
    assert "button" in self.pad.components, \
        "a {: .button } under a link is the learner's first part — it must be listed"
    :::

  Scenario: The source is painted to match the components
    Given the résumé pad
    :::python
    self.pad: Mdpad = self.page.cv_deco
    :::
    Then each decoration line wears its band, with the class and the knobs coloured
    :::python
    assert ".pitch" in self.pad.painted("cls") and ".cards" in self.pad.painted("cls"), self.pad.painted("cls")
    assert "cols" in self.pad.painted("key"), self.pad.painted("key")
    assert len(self.pad.painted("ial")) >= 3, self.pad.painted("ial")
    :::
    And the fences are muted and the heading has its colour
    :::python
    assert any(f.startswith("```") for f in self.pad.painted("fence")), self.pad.painted("fence")
    assert any("Ana Diaz" in h for h in self.pad.painted("h")), self.pad.painted("h")
    :::

  Scenario: A plain pad still previews text only
    Given the playground pad
    :::python
    self.pad: Mdpad = self.page.playground
    :::
    Then it raises no components
    :::python
    assert self.pad.components == [], self.pad.components
    :::
```
{: .feature tags="code" status="passing" }

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

> Common confusion: learners use `###` expecting it to create a new slide.
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

Use a plain markdown table for ≤10 static rows. Use `{: .datagrid }` when learners need to sort, filter, or scroll through many rows — see [📊 Datagrid](/components/datagrid).

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

[^marked]: **marked.js** — a fast, lightweight JavaScript Markdown parser (~50 KB). It renders the live preview entirely in the browser. On its own it knows CommonMark / GitHub-Flavored Markdown, not kramdown's extras, so the pad adds the IAL part itself: inline colours like `*word*{: .red}` always, and with `decorations="true"` every `{: … }` line, components included. Footnotes are not rendered in the pad's preview.

```yaml
bot: doc
face:
  zoom: 1.2
script: []
stories:
  make a tour, select components and describe them:
    - 'You might wonder: make a tour, select components and describe them'
    - at: playground
      say: >-
        This live markdown pad lets you edit syntax on the right and see instant rendered preview
        updates on the left.
    - at: my_scratch
      say: >-
        This editor demonstrates personal persistence by saving your work directly into your own
        connected repository.
```
{: .avatar #guide dock="true" size="115" }
