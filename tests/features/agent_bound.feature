Feature: The agent's bound= knob — legacy pinned, expressions added
  bound= has meant "tie me to a .run editor" since the beginning: every Ask
  carries the editor's code and last output, and a python block in the reply
  grows an Apply button that writes back. Fleet pages depend on it, so the
  legacy path is PINNED here before any new meaning of bound ships. The new
  meaning — bound="{=expr}" evaluates a cell expression and hands the value
  to the model — must coexist without touching the old one.

  Scenario: Legacy — a bound agent carries the editor's code and applies fixes
    Given I have a clean browser page
    And a builder key is connected
    And the recording model endpoint replies with a python fix "print('fixed')"
    When I navigate to "/components/agent"
    And I wait for the page to be interactive
    And I connect the "tutor" agent with key "test-key"
    And I ask the "tutor" agent "help me fix it"
    Then the model request carried the editor code "print('hello'"
    When I apply the agent's fix
    Then the "buggy" editor now holds "print('fixed')"

  Scenario: Expression — bound reads a pad through a cell expression
    Given I have a clean browser page
    And a builder key is connected
    And the recording model endpoint replies with a python fix "ok"
    And the GitHub contents API serves "courses/demo/module_01/bind.md" with the document:
      """
      # Bind page

      ```markdown
      my resume draft, version one
      ```
      {: .mdpad #cv1 rows="4" }

      ```yaml
      system: Review what you are handed.
      ```
      {: .agent #desk bound="{=cv1.source}" rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/bind.md"
    And I wait for the page to be interactive
    And I connect the "desk" agent with key "test-key"
    And I ask the "desk" agent "review it"
    Then the model request carried the editor code "my resume draft, version one"

  Scenario: A provider error speaks its own sentence, even array-wrapped
    Google wraps error JSON in an array; the panel must surface the
    provider's message, not a bare status code.

    Given I have a clean browser page
    And the model endpoint rejects with an array-wrapped 404 saying "models/ghost is not found"
    And the GitHub contents API serves "courses/demo/module_01/err.md" with the document:
      """
      # Err page

      ```yaml
      system: Review.
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/err.md"
    And I wait for the page to be interactive
    And I connect the "desk" agent with key "test-key"
    And I ask the desk agent into the void "hello"
    Then the desk relays "models/ghost is not found"

  Scenario: The two 429 walls are told apart
    A per-minute limit refills by itself; the day's free allowance does not.
    A learner must know which wall they hit.

    Given I have a clean browser page
    And the model endpoint answers 429 saying "Quota exceeded for quota metric 'Generate requests per day'"
    And the GitHub contents API serves "courses/demo/module_01/quota.md" with the document:
      """
      # Quota page

      ```yaml
      system: Review.
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/quota.md"
    And I wait for the page to be interactive
    And I connect the "desk" agent with key "test-key"
    And I ask the desk agent into the void "hello"
    Then the desk relays "today"

  Scenario: A 403 keeps the key — pasting the same one again would not help
    Michel, 2026-08-05: "it asks every time after a refresh". A 403 means the
    key is valid but not allowed to make THIS call (limited to certain
    websites, service not switched on, a proxy in the way). The old code
    treated it like 401 and DELETED the key, so one 403 at any desk threw
    away what the join door had just saved.

    Given I have a clean browser page
    And an energy key "AIzaKeepMe" is already saved on this device
    And the model endpoint answers with status 403 saying "Requests from referer are blocked."
    And the GitHub contents API serves "courses/demo/module_01/ref.md" with the document:
      """
      # Ref page

      ```yaml
      system: Review.
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/ref.md"
    And I wait for the page to be interactive
    And I ask the desk agent into the void "hello"
    Then the desk relays "Requests from referer are blocked."
    And the energy key is still saved on this device
    And the desk is still connected

  Scenario: A 401 does drop the key, and says why on the form that asks again
    401 is the one answer that means "paste a different key". Dropping it is
    right — but the explanation used to be written into the chat status line,
    which the auth wall hides in the same tick, so the learner was left with
    a paste box carrying no reason at all.

    Given I have a clean browser page
    And an energy key "AIzaStale" is already saved on this device
    And the model endpoint answers with status 401 saying "API key not valid"
    And the GitHub contents API serves "courses/demo/module_01/dead.md" with the document:
      """
      # Dead page

      ```yaml
      system: Review.
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/dead.md"
    And I wait for the page to be interactive
    And I ask the desk agent into the void "hello"
    Then the energy key is gone from this device
    And the desk asks for a key and explains "401"

  Scenario: A saved key opens every desk connected, refresh after refresh
    The whole point of saving it: no paste ceremony on any page, any reload.

    Given I have a clean browser page
    And an energy key "AIzaSaved" is already saved on this device
    And the GitHub contents API serves "courses/demo/module_01/two.md" with the document:
      """
      # Two desks

      ```yaml
      system: One.
      ```
      {: .agent #desk rows="3" }

      ```yaml
      system: Two.
      ```
      {: .agent #desk2 rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/two.md"
    And I wait for the page to be interactive
    Then the desk is still connected
    And every desk on the page is connected
    When I reload the page
    And I wait for the page to be interactive
    Then every desk on the page is connected

  Scenario: The day's AI spend is counted once, wherever it was asked
    A free key is a budget, and until now each panel counted only its own
    session while the docked guide counted nothing — so a learner could burn
    a day across six pages and never see a number (Michel, 2026-08-13).

    Given I have a clean browser page
    And a builder key is connected
    And the recording model endpoint replies with a python fix "ok"
    When I navigate to "/components/agent"
    And I wait for the page to be interactive
    And I connect the "tutor" agent with key "test-key"
    And I ask the "tutor" agent "help me fix it"
    Then the day's ledger counted 1 question
    And the ledger's sentence warns that the free key is limited
