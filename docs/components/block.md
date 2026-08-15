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
{: .wide_first }


## Notes

- Without `### headings` the entire content becomes one block.
- `.block` is shorthand for `.blocks cols="1"` — same component.
- Nested components work inside blocks: `{: .video }`, `{: .quiz }`, `{: .run }`, `{: .button }`.
- On small screens columns collapse to a single column automatically.

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
