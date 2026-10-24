# 🧱 Block

Wrap content in a bordered card. Use `cols` to place multiple blocks side by side.🧪

**The rule:** one fenced block, one IAL tag. `### Headings` inside divide it into multiple blocks.

## Syntax

Single block:

````markdown
```
### Optional title
Text, images, lists — any markdown.
```
{: .block }
````

Multiple blocks side by side:

````markdown
```
### Left title
Content on the left.

### Right title
Content on the right.
```
{: .blocks cols="2" }
````

## Options

| Attribute | Default | Description |
|-----------|---------|-------------|
| `cols` | `1` | Number of side-by-side columns — or their **proportions**: `cols="2;1"` gives two columns, the first twice as wide as the second. `;` `:` `,` or a space all separate |
| `tone` | *(none)* | The register the card belongs to: `paper` the course talking · `app` the app the learner acts in · `tool` the course's own scaffolding. Three values, no others — an unknown word keeps the plain card |
| `title` | *(none)* | **Turns the card into an app window** — three dots and the title in a bar, the same chrome an embedded runner wears. Give it to content the learner *acts in*; leave it off and you keep the plain card |
{: .wide_first }


## Notes

- Without `### headings` the entire content becomes one block.
- `.block` is shorthand for `.blocks cols="1"` — same component.
- Nested components work inside blocks: `{: .video }`, `{: .quiz }`, `{: .run }`, `{: .button }`.
- On small screens columns collapse to a single column automatically.
- `layout="beside"` on any part's decoration draws it next to the block above — the same row, without a fence to nest; `layout="behind"` puts it behind, as a tab (see below). `below` is the default, never written.

## 🖥 `title=` — the card becomes an app window

A block with a `title=` stops being a card and becomes a **window**: three
dots, the title in a bar. It is the one look that says *you are in an app
now* — the same chrome an embedded [runner](/components/runner) wears, so a
learner reads it the same whether the app is another file or written right
here.

````markdown
```
[Say it](#)
{: .button #hello_btn }
```
{: .block title="Say hello" }
````

The rule is that simple: **`title=` present → window; absent → card.** Nothing
else switches it, and no other component is needed to frame an inline app.

````
### 🐕 Walk Lucky
Lucky is waiting. Press the button.

[🦴 Give a treat](#)
{: .button #treat_btn }
```python
treat = "Lucky wags his tail. 🐕"
```
{: .onclick }

{=treat}
````
{: .block title="Lucky's day" }

> `tone=` is a different question — it says which **register** a card belongs
> to (paper, app, tool), not what it *is*. A window already says "app" out
> loud, so it needs no tone beside it.
{: .speaker-note }

**Q:** You wrote a form and a button inside a fenced block and want it to read as an app. What do you add?

- [x] `title="…"` — the block becomes a window
- [ ] `{: .runner }` — that renders another file, and needs a `src=`
- [ ] `frame="app"`
- [ ] Nothing; any block is already an app window
{: .quiz }

## Example — single block

```
### 🐕 Meet Lucky
![Lucky](/assets/lab.jpg)

This is **Lucky** — a three-year-old Lab who loves parks, tennis balls, and long naps.💤
```
{: .block }

```gherkin
Feature: A fenced block becomes a bordered card
  As a lowcoder
  I want content wrapped in a card, optionally side by side
  So that I can lay out blocks with no HTML or CSS

  Scenario: Each section becomes a block card
    Given the block examples on this page
    :::python
    self.cells: list = Object._all(".lc-block")
    :::
    When they have rendered
    Then there are block cards and one holds Lucky's profile
    :::python
    assert len(self.cells) >= 2, len(self.cells)
    assert any("Lucky" in c.text for c in self.cells), [c.text[:30] for c in self.cells]
    :::
```
{: .feature tags="ui" status="passing" }

## Example — two blocks side by side

```
### 🐕 About Lucky
- **Breed:** Beagle
- **Age:** 3 years
- **Top speed:** 40 km/h
- **Personality:** curious, friendly, easily distracted by smells

### 🎯 What blocks can hold
- Text and **markdown**
- Images
- Lists and links
- Nested `.video`, `.quiz`, `.run`
```
{: .blocks cols="2" }

## ↔️ `layout=` — beside the one above, or behind it, no fence to nest

Any part can take `layout=` on its decoration line: `below` is where a
part goes anyway (never written), `beside` draws it **next to the block
above**, `behind` puts it **behind** the block above, as a tab.

### ↔️ `layout="beside"` — in the same row

A part with `layout="beside"` is drawn next to the block above instead of under it. Two or three in a row
fold into one row of equal columns, the same row `.blocks cols=` makes —
same gap, same stacking on a phone — and source order stays visual
order. Nothing to nest: three parts, three decorations.

```csv
name,legs
Rex,4
Tweety,2
Nemo,0
```
{: .dataset #pets_row }

[Pets](#)
{: .datagrid source="pets_row" }

```sql
SELECT name, legs FROM pets_row WHERE legs > 0
```
{: .query bind="pets_row" #walkers }

[Legs](#)
{: .chart source="walkers" type="bar" x="name" y="legs" layout="beside" }

````markdown
[Pets](#)
{: .datagrid source="pets_row" }

```sql
SELECT name, legs FROM pets_row WHERE legs > 0
```
{: .query bind="pets_row" #walkers }

[Legs](#)
{: .chart source="walkers" type="bar" x="name" y="legs" layout="beside" }
````

A dataset or a query between them has no face, so "the block above" is
the last one that shows: the chart lands beside the table, and the query
rides along inside the row, unseen.

```gherkin
Feature: layout="beside" draws a part next to the one above
  As a learner laying out two faces of one dataset
  I want the chart beside the table with one word
  So that a row needs no fence inside a fence

  Scenario: The chart sits beside the table, in one row of two
    Given the table and the chart above
    :::python
    rows = Object._all(".lc-blocks[data-lc-beside]")
    self.row = rows[0]
    :::
    Then they share one row of two equal columns, the query riding along unseen
    :::python
    assert int(self.row._el.children.length) == 3, int(self.row._el.children.length)
    assert str(self.row._el.style.gridTemplateColumns) == "repeat(2, 1fr)", str(self.row._el.style.gridTemplateColumns)
    chip = self.row._el.querySelector(".lc-query")
    assert chip is not None and chip.offsetParent is None, "the query shows a face"
    :::
    And the table is first, the chart last — source order is visual order
    :::python
    first = self.row._el.children.item(0)
    last = self.row._el.lastElementChild
    assert first.querySelector("table") is not None, "the table is not first"
    assert "lc-chart" in str(last.className), "the chart is not last: " + str(last.className)
    :::
```
{: .feature #beside_proof tags="ui" status="passing" }

### 🗂️ `layout="behind"` — in the same place, as tabs

`behind` puts a part **behind the block above**: the same place, as tabs,
the block above in front. Each tab is named by its link words. Good for
two faces of one thing when the page has no room for both side by side —
a phone, a long table and its chart.

```csv
name,legs
Rex,4
Tweety,2
Nemo,0
```
{: .dataset #pets_tabs }

[the pets](#)
{: .datagrid source="pets_tabs" #pets_tab_grid }

[their legs](#)
{: .chart source="pets_tabs" type="bar" x="name" y="legs" layout="behind" #pets_tab_chart }

````markdown
[the pets](#)
{: .datagrid source="pets_tabs" }

[their legs](#)
{: .chart source="pets_tabs" type="bar" x="name" y="legs" layout="behind" }
````

In a pad, **⌃⌥→** puts the block under the caret beside the one above,
**⌃⌥↑** behind it, **⌃⌥←** back below. A pad's own `layout=` says where its
source stands against its preview: `beside` (the default), `below`,
`behind` — see the [text pad](text).

```gherkin
Feature: layout="behind" stacks a part behind the one above, as tabs
  As a learner with two faces of one list and little room
  I want the chart behind the table with one word
  So that the page shows one at a time, and a tap shows the other

  Scenario: The table in front, the chart behind it, a tap swaps them
    Given the table and the chart above
    :::python
    self.box = Object._all(".lc-behind[data-lc-behind]")[0]
    self.tabs = self.box._el.querySelectorAll(".lc-behind-tab")
    :::
    Then two tabs, named by their links, the table's in front
    :::python
    assert int(self.tabs.length) == 2, int(self.tabs.length)
    assert "the pets" in str(self.tabs.item(0).textContent), str(self.tabs.item(0).textContent)
    assert "their legs" in str(self.tabs.item(1).textContent), str(self.tabs.item(1).textContent)
    assert str(self.tabs.item(0).getAttribute("aria-selected")) == "true"
    front = self.box._el.querySelector(".lc-behind-pane.lc-on")
    assert front.querySelector("table") is not None, "the table is not in front"
    :::
    When the chart's tab is tapped
    :::python
    self.tabs.item(1).click()
    :::
    Then the chart comes in front
    :::python
    front = self.box._el.querySelector(".lc-behind-pane.lc-on")
    assert front.querySelector(".lc-chart") is not None, "the chart is not in front"
    self.tabs.item(0).click()
    :::
```
{: .feature #behind_proof tags="ui" status="passing" }

## Example — weighted columns
```
### ⚖️ Equal
cols="2" — two columns of the same width.

### 📐 Weighted
cols="2;1" — the first column takes two thirds, the second one third.
Useful when one side is prose and the other a picture or a clip.
```
{: .blocks cols="2;1" }

## Example — tone

A course page speaks in three registers, and the [seam](/components/seam) names them
out loud. `tone` is the same three worn quietly by a card: the seam says it,
the tone echoes it, so a reader who skimmed past the line still feels the
change. Colour never carries the meaning on its own.

```
### 📄 paper
The course talking — the voice that explains.

### 📱 app
The thing the learner acts in. A shipped app looks like this.

### 🔧 tool
A checker, a 💾, a ▶ Run. Scaffolding, and it says so.
```
{: .blocks cols="3" }

```
### 📄 tone="paper"
Warm and quiet. The default voice of a lesson.
```
{: .block tone="paper" }

```
### 📱 tone="app"
Cool, with a solid edge — you are inside the app now.
```
{: .block tone="app" }

```
### 🔧 tone="tool"
Dashed, because scaffolding is temporary by nature.
```
{: .block tone="tool" }

```gherkin
Feature: A card can wear its register
  As an author mixing lesson, app and tools on one page
  I want each card to carry the register it belongs to
  So that a reader never has to guess which voice is speaking

  Scenario: The three tones each style their own cards
    Given the tone examples on this page
    :::python
    self.app: list = Object._all(".lc-tone-app")
    self.tool: list = Object._all(".lc-tone-tool")
    :::
    When the page has rendered
    Then each tone reached its own wrapper
    :::python
    assert len(self.app) >= 1, len(self.app)
    assert len(self.tool) >= 1, len(self.tool)
    :::
    And a toned wrapper still holds ordinary block cards
    :::python
    n: int = len(Object._all(".lc-tone-app .lc-block"))
    assert n >= 1, n
    :::
```
{: .feature #tone_proof tags="ui" status="passing" }
