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

That's it. The runner loads Python[^wasm] on first click (~300 KB, cached after). Next run is instant. CPython's `f'{x = }'` works here too — the runner rewrites it before MicroPython sees it.

```gherkin
Feature: A fenced block becomes a Python runner
  As a lowcoder
  I want to run Python in the browser with a Run button
  So that lessons are executable with no server

  Scenario: The block upgrades into a runner
    Given the runner above
    :::python
    self.runner: Object = Object._all(".lc-pyrun")[0]
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

```gherkin
Feature: The editor numbers lines, not wrapped rows
  As a learner reading my program on a phone
  I want line 16 to be line 16
  So that a tutor's "line 16" and my gutter agree

  Scenario: A long line keeps one number and scrolls sideways
    Given the first editor above
    :::python
    self.ta = Object._all("#lc-pyrun-first_run .lc-pyrun-code")[0]
    self.gutter = Object._all("#lc-pyrun-first_run .lc-pyrun-gutter-inner")[0]
    self.was = str(self.ta._el.value)
    :::
    When a line longer than the editor is typed
    :::python
    self.ta._el.value = "x = 1\n" + "# " + "a very long comment line, " * 12 + "\ny = 2"
    self.ta._el.dispatchEvent(js.Event.new("input"))
    :::
    Then the gutter counts three lines, one per newline
    :::python
    self.rows = str(self.gutter._el.textContent).split("\n")
    numbers = [r for r in self.rows if r]
    assert numbers == ["1", "2", "3"], f"gutter numbers {numbers}"
    :::
    And the editor does not wrap — the long line scrolls sideways
    :::python
    cs = js.window.getComputedStyle(self.ta._el)
    assert str(cs.whiteSpace) == "pre", f"white-space is {cs.whiteSpace}"
    assert int(self.ta._el.scrollWidth) > int(self.ta._el.clientWidth), "the long line did not overflow sideways"
    assert self.rows == ["1", "2", "3"], f"gutter rows {self.rows}"
    self.ta._el.value = self.was
    self.ta._el.dispatchEvent(js.Event.new("input"))
    :::

  Scenario: The editor grows with the program instead of scrolling inside
    Given the first editor above, with no rows= of its own
    :::python
    self.ta = Object._all("#lc-pyrun-first_run .lc-pyrun-code")[0]
    self.was = str(self.ta._el.value)
    :::
    When a twenty-line program is typed
    :::python
    self.ta._el.value = "\n".join(f"x{i} = {i}" for i in range(20))
    self.ta._el.dispatchEvent(js.Event.new("input"))
    :::
    Then every line is in view — nothing to scroll inside the editor
    :::python
    assert int(self.ta._el.rows) >= 20, f"rows {self.ta._el.rows}"
    assert int(self.ta._el.scrollHeight) <= int(self.ta._el.clientHeight) + 2, "the editor scrolls inside"
    self.ta._el.value = self.was
    self.ta._el.dispatchEvent(js.Event.new("input"))
    :::

  Scenario: Tab indents, and undo takes it back like typing
    Given the first editor above, with the caret at its start
    :::python
    self.ta = Object._all("#lc-pyrun-first_run .lc-pyrun-code")[0]
    self.was = str(self.ta._el.value)
    self.ta._el.focus()
    self.ta._el.setSelectionRange(0, 0)
    :::
    When Tab is pressed
    :::python
    ev = js.KeyboardEvent.new("keydown", {"key": "Tab", "bubbles": True, "cancelable": True})
    self.ta._el.dispatchEvent(ev)
    assert str(self.ta._el.value) == "    " + self.was, "Tab did not indent"
    :::
    Then undo brings the line back — the edit was typed, not assigned
    :::python
    js.document.execCommand("undo")
    assert str(self.ta._el.value) == self.was, f"undo left {self.ta._el.value[:20]!r}"
    :::
```
{: .feature tags="ui" status="pending" }

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
| `rows="3"` | Pins the editor height in lines; it then scrolls inside. Without it the editor fits its program (6 lines at least) and the page scrolls instead |
| `folded="true"` | Editor starts hidden behind a click-to-expand toggle — great for "here's the setup code" |
| `bound="o"` | Mirror a variable `o` as a live card above the editor — see the card section below |
| `init="…"` | One-liner Python that runs silently before the editor body |
| `# ---` in the code | Split marker: code above runs as init (hidden); code below is the editable body |
| `silent="true"` | No UI at all — runs once on page load, stdout swallowed, errors go to the console |
| `expected="…"` | After ▶ Run, compare printed output to this string. ✓ if it matches; counts toward the 🏆 score |
| `mypy="true"` | A 🩺 Dr. mypy (lite) button: the type hints checked, strict, in mypy's words — `"loose"` forgives missing hints |
| `readonly="true"` | A program to read, run and import, not to edit — a module the page documents (its title says so) |
| `subtitles="on"` | The 💬 Subtitles start shown: every part of the program says what it is (a parameter, a default value, a type hint, a loop variable, a call, a named argument…) on hover or tap. The button is on every runner; the knob only opens it first |

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

## 🧪 Doctests — click 🧪 Test, or call doctest

Every runner has a **🧪 Test** button next to ▶ Run. It runs every `>>>` example in every docstring — doctest's way: each docstring in its own namespace, a statement (`>>> p = Pet("Luna")`) expects nothing, an expression's `repr` (or what it prints) is compared with the lines below it — and shows one ✅ or ❌ row per example.

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

Hit **🧪 Test**. Try breaking a return value to see a red failure row.

**The course's files run as written.** The browser Python[^wasm] keeps no docstrings and has no `doctest` module, so the runner reads them from the program's text: `import doctest` and `doctest.testmod()` print CPython's report (silent when all pass, *Expected / Got* when not), `verbose=True` prints every *Trying / Expecting / ok* and the summary, and `__doc__`, `jump.__doc__`, `help(jump)` answer as in a terminal.

```python
"""
For an anxious coder
Who wants to be sure to check his code before sharing
"""


def jump(start: int, leap: int) -> int:
    """
    Makes an absolute jump from start.

    >>> jump(2, 3)
    5
    >>> jump(1, -1)
    2
    """
    return start + leap


if __name__ == "__main__":
    print(__doc__)
    import doctest
    doctest.testmod()
    help(jump)
```
{: .run #doctest_module }

**Doctest rules in brief:**

- Examples live inside `"""…"""` docstrings — a module's, a class's, a function's, a method's.
- `>>> statement` lines (`p = Pet("Luna")`) expect nothing; `... ` continues a line.
- The expected lines follow, up to a blank line — strings with their quotes: `'Lucky!'` not `Lucky!`.
- An expected `Traceback (most recent call last):` matches when the last line names the same error.

## 🩺 Dr. mypy (lite) — type hints, checked in the page

`mypy` cannot run in the browser, so the runner carries a small one that reads the hints from the text and answers in mypy's own words and codes: a `def` without its hints (`--strict`: *Function is missing a return type annotation  [no-untyped-def]*), a `return` against its hint (*Incompatible return value type*, *Return value expected*, *No return value expected*, *Missing return statement*), a literal argument against its parameter (*Argument 1 to "jump" has incompatible type "str"; expected "int"*). It never guesses: what is not written as a literal is not judged.

Two doors. `import mypy.api` and `mypy.api.run(["--strict", "--pretty", __file__])` return `(out, err, status)` as the real one does, so the PythonAnywhere recipe runs unchanged. And `mypy="true"` on a runner adds a **🩺 Dr. mypy** button: the verdict without running the program.

```python
def cut_budget(budget: float, cut: float):
    """ Cuts budget by cut%

    >>> cut_budget(100, .10)
    90.0
    """
    new_budget = budget * (1 - cut)
    return new_budget


if __name__ == "__main__":
    print("New budget: ", cut_budget(100, .1))

    import mypy.api
    out, err, status = mypy.api.run(["--strict", "--pretty", __file__])
    print("✅ Dr. mypy: no type errors" if status == 0 else f"❌ Dr. mypy:\n{out or err}")
```
{: .run #mypy_demo mypy="true" }

Press 🩺 Dr. mypy, then add `-> float` to the `def` line and press it again. A [✍️ pad](/components/mdpad) wears the same check on its python fences with `mypy="true"`: ⚠ on the line, mypy's words beside it.

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

## 🙋 `input()` — asking the reader

`input(prompt)` works. It doesn't freeze the tab, because it doesn't wait: the pass stops at the first unanswered question, the console shows the prompt with a box under it, and your answer restarts the script from the top with that answer already in hand. You see the finished transcript, exactly as a terminal would print it.

```python
name = input("your name: ")
print(f"Hello, {name}! 🎉")
```
{: .run #ask_name rows="3" }

A loop needs nothing special — answers are queued by **call order**, so the second time around the loop asks the second question:

```python
total = 0
while True:
    line = input("number (blank to stop): ")
    if not line:
        break
    total += int(line)
print("total:", total)
```
{: .run #ask_loop rows="8" }

Type `3`, Enter, `4`, Enter, then just Enter. Three questions, one transcript, `total: 7`.

> Because each pass re-runs the whole script, keep asking scripts side-effect free —
> the same rule as a pure function. Changing an answer mid-way re-asks from that
> question on, which is the behaviour readers expect.
{: .speaker-note }

**Q:** Your script asks three times inside a loop. How many times does the code actually run from the top?

- [ ] Once — the runner pauses the interpreter.
- [x] Four times — one pass per answer, plus the final pass that finishes.
- [ ] Three times, in three separate tabs.
- [ ] It doesn't run at all; `input()` is refused.
{: .quiz }

## 🎞️ Animation — `time.sleep` and `os.system('clear')`

A terminal animation runs as written: each `os.system('clear')` starts a
new frame, each `time.sleep(s)` holds it on screen. The script itself runs
in one go (the browser Python is single-threaded), then the console plays
the frames back with the same pauses — the last screen stays.

```python
import os
import time

for left in range(5, -1, -1):
    os.system('clear')
    print("🏁" + "-" * left + "🐶")
    time.sleep(0.3)
print("Lucky made it! 🎉")
```
{: .run #countdown rows="8" }

Pauses are capped at 2 s each, so a slip like `sleep(60)` never freezes a
lesson. The same frames play in an [inspector](/components/examples/model)'s
console when a verb animates.

## 🎵 Sound — `play()`

The browser has a synthesizer; every runner has `play`. A note is a name
(`"C5"`, `"F#4"`, `"Bb3"`, `"R"` for a rest) and a length in beats; calls queue
one after the other, so a loop is a melody. Any object with `note` and
`duration` works — a tuple, a dict, your own class, a dataset row.

```python
play.tempo = 180
play.wave = "square"            # sine, square, triangle, sawtooth
coin = [("B5", 1), ("E6", 3)]
for note, beats in coin:
    play(note, beats)
print("ping!")
```
{: .run #play_coin }

Audio needs one gesture from the reader — ▶ Run is one. The block records
what was queued (`data-lc-played`, `data-lc-last-note`), so a proof can
check a song without ears.

## 💬 Subtitles — what each part of the program is

Flip the **💬 switch** on the bar: the program is read for you, part by part. Hover a
word on a laptop, tap it on a phone, and the line under the bar says what it
is — *a parameter*, *a parameter with a default value*, *a type hint*, *the
loop variable*, *a function call*, *a named argument*, *a docstring*, *an
f-string*… in plain words. Press again to edit. `subtitles="on"` opens them
first, for a page that reads before it runs. The bar itself speaks softly: ▶ Run keeps its word, the rest are icons with a tooltip (🧪 Test, 🩺 Dr. mypy, 🧹 Clear), and 💬 shows its state.

```python
def greet(name: str, times: int = 1) -> str:
    """Says hello, as many times as asked.

    >>> greet("Lucky")
    'Hello, Lucky!'
    """
    hello = f"Hello, {name}!"
    for i in range(times):
        print(hello)
    return hello

greet("Lucky", times=2)
```
{: .run #subtitled subtitles="on" mypy="true" }

## 💡 Completion, and the same symbol lit

**Ctrl+Space** — or two letters of a word — lists what fits: keywords, the
helpers (`play`, `show`), the program's own names (its functions, classes,
variables, loop variables), and after a dot the attributes the program
already uses on that name (`play.` → `tempo`, `wave`, `stop()`). ↑ ↓ to
choose, Enter or Tab to take it, Esc to close. Nothing is invented: the
list is read from the program and the runner.

**Select a word** — a double-click does — and every other occurrence of it
lights up under the colours: where a variable is used, where a parameter
goes. Click elsewhere and the light goes out.

## 📦 A runner is a module — `import <id>`

Every runner has a pythonic id, so another runner on the page can import
it: `import helpers`, `from helpers import twice`. The imported program
runs once into its own namespace, with `__name__` set to its id — so a
demo under `if __name__ == "__main__":` stays quiet on import — and
`sys.modules` keeps it. Imports chain. Nothing is declared twice.

```python
def twice(x: int) -> int:
    """
    >>> twice(21)
    42
    """
    return 2 * x

if __name__ == "__main__":
    print("helpers, run on its own")
```
{: .run #helpers readonly="true" }

```python
from helpers import twice
print("twice(4) is", twice(4))
```
{: .run #uses_helpers }

Inside a call, the completion offers the function's parameters first —
`play(` → `note=`, `beats=` — read from its `def` on this page, on any
runner, or from the helpers.

**The palette**: keywords bold red, strings navy, numbers blue, comments
a light grey, operators brown, punctuation grey; a name wears the same
colour where it is defined and where it is called (`Note` the class,
`Note(...)` the call).

## 🧪 From a proof — `self.page.<id>`

A page's feature reaches a runner by its id, as every component: no
selector. What the block records is what a step reads.

| On `self.page.<id>` | What it says |
|---|---|
| `.output` | The output pane's text |
| `.played` · `.last_note` | What `play()` queued since the page opened |
| `.doctests.green` · `.passed` · `.total` | The last 🧪 Test's tally — the doctests verify the functions, the proof verifies the doctests are green |
| `.run()` · `.test()` | Press ▶ Run or 🧪 Test, as a person would |

## 🧰 Built-in helpers (always available)

| Symbol | What it does |
|---|---|
| `print(…)` | Writes to the dark output pane |
| `input(prompt)` | Asks in the console, then re-runs the script with the answer |
| `time.sleep(s)` · `os.system('clear')` | Animation: a pause and a new frame, played back after the run |
| `Object(**kw)` | Simple attribute holder. Pair with `bound=` to show a live card |
| `show(obj, title=None)` | Renders `obj` as a card below the output |
| `show.clear()` | Removes all cards |
| `show.grid(rows, title=None, height=300)` | Renders a sortable/filterable [📊 Datagrid](/components/datagrid) |
| `show.form(obj, title=None)` | Renders a [☷ Form](/components/form) |
| `play(note, beats=1)` · `play(notes)` | Plays a note (`"C5"`), or a list of notes, tuples, dicts or objects with `note` and `duration`, one after the other — `play.tempo`, `play.wave`, `play.stop()` |
| `yaml.load(s)` | Parses a YAML string into Python objects |

## ⚠️ Limits worth knowing

- **Slim stdlib.** The browser Python[^wasm] has `json`, `math`, `re`, `collections`, `itertools` and more — but no `numpy`, `pandas`, `requests`, or any C extension. For the full Python ecosystem you'd switch to Pyodide (~10 MB).
- **No real `doctest` or `mypy`.** The runner stands in for both from the program's text (above): `testmod()` and its report, `__doc__`, `help()`, and the type checks a beginner meets first. `importlib`-based recipes do not run here.
- **No filesystem.** `open()` doesn't work. Use `yaml.load()`, inline strings, or `show()` for data.
- **Single thread.** No `threading`, no `asyncio`. Code blocks the tab while running (fast scripts only). That's why `input()` re-runs the script instead of waiting — see above.
- **No persistence.** Variables reset between page loads. Use `bound=` to keep state visible between runs within the same session.

## 🏁 Final exam — boss level

**Q:** Which of these are TRUE about the Python runner? (Pick all that apply.)

- [x] `{: .run }` goes on the line right after the closing fence.
- [x] `show.grid(rows)` renders a sortable datagrid.
- [ ] The runner has full access to `numpy` and `pandas`.
- [x] `# ---` in the code splits init from the editable body.
- [ ] `silent="true"` shows a minimal output pane but suppresses errors.
{: .quiz multi="true" }

**Q:** A learner hits ▶ Run and nothing happens for 3 seconds, then the output appears. What's going on?

- [ ] The server is slow — try at midnight.
- [x] Python is loading into the browser for the first time (~300 KB). Subsequent runs are instant.
- [ ] The learner's code has an infinite loop. Always.
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
