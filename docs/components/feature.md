---
---
# 🦄 Feature

Render Gherkin BDD scenarios as styled cards. Pair a `.feature` block with a `.jssteps` block — the card gives the scenario its visual shape; the step runner verifies assertions live in the page.

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

The `.feature` card renders the Gherkin. The `.jssteps` block below it owns execution — each `@scenario` maps to a Gherkin step.

```gherkin
Feature: Temperature converter
  Scenario: Celsius to Fahrenheit
    Given a temperature of 100 degrees Celsius
    When converted to Fahrenheit using (C × 9/5) + 32
    Then the result should be 212
    And zero Celsius equals 32 Fahrenheit
```
{: .feature id="temp-feature" status="pending" tags="math,utils" }

```python
@scenario("Given a temperature of 100 degrees Celsius")
def step_given(self):
    self.celsius = 100

@scenario("When converted to Fahrenheit using (C × 9/5) + 32")
def step_when(self):
    self.fahrenheit = (self.celsius * 9 / 5) + 32

@scenario("Then the result should be 212")
def step_then(self):
    assert self.fahrenheit == 212.0, f"Got {self.fahrenheit}"

@scenario("And zero Celsius equals 32 Fahrenheit")
def step_and(self):
    assert (0 * 9 / 5) + 32 == 32.0
```
{: .jssteps }

Scenarios share the same context object (`self`), so state set in one step (`self.celsius`) is available in the next.

## 😰 Failing step example

```gherkin
Feature: List validator
  Scenario: Reject empty lists
    Given an empty list
    When I check if it is valid
    Then validation should fail
```
{: .feature id="list-feature" status="pending" tags="validation" }

```python
@scenario("Given an empty list")
def step_given(self):
    self.items = []

@scenario("When I check if it is valid")
def step_when(self):
    self.result = len(self.items) > 0

@scenario("Then validation should fail")
def step_then(self):
    assert self.result == False, "Expected validation to fail for empty list"
```
{: .jssteps }

## 🔬 DOM bridge probe

Can MicroPython reach the browser DOM via `import js`? This suite replaces the old `.steps`-based probe.

```gherkin
Feature: MicroPython JS bridge
  Scenario: DOM access from Python steps
    Given the js module is importable
    When I read document.title
    Then I can query a DOM element
    And I can read an element attribute
```
{: .feature id="js-bridge-feature" status="pending" tags="probe,js-bridge" }

```python
@scenario("Given the js module is importable")
def step_import(self):
    import js
    self.js = js
    assert self.js is not None, "import js failed"

@scenario("When I read document.title")
def step_title(self):
    self.title = self.js.document.title
    assert isinstance(self.title, str), f"document.title is not a string: {repr(self.title)}"

@scenario("Then I can query a DOM element")
def step_query(self):
    self.el = self.js.document.querySelector("body")
    assert self.el is not None, "querySelector('body') returned None"

@scenario("And I can read an element attribute")
def step_attr(self):
    tag = self.el.tagName
    assert tag is not None, f"tagName returned None — got: {repr(tag)}"
```
{: .jssteps }

## 🥸 How to write one

Write a `.feature` card for the Gherkin shape, then a `.jssteps` block for the step implementations:

````markdown
```gherkin
Feature: My feature
  Scenario: A scenario
    Given some precondition
    When an action happens
    Then the result is correct
```
{: .feature id="my-feature" status="pending" tags="example" }

```python
@scenario("Given some precondition")
def step_given(self):
    self.x = 42

@scenario("When an action happens")
def step_when(self):
    self.y = self.x * 2

@scenario("Then the result is correct")
def step_then(self):
    assert self.y == 84
```
{: .jssteps }
````

- Each `@scenario` label should match or paraphrase a Gherkin step for readability.
- **Shared context**: `self` is the same object across all scenarios in a suite — store state with `self.<name>`.
- Give the `.feature` card an `id` if you want to inspect it from jssteps via `self.page.my_feature`.
- The two built-in scenarios ("component ids are unique" and "component ids are python compatible") run before your scenarios on every suite.

## 🎛️ Knobs

| Block | Attribute | Values | What it does |
|---|---|---|
| `.feature` | `status="…"` | `passing` · `failing` · `pending` | Border colour and badge |
| `.feature` | `tags="…"` | comma-separated | Chips in the card header |
| `.feature` | `id="…"` | Python-compatible id | Makes the card reachable as `self.page.<id>` in jssteps |
