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

## 😰 Failing step example

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

## 🔬 DOM bridge probe

Can MicroPython steps reach page components via `self.page`?

```gherkin
Feature: MicroPython JS bridge
  As a test author
  I want to access page components via self.page
  So that I can write UI assertions without raw JavaScript
  Scenario: DOM access via self.page
    Given temp-feature card is reachable via self.page
    :::python
    self.card = self.page.temp_feature
    assert self.card.exists, "temp-feature not found — is id set?"
    :::
    When I read its data-lc-id attribute
    :::python
    id_val = self.card.attr("data-lc-id")
    assert id_val == "temp_feature", f"expected 'temp_feature', got {repr(id_val)}"
    :::
    Then the card is visible
    :::python
    assert self.card.visible, "temp-feature card is not visible"
    :::
    And I can reach a child element inside it
    :::python
    header = self.card.q(".lc-feature-header")
    assert header.exists, ".lc-feature-header not found in card"
    :::
```
{: .feature id="js_bridge_feature" status="pending" tags="probe,js-bridge" }

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
- All jssteps classes are available without import: `self.page`, `Dataset`, `Datagrid`, `Chart`, `FeatureCard`.
- Give the `.feature` card an `id` to make it reachable as `self.page.my_feature` from other `.jssteps` blocks.
- Click a step row to **expand its implementation** inline.

## 🎛️ Knobs

| Block | Attribute | Values | What it does |
|---|---|---|---|
| `.feature` | `status="…"` | `passing` · `failing` · `pending` | Border colour and badge; updated live after a run |
| `.feature` | `tags="…"` | comma-separated | Chips in the card header |
| `.feature` | `id="…"` | Python-compatible id | Makes the card reachable as `self.page.<id>` in jssteps |
