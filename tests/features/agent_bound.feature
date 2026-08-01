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
    And I ask the "desk" agent "review it"
    Then the model request carried the editor code "my resume draft, version one"
