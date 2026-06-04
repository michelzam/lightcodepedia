---
title: Feature (Gherkin BDD)
---

# Feature (Gherkin BDD)

Render Gherkin BDD scenarios as styled cards — complete with a status badge and tag chips. Write your acceptance criteria directly in the page; the card header extracts the Feature name automatically.

## See it in action

```gherkin
Feature: User Login
  As a registered user
  I want to log in with my credentials
  So that I can access my account

  Scenario: Successful login
    Given I am on the login page
    When I enter a valid username and password
    Then I should be redirected to the dashboard
    And I should see a welcome message
```
{: .feature status="passing" tags="smoke,auth" }

```gherkin
Feature: Password Reset
  Scenario: Request reset email
    Given my account exists
    When I click "Forgot password"
    And I enter my email address
    Then I should receive a reset link within 5 minutes
```
{: .feature status="pending" tags="auth" }

```gherkin
Feature: Two-Factor Authentication
  Scenario: Login blocked without OTP
    Given 2FA is enabled on my account
    When I enter correct credentials
    Then I should be prompted for a one-time code
    And login should fail without it
```
{: .feature status="failing" tags="auth,2fa" }

## How to make one

Write a `gherkin` fenced block, then add `{: .feature }` on the very next line:

````markdown
```gherkin
Feature: My feature
  Scenario: A scenario
    Given some precondition
    When an action is taken
    Then a result is expected
```
{: .feature }
````

The Feature name on the first line becomes the card heading. Everything else is syntax-highlighted Gherkin.

## Knobs

| Attribute | Values | What it does |
|---|---|---|
| `status="…"` | `passing` · `failing` · `pending` | Colours the left border and shows a badge (green · red · amber) |
| `tags="…"` | comma-separated list | Displays tag chips in the card header |

A card with no knobs renders with a neutral grey border and no badge — useful for drafting scenarios:

```gherkin
Feature: Draft scenario
  Scenario: Not yet implemented
    Given a placeholder step
    When nothing happens yet
    Then this is a work in progress
```
{: .feature }

## In the editor

Open the page in the editor (✏️), select the block in the Blocks tab, and set **Type → .feature**. A knob hint appears below the type selector reminding you of the available attributes. Type the knobs directly into the **Knobs** field — for example:

```
status="passing" tags="smoke,auth"
```

Hit **Apply** to write the IAL back into the raw markdown.
