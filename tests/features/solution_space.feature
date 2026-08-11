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
    Then the event flow "demo_flow" shows 11 steps
    And the event flow "demo_flow" step 1 is a "user" note
    And the event flow "demo_flow" step 2 is a "ui" note
    And the event flow "demo_flow" step 3 is a "command" note

  Scenario: A rule never issues a command — the person does
    A first cut opened each beat with the rule that enabled it, which read
    as though the rule told the family what to do. It cannot. So the actor
    heads their own beats and every one of them begins with the command
    that person gives (Michel, 2026-08-11).

    When I navigate to "/components/event_flow"
    And I wait for the page to be interactive
    Then the event flow "demo_flow" groups its steps under 2 users
    And the event flow "demo_flow" reads in 3 lines
    And line 1 of "demo_flow" begins with a "ui" note
    And line 2 of "demo_flow" begins with a "ui" note
    And no line of "demo_flow" begins with a "rule" note

  Scenario: The kind carries a glyph, not only a colour
    Printed in grey or read aloud, blue and purple are the same note.

    When I navigate to "/components/event_flow"
    And I wait for the page to be interactive
    Then every "user" note in "demo_flow" starts with "👤"

  Scenario: The legend explains the colors when asked
    When I navigate to "/components/event_flow"
    And I wait for the page to be interactive
    Then the event flow "demo_flow" shows its legend
    And the event flow legend mentions "rule"

  Scenario: A step's marked words wear the flow's colours
    The keyword decides — Given paints data, When paints a command, Then
    paints an event — and only marked words are painted, so nothing is
    guessed from the words themselves (Michel, 2026-08-11).

    When I navigate to "/components/feature"
    And I wait for the page to be interactive
    Then in "paint_demo" the word "Biscuit" is painted "data"
    And in "paint_demo" the word "names a dog" is painted "command"
    And in "paint_demo" the word "is open" is painted "event"

  Scenario: An IAL after a marked word overrides the keyword
    When I navigate to "/components/feature"
    And I wait for the page to be interactive
    Then in "paint_demo" the word "dog_grid" is painted "ui"

  Scenario: A diagram fence injected after load still becomes a diagram
    Module 04's data page renders through the runner, AFTER the one-shot
    mermaid pass — its flowchart showed as raw text (2026-08-11). The
    upgrader path converts whatever the scanner injects later.

    When I navigate to "/components/event_flow"
    And I wait for the page to be interactive
    And a mermaid fence is injected the way the runner renders one
    Then the injected fence becomes a diagram
