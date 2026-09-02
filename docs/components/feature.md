# 🦄 Feature

Render Gherkin BDD scenarios as styled cards. Embed `:::python ... :::` blocks directly after each step to attach a runnable implementation — the card gets a **▶ Run** button and the code appears as expandable step panels. `self.page`, `Dataset`, `Block`, `Datagrid`, `Chart`, and `Feature` are available in every step.

> **Visibility:** a `.feature` is **hidden by default** — it's a spec/test, not learner-facing content, so it stays out of sight and out of the page's flow. Add `visible="true"` (or a `.visible` class) to show a card; every example on this page opts in explicitly. Inside the **editor preview**, features always show so you can author them.

## 📺 Display-only (no runner)

```gherkin
Feature: User login
    As a curious lowcoder to be
    I want to see the dashboard 
    So that I can decide quickly
  Scenario: Successful login
    Given I am on the login page
    When I enter valid credentials
    Then I should see the dashboard
```
{: .feature visible="true" tags="spec" }

## 🏃🏻‍♀️ With runnable steps

Click a step row to see its implementation. Click **▶ Run** to execute all steps.

```gherkin
Feature: Temperature converter
  As a developer working with temperature data
  I want to convert between Celsius and Fahrenheit
  So that I can display temperatures in the right unit
  Scenario: Celsius to Fahrenheit
    Given a temperature of 100 degrees Celsius
    :::python
    self.celsius: int = 100
    :::
    When converted to Fahrenheit using (C × 9/5) + 32
    :::python
    self.fahrenheit: float = (self.celsius * 9 / 5) + 32
    :::
    Then the result should be 212
    :::python
    assert self.fahrenheit == 212.0, f"Got {self.fahrenheit}"
    :::
    And zero Celsius equals 32 Fahrenheit
    :::python
    assert (0 * 9 / 5) + 32 == 32.0
    :::
```
{: .feature visible="true" #temp_feature status="passing" tags="lifecycle" celebration="true" }

`self` is shared across all steps in a run — state set in one step (`self.celsius`) is available in later ones.

## 🔍 Negative assertion

```gherkin
Feature: List validator
  As a data validation engineer
  I want to detect empty lists early
  So that invalid data does not propagate downstream
  Scenario: Reject empty lists
    Given an empty list
    :::python
    self.items: list = []
    :::
    When I check if it is valid
    :::python
    self.result: int = len(self.items) > 0
    :::
    Then validation should fail
    :::python
    assert self.result == False, "Expected validation to fail for empty list"
    :::
```
{: .feature visible="true" #list_feature status="pending" tags="spec" }

## 🔬 Page access probe

Steps can reach any component on the page via `self.page.<id>`. The dataset and chart below have ids — the card probes them.

```json
[{"label":"A","value":3},{"label":"B","value":7},{"label":"C","value":5}]
```
{: .dataset #probe_data }

[Probe chart](#)
{: .chart bind="probe_data" type="bar" x="label" y="value" #probe_chart }

```gherkin
Feature: Page component access
  As a test author
  I want to reach any named component via self.page
  So that I can assert on the UI without leaving Python
  Scenario: Access probe_chart from Python steps
    Given probe_chart is on this page
    :::python
    assert self.page.probe_chart, "probe_chart not found — is id set?"
    :::
    And it is visible
    :::python
    assert self.page.probe_chart.visible, "probe_chart not visible"
    :::
    And its type and axes match the knobs
    :::python
    assert self.page.probe_chart.type == "bar",   f"type: {self.page.probe_chart.type}"
    assert self.page.probe_chart.x    == "label", f"x: {self.page.probe_chart.x}"
    assert self.page.probe_chart.y    == "value", f"y: {self.page.probe_chart.y}"
    :::
    And its source references probe_data
    :::python
    assert self.page.probe_chart.source == self.page.probe_data, \
        f"source mismatch: {self.page.probe_chart.source._id!r}"
    :::
    Then it has rendered bars
    :::python
    assert self.page.probe_chart.bar_count > 0, f"got {self.page.probe_chart.bar_count} bars"
    :::
    And bar heights reflect the data order (A < C < B)
    :::python
    bars: list = self.page.probe_chart.bars
    assert bars[0].value < bars[2].value < bars[1].value, \
        f"expected 3 < 5 < 7, got {[b.value for b in bars]}"
    :::
```
{: .feature visible="true" #page_probe status="pending" tags="spec" }

## 🖱️ Button with Python handler

Click the button to highlight the tallest bar; click again to reset. The `:::python:::` fence after the `.button` IAL defines the click handler; `button.page` gives full page access.

[Highlight max bar ▶](#)
{: .button #highlight_btn }

```python
def on_click(button):
    bars = button.page.probe_chart.bars
    max_bar = max(bars, key=lambda b: b.value)
    if max_bar.color == "orange":          # already highlighted → reset
        for bar in bars:
            bar.color = "#0066cc"
        button.text = "Highlight max bar ▶"
        button.color = ""
    else:                                  # highlight the tallest bar
        max_bar.color = "orange"
        button.text = f"Max is {int(max_bar.value)} — click to reset"
        button.color = "muted"
```
{: .onclick }

```gherkin
Feature: Button handler
  As a page author
  I want to attach Python to a button
  So that clicking it modifies the chart without writing JavaScript
  Scenario: Clicking the button highlights the tallest bar
    Given the button and chart are present
    :::python
    assert self.page.highlight_btn, "highlight_btn not found"
    assert self.page.probe_chart,   "probe_chart not found"
    :::
    When the button is clicked from a clean state
    :::python
    for bar in self.page.probe_chart.bars:   # reset so one click highlights
        bar.color = "#0066cc"
    self.page.highlight_btn.click()
    :::
    Then bar B is painted orange
    :::python
    err: str = self.page.highlight_btn._attr("data-lc-err") or ""
    bars: list = self.page.probe_chart.bars
    self.max_bar: Object = max(bars, key=lambda b: b.value)
    assert self.max_bar.color == "orange", f"expected orange, got {self.max_bar.color!r} | click_err={err!r}"
    :::
    And the button label shows the max value
    :::python
    assert "Max is 7" in self.page.highlight_btn.text, \
        f"unexpected label: {self.page.highlight_btn.text!r}"
    :::
    And it is bar B not A or C
    :::python
    bars: list = self.page.probe_chart.bars
    assert self.max_bar.value > bars[0].value
    assert self.max_bar.value > bars[2].value
    :::
```
{: .feature visible="true" #btn_handler status="pending" tags="code" }

## 🎉 Celebration & state — green that opens doors

Two knobs and a verb make a feature card the page's heartbeat:

- **State**: a card with an `#id` publishes `id.passing` / `id.status` to
  the page's [cells](/components/cells) — any block can wear
  `visible="= audit.passing"` and unfold the moment the run turns green.
- **`celebration="true"`**: the card's **first** honest red→green earns a
  confetti burst. Re-running an already-green card celebrates nothing, and
  reduced-motion users get a quiet ✨ instead of the storm. The **Celsius
  card above wears it** — press its ▶ Run and watch; press it again and
  nothing falls, because nothing was earned the second time.
- **`confetti()`**: the authored version — any component speaks it from a
  step (`self.page.audit.confetti()`), a `.button`, anywhere. Put it after
  the asserts of a final step: it only fires when everything above survived.

The engine never celebrates on its own — like scores, celebrations belong
to the page.

## 🥸 How to write one

After each Gherkin step, add a `:::python ... :::` block with the implementation:

````markdown
```gherkin
Feature: My feature
  Scenario: A scenario
    Given some precondition
    :::python
    self.x: int = 42
    :::
    When an action happens
    :::python
    self.y: int = self.x * 2
    :::
    Then the result is correct
    :::python
    assert self.y == 84
    :::
```
{: .feature visible="true" #my_feature status="pending" tags="spec" }
````

- `:::python ... :::` is parsed from the Gherkin block — not rendered as a separate code block.
- **Shared context**: `self` is the same object across all steps in a run.
- Available without import: `self.page`, `Dataset`, `Block`, `Datagrid`, `Chart`, `Feature`. Inherit from `Block` for custom wrappers.
- Give the `.feature` card an `id` to make it reachable as `self.page.my_feature` from any feature step.
- Click a step row to **expand its implementation** inline.

## 🎨 Given/When/Then, in the flow's colours

A step's words carry the same grammar an [event flow](/components/event_flow)
draws, so they wear the same paint. The **keyword** decides the colour —
nothing is guessed from the words themselves — and only **marked** words are
painted, so the author chooses what matters:

| keyword | paints marked words as |
|---|---|
| `Given` | 📦 `data` — shown on a 🖥️  **ui**{: .ui }|
| `When` | 🗣️ `command` — what **someone**{: .user } does |
| `Then` | ⚡ `event` — what became true |

`And` / `But` inherit the last real keyword. Mark a word with **`**bold**`**
or `` `backticks` ``, and override the colour with an IAL right after it:

```gherkin
Feature: A step says what it means
  Scenario: The colours follow the keyword
    Given `Biscuit` is shown on the **dog_grid**{: .ui }
    :::python
    self.here: bool = True
    :::
    When **the family**{: .user } **names a dog**
    :::python
    self.named: bool = True
    :::
    Then `Biscuit`{: .data } **is open**{: .event } for a visit
    :::python
    assert self.here and self.named
    :::
```
{: .feature #paint_demo visible="true" status="pending" tags="code" }

Unmarked words stay plain; a marked word with no colour in play renders as
ordinary **bold** or `code`. That is the whole rule — a check is one beat of
the workflow, written down.

## 🏷️ Where the tags show up

A page's tags come from its feature cards — including the hidden ones. They
now appear in three places, all from that one source:

| Where | Looks like |
|---|---|
| Beside the page title | small grey pills inside the `<h1>`, on the same line |
| On the folder card | blue chips that also **filter** the folder |
| In the card header | one chip per tag on a visible card |

Nothing to write for the first two — tag a feature and the page wears it. A
page with no tagged feature keeps a bare title, which is the honest signal
that it has nothing claimed about it yet.

## 🎛️ Knobs

| Block | Attribute | Values | What it does |
|---|---|---|---|
| `.feature` | `status="…"` | `passing` · `failing` · `pending` | Border colour and badge; updated live after a run |
| `.feature` | `tags="…"` | comma-separated | Chips in the card header |
| `.feature` | `#<id>` | Python-compatible id | Makes the card reachable as `self.page.<id>` in any step |

## 🧠 Quick check

**Q:** A `.feature` is hidden by default. Why hide your beautiful specs?

- [x] They're tests, not lesson content — they run quietly and prove things still work.
- [ ] Specs are introverts.
- [ ] To build suspense before the big reveal.
- [ ] The author is embarrassed by their Gherkin.
{: .quiz }
