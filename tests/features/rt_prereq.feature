Feature: RT prerequisite gate — the key names the content, not the runner
  A course page rendered through /run declares its prerequisite with a
  relative link to a sibling page. The gate must check the score bucket that
  sibling actually earns into (gh:owner/repo/…), never the runner's own
  pathname — otherwise every vault gate would stay forever shut (or forever
  open) regardless of what the learner earned.

  Scenario: The component page's own site-side gate still works
    Given I have a clean browser page
    When I navigate to "/components/prerequisite"
    And I wait for the page to be interactive
    Then a prerequisite gate offers "Tutorial 101"

  Scenario: An unmet prerequisite gates a rendered course page
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/next.md" with the document:
      """
      # Next module

      - [Basics](basics.md)
      {: .prerequisite }

      ## Deep content

      Secret wisdom here.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/next.md"
    And I wait for the page to be interactive
    Then a prerequisite gate offers "Basics"
    And the gated content "Secret wisdom here." is hidden

  Scenario: Points earned on the sibling page open the gate
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the learner has earned points on "gh:acme/demo/courses/demo/mod/basics"
    And the GitHub contents API serves "courses/demo/mod/next.md" with the document:
      """
      # Next module

      - [Basics](basics.md)
      {: .prerequisite }

      ## Deep content

      Secret wisdom here.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/next.md"
    And I wait for the page to be interactive
    Then the prerequisites are met
    And the gated content "Secret wisdom here." is visible
