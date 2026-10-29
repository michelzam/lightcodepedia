# ✍️ Pad

The pad is where a learner **builds**: Markdown on one side, the living
page on the other, updated as they type. Seed it with a fence; what they
write is theirs. Markdown itself — headings, lists, tables, footnotes —
is on the [✍️ Text](text) page, with its own playground.

## 👀 See it in action

````markdown
## 🐾 My first page

A **sentence** with *style*, and a list:

- one thing
- another

```csv
name,age
Rex,3
Luna,5
```
{: .dataset #my_pets }

[the pets](#)
{: .datagrid source="my_pets" }
````
{: .mdpad #pad_demo rows="14" decorations="true" }

Change a name, add a row to the list: the grid follows. With
`decorations="true"` the preview is the site's own pipeline — a dataset,
a grid, a chart, a class come alive as they would on a published page.

```gherkin
Feature: The pad renders what is typed
  As a learner
  I want to see my page as I write it
  So that syntax is never the blocker

  Scenario: The seed renders, and a component in it is alive
    Given the pad above
    :::python
    self.pad: Mdpad = self.page.pad_demo
    :::
    When I read its preview
    :::python
    self.rows: int = self.page.my_pets.count
    :::
    Then the dataset in it has its rows
    :::python
    assert self.rows == 2, f"{self.rows} rows, the seed holds 2"
    :::
```
{: .feature #pad_proof visible="true" status="pending" tags="pad" }

## 🧰 What a pad does

- **Yours, in your bench.** `save="cv.md"` makes the fence the author's
  seed and the learner's copy a file in their own repo: 💾 commits it, ↺
  restores the seed, and the author republishes the lesson forever without
  touching anyone's work. `save="/my/…"` for files that outlive one lesson.
- **A diary of versions.** `comment="true"` asks one line at 💾 — *what
  did you just do?* — and 🕘 Versions lists them; any row shows that
  version, read-only.
- **Time travel.** 🎞 Replay plays the saved versions forward (▶) and
  backward (◀ Moonwalk): added lines unfold, removed ones fold, the
  changed component pulses in the preview, and the version's own words
  float as a caption. `replay="1.5"` sets the pace.
- **The source, painted.** A fence and its body muted, a decoration on
  its own band — class, `#id` and knobs in their colours — line numbers
  and a component icon in the gutter (`numbers="true"`), blocks banded
  like a piano (`piano="true"`).
- **Errors in the gutter.** A fence that never closes, a decoration
  without its `}`, a Python fence that does not compile: ⚠ on the line, one
  sentence under the pad.
- **Type hints, checked.** `mypy="true"` lets Dr. mypy (lite) read every
  Python fence too — a `def` without its hints, a `return` or a literal
  argument against them — ⚠ on the line in mypy's own words, as the
  [🐍 runner](run)'s 🩺 Dr. mypy says them. `"loose"` forgives a missing
  hint and checks only the ones written.

````markdown
## 🐶 A typed pet

```python
class Pet:
    def __init__(self, name: str) -> None:
        self.name = name

    def greet(self):
        return f"Hello, I am {self.name}!"
```
````
{: .mdpad #typed_pad mypy="true" numbers="true" rows="10" }

  `greet` gives back a `str` and does not say so: line 8 wears the ⚠.
  Type `-> str` before its colon and the ⚠ goes.
- **Examples, run as you write.** `doctest="true"`: every Python fence
  runs its own `>>>` examples — no `if __name__ == "__main__":`, no
  `doctest.testmod()` — and a failing one wears ⚠ on its `>>>` line:
  *got 0, expected 2*. A fence runs again only when its own text changes.

````markdown
## 🦘 jump

```python
def jump(start: int, leap: int) -> int:
    """
    Makes an absolute jump from start.

    >>> jump(2, 3)
    5
    >>> jump(1, -1)
    2
    """
    return start + leap
```
````
{: .mdpad #doctest_pad doctest="true" mypy="true" numbers="true" rows="14" }

  Line 10 wears the ⚠: `jump(1, -1)` gives `0`. Fix the example (or the
  code) and the gutter clears.
- **Keys and the phone.** ⌘↑/↓ jumps between blocks, ⌥ moves one, ⇥ folds
  the editor away so the preview takes the whole width (✎ brings it back);
  `folded="true"` opens that way. `?` on the pad lists the keys of this
  computer.
- **Invisible parts, shown.** A dataset or a class has no face; with the
  caret in it, a ghost line in the preview says where it sits.
- **Wires that break are drawn broken.** A `source=` or `master=` to an id
  the page no longer has: dashed frame, one chip, and the pad says so.
- **A builder beside it.** An [`.agent`](agent) bound to a pad proposes
  the lines a red proof needs; ⬇ Add puts them in, ▶ runs again.

## 🔧 Knobs

| Attribute | Default | What it does |
|---|---|---|
| `rows="N"` | `12` | editor height in text rows |
| `save="cv.md"` | — | the learner's copy, beside the lesson in their bench; `/my/…` at the bench root |
| `save="here:site.md"` | — | the file on the host that served this page: 💾 writes it there when the host takes saves (`--edit`), the old copy stamped in `__backup/`; 🕘 Versions lists those copies. On a read-only host no 💾 is offered — the bar says “read-only” — and the gear offers nothing on the page |
| `comment="true"` | off | 💾 Save… asks for one line, the version's name |
| `replay="1.5"` | `1.5` | seconds per frame in 🎞 Replay |
| `decorations="true"` | off | the preview runs the site's pipeline: components come alive |
| `piano="true"` | off | blocks banded in two shades, the caret's in a third |
| `numbers="true"` | off | line numbers and component icons in a gutter |
| `doctest="true"` | off | each Python fence runs its own `>>>` examples as you write; a failing one is marked ⚠ on its line |
| `mypy="true"` | off | Dr. mypy (lite) reads the Python fences: missing hints and wrong types, ⚠ on the line (`"loose"`: written hints only) |
| `folded="true"` | off | opens with the editor folded away |
| `layout="below"` | `beside`, side by side | preview above the source |
| `layout="behind"` | `beside`, side by side | one face at a time: the result in front, ✎ brings the source |

## 🔗 Related components & examples

```
/components/text
/components/agent
/components/dataset
```
{: .related }

## 🎯 Focus — the caret's block, on both sides

Put the caret in a block on the right and that block **pulses** on the left,
so a learner changing a line sees where the change lands. With
`piano="true"` the source pane bands consecutive blocks in two shades and
marks the caret's block in a third; with `numbers="true"` a gutter numbers
the lines, and a decoration's line wears its component's icon there — 🛢️
beside `{: .dataset }`, ▦ beside `{: .datagrid }`. Both off by default, both pure rendering: the text is untouched.

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

## 🎞 Replay — watch the document grow

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

## 🔧 Knobs

| Attribute | What it does |
|---|---|
| `rows="14"` | Editor height in text rows (default 12) |
| `piano="true"` | The **piano**: consecutive blocks banded in two shades of the source pane, the caret's block in a third — see *Focus* below |
| `numbers="true"` | A line number per source line in a gutter; wrapped lines keep one number; a decoration's line also shows its component's icon. Off by default |
| `replay="1.5"` | Seconds per frame when 🎞 **Replay** plays the saved versions (default 1.5). The button sits at the head of 🕘 **Versions**; any row of that list, clicked, shows that version |
| `comment="true"` | 💾 **Save…** asks for one line — what you just did — and the line names the version in 🕘 Versions. An empty line keeps nothing |
| `save="true"` | Adds a 💾 **Save** button that commits the block straight back to the page source — no x-ray, no page editor |
| `save="cv.md"` | The **two-repo contract**: the fence stays the author's seed; the reader's copy persists in *their own* connected repo — relative lands beside the lesson, `/my/cv.md` at the bench root — see below |
| `decorations="true"` | The preview renders the way the site does: block decorations apply and component fences come alive — see below |
| `save="<path>"` **+** `decorations="true"` | An **app screen**: the pad is a page of the learner's own app, so the preview wears app chrome — a title bar mirroring the page's `#` line (the file's name until there is one) |
| `layout="below"` | Preview **above** the source instead of beside it — for a landscape document (a story in colour) that half a pane would squeeze. Default: `beside`, side by side |
| `layout="behind"` | One face at a time: the result in front, **✎** brings the source, **👁** the result again — a phone's way |
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

## 🕘 Versions, ↺ Start over, 🔍 Find

**🕘 Versions** lists every version the pad kept, the lesson's starter
first of all; its head carries 🎞 Replay and **↺ Start over** (the
starter back in the editor — your saved copy stays until you 💾 again).
**🔍** at the editor's corner, or ⌘F / Ctrl+F in it, floats a finder:
every match glows, ↑ ↓ (or Enter, ⇧Enter) walk them, Esc leaves the
caret on the one you were on.

**The text as a program.** In the editor, the wires are live:

| key | what it does |
|---|---|
| ⌘-click (Ctrl-click) on a wire | jumps to its `#id`; on the `#id`, walks its uses one by one |
| F2 on a wire | renames the id everywhere it is wired — `#id`, `source="id"`, `FROM id`, `{= id… }` — prose untouched, one ⌘Z |
| ⌥↑ / ⌥↓ | moves the block under the caret past its neighbour — words and decoration together |
| ⌃⌥→ / ⌃⌥↑ / ⌃⌥← | puts the block beside the one above (`layout="beside"`), behind it as a tab (`layout="behind"`), or back below it |
| Tab / ⇧Tab | outside a fence, the next (or previous) thing you can change — a part's title, its class, its `#id`, each knob's value; a value or a class opens its pick list. Inside a fence, Tab indents (two spaces in yaml). Esc, then Tab, leaves the editor |
| Ctrl+Space | completes what fits the caret: a component after `{: .`, a knob, a knob's value (a `source=` offers the pad's datasets, an `x=` the source's columns); on an empty line, a whole part from the course's catalogue — Tab then jumps over its blanks |

The editor's corner carries small pills: **?** lists all of this, **🔍**
(while you edit) finds, **⇥** hides the editor and **✎** brings it back —
Doc says `fold` and `show`. The caret in a part the page does not show (a
dataset, a query) draws a dashed line in the preview where it sits:
*🛢️ Dataset (invisible)*.

A proof can read how the work was kept: `pad.versions` — the names of
the versions kept, newest first; `pad.replayed` — how many times its
film was played.

## 🎨 Decorations — the page, not only the text

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
```csv
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

  Scenario: layout="beside" works in the pad, and the caret still finds its block
    Given the wires pad, whole, with a chart beside the grid
    :::python
    self.pad: Mdpad = self.page.wires_pad
    self.pad.source = self.was
    self.pad.source = self.was + '\n\n```sql\nSELECT name, legs FROM pets WHERE legs > 0\n```\n{: .query bind="pets" #walkers }\n\n[Legs](#)\n{: .chart source="walkers" type="bar" x="name" y="legs" layout="beside" }'
    :::
    Then the grid and the chart share one row — the faceless query between them rides along — and no wire is broken
    :::python
    rows = Object._all('[data-lc-id="wires_pad"] .lc-blocks[data-lc-beside]')
    assert len(rows) == 1 and int(rows[0]._el.children.length) == 3, len(rows)
    assert str(rows[0]._el.style.gridTemplateColumns) == "repeat(2, 1fr)", str(rows[0]._el.style.gridTemplateColumns)
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
    Given the scratch pad, which has no decorations
    :::python
    self.pad: Mdpad = self.page.my_scratch
    :::
    Then it raises no components
    :::python
    assert self.pad.components == [], self.pad.components
    :::
```
{: .feature tags="code" status="passing" }

## 📏 Ask the pad questions

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

The playground these proofs read — the Text page's own, with no decorations:

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
{: .mdpad #playground rows="12" }

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

  Scenario: ✎ Hide folds the editor away, and the preview takes the whole width
    Given the playground pad, editor shown
    :::python
    self.pad: Mdpad = self.page.playground
    self.pad.unfold()
    self.before: float = float(self.pad._el.querySelector(".lc-mdpad-out").getBoundingClientRect().width)
    :::
    When the editor is folded
    :::python
    self.pad.fold()
    :::
    Then the preview is wider and the source is gone from view
    :::python
    assert self.pad.folded, "not folded"
    after: float = float(self.pad._el.querySelector(".lc-mdpad-out").getBoundingClientRect().width)
    assert after > self.before, f"preview {after} not wider than {self.before}"
    assert self.pad._el.querySelector(".lc-mdpad-src").offsetParent is None, "the source is still shown"
    :::
    And ✎ Edit brings the editor back
    :::python
    self.pad.unfold()
    assert not self.pad.folded, "still folded"
    assert self.pad._el.querySelector(".lc-mdpad-src").offsetParent is not None, "the source did not come back"
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
