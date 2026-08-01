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

  Scenario: A prerequisite in the PARENT folder opens from ../
    A module's index often requires the course-level setup page one folder
    up. "../join.md" must name the parent's file, not a site path — the
    exact line an author writes at the top of module_00/index.md.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And the learner has earned points on "gh:acme/demo/courses/demo/join"
    And the GitHub contents API serves "courses/demo/module_00/index.md" with the document:
      """
      # Module 00

      - [⚙️ Setup](../join.md)
      {: .prerequisite }

      ## The lesson

      Secret wisdom here.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_00/index.md"
    And I wait for the page to be interactive
    Then the prerequisites are met
    And the gated content "Secret wisdom here." is visible

  Scenario: The same parent link stays shut without the points
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/module_00/index.md" with the document:
      """
      # Module 00

      - [⚙️ Setup](../join.md)
      {: .prerequisite }

      ## The lesson

      Secret wisdom here.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_00/index.md"
    And I wait for the page to be interactive
    Then a prerequisite gate offers "Setup"
    And the gated content "Secret wisdom here." is hidden

  Scenario: Components that upgrade after the gate stay hidden
    A gate that tags the blocks it can see loses them the moment a component
    replaces its block with a rendered one — the page leaks its whole body
    back into view. Everything after a locked gate must stay gone.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/locked.md" with the document:
      """
      # Locked module

      - [Basics](basics.md)
      {: .prerequisite escape="true" }

      ```csv
      name,breed
      Lucky,Beagle
      Nova,Lab
      ```
      {: .dataset #dogs_l }

      [Dogs](#)
      {: .datagrid source="dogs_l" #grid_l }

      ```
      ### The worry
      Secret wisdom here.
      ```
      {: .block }

      **Q:** Ready?

      - [x] Yes
      - [ ] No
      {: .quiz }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/locked.md"
    And I wait for the page to be interactive
    Then a prerequisite gate offers "Basics"
    And nothing below the gate is visible
    When I show the page anyway
    Then the gated content "Secret wisdom here." is visible

  Scenario: The default gate has no way through
    A gate anyone can wave away teaches that gates are decoration. The
    escape hatch is the author's decision, not the platform's.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/strict.md" with the document:
      """
      # Strict page

      - [Basics](basics.md)
      {: .prerequisite }

      ## Body

      Secret wisdom here.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/strict.md"
    And I wait for the page to be interactive
    Then a prerequisite gate offers "Basics"
    And no escape hatch is offered
    And the gated content "Secret wisdom here." is hidden

  Scenario: The author may open a door, in their own words
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/kind.md" with the document:
      """
      # Kind page

      - [Basics](basics.md)
      {: .prerequisite escape="Peek anyway (you'll miss the point)" }

      ## Body

      Secret wisdom here.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/kind.md"
    And I wait for the page to be interactive
    Then the escape hatch reads "Peek anyway (you'll miss the point)"
    When I show the page anyway
    Then the gated content "Secret wisdom here." is visible

  Scenario: Half the points do not open a gate that asks for all of them
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the learner has earned some points on "gh:acme/demo/courses/demo/mod/basics"
    And the GitHub contents API serves "courses/demo/mod/mastery.md" with the document:
      """
      # Mastery page

      - [Basics](basics.md)
      {: .prerequisite }

      ## Body

      Secret wisdom here.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/mastery.md"
    And I wait for the page to be interactive
    Then a prerequisite gate offers "Basics"
    And the gated content "Secret wisdom here." is hidden

  Scenario: The same half opens a gate that asks for half
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the learner has earned some points on "gh:acme/demo/courses/demo/mod/basics"
    And the GitHub contents API serves "courses/demo/mod/relaxed.md" with the document:
      """
      # Relaxed page

      - [Basics](basics.md)
      {: .prerequisite pass="50" }

      ## Body

      Secret wisdom here.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/relaxed.md"
    And I wait for the page to be interactive
    Then the prerequisites are met
    And the gated content "Secret wisdom here." is visible
