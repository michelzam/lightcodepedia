---
title: Block
---
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
![Lucky](https://lightcodepedia.jollybush-84a428fe.francecentral.azurecontainerapps.io/media/8fd1c9c5fa0e06f96b21dd9440b20d673e30499dda6a6ade356edb3c.jpg)

This is **Lucky** — a three-year-old Beagle who loves parks, tennis balls, and long naps.
```
{: .block }

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

{% include backtotop.md %}
