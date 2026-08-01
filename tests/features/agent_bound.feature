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
