{% include topbar.md title="💻 Code" %}

Show source code (YAML, Python, JSON, …) elegantly. Three options, from least to most powerful.

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

## Option 2 — `code.md` include (inline content with chrome)

Wraps a fenced block in a styled "file viewer" card with a title bar and language badge.

{% raw %}
```liquid
{% capture _yaml %}
module:
  - name: dog_ui
    doc: "Just a Text"
    icon: "🐕"
{% endcapture %}
{% include code.md content=_yaml lang="yaml" title="dog_ui.yaml" %}
```
{% endraw %}

Renders to:

{% capture _yaml %}
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
{% endcapture %}
{% include code.md content=_yaml lang="yaml" title="dog_ui.yaml" %}

Same trick for Python:

{% capture _py %}
def greet(name):
    print(f"Hello, {name}!")

greet("Lightcoder")
{% endcapture %}
{% include code.md content=_py lang="python" title="hello.py" %}

✅ Pretty chrome, server-side highlighting, supports yaml / python / json / html / css / bash / ruby / javascript / liquid.  
⚠️ Content is inline — you have to copy-paste it into the page, so it can drift from the real file.

## Option 3 — `code_file.md` include (live fetch from URL)

Always shows the current content of a real file. Fetched at runtime via JavaScript.

{% raw %}
```liquid
{% include code_file.md src="https://cdn.jsdelivr.net/gh/michelzam/lightcodepedia@main/modules/dog_ui.yaml" lang="yaml" title="modules/dog_ui.yaml" %}
```
{% endraw %}

Renders to:

{% include code_file.md src="https://cdn.jsdelivr.net/gh/michelzam/lightcodepedia@main/modules/dog_ui.yaml" lang="yaml" title="modules/dog_ui.yaml" %}

Python from the same repo:

{% include code_file.md src="https://cdn.jsdelivr.net/gh/michelzam/lightcodepedia@main/main.py" lang="python" title="main.py" %}

✅ Always live, single source of truth.  
⚠️ No syntax highlighting (no Rouge — content arrives after build). Depends on the URL serving CORS-friendly text (jsDelivr does; `raw.githubusercontent.com` usually does too).

## Options

| Parameter | Default | Description |
|---|---|---|
| `content` | required for `code.md` | The raw code string (use `{% raw %}{% capture %}…{% endcapture %}{% endraw %}` for multi-line) |
| `src` | required for `code_file.md` | URL to fetch the code from |
| `lang` | `text` | Language tag for highlighting / class. `yaml`, `python`, `json`, `html`, `css`, `bash`, `ruby`, `javascript`, `liquid` |
| `title` | (defaults to `src` for `code_file`) | File label shown in the title bar |

## When to use which

- **Plain fenced** for ad-hoc snippets inside prose.
- **`code.md`** when you want a file-viewer look and the content is short enough to keep in the page.
- **`code_file.md`** for long source files you want to keep in sync — the page becomes a live mirror.

## 🐍 Bonus — actually run Python in the browser

The `python_run.md` include boots **MicroPython compiled to WebAssembly** the first time you click ▶ Run (~300 KB, then cached). Edit the code in the box and click Run again.

{% raw %}
```liquid
{% capture _py %}
# Lightcoder's first interactive snippet
def woof(name, n=3):
    for i in range(1, n + 1):
        print(f"{i}. Woof! I'm {name}.")

woof("Lucky")
woof("Wanda", 2)
{% endcapture %}
{% include python_run.md id="demo1" code=_py %}
```
{% endraw %}

{% capture _py %}
# Lightcoder's first interactive snippet
def woof(name, n=3):
    for i in range(1, n + 1):
        print(f"{i}. Woof! I'm {name}.")

woof("Lucky")
woof("Wanda", 2)
{% endcapture %}
{% include python_run.md id="demo1" code=_py %}

A second runner with a more numeric example:

{% capture _py2 %}
# Compute factorials
def fact(n):
    return 1 if n <= 1 else n * fact(n - 1)

for i in range(1, 8):
    print(f"{i}! = {fact(i)}")
{% endcapture %}
{% include python_run.md id="demo2" code=_py2 rows="8" %}

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `id` | `default` | Unique id — required if you have multiple runners on the same page |
| `code` | `print('Hello…')` | Initial code shown in the editor (use `{% raw %}{% capture %}…{% endcapture %}{% endraw %}` for multi-line) |
| `rows` | `6` | Initial height of the editor in lines |

✅ Native Python syntax, runs entirely in the browser, no server.  
⚠️ MicroPython has a slim stdlib — no `numpy`, no `pandas`, no `requests`. For the full Python ecosystem you'd switch to Pyodide (~10 MB).

{% include backtotop.md %}
