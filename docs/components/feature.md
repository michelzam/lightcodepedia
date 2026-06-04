---
title: Feature (Gherkin BDD)
---

# Feature (Gherkin BDD)

Render Gherkin BDD scenarios as styled cards. Optionally embed a Python implementation for each step using `:::python` / `:::` markers — a **▶ Run** button appears automatically, executes each step in MicroPython, and updates the status badge live.

## Display-only (no runner)

```gherkin
Feature: User login
  Scenario: Successful login
    Given I am on the login page
    When I enter valid credentials
    Then I should see the dashboard
```
{: .feature status="passing" tags="smoke,auth" }

## With runnable steps

Click a step row to see its implementation. Click **▶ Run** to execute them all.

```gherkin
Feature: Temperature converter
  As a developer using the utils module
  I want to convert between temperature scales

  Scenario: Celsius to Fahrenheit
    Given a temperature of 100 degrees Celsius
    :::python
    celsius = 100
    :::
    When converted to Fahrenheit using (C × 9/5) + 32
    :::python
    fahrenheit = (celsius * 9 / 5) + 32
    :::
    Then the result should be 212
    :::python
    assert fahrenheit == 212.0, "Got " + str(fahrenheit)
    :::
    And zero Celsius equals 32 Fahrenheit
    :::python
    assert (0 * 9 / 5) + 32 == 32.0
    :::
```
{: .feature status="pending" tags="math,utils" }

## Failing step example

```gherkin
Feature: List validator
  Scenario: Reject empty lists
    Given an empty list
    :::python
    items = []
    :::
    When I check if it is valid
    :::python
    def is_valid(lst):
        return len(lst) > 0
    result = is_valid(items)
    :::
    Then validation should fail
    :::python
    assert result == True   # intentional bug: should be False
    :::
```
{: .feature status="pending" tags="validation" }

## How to write one

Write a `gherkin` fenced block and add `{: .feature }` on the next line. To attach Python to a step, place a `:::python` block immediately after it — still inside the same fence:

````markdown
```gherkin
Feature: My feature
  Scenario: A scenario
    Given some precondition
    :::python
    x = 42
    :::
    When an action happens
    :::python
    y = x * 2
    :::
    Then the result is correct
    :::python
    assert y == 84
    :::
```
{: .feature status="pending" tags="example" }
````

- Steps **share context** — variables from earlier steps are available in later ones.
- Each run starts a **fresh MicroPython interpreter** so runs are isolated from each other.
- Clicking a step row **toggles its Python implementation** inline.
- Steps after a failure are **skipped** (shown with ○).

## Knobs

| Attribute | Values | What it does |
|---|---|---|
| `status="…"` | `passing` · `failing` · `pending` | Left border colour and badge; updated live after a run |
| `tags="…"` | comma-separated | Tag chips in the card header |

A card without any knobs renders with a neutral grey border and no badge.
