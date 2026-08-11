Feature: Solution space — the event flow

  A page's story as an event-storming sequence: colored sticky notes,
  the key of each YAML line is the color, the value is the words.

  Background:
    Given I have a clean browser page

  Scenario: The event flow page loads without errors
    When I navigate to "/components/event_flow"
    And I wait for the page to be interactive
    Then the LC platform is loaded
    And there are no JS console errors

  Scenario: Every step renders as a colored note
    When I navigate to "/components/event_flow"
    And I wait for the page to be interactive
    Then the event flow "demo_flow" shows 7 steps
    And the event flow "demo_flow" step 1 is a "actor" note
    And the event flow "demo_flow" step 2 is a "command" note
    And the event flow "demo_flow" step 3 is a "event" note

  Scenario: The legend explains the colors when asked
    When I navigate to "/components/event_flow"
    And I wait for the page to be interactive
    Then the event flow "demo_flow" shows its legend
    And the event flow legend mentions "policy"

  Scenario: A diagram fence injected after load still becomes a diagram
    Module 04's data page renders through the runner, AFTER the one-shot
    mermaid pass — its flowchart showed as raw text (2026-08-11). The
    upgrader path converts whatever the scanner injects later.

    When I navigate to "/components/event_flow"
    And I wait for the page to be interactive
    And a mermaid fence is injected the way the runner renders one
    Then the injected fence becomes a diagram
