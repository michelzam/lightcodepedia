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

## Option 2 — Fenced block + `{: .code }` (chrome via kramdown attribute list)

Just write a normal fenced code block and add `{: .code }` on the line right after the closing fence. A global scanner wraps the block in the styled "file viewer" card. Add `title="…"` for a file label, leave it off for chrome-only.

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
⚠️ The `{: …}` must sit on its own line immediately after the closing fence (kramdown rule). Section titles for the snippet go above as normal markdown headings.

## Option 3 — `code_file.md` include (live fetch from URL)

Always shows the current content of a real file. Fetched at runtime via JavaScript.

{% raw %}
```liquid
{% include code_file.md src="https://cdn.jsdelivr.net/gh/michelzam/lightcodepedia@main/modules/dog_ui.yaml" lang="yaml" title="modules/dog_ui.yaml" %}
```
{% endraw %}

Renders to:

{% include code_file.md src="https://cdn.jsdelivr.net/gh/michelzam/lightcodepedia@main/modules/dog_ui.yaml" lang="yaml" title="modules/dog_ui.yaml" %}

✅ Always live, single source of truth.  
⚠️ No syntax highlighting (no Rouge — content arrives after build). Depends on the URL serving CORS-friendly text (jsDelivr does; `raw.githubusercontent.com` usually does too).

## Options

| Where | Knob | Description |
|---|---|---|
| `{: .code … }` | `title="…"` | File label shown in the title bar; omit for chrome-only |
| `code_file.md` | `src="…"` | URL to fetch the code from (required) |
| `code_file.md` | `lang="…"` | Language tag for the badge (`yaml`, `python`, `json`, …). Defaults to `text` |
| `code_file.md` | `title="…"` | File label; defaults to `src` |

## When to use which

- **Plain fenced** for ad-hoc snippets inside prose.
- **`{: .code }`** when you want a file-viewer look and the content lives in the page.
- **`code_file.md`** for long source files you want to keep in sync — the page becomes a live mirror.

## 🐍 Bonus — actually run Python in the browser

The `python_run.md` include boots **MicroPython compiled to WebAssembly** the first time you click ▶ Run (~300 KB, then cached). Edit the code in the box and click Run again.

### Tiniest possible runner — `{: .run }` on a fenced block

Just tag a fenced code block with `{: .run }` and the page upgrades it into a live runner. The fence content becomes the editor's initial code.

{% raw %}
````markdown
```python
def greet(name):
    print(f"Hello, {name}!")

greet("Lightcoder")
```
{: .run }
````
{% endraw %}

Renders to:

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Lightcoder")
```
{: .run }

Optional attributes: `bound="o"`, `folded="true"`, `rows="3"`, `init="short_python"`, `id="myrunner"`. For multi-line `init` or anything fancier, fall back to the explicit `{% raw %}{% include python_run.md … %}{% endraw %}` form below.

### Smallest live loop — a bound object

A pre-defined `Object` (a `SimpleNamespace`-style holder, baked into the runner) is created on load and rendered as a card. The editor below is **folded** — click to open, hit ▶ Run, and watch the card mirror your change.

{% capture _bound_init %}o = Object(name='🐕 Lucky', age=3){% endcapture %}
{% capture _bound_code %}o.age += 1
print(o)
{% endcapture %}
{% include python_run.md id="bound1" init=_bound_init code=_bound_code bound="o" folded=true rows="3" %}

Three new include parameters make this work:

| Parameter | Description |
|---|---|
| `init` | Python that runs once on page load, before the user clicks anything. Use it to create the bound object(s). |
| `bound` | Name of a variable to mirror as a card above the editor. Repaints after every Run. |
| `folded` | When `true`, the editor starts collapsed behind a click-to-expand toggle. |

The Python only ever mutates an in-memory object (`o.age += 1`). The page redraws because `bound="o"` registered the card. No view code, no Streamlit, no DOM calls inside Python.

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

### Show objects as cards on the page

Every runner also exposes a built-in `show(obj)` helper. It introspects the value and renders a card in a grid right below the output. Works for **strings, numbers, dicts, lists, and your own classes** (it reads `__dict__`).

Lightcoding-style: describe the objects in **YAML**, then iterate and `show()`. The runner exposes a built-in `yaml.load(s)` helper (powered by `js-yaml`).

{% capture _py3 %}
# Describe the objects in YAML, render them as cards
dogs = yaml.load("""
- name: Lucky
  age: 3
  breed: Beagle
  icon: 🐶
- name: Wanda
  age: 5
  breed: Poodle
  icon: 🐩
- name: Max
  age: 2
  breed: Husky
  icon: 🐺
""")

for d in dogs:
    show(d)

print(f"Showed {len(dogs)} dogs.")
{% endcapture %}
{% include python_run.md id="demo3" code=_py3 rows="16" %}

Works with custom classes too — `show()` reads `__dict__`:

{% capture _py4 %}
class Pet:
    def __init__(self, name, age, breed):
        self.name = name
        self.age = age
        self.breed = breed

pets = [Pet("Lucky", 3, "Beagle"), Pet("Wanda", 5, "Poodle")]
for p in pets:
    show(p)

# Modify and re-show
pets[0].age += 1
show(pets[0], title="Lucky (one year later)")
{% endcapture %}
{% include python_run.md id="demo4" code=_py4 rows="11" %}

You can also call `show.clear()` to wipe the card area, and pass `title="…"` to override the card heading.

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `id` | `default` | Unique id — required if you have multiple runners on the same page |
| `code` | `print('Hello…')` | Initial code shown in the editor (use `{% raw %}{% capture %}…{% endcapture %}{% endraw %}` for multi-line) |
| `rows` | `6` | Initial height of the editor in lines |
| `init` | _empty_ | Python that runs once on page load (before the user clicks Run). Typically used to create bound objects. |
| `bound` | _empty_ | Name of a variable to mirror as a card above the editor; repaints after every Run. Forces the runtime to load eagerly. |
| `folded` | `false` | When `true`, the editor starts collapsed behind a click-to-expand toggle. |

### Built-in helpers (available inside the runner)

| Symbol | What it does |
|---|---|
| `print(...)` | Writes to the dark output pane |
| `Object(**kw)` | `SimpleNamespace`-style holder. `o = Object(name='Lucky', age=3)` then `o.age += 1`. Pair with `bound="o"` to mirror it as a live card. |
| `show(obj, title=None)` | Renders `obj` as a card in the grid below the output. Dicts and instances become labelled rows; lists/tuples render each item as its own card. |
| `show.clear()` | Removes all cards from the grid |
| `yaml.load(s)` | Parses a YAML string into Python objects (dicts, lists, scalars). Powered by `js-yaml` — loaded once, alongside the runtime. |

✅ Native Python syntax, runs entirely in the browser, no server.  
⚠️ MicroPython has a slim stdlib — no `numpy`, no `pandas`, no `requests`. For the full Python ecosystem you'd switch to Pyodide (~10 MB).

{% include backtotop.md %}
