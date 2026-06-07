# 🦄 Feature

Render Gherkin BDD scenarios as styled cards. Embed `:::python ... :::` blocks directly after each step to attach a runnable implementation — the card gets a **▶ Run** button and the code appears as expandable step panels. `self.page`, `Dataset`, `Block`, `Datagrid`, `Chart`, and `FeatureCard` are available in every step.

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
{: .feature tags="smoke,auth" }

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
    self.celsius = 100
    :::
    When converted to Fahrenheit using (C × 9/5) + 32
    :::python
    self.fahrenheit = (self.celsius * 9 / 5) + 32
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
{: .feature id="temp_feature" status="pending" tags="math,utils" }

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
    self.items = []
    :::
    When I check if it is valid
    :::python
    self.result = len(self.items) > 0
    :::
    Then validation should fail
    :::python
    assert self.result == False, "Expected validation to fail for empty list"
    :::
```
{: .feature id="list_feature" status="pending" tags="validation" }

## 🔬 Page access probe

Steps can reach any component on the page via `self.page.<id>`. The dataset and chart below have ids — the card probes them.

```json
[{"label":"A","value":3},{"label":"B","value":7},{"label":"C","value":5}]
```
{: .dataset id="probe_data" }

[Probe chart](#)
{: .chart bind="probe_data" type="bar" x="label" y="value" id="probe_chart" }

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
    And its bind references probe_data
    :::python
    assert self.page.probe_chart.bind == self.page.probe_data, \
        f"bind mismatch: {self.page.probe_chart.bind._id!r}"
    :::
    Then it has rendered bars
    :::python
    assert self.page.probe_chart.bar_count > 0, f"got {self.page.probe_chart.bar_count} bars"
    :::
    And bar heights reflect the data order (A < C < B)
    :::python
    bars = self.page.probe_chart.bars
    assert bars[0].value < bars[2].value < bars[1].value, \
        f"expected 3 < 5 < 7, got {[b.value for b in bars]}"
    :::
```
{: .feature id="page_probe" status="pending" tags="probe" }

## 🖱️ Button with Python handler

Click the button to highlight the tallest bar. The `:::python:::` fence after the `.button` IAL defines the click handler; `button.page` gives full page access.

[Highlight max bar ▶](#)
{: .button data-lc-id="highlight_btn" }

```python
def on_click(button):
    bars = button.page.probe_chart.bars
    max_bar = max(bars, key=lambda b: b.value)
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
  Scenario: Handler identifies the tallest bar correctly
    Given the button and chart are present
    :::python
    assert self.page.highlight_btn, "highlight_btn not found"
    assert self.page.probe_chart,   "probe_chart not found"
    :::
    When the handler logic runs
    :::python
    bars = self.page.probe_chart.bars
    self.max_bar = max(bars, key=lambda b: b.value)
    :::
    Then bar B has the highest value
    :::python
    assert self.max_bar.value == 7.0, f"expected 7.0, got {self.max_bar.value}"
    :::
    And it is not bar A or bar C
    :::python
    assert self.max_bar.value > self.page.probe_chart.bars[0].value
    assert self.max_bar.value > self.page.probe_chart.bars[2].value
    :::
```
{: .feature id="btn_handler" status="pending" tags="button,probe" }

## 🥸 How to write one

After each Gherkin step, add a `:::python ... :::` block with the implementation:

````markdown
```gherkin
Feature: My feature
  Scenario: A scenario
    Given some precondition
    :::python
    self.x = 42
    :::
    When an action happens
    :::python
    self.y = self.x * 2
    :::
    Then the result is correct
    :::python
    assert self.y == 84
    :::
```
{: .feature id="my_feature" status="pending" tags="example" }
````

- `:::python ... :::` is parsed from the Gherkin block — not rendered as a separate code block.
- **Shared context**: `self` is the same object across all steps in a run.
- Available without import: `self.page`, `Dataset`, `Block`, `Datagrid`, `Chart`, `FeatureCard`. Inherit from `Block` for custom wrappers.
- Give the `.feature` card an `id` to make it reachable as `self.page.my_feature` from any feature step.
- Click a step row to **expand its implementation** inline.

## 🎛️ Knobs

| Block | Attribute | Values | What it does |
|---|---|---|---|
| `.feature` | `status="…"` | `passing` · `failing` · `pending` | Border colour and badge; updated live after a run |
| `.feature` | `tags="…"` | comma-separated | Chips in the card header |
| `.feature` | `id="…"` | Python-compatible id | Makes the card reachable as `self.page.<id>` in any step |
