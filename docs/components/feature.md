---
---
# 🦄 Feature

Render Gherkin BDD scenarios as styled cards. Embed `:::python ... :::` blocks directly after each step to attach a runnable implementation — the card gets a **▶ Run** button and the code appears as expandable step panels. `self.page`, `Dataset`, and all jssteps classes are available in every step.

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
{: .feature id="temp-feature" status="pending" tags="math,utils" }

`self` is shared across all steps in a run — state set in one step (`self.celsius`) is available in later ones.

## 😰 Failing step example

```gherkin
Feature: List validator
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
{: .feature id="list-feature" status="pending" tags="validation" }

## 🔬 DOM bridge probe

Can MicroPython steps reach the browser DOM via `import js`?

```gherkin
Feature: MicroPython JS bridge
  Scenario: DOM access from Python steps
    Given the js module is importable
    :::python
    import js
    self.js = js
    assert self.js is not None, "import js failed"
    :::
    When I read document.title
    :::python
    self.title = self.js.document.title
    assert isinstance(self.title, str), f"document.title is not a string: {repr(self.title)}"
    :::
    Then I can query a DOM element
    :::python
    self.el = self.js.document.querySelector("body")
    assert self.el is not None, "querySelector('body') returned None"
    :::
    And I can read an element attribute
    :::python
    tag = self.el.tagName
    assert tag is not None, f"tagName returned None — got: {repr(tag)}"
    :::
```
{: .feature id="js-bridge-feature" status="pending" tags="probe,js-bridge" }

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
{: .feature id="my-feature" status="pending" tags="example" }
````

- `:::python ... :::` is parsed from the Gherkin block — not rendered as a separate code block.
- **Shared context**: `self` is the same object across all steps in a run.
- All jssteps classes are available without import: `self.page`, `Dataset`, `Datagrid`, `Chart`, `FeatureCard`.
- Give the `.feature` card an `id` to make it reachable as `self.page.my_feature` from other `.jssteps` blocks.
- Click a step row to **expand its implementation** inline.

## 🎛️ Knobs

| Block | Attribute | Values | What it does |
|---|---|---|---|
| `.feature` | `status="…"` | `passing` · `failing` · `pending` | Border colour and badge; updated live after a run |
| `.feature` | `tags="…"` | comma-separated | Chips in the card header |
| `.feature` | `id="…"` | Python-compatible id | Makes the card reachable as `self.page.<id>` in jssteps |
