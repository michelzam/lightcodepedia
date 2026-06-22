# 🐍 Run

Write Python in the browser and run it on the spot — no install, no server, nothing to configure.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode. Every example below is live; try them as you read.

## 🏃 Try it now

Here's a Python runner. Hit ▶ Run, read the output, change something, run again.

```python
def greet(name):
    print(f"Hello, {name}! 🎉")

greet("Lightcoder")
greet("World")
```
{: .run #first_run }

That's it. The runner loads Python[^wasm] on first click (~300 KB, cached after). Next run is instant.

```gherkin
Feature: A fenced block becomes a Python runner
  As a lowcoder
  I want to run Python in the browser with a Run button
  So that lessons are executable with no server

  Scenario: The block upgrades into a runner
    Given the runner above
    :::python
    self.runner = Object._all(".lc-pyrun")[0]
    :::
    When the page has upgraded it
    Then it is a visible runner
    :::python
    assert self.runner.visible
    :::
```
{: .feature tags="code" status="passing" }

> Ask yourself: "What do you expect to see before you click ▶ Run?"
> Pause. Predict, then run it. The prediction habit is the whole lesson.
{: .speaker-note }

**Q:** You changed `"World"` to `"Python"` and hit ▶ Run. What do you see?

- [ ] Nothing — you need to save the file first.
- [x] `Hello, Python! 🎉` in the output.
- [ ] A syntax error because you touched the code.
- [ ] A terminal opens and asks for your password.
{: .quiz }

## 🛠️ How to make a runner

Write a Python fenced block, then put `{: .run }` on the very next line:

````markdown
```python
print("hello")
```
{: .run }
````

That's the whole syntax. The page upgrades the static code block into a live editor + output pane.

> The IAL[^ial] `{: .run }` must be on the line directly after the closing fence — no blank line between.
> That's the only gotcha.
{: .speaker-note }

**Q:** Which line makes a fenced code block into a live runner?

- [ ] `# run this`
- [ ] `<!-- run -->`
- [x] `{: .run }` on the line right after the closing fence
- [ ] Double-clicking the code block. It just knows.
{: .quiz }

## 🔧 Knobs to tune

| Attribute | What it does |
|---|---|
| `#id` | Optional — auto-assigned if omitted; add one only to reference this runner from elsewhere |
| `rows="3"` | Editor height in lines (default 6) |
| `folded="true"` | Editor starts hidden behind a click-to-expand toggle — great for "here's the setup code" |
| `bound="o"` | Mirror a variable `o` as a live card above the editor — see the card section below |
| `init="…"` | One-liner Python that runs silently before the editor body |
| `# ---` in the code | Split marker: code above runs as init (hidden); code below is the editable body |
| `silent="true"` | No UI at all — runs once on page load, stdout swallowed, errors go to the console |
| `expected="…"` | After ▶ Run, compare printed output to this string. ✓ if it matches; counts toward the 🏆 score |

**Q:** You want the editor to start collapsed so it doesn't intimidate beginners. Which attribute do you add?

- [x] `folded="true"`
- [ ] `hidden="true"`
- [ ] `collapsed="true"`
- [ ] Put the code in a `<details>` tag and hope for the best.
{: .quiz }

## ✂️ Init code — the `# ---` split

Sometimes you need setup code that shouldn't clutter the learner's editor. Put it above a `# ---` line:

```python
# this runs silently on load — learners never edit it
dogs = ["Lucky", "Wanda", "Max"]
# ---
# learner edits this part
for d in dogs:
    print(d)
```
{: .run #init_split rows="4" }

Everything above `# ---` is init — runs once, invisible to the learner. Everything below is the editable body.

> Useful for anything the lesson *depends on* but shouldn't distract from:
> pre-loaded data, helper functions, imports.
{: .speaker-note }

## 🤫 Silent mode — background setup

`silent="true"` runs the block at page load with no visible UI. Use it to pre-compute something or render into an element elsewhere on the page.

```python
from js import document
el = document.getElementById("hello_target")
if el is not None:
    el.innerHTML = "✨ rendered by silent Python ✨"
```
{: .run silent="true" }

(loading…)
{: #hello_target }

The text above was written by the invisible runner above. No button, no output pane — just the effect.

## 🃏 Cards — visualizing objects

Every runner has a `show(obj)` helper that renders an object as a card below the output. Chain multiple `show()` calls to build a grid of cards.

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
{: .run #yaml_cards rows="18" }

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
```
{: .run #custom_class rows="10" }

For a sortable, filterable table instead of cards, use `show.grid(rows)`:

```python
dogs = [
    {"name": "Lucky", "age": 3, "breed": "Beagle"},
    {"name": "Wanda", "age": 5, "breed": "Poodle"},
    {"name": "Max",   "age": 2, "breed": "Husky"},
]
show.grid(dogs, title="Shelter dogs", height=200)
print("Grid rendered.")
```
{: .run #show_grid rows="8" }

## 🧲 Bound card — a live mirrored object

`bound="o"` keeps a card permanently in sync with a Python object. Every ▶ Run repaints the card. The object lives in memory; no DOM calls inside Python.

```python
o = Object(name='Lucky', age=3, breed='Beagle')
# ---
o.age += 1
print(o)
```
{: .run bound="o" folded="true" rows="3" #bound_demo }

`Object(**kw)` is a built-in `SimpleNamespace`-style holder. Pair it with `bound="o"` and the card above the editor reflects every mutation.

> The card demo is often more memorable than the output.
> "Your data has a face now" — it clicks for visual learners.
{: .speaker-note }

## 🧪 Doctests — click 🧪 Test

Every runner has a **🧪 Test** button next to ▶ Run. It finds `>>> expr` lines inside docstrings, runs each expression, and compares `repr(value)` to the expected line below it.

```python
def fact(n):
    """
    >>> fact(0)
    1
    >>> fact(5)
    120
    >>> fact(10)
    3628800
    """
    return 1 if n <= 1 else n * fact(n - 1)

def greet(name):
    """
    >>> greet("Lucky")
    'Hello, Lucky!'
    """
    return "Hello, " + name + "!"
```
{: .run #doctests_demo rows="18" }

Hit **▶ Run** first (so the functions exist), then **🧪 Test**. Try breaking a return value to see a red failure row.

**Doctest rules in brief:**

- Tests live inside `"""…"""` docstrings.
- Each test is `>>> expression` followed by one line of expected output.
- Expected output is compared against `repr(value)` — strings need their quotes: `'Lucky!'` not `Lucky!`.
- `None`-returning calls need no expected line (or a blank line).

## ⌨️ REPL — line-by-line exploration

The REPL[^repl] is the interactive prompt — type a Python expression, press Enter, see the result immediately. Great for exploration; not for multi-line `def`/`class`/`for` (use a `.run` block for those).

```python
```
{: .repl #main_repl }

Try typing these one at a time:

| You type | What happens |
|---|---|
| `2 + 2` | `4` — expression evaluated, repr printed |
| `name = "Lucky"` | nothing — assignment is a statement |
| `name` | `'Lucky'` — with quotes, that's `repr` |
| `len(name)` | `5` |
| `[1,2,3]*3` | `[1, 2, 3, 1, 2, 3, 1, 2, 3]` |
| `1 / 0` | `ZeroDivisionError` — caught and shown |

Use ↑ / ↓ to walk history.

A pre-warmed REPL with `math` already imported:

```python
import math
print("math loaded!")
```
{: .repl #prewarmed }

**Q:** You type `x = 5` in the REPL and press Enter. What do you see?

- [ ] `5`
- [ ] `x = 5`
- [x] Nothing — assignment is a statement, not an expression.
- [ ] A pop-up asking if you want to save the variable.
{: .quiz }

## 🧰 Built-in helpers (always available)

| Symbol | What it does |
|---|---|
| `print(…)` | Writes to the dark output pane |
| `Object(**kw)` | Simple attribute holder. Pair with `bound=` to show a live card |
| `show(obj, title=None)` | Renders `obj` as a card below the output |
| `show.clear()` | Removes all cards |
| `show.grid(rows, title=None, height=300)` | Renders a sortable/filterable [📊 Datagrid](/components/datagrid) |
| `show.form(obj, title=None)` | Renders a [📝 Form](/components/form) |
| `yaml.load(s)` | Parses a YAML string into Python objects |

## ⚠️ Limits worth knowing

- **Slim stdlib.** The browser Python[^wasm] has `json`, `math`, `re`, `collections`, `itertools` and more — but no `numpy`, `pandas`, `requests`, or any C extension. For the full Python ecosystem you'd switch to Pyodide (~10 MB).
- **No filesystem.** `open()` doesn't work. Use `yaml.load()`, inline strings, or `show()` for data.
- **Single thread.** No `threading`, no `asyncio`. Code blocks the tab while running (fast scripts only).
- **No persistence.** Variables reset between page loads. Use `bound=` to keep state visible between runs within the same session.

## 🏁 Final exam — boss level

**Q:** Which of these are TRUE about the Python runner? (Pick all that apply.)

- [x] `{: .run }` goes on the line right after the closing fence.
- [x] `show.grid(rows)` renders a sortable datagrid.
- [ ] The runner has full access to `numpy` and `pandas`.
- [x] `# ---` in the code splits init from the editable body.
- [ ] `silent="true"` shows a minimal output pane but suppresses errors.
{: .quiz multi="true" }

**Q:** A student hits ▶ Run and nothing happens for 3 seconds, then the output appears. What's going on?

- [ ] The server is slow — try at midnight.
- [x] Python is loading into the browser for the first time (~300 KB). Subsequent runs are instant.
- [ ] The student's code has an infinite loop. Always.
- [ ] Chrome blocked it. Always Chrome.
{: .quiz }

**Q:** You want `for i in range(5): print(i)` to verify against expected output `0\n1\n2\n3\n4`. Which attribute do you add to `{: .run }`?

- [ ] `verify="0\n1\n2\n3\n4"`
- [x] `expected="0\n1\n2\n3\n4"`
- [ ] `assert="0\n1\n2\n3\n4"`
- [ ] `correct="0\n1\n2\n3\n4"` — quiz rules apply everywhere

  > `expected=` compares trimmed stdout to the string you provide, then reports to the 🏆 score tracker.
{: .quiz }

[^wasm]: **WebAssembly (WASM)** — a binary format that runs near-native speed in every modern browser. The Python engine here is MicroPython compiled to WASM: a lean, standards-compliant Python 3 interpreter (~300 KB gzipped) that needs no install and no server.

[^ial]: **IAL (Inline Attribute List)** — kramdown's `{: .class key="value" }` syntax. Put it on its own line right after a fenced block (or any block) to attach HTML attributes — id, classes, custom data. All components on this site are activated this way.

[^repl]: **REPL** — Read → Eval → Print → Loop. The interactive Python prompt (`>>>`) where you type one expression, see the result, and type the next. Same thing you get if you run `python3` in a terminal.
