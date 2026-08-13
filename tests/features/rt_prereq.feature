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

  Scenario: A met prerequisite is still a door
    Green used to turn the title into plain text, so the one list a learner
    would use to go back and re-read something was the one place they could
    not click (Michel, 2026-08-13).

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
    And "Basics" is still a link I can follow

  Scenario: Points alone do not open a strict gate
    features="true" says the proofs count as well: a page whose .feature
    cards were never run is a page the learner read, not one they did
    (Michel, 2026-08-13: "a more strict way to validate a page and a
    module, and avoid learners to build on brittle knowledge").

    Given I have a clean browser page
    And a marked shim is preinstalled
    And the learner has earned points on "gh:acme/demo/courses/demo/mod/basics"
    And the GitHub contents API serves "courses/demo/mod/basics.md" with the document:
      """
      # Basics

      ```gherkin
      Given a page
      Then it proves itself
      ```
      {: .feature #proof }
      """
    And the GitHub contents API serves "courses/demo/mod/strict.md" with the document:
      """
      # Next module

      - [Basics](basics.md)
      {: .prerequisite features="true" }

      ## Deep content

      Secret wisdom here.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/strict.md"
    And I wait for the page to be interactive
    Then a prerequisite gate offers "Basics"
    And the gated content "Secret wisdom here." is hidden

  Scenario: The same points open it once the proof is green
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the learner has earned points on "gh:acme/demo/courses/demo/mod/basics"
    And the learner turned "proof" green on "gh:acme/demo/courses/demo/mod/basics"
    And the GitHub contents API serves "courses/demo/mod/basics.md" with the document:
      """
      # Basics

      ```gherkin
      Given a page
      Then it proves itself
      ```
      {: .feature #proof }
      """
    And the GitHub contents API serves "courses/demo/mod/strict.md" with the document:
      """
      # Next module

      - [Basics](basics.md)
      {: .prerequisite features="true" }

      ## Deep content

      Secret wisdom here.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/strict.md"
    And I wait for the page to be interactive
    Then the prerequisites are met
    And the gated content "Secret wisdom here." is visible

  Scenario: By default the proofs are not asked about
    The knob is opt-in: the same page without features="true" opens on the
    points alone, exactly as every course page does today.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And the learner has earned points on "gh:acme/demo/courses/demo/mod/basics"
    And the GitHub contents API serves "courses/demo/mod/basics.md" with the document:
      """
      # Basics

      ```gherkin
      Given a page
      Then it proves itself
      ```
      {: .feature #proof }
      """
    And the GitHub contents API serves "courses/demo/mod/open.md" with the document:
      """
      # Next module

      - [Basics](basics.md)
      {: .prerequisite }

      ## Deep content

      Secret wisdom here.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/open.md"
    And I wait for the page to be interactive
    Then the prerequisites are met
    And the gated content "Secret wisdom here." is visible

  Scenario: ?strict=1 asks for the proofs on every page of the frame
    Two levels (Michel, 2026-08-13): the URL sets the scope's default — a
    whole course walked the strict way, with no page edited — and a block's
    own features= is the local word.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And the learner has earned points on "gh:acme/demo/courses/demo/mod/basics"
    And the GitHub contents API serves "courses/demo/mod/basics.md" with the document:
      """
      # Basics

      ```gherkin
      Given a page
      Then it proves itself
      ```
      {: .feature #proof }
      """
    And the GitHub contents API serves "courses/demo/mod/plain.md" with the document:
      """
      # Next module

      - [Basics](basics.md)
      {: .prerequisite }

      ## Deep content

      Secret wisdom here.
      """
    When I navigate to "/run.html?strict=1#src=gh:acme/demo/courses/demo/mod/plain.md"
    And I wait for the page to be interactive
    Then a prerequisite gate offers "Basics"
    And the gated content "Secret wisdom here." is hidden

  Scenario: A page may opt out of a strict frame
    features="false" is the local word against the URL's default — the page
    that only needs the points, inside a course that asks for the proofs.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And the learner has earned points on "gh:acme/demo/courses/demo/mod/basics"
    And the GitHub contents API serves "courses/demo/mod/basics.md" with the document:
      """
      # Basics

      ```gherkin
      Given a page
      Then it proves itself
      ```
      {: .feature #proof }
      """
    And the GitHub contents API serves "courses/demo/mod/lenient.md" with the document:
      """
      # Next module

      - [Basics](basics.md)
      {: .prerequisite features="false" }

      ## Deep content

      Secret wisdom here.
      """
    When I navigate to "/run.html?strict=1#src=gh:acme/demo/courses/demo/mod/lenient.md"
    And I wait for the page to be interactive
    Then the prerequisites are met
    And the gated content "Secret wisdom here." is visible

  Scenario: A met prerequisite links back through the runner, not into a 404
    The gate builds its own anchors AFTER the runner healed the page's links,
    so it was handing out the raw "welcome.md" — which the site has no page
    for (Michel, 2026-08-13: "prerequisite links fail: example between
    adoption day and previous (welcome)").

    Given I have a clean browser page
    And a marked shim is preinstalled
    And the learner has earned points on "gh:acme/demo/courses/demo/mod/welcome"
    And the GitHub contents API serves "courses/demo/mod/adoption.md" with the document:
      """
      # Adoption Day

      - [Welcome](welcome.md)
      {: .prerequisite }

      A story from the future.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/adoption.md"
    And I wait for the page to be interactive
    Then the prerequisites are met
    And "Welcome" leads back through the runner to "courses/demo/mod/welcome.md"
