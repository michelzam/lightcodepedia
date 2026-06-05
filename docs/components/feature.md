# 🦄 Feature

Render Gherkin BDD scenarios as styled cards. Pair a `.feature` block with a `.steps` Python block to get a **▶ Run** button — the steps block disappears from the page and its implementations slot into the card's expandable step rows.
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

Click any step row to see its Python implementation. Click **▶ Run** to execute all steps.

```gherkin
Feature: Temperature converter
  Scenario: Celsius to Fahrenheit
    Given a temperature of 100 degrees Celsius
    When converted to Fahrenheit using (C × 9/5) + 32
    Then the result should be 212
    And zero Celsius equals 32 Fahrenheit
```
{: .feature status="passing" tags="math,utils" }

```python
# Given a temperature of 100 degrees Celsius
celsius = 100

# When converted to Fahrenheit using (C × 9/5) + 32
fahrenheit = (celsius * 9 / 5) + 32

# Then the result should be 212
assert fahrenheit == 212.0, "Got " + str(fahrenheit)

# And zero Celsius equals 32 Fahrenheit
assert (0 * 9 / 5) + 32 == 32.0
```
{: .steps }

## 😰 Failing step example

```gherkin
Feature: List validator
  Scenario: Reject empty lists
    Given an empty list
    When I check if it is valid
    Then validation should fail
```
{: .feature status="failing" tags="validation" }

```python
# Given an empty list
items = []

# When I check if it is valid
def is_valid(lst):
    return len(lst) > 0
result = is_valid(items)

# Then validation should fail
assert result == True   # intentional bug — should be False
```
{: .steps }

## 🥸 How to write one

Add `{: .feature }` after a gherkin fence. For runnable steps, add a python fence immediately after with `{: .steps }` — the Python block disappears from the page and its implementations are slotted into the card.

````markdown
```gherkin
Feature: My feature
  Scenario: A scenario
    Given some precondition
    When an action happens
    Then the result is correct
```
{: .feature status="pending" tags="example" }

```python
# Given some precondition
x = 42

# When an action happens
y = x * 2

# Then the result is correct
assert y == 84
```
{: .steps }
````

- Start each step's Python with a `# Keyword ...` comment matching the Gherkin keyword.
- Steps **share context** — variables from earlier steps are available in later ones.
- Each **▶ Run** starts a fresh MicroPython interpreter; runs are isolated from each other.
- Click a step row to **expand its implementation** inline.
- Steps after a failure are **skipped** (shown with ○).

## 🎛️ Knobs

| Block | Attribute | Values | What it does |
|---|---|---|---|
| `.feature` | `status="…"` | `passing` · `failing` · `pending` | Border colour and badge; updated live after a run |
| `.feature` | `tags="…"` | comma-separated | Chips in the card header |
