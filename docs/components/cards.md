# 🃏 Cards

A responsive grid of content cards — each with a title, body text, and optional link. Swap `{: .grid }` for `{: .cards }` and you get clickable cards instead of plain cells.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 See it in action

```
### 🎬 Demo
Try the live LightCode demo right in your browser.
[Open demo →](/demo)

### 📚 Chapters
Read the course materials covering low-code fundamentals.
[Start reading →](/chapters)

### 🤖 Ari
Chat with your AI pair lightcoder.
[Chat with Ari →](/ari)
```
{: .cards cols="3" }

Hover over a card — it lifts and gets a blue border. Resize the window to see auto-reflow.

> Ask yourself: "Which card would you click first, and why?"
> The hover effect is a tiny UX cue that says "I'm clickable."
{: .speaker-note }

**Q:** You hover over a card. What visual feedback does it give?

- [ ] Nothing — cards are purely decorative.
- [x] The card lifts slightly and gets a blue border — a subtle "I'm clickable" cue.
- [ ] The card expands to full width.
- [ ] A tooltip with the link URL appears.
{: .quiz }

## 🛠️ How to make one

A fenced block with `### ` sections, then `{: .cards }` on the next line:

````markdown
```
### 🎯 Title
Body text goes here.
[Optional link →](url)
```
{: .cards }
````

Each `### Heading` becomes one card. The body can be any markdown — paragraphs, links, bullet lists.

**Q:** You write `{: .cards }` on a fenced block that has no `### ` headings. What renders?

- [ ] An error message in the page.
- [ ] A single card with all the text as the body.
- [x] Nothing — the upgrade finds no sections and does not replace the block.
- [ ] A blank grid container appears.
{: .quiz }

## 🔧 Knobs

| Attribute | Default | What it does |
|---|---|---|
| `cols="N"` | `auto` | Fixed column count. `auto` = responsive `minmax(240px, 1fr)` |
| `gap="N"` | `18` | Gap between cards in pixels |

**Two-column layout:**

```
### 🐕 Dogs
Loyal, energetic, need walks.
Best for active lifestyles.

### 🐈 Cats
Independent, low-maintenance.
Best for busy schedules.
```
{: .cards cols="2" }

**Q:** You want exactly four cards side-by-side on wide screens. Which IAL?

- [ ] `{: .cards auto="4" }`
- [ ] `{: .cards min="4" }`
- [x] `{: .cards cols="4" }`
- [ ] `{: .cards grid="4" }`
{: .quiz }

## 🔄 Relation to grid

Cards and grid share the same `### ` source format — swap the IAL class to change the widget:

| IAL | Result |
|---|---|
| `{: .grid }` | Plain cells, optional heading labels |
| `{: .cards }` | Bordered cards with hover effect |
| `{: .accordion }` | Collapsible sections |
| `{: .tabs }` | Tabbed panels |
| `{: .radio }` | Radio-button selector |

**Q:** You already have a `{: .grid cols="3" }` block. You want it to look like cards instead. What's the minimum change?

- [x] Replace `.grid` with `.cards` — the `### ` format is identical.
- [ ] Also change each `### ` heading to `## `.
- [ ] Rewrite the content into YAML.
- [ ] Add `type="cards"` to the IAL instead of swapping the class.
{: .quiz }

## 🏁 Final exam

**Q:** Which of these are TRUE about cards? (Pick all that apply.)

- [x] Each `### Heading` becomes one card title.
- [x] The body can include markdown links — they render inside the card.
- [ ] `cols=` is required — there is no responsive default.
- [x] `{: .cards }` and `{: .grid }` use the same `### ` source format.
- [x] Cards lift and get a blue border on hover.
{: .quiz multi="true" }
