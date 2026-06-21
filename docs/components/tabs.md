# 📑 Tabs

Show alternative content panels — only one tab visible at a time. Each `### Heading` in a content file becomes a tab label; everything below it becomes the panel body.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 See it in action

[→](pages/tabs_example)
{: .tabs }

Click any tab. The active tab is highlighted in blue; the others hide. That's the whole widget.

> Ask: "When would you use tabs vs a bullet list?"
> Good answers: comparing alternatives side-by-side, hiding advanced content until needed,
> showing the same thing in multiple languages.
{: .speaker-note }

**Q:** A learner clicks the second tab. What happens to the first tab's content?

- [ ] It stays visible below — tabs stack vertically on click.
- [x] It hides — only one panel is visible at a time.
- [ ] It collapses to just its heading.
- [ ] It slides into a drawer on the right. Very smooth.
{: .quiz }

## 🛠️ How to make one

Two steps. That's all.

**Step 1** — add one line to your page:

```markdown
[→](pages/my_tabs)
{: .tabs }
```

**Step 2** — create `docs/pages/my_tabs.md`. Each `### Heading` becomes a tab; the content below it becomes the panel body:

```markdown
### 🐍 Python
Python is a great first language.
- Easy to read
- Huge community

### 🎬 Demo
Click here to try the demo.

### 📚 Resources
- [Official docs](https://docs.python.org)
```

Add another `### Section` → a new tab appears. Remove one → it's gone.

> Put tab content files in `docs/pages/` — they show up in the Pages editor and stay out of the Components listing.
{: .speaker-note }

**Q:** You want to add a fourth tab called "🧪 Exercises". What do you do?

- [ ] Add `tab4="🧪 Exercises"` to the link line.
- [ ] Edit `_includes/tabs.md` directly.
- [x] Add `### 🧪 Exercises` (and its body) to your content file.
- [ ] Create a new `tabs4.md` file. One file per tab.
{: .quiz }

## 🔧 Options

| Attribute | Default | What it does |
|---|---|---|
| `id="…"` | auto | Required when more than one tabs widget lives on a page |

```markdown
[→](pages/my_tabs)
{: .tabs #tab1 }
```

## ⚠️ Limits worth knowing

- **One active tab at a time.** No multi-open accordion mode.
- **Two-file requirement.** The content must live in a separate `.md` file in `docs/pages/`. You can't write tab content inline in the same page.
- **No live components inside panels.** Python runners, datagrids etc. won't upgrade inside a tab panel fetched this way.
- **Requires public repo.** Tab content is fetched from `raw.githubusercontent.com` — works on public repos without authentication.

## 🏁 Final exam — boss level

**Q:** You add `### ⚡ Speed` to the content file but the new tab doesn't appear after you save. What's missing?

- [ ] You need to add `tab5="⚡ Speed"` to the link line.
- [ ] The content file requires a front-matter `tabs: true` flag.
- [x] A GitHub Pages build (~35 s) — the raw file is fetched from the pushed commit.
- [ ] The `### ` must be at column 1 with exactly one space after the hashes.

  > Push → wait ~35 s → reload. The raw file is fetched from the latest committed version.
{: .quiz }

**Q:** You want two separate tabs widgets on the same page. What do you add to each link line?

- [ ] Nothing — tabs widgets are automatically namespaced by file path.
- [x] A distinct `id="…"` attribute on each `{: .tabs }` IAL.
- [ ] A `namespace="…"` parameter.
- [ ] You can't — one tabs widget per page is the hard limit.
{: .quiz }
