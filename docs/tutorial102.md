# ⚙️ Now let's build one

In the previous tutorial you explored every building block. Now let's see how each one is made — and add them to your own page.

- [x] Make your own copy of this site (two minutes, free)
- [x] Open any page in the browser editor
- [x] Add a text block, a runner, a map, a chart
- [x] Save — your page is live within 35 seconds

> Tell learners: "By the end of this page, each of you will have a live website with your name on it — and at least one block you added yourself."
{: .speaker-note }

---

## 🍴 Step 1 — Make your own copy

Every Lightcodepedia site is a free, forkable template on GitHub.

1. Go to [github.com/michelzam/lightcodepedia](https://github.com/michelzam/lightcodepedia)
2. Click **Fork → Create a new fork**
3. Keep the default name and click **Create fork**
4. In your new repo → **Settings → Pages → Build and deployment → GitHub Actions**
5. Make any tiny change to trigger the first build (edit a file, add a space, save)

Your site goes live at `https://your-name.github.io/lightcodepedia` in about a minute.

> Show this live on the projector. The moment the Pages URL appears — "it's really live?" — is always a crowd moment.
{: .speaker-note }

**Q:** After you fork the repo, your new site is hosted…

- [ ] On Lightcodepedia's servers — they host all forks for free.
- [x] On GitHub's free hosting, under your own GitHub account.
- [ ] Nowhere — you still need to configure a hosting service.
- [ ] On your laptop — you need to run a local server.
{: .quiz }

---

## ✏️ Step 2 — Open the editor

Every page on your site has a built-in editor — the **✏️** button at the bottom right.

To connect it you need a short access key with permission to save files:

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens) → **Generate new token (classic)**
2. Give it a name. Check the **`repo`** box. Click **Generate** and copy the key.
3. On your forked site, click **✏️** — paste the key and your repo name (`your-name/lightcodepedia`), click **Connect**

The file tree on the left loads. Click any file to open it. Edit. Save. Done.

> Common stumble: extra space or capital letter in the repo name. Check that first if someone can't connect.
{: .speaker-note }

---

## 📖 How to add a text block

A text block is just markdown. Open any page and type.

```markdown
## My heading

A paragraph with **bold**, _italic_ and a [link](https://example.com).

- Item one
- Item two
```

No tag needed — plain text is already a text block. Every section of every tutorial page you've read so far is a text block.

_Every block type has a documentation page. [Text / markdown reference →](https://www.markdownguide.org/cheat-sheet/)_

---

## ▶️ How to add a code runner

Take a code block and add `{: .run }` on the next line. That's the whole trick.

````markdown
```python
print("Hello from my page! 🎉")
```
{: .run }
````

The `{: .run }` tag is what turns a plain code block into a live runner. Without it: displayed code. With it: a button that runs.

Try it: open your home page in the editor, paste that block, click **Save**, wait 35 seconds, reload.

> Demo live. Paste it, save, reload, click ▶. Then ask a learner to change the message and save again. Two edits in under two minutes — that's the aha moment.
{: .speaker-note }

_[Code runner documentation →](/components/run)_

---

## 🗺️ How to add a map

Write your locations as a JSON list, then add `{: .map }`.

````markdown
```json
[
  { "lat": 48.85, "lon": 2.35, "label": "Paris 🇫🇷" },
  { "lat": 52.52, "lon": 13.40, "label": "Berlin 🇩🇪" }
]
```
{: .map height="280" zoom="4" }
````

Each entry is a pin. Add as many as you like. The map zooms to fit all pins automatically.

_[Map documentation →](/components/map)_

---

## 📊 How to add a data table and chart

Paste a CSV block, add `{: .datagrid format="csv" #my_grid }`. Then paste the same CSV again for the chart, add `{: .chart bound-to="my_grid" }`.

````markdown
```csv
city,population,area
Paris,2161000,105
Berlin,3600000,892
Madrid,3300000,604
```
{: .datagrid #city_grid format="csv" }

```csv
city,population,area
Paris,2161000,105
Berlin,3600000,892
Madrid,3300000,604
```
{: .chart type="bar" bound-to="city_grid" x="city" }
````

The `#city_grid` gives the table a name. `bound-to="city_grid"` tells the chart to listen to it. Use **snake_case** names — component ids double as Python identifiers in the typed layer (`self.page.city_grid`).

**Q:** What turns a plain code block into an interactive component?

- [ ] A setting in the GitHub repo configuration.
- [ ] A special file you upload separately.
- [x] The `{: .tag }` line written immediately after the block.
- [ ] Nothing — all code blocks are interactive by default.
{: .quiz }

_[Datagrid documentation →](/components/datagrid) · [Chart documentation →](/components/chart)_

---

## 🤖 How to add an AI assistant

Write a YAML block with a `system:` prompt, add `{: .agent }`.

````markdown
```yaml
system: |
  You are a teaching assistant for my Python class.
  Keep answers short. Only answer questions about Python.
intro: "Ask me anything about Python!"
```
{: .agent }
````

The `system:` field is the assistant's instructions — its personality, knowledge and limits. You write it; the AI follows it.

_[Agent documentation →](/components/agent)_

---

## 📑 How to add tabs

Create a file in `docs/pages/` with `### Heading` sections. Then link to it with `{: .tabs }`.

**`docs/pages/my_tabs.md`:**

```markdown
### 🐍 Python
Python is great for beginners...

### ☕ Java
Java is widely used in enterprise...

### 🦀 Rust
Rust is fast and memory-safe...
```

**On your page:**

```markdown
[→](pages/my_tabs)
{: .tabs }
```

Each `### Heading` becomes a tab. The content below it becomes the panel.

_[Tabs documentation →](/components/tabs)_

---

## 🎛️ Quick reference — every tag

| What you want | Tag to write after the block |
|---|---|
| Code runner | `{: .run }` |
| Map | `{: .map height="300" }` |
| Data table | `{: .datagrid format="csv" #my_id }` |
| Bar chart | `{: .chart type="bar" bound-to="my_id" x="col" }` |
| AI assistant | `{: .agent }` |
| Tabs | `{: .tabs }` (on a link to a pages/ file) |
| Accordion | `{: .accordion }` |
| Card grid | `{: .cards cols="3" }` |
| Folder of cards | `{: .folder cols="3" }` (on a link to a folder) |
| Embed a page | `{: .embed-page }` |
| Video | `{: .video }` |

---

## 🚀 What's next?

Your page is live and you've added your own blocks. The next step: give it its own address, bring in your own data, and connect with the community.

```
### 🚀 Step 3 — Go further
Custom address, your own data, and what to do next.

[Go further →](/tutorial103)

### 🧩 Component library
Every block, with live examples and documentation.

[Browse →](/components/)

### 🏠 Back to home
[Home →](/)
```
{: .cards cols="3" }
