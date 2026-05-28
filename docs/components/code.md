{% include topbar.md title="💻 Code" %}

Show source code (YAML, Python, JSON, …) elegantly. Three options, from least to most powerful. To **run** Python in the browser, see [🐍 Run](/components/run).

## Option 1 — Plain fenced code (built into markdown)

Just write a fenced code block with the language tag. Jekyll's Rouge highlights it server-side.

````markdown
```yaml
module:
  - name: dog_ui
    doc: "Just a Text"
    icon: "🐕"
```
````

Renders to:

```yaml
module:
  - name: dog_ui
    doc: "Just a Text"
    icon: "🐕"
```

✅ Zero setup, syntax-highlighted, native markdown.  
⚠️ No title bar, no file label, plain visual chrome.

## Option 2 — Fenced block + `{: .code }` (chrome via kramdown attribute list)

Write a normal fenced code block and add `{: .code }` on the line right after the closing fence. A global scanner wraps the block in the styled "file viewer" card. Add `title="…"` for a file label, omit it for chrome-only.

{% raw %}
````markdown
```python
def greet(name):
    print(f"Hello, {name}!")

greet("Lightcoder")
```
{: .code title="hello.py" }
````
{% endraw %}

Renders to:

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Lightcoder")
```
{: .code title="hello.py" }

YAML, same recipe:

```yaml
module:
  - name: dog_ui
    doc: "Just a Text"
    icon: "🐕"

imports:
  - !Module
    name: blocks

instances:

  - !Text
    title: "Dog"
    icon: "🐕"
    as_name: dog
    border: False
    text: "Man's best friend :dog:"
    help: Dogs are cute and fast
    media: https://picsum.photos/id/237/500/400
```
{: .code title="dog_ui.yaml" }

Or without a file label — just border + language badge:

```json
{"name": "Lucky", "age": 3}
```
{: .code }

✅ Pure markdown — no Liquid `{% raw %}{% capture %}{% endraw %}` dance. Server-side Rouge highlighting is preserved. Works for any language Rouge knows.  
⚠️ The `{: …}` must sit on its own line immediately after the closing fence (kramdown rule). A blank line before it is tolerated.

## Option 3 — `code_file.md` include (live fetch from a real file)

Always shows the current content of a file. Fetched at runtime via JavaScript.

The short form points at a file **inside this repo** — and works automatically in forks (each fork's page fetches from its own repo):

{% raw %}
```liquid
{% include code_file.md path="modules/dog_ui.yaml" lang="yaml" %}
```
{% endraw %}

Renders to:

{% include code_file.md path="modules/dog_ui.yaml" lang="yaml" %}

### Live by default, cached on demand

By default the page fetches from `raw.githubusercontent.com` of the current repo — fast feedback after a push (~1 s freshness). To switch to the edge-cached jsDelivr version (faster for end users, pinned to the build commit so it's always fresh), add `?cdn=1` to the URL:

- `…/components/code` → live mode (raw) — designer-friendly
- `…/components/code?cdn=1` → cdn mode (jsDelivr) — viewer-friendly

The mode is shown in italics in the file viewer's title bar. You can also set `lc_canonical_host:` in `_config.yml` to a hostname (e.g. your custom domain) and any visitor on that host will get cdn mode automatically.

### External files via `src="…"`

Use `src="…"` when the file lives outside the repo. The hostname/`?cdn=1` switch is bypassed (we don't know an alternate URL):

{% raw %}
```liquid
{% include code_file.md src="https://raw.githubusercontent.com/torvalds/linux/master/README" lang="text" title="Linux README" %}
```
{% endraw %}

### Parameters

| Where | Knob | Description |
|---|---|---|
| `{: .code … }` | `title="…"` | File label shown in the title bar; omit for chrome-only |
| `code_file.md` | `path="…"` | Repo-relative path (recommended). Auto-builds raw + jsDelivr URLs from `site.github.repository_nwo` |
| `code_file.md` | `src="…"` | Full URL escape hatch — use for files outside the repo |
| `code_file.md` | `repo="…"` / `branch="…"` | Override the inferred repo / branch (defaults: current repo / `main`) |
| `code_file.md` | `lang="…"` | Language badge (`yaml`, `python`, `json`, …). Defaults to `text` |
| `code_file.md` | `title="…"` | File label; defaults to `path` (or `src`) |

## When to use which

- **Plain fenced** for ad-hoc snippets inside prose.
- **`{: .code }`** when you want a file-viewer look and the content lives in the page.
- **`code_file.md`** for long source files you want to keep in sync — the page becomes a live mirror, and forks mirror their own copies.

See [🐍 Run](/components/run) for executable Python blocks via `{: .run }`.

{% include backtotop.md %}
