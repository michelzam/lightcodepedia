# 🧱 Block

Wrap content in a bordered card. Use `cols` to place multiple blocks side by side.

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
| `cols` | `1` | Number of side-by-side columns |

## Notes

- Without `### headings` the entire content becomes one block.
- `.block` is shorthand for `.blocks cols="1"` — same component.
- Nested components work inside blocks: `{: .video }`, `{: .quiz }`, `{: .run }`, `{: .button }`.
- On small screens columns collapse to a single column automatically.

## Example — single block

```
### 🐕 Meet Lucky
![Lucky](/assets/lab.jpg)

This is **Lucky** — a three-year-old Beagle who loves parks, tennis balls, and long naps.
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
    self.cells = Object._all(".lc-block")
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
