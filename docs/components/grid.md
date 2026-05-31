# 🔲 Grid

Lay content out in columns — auto-responsive by default, or fixed with `cols="N"`. Each `### Heading` in a fenced block becomes a column cell.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 See it in action

```
### ⚡ Fast
WebAssembly runs Python at near-native speed in your browser. No server round-trip.

### 🔒 Private
Your code never leaves your browser. No data sent to any server.

### 🆓 Free
No login, no API key, no quota. Open source, forever.
```
{: .grid }

Resize your browser window — the columns reflow automatically.

> Grid + icons is the classic "feature highlight" layout.
> Ask: "Where have you seen this pattern before?" They'll name a dozen SaaS landing pages.
{: .speaker-note }

**Q:** You shrink the browser to phone width. What happens to the three columns?

- [ ] The columns overflow horizontally — scroll right to see the rest.
- [ ] The text shrinks until it fits.
- [x] The columns reflow — `auto-fit` wraps them into fewer columns or a single column.
- [ ] The grid disappears below 768 px.
{: .quiz }

## 🛠️ How to make one

Plain fenced block, `### ` sections, `{: .grid }` IAL:

````markdown
```
### 🎯 Goal
What you want learners to achieve.

### 🛠️ Method
How you'll help them get there.
```
{: .grid cols="2" }
````

## 🔧 Knobs

| Attribute | Default | What it does |
|---|---|---|
| `cols="N"` | `auto` | Fixed column count. `auto` = responsive `minmax(280px, 1fr)` |
| `gap="N"` | `18` | Gap between cells in pixels |
| `headings="hide"` | (show) | Hide the `### ` label — show only the cell body |

**Two-column fixed:**

```
### 🐕 Dogs
Loyal, energetic, need walks. Best for active lifestyles.

### 🐈 Cats
Independent, low-maintenance. Best for busy schedules.
```
{: .grid cols="2" }

**Hidden headings — pure content cells:**

```
🚀 Deploy in seconds.

🔒 Zero-config security.

📊 Real-time analytics.
```
{: .grid cols="3" headings="hide" }

**Q:** You want a two-column layout with no heading labels. Which IAL?

- [ ] `{: .grid cols="2" labels="none" }`
- [x] `{: .grid cols="2" headings="hide" }`
- [ ] `{: .grid-2 }`
- [ ] `{: .grid cols="2" hide="true" }`
{: .quiz }

## 🏁 Final exam

**Q:** Which of these are TRUE about the grid widget? (Pick all that apply.)

- [x] `auto` columns reflow responsively based on available width.
- [x] `headings="hide"` suppresses the `### ` label — only the body renders.
- [ ] You must specify `cols=` — there is no default.
- [x] Gap defaults to 18 px and can be changed with `gap=`.
- [x] Swapping `{: .grid }` to `{: .accordion }` gives the same content as an accordion.
{: .quiz multi="true" }
