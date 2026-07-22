Feature: The instant runner (RT) — Phase A parity

  Renders raw markdown into live components using the same client-side pipeline
  as the editor preview. Behaviour parity with Jekyll, not identical DOM.

  Background:
    Given I have a clean browser page

  Scenario: The /run page renders markdown text from a hash source
    When I open the runner page on "/run_samples/probe.txt"
    And I wait for the runner to render
    Then the runner shows a heading "RT probe page"
    And the runner shows bold text

  Scenario: The runner upgrades a component the way Jekyll does
    When I open the runner page on "/run_samples/probe.txt"
    And I wait for the runner to render
    Then the runner contains a ".lc-block" element
    And the rendered block mentions "Lucky"

  Scenario: A missing source shows a clear message, not a blank page
    When I open the runner page on "/run_samples/does-not-exist.txt"
    Then the runner reports it could not load

  Scenario: A component inside an RT render keeps its editable fence source
    When I open the runner page on "/components/block.md"
    And I wait for the runner to render
    Then a rendered component carries an editable source snapshot

  Scenario: Kramdown footnotes render in an RT render
    When I open the runner page on "/components/datagrid.md"
    And I wait for the runner to render
    Then footnote refs and their definitions render, none left raw

  Scenario: The bar replaces the page title and names the source
    When I open the runner page on "/run_samples/probe.txt"
    And I wait for the runner to render
    Then the runner bar names the source "probe.txt"
    And the runner page title is hidden

  Scenario: A course page on a bench offers Make it mine
    Given a stubbed bench with a course page
    When I open the bench page "course/ex1.md"
    Then the runner bar marks it as course material

  Scenario: Make it mine copies the page into my space and opens it
    Given a stubbed bench with a course page
    When I open the bench page "course/ex1.md"
    And I click Make it mine
    Then the bench received my copy
    And the runner bar marks it as my page

  Scenario: The bar flags an original that changed since my copy
    Given a stubbed bench with a course page
    And my copy exists from an older original
    When I open the bench page "my/ex1.md"
    Then the runner bar flags the changed original

  Scenario: A bench flips the topbar into bench mode
    Given a stubbed bench with a course page
    When I open the bench page "course/ex1.md"
    Then the topbar switches to bench mode

  Scenario: A bench menu takes over the topbar links
    Given a stubbed bench with a course page
    And the bench ships a menu
    When I open the bench page "course/ex1.md"
    Then the topbar switches to bench mode
    And the topbar menu comes from the bench

  Scenario: Relative links in a rendered page stay in the repo
    Given a stubbed bench with a course page
    When I open the bench page "README.md"
    Then the link "Exercise 1" opens gh path "course/ex1.md"

  Scenario: Parent-relative links resolve within the repo
    Given a stubbed bench with a course page
    When I open the bench page "course/ex1.md"
    Then the link "Back to the bench" opens gh path "README.md"
