Feature: The pad types like a text field, painted
  Michel, 2026-10-08: colours in the pad's source so learners match the
  components — and the colours must not cost undo: a run of typing is one
  ⌘Z, as in the run editor (the mirror is patched, not rebuilt, per key).

  Background:
    Given I have a clean browser page
    When I navigate to "/components/text"
    And I wait for the page to be interactive
    And I wait for the selector "[data-lc-id='playground'] .lc-mdpad-in"

  Scenario: A run of typing undoes as one, and the mirror follows the text
    When I type "  # hello" at the end of the "playground" pad
    Then the "playground" pad ends with "  # hello"
    And the "playground" pad's mirror shows "# hello"
    When I undo in the "playground" pad
    Then the "playground" pad does not contain "# hello"
    And the "playground" pad's mirror does not show "# hello"
