{% include topbar.md title="🐍 Run" %}

Edit Python in the browser and run it on the spot. Powered by **MicroPython compiled to WebAssembly** (~300 KB, loaded on first ▶ Run, cached after). To just **display** code without running it, see [💻 Code](/components/code).

## Tiniest runner — `{: .run }` on a fenced block

Add `{: .run }` on the line right after a Python fenced block's closing fence. The page upgrades the block into a live editor + runner.

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

## Knobs on `{: .run … }`

| Attribute | Description |
|---|---|
| `id="myrunner"` | Required if you have multiple runners on the same page |
| `rows="3"` | Editor height in lines (default 6) |
| `folded="true"` | Editor starts collapsed behind a click-to-expand toggle |
| `bound="o"` | Mirror the variable `o` as a card above the editor; repaints after every Run |
| `init="…"` | Single-line Python that runs once on page load |
| `# ---` (inside the block) | Magic separator: above = init, below = editor body |

## Bound card — a live in-memory object

A pre-defined `Object` (a `SimpleNamespace`-style holder, baked into the runner) gets created on load and rendered as a card. The editor below is folded — click to open, hit ▶ Run, watch the card update.

```python
o = Object(name='🐕 Lucky', age=3)
# ---
o.age += 1
print(o)
```
{: .run bound="o" folded="true" rows="3" }

The Python only mutates an in-memory object (`o.age += 1`). The page redraws because `bound="o"` registered the card. No view code, no Streamlit, no DOM calls inside Python.

## Cards from YAML

Every runner exposes a built-in `show(obj)` helper that renders a card in a grid below the output. Combined with `yaml.load()`, you can describe data in YAML and visualize it:

```python
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
```
{: .run id="yaml-cards" rows="16" }

Custom classes work too — `show()` reads `__dict__`:

```python
class Pet:
    def __init__(self, name, age, breed):
        self.name = name
        self.age = age
        self.breed = breed

pets = [Pet("Lucky", 3, "Beagle"), Pet("Wanda", 5, "Poodle")]
for p in pets:
    show(p)

pets[0].age += 1
show(pets[0], title="Lucky (one year later)")
```
{: .run id="custom-class" rows="11" }

## Doctests — click 🧪 Test

Every runner has a **🧪 Test** button next to ▶ Run. It scans the editor for `>>> expr` lines inside triple-quoted docstrings, runs each one, and compares `repr(value)` to the expected output on the next line. Pass/fail rendered inline.

```python
def fact(n: int) -> int:
    """
    Recursive factorial.

    >>> fact(0)
    1
    >>> fact(1)
    1
    >>> fact(5)
    120
    >>> fact(10)
    3628800
    """
    return 1 if n <= 1 else n * fact(n - 1)


def greet(name: str) -> str:
    """
    >>> greet("Lucky")
    'Hello, Lucky!'
    >>> greet("")
    'Hello, !'
    """
    return "Hello, " + name + "!"
```
{: .run id="doctests-demo" rows="22" }

▶ Run executes the module (no output unless you call something). 🧪 Test runs every `>>>` line and shows a pass/fail summary. Try editing one of the expected values to see a red row.

### Doctest rules

- Tests live inside `"""…"""` or `'''…'''` docstrings.
- Each test is `>>> <expression>` followed by **one line** of expected output.
- The expression is `eval()`-d. Its **`repr()`** is compared against the expected line (so strings need their quotes: `'Hello, Lucky!'` not `Hello, Lucky!`).
- Expressions that return `None` should have a blank line after — or just nothing.
- `print(...)`-based doctests aren't captured (the runner uses `eval`, not stdout). Test return values instead.
- Function definitions and module-level code run first, so doctests see your full namespace.

## Built-in helpers (available inside every runner)

| Symbol | What it does |
|---|---|
| `print(...)` | Writes to the dark output pane |
| `Object(**kw)` | `SimpleNamespace`-style holder. Pair with `bound="…"` to mirror as a card. |
| `show(obj, title=None)` | Renders `obj` as a card in the grid below the output |
| `show.clear()` | Removes all cards from the grid |
| `yaml.load(s)` | Parses YAML into Python objects (powered by `js-yaml`) |
| 🧪 Test button | Scans the editor for `>>>` doctests, runs each, compares `repr(value)` against expected |

## When `{: .run }` isn't enough — explicit `{% raw %}{% include python_run.md %}{% endraw %}`

Fall back to the include form when you need a multi-line `init`, or when the editor code itself contains a `# ---` line you don't want interpreted as the separator.

{% raw %}
```liquid
{% capture _py %}
def fact(n):
    return 1 if n <= 1 else n * fact(n - 1)

for i in range(1, 8):
    print(f"{i}! = {fact(i)}")
{% endcapture %}
{% include python_run.md id="explicit" code=_py rows="8" %}
```
{% endraw %}

{% capture _py %}
def fact(n):
    return 1 if n <= 1 else n * fact(n - 1)

for i in range(1, 8):
    print(f"{i}! = {fact(i)}")
{% endcapture %}
{% include python_run.md id="explicit" code=_py rows="8" %}

✅ Native Python syntax, runs entirely in the browser, no server.  
⚠️ MicroPython's stdlib is slim — no `numpy`, no `pandas`, no `requests`. For the full Python ecosystem you'd switch to Pyodide (~10 MB).

{% include backtotop.md %}
