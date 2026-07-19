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
