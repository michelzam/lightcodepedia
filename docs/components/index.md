# 🧩 Component Gallery

Welcome, lowcoder! Every interactive component you can use in your `.md` pages.

**The rule of the game:** you only write markdown. Components activate via `{: .class }` — an IAL tag on the line after a fenced block or link. No HTML, no CSS, no JavaScript needed.

## Available components

```
### ✍️ Text
Markdown basics — headings, lists, links, code, tables. Plus footnote popovers `[^x]` for inline definitions.

[Open →](text)

### 📑 Tabs
Alternative content panels — only one visible at a time. Split by `###`.

[Open →](tabs)

### 🎠 Carousel
Auto-rotating items with clickable dots. Bullet list with `{: .carousel }`.

[Open →](carousel)

### 📋 Dropdown
Click-to-reveal vertical menu. Bullet list with `{: .dropdown }`.

[Open →](dropdown)

### 🔘 Button
Styled link button with 5 color variants. Inline `{: .lc-btn }` on any link.

[Open →](button)

### 📻 Radio
Pick-one selector that reveals different content per choice.

[Open →](radio)

### 🪗 Accordion
Multiple collapsibles from one fenced block, split by `###`.

[Open →](accordion)

### 📜 Scrollable
Fixed-height container with internal scrollbar.

[Open →](scrollable)

### 🪟 Embed
Wrap a URL, internal page, video or Google Drive file in an iframe.

[Open →](embed_page)

### 🃏 Cards
Responsive grid of bordered cards with hover effect. Fenced block + `{: .cards }`.

[Open →](cards)

### 📐 Grid
Free-form layout grid — cells can hold any content. Same `###` format as cards.

[Open →](grid)

### 📊 Chart
CSV fenced block → Chart.js bar, line, pie or doughnut. `{: .chart type="bar" }`.

[Open →](chart)

### 📊 Chart + Datagrid
Live chart bound to a datagrid row — master/detail for data visualization.

[Open →](chart_datagrid)

### 🗺️ Map
Interactive Leaflet map with CSV markers. `{: .map lat= lng= zoom= }`.

[Open →](map)

### 💻 Code
Show YAML, Python, JSON with a title bar, or live-fetch from a repo file.

[Open →](code)

### 🐍 Run
Live Python editor + runner via `{: .run }` — MicroPython in WebAssembly.

[Open →](run)

### 📊 Datagrid
Sortable, filterable tables via `{: .datagrid }` — AG Grid, YAML/JSON/CSV.

[Open →](datagrid)

### 📝 Form
Single-object attribute view via `{: .form }`. Pairs with datagrid for master/detail.

[Open →](form)

### 📽️ Slides
Present any page as a deck — `## h2` becomes a slide. Click 📽️ bottom-left.

[Open →](slides)

### 🧪 Quiz
Interactive question from a bullet list. Single-choice or multi-select.

[Open →](quiz)

### 🤖 Agent
Chat-style LLM panel via GitHub Models. Each user brings their own PAT.

[Open →](agent)

### 📁 Folder
Auto-generate cards from all pages in a folder. One link, zero maintenance.

[Open →](folder)

### 🎬 Recorder
Record your screen with face overlay — downloads as a video file, no install.

[Open →](recorder)
```
{: .cards cols="3" }

{% include backtotop.md %}
