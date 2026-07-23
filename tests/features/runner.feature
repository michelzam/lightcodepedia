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
    When I open the bench page "index.md"
    Then the link "Exercise 1" opens gh path "course/ex1.md"

  Scenario: Parent-relative links resolve within the repo
    Given a stubbed bench with a course page
    When I open the bench page "course/ex1.md"
    Then the link "Back to the bench" opens gh path "index.md"

  Scenario: A bare .folder inside a render lists the current folder
    # {: .folder } with no path knob defaults to the folder it lives in, and
    # runner mode is implied inside a render — "just show what's here".
    Given a stubbed bench with a course page
    When I open the bench page "shelf.md"
    Then the shelf lists a card opening gh path "lesson_a.md"

  Scenario: The runtime opens the rich page editor bound to the rendered source
    # /run.html has no page of its own to edit — the same rich editor must
    # target the RENDERED file (gh:repo/path the runner stamped), so course
    # material and benches are editable with the full Blocks/Raw/preview drawer.
    Given a stubbed bench with a course page
    When I open the bench page "course/ex1.md"
    And I open the page editor
    Then the page editor is editing "course/ex1.md"
    And the raw editor contains "Solve it your way"
