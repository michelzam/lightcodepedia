# 💻 Code

Display source code with syntax highlighting and an optional file-viewer chrome. Three options, from simplest to most powerful — pick the one that fits. To **run** Python in the browser, see [🐍 Run](/components/run).

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 Try it now

Here's a code block with full file-viewer chrome — language badge, title bar, copy button:

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Lightcoder")
```
{: .code title="hello.py" }

That's Option 2 — one IAL[^ial] line added to a plain fenced block. Let's build up from the simplest form.

> When demoing: point at the language badge (top-right) and the title bar.
> Ask yourself: "how many lines of extra markup did that take?" Answer: one.
{: .speaker-note }

## ✏️ Option 1 — plain fenced block (built-in)

Zero setup. Write a fenced code block with a language tag and Jekyll[^jekyll] highlights it server-side via Rouge[^rouge].

````markdown
```yaml
name: Lucky
age: 3
breed: Beagle
```
````

Renders to:

```yaml
name: Lucky
age: 3
breed: Beagle
```

✅ Native markdown — works in any markdown viewer, no extras needed.
⚠️ No title bar, no file label, no copy button.

**Use this for:** short snippets inside prose where you just want highlighting, nothing more.

**Q:** You want to show a quick 3-line YAML example inline in a tutorial paragraph. Which option is right?

- [x] Plain fenced block — zero setup, inline highlighting, no chrome overhead.
- [ ] `{: .code }` — you should always add chrome for professionalism.
- [ ] `code_file.md` — even for inline snippets, the file-loader is more future-proof.
- [ ] Put it in a `<pre>` tag. Classic HTML never lets you down.
{: .quiz }

## 🎨 Option 2 — `{: .code }` (add chrome)

Add `{: .code }` on the line right after the closing fence to wrap the block in a styled file-viewer card. Add `title="…"` for a filename label.

````markdown
```python
def greet(name):
    print(f"Hello, {name}!")

greet("Lightcoder")
```
{: .code title="hello.py" }
````

Same block without a title — just the border and language badge:

```json
{"name": "Lucky", "age": 3}
```
{: .code }

Works for any language Rouge[^rouge] knows: `python`, `yaml`, `json`, `markdown`, `bash`, `liquid`, `csv`, and many more.

✅ Pure markdown — no Liquid `{% raw %}{% capture %}{% endraw %}` needed. Server-side highlighting preserved.
⚠️ The `{: .code }` must be on the line directly after the closing fence. A blank line before it is tolerated; no line at all means the IAL attaches to the wrong block.

**Q:** You add `{: .code title="config.yaml" }` but the title bar never shows up. What's the most likely cause?

- [ ] YAML blocks don't support titles — use `{: .code-yaml }`.
- [ ] The title string has a dot in it, which breaks the IAL parser.
- [x] There's a blank line between the closing fence and the IAL — it attached to nothing.
- [ ] You need `format="yaml"` alongside `title=`.
{: .quiz }

## 📂 Option 3 — live from a repo file

`{% raw %}{% include code_file.md path="…" %}{% endraw %}` fetches the current content of a file from the repo at page load. The page becomes a live mirror — no copy-paste, always in sync.

{% raw %}
```liquid
{% include code_file.md path="modules/dog_ui.yaml" lang="yaml" %}
```
{% endraw %}

Renders to:

{% include code_file.md path="modules/dog_ui.yaml" lang="yaml" %}

By default the page fetches from `raw.githubusercontent.com` (fresh after every push, ~1 s latency). When viewed on the canonical host[^cdn] or with `?cdn=1`, it switches to jsDelivr (edge-cached, faster for end users).

The mode — *(live)* or *(cdn)* — is shown in italics in the title bar.

### File-loader knobs

| Knob | What it does |
|---|---|
| `path="…"` | Repo-relative path — auto-builds raw + jsDelivr URLs from the repo metadata |
| `src="https://…"` | External URL escape hatch — use for files outside the repo |
| `repo="org/repo"` `branch="…"` | Override repo + branch (defaults: current site, `main`) |
| `lang="…"` | Language badge: `yaml`, `python`, `json`, etc. Defaults to `text` |
| `title="…"` | File label in the title bar; defaults to `path` (or `src`) |

An example loading a CSV from the repo:

{% include code_file.md path="data/dogs.csv" lang="csv" title="data/dogs.csv" %}

## 🤔 Which option to pick

| Situation | Best choice |
|---|---|
| Short snippet inside a tutorial paragraph | Plain fenced block |
| Snippet that deserves a title / file-viewer look | `{: .code title="…" }` |
| Full source file you want to keep in sync | `code_file.md path="…"` |
| External file from another repo | `code_file.md src="…"` |
| Python code the student should **run** | `{: .run }` — see [🐍 Run](/components/run) |

> Rule of thumb: start with Option 1 (plain fenced). Upgrade to Option 2 when you want chrome.
> Upgrade to Option 3 when the source file already exists and you'd have to maintain two copies otherwise.
{: .speaker-note }

**Q:** You have a 200-line Python module in `src/parser.py`. You want it displayed on a tutorial page, always showing the latest committed version. Which option do you pick?

- [ ] Copy-paste into a plain fenced block. 200 lines is fine, you'll remember to update it.
- [ ] `{: .code title="parser.py" }` — the chrome makes it look like a real file.
- [x] `code_file.md path="src/parser.py"` — the page fetches the live file; no copy-paste ever.
- [ ] A hyperlink to the GitHub file view. Let GitHub's UI do the heavy lifting.
{: .quiz }

## 🏁 Final exam — boss level

**Q:** Which of these are TRUE about the code widget? (Pick all that apply.)

- [x] Plain fenced blocks use server-side highlighting via Rouge — no JS needed.
- [x] `{: .code }` without a `title=` still adds the border and language badge.
- [ ] `code_file.md` only works for files smaller than 100 KB.
- [x] `?cdn=1` in the URL switches `code_file.md` to the jsDelivr edge-cached version.
- [ ] All three options require JavaScript to render.
{: .quiz multi="true" }

**Q:** You add `{: .run }` to a Python block instead of `{: .code }`. What's different?

- [ ] Nothing — `.run` and `.code` do the same thing.
- [ ] The block gets a title bar but the code is still read-only.
- [x] The block becomes a live editor: you can edit and run the code.
- [ ] The page crashes because `.run` is only valid on YAML blocks.
{: .quiz }

[^ial]: **IAL (Inline Attribute List)** — kramdown's `{: .class key="value" }` syntax, placed on its own line right after a block, attaches HTML attributes to that block. See [✍️ Text](/components/text).

[^jekyll]: **Jekyll** — the static site generator that builds this site. It processes Markdown files into HTML pages, applying Liquid templates and the kramdown parser. Deployed automatically on GitHub Pages.

[^rouge]: **Rouge** — a Ruby syntax highlighter used by Jekyll. Runs at build time (server-side), so no JavaScript is needed for static code blocks. Supports 200+ languages.

[^cdn]: **CDN (Content-Delivery Network)** — a globally distributed network of servers that caches and serves files from an edge node geographically close to the visitor. This site uses jsDelivr to serve library files and cached repo content.
