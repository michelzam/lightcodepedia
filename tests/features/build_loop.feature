Feature: Build Loop — the turning hex hive

  Background:
    Given I have a clean browser page

  Scenario: The component page loads without errors
    When I navigate to "/components/build_loop"
    And I wait for the page to be interactive
    Then the LC platform is loaded
    And there are no JS console errors

  Scenario: The loop renders a canvas
    When I navigate to "/components/build_loop"
    And I wait for the page to be interactive
    Then the build loop canvas is visible

  Scenario: Every station in the fence becomes a chip
    When I navigate to "/components/build_loop"
    And I wait for the page to be interactive
    Then the build loop shows 6 station chips
    And the build loop chips include "Design"

  Scenario: A station explains itself on hover
    When I navigate to "/components/build_loop"
    And I wait for the page to be interactive
    And I hover the build loop chip "AI"
    Then the build loop readout mentions "partner"

  Scenario: A loop folded inside an accordion still builds
    When I navigate to "/components/build_loop"
    And I wait for the page to be interactive
    And I open the accordion section "A folded loop"
    Then the page shows 2 build loops
    And the build loop chips include "Check"

  Scenario: Clicking a station pins a legend to it
    When I navigate to "/components/build_loop"
    And I wait for the page to be interactive
    And I pin the build loop station "Design"
    Then 1 legend is pinned to the loop
    And the pinned legend mentions "hold"

  Scenario: The pinned legend rides its station as the hive turns
    When I navigate to "/components/build_loop"
    And I wait for the page to be interactive
    And I pin the build loop station "Design"
    Then the pinned legend follows its station

  Scenario: Clicking the same station again closes its legend
    When I navigate to "/components/build_loop"
    And I wait for the page to be interactive
    And I pin the build loop station "Design"
    And I pin the build loop station "Design"
    Then 0 legends are pinned to the loop

  Scenario: Several legends can stay open at once
    When I navigate to "/components/build_loop"
    And I wait for the page to be interactive
    And I pin the build loop station "Design"
    And I pin the build loop station "Ship"
    Then 2 legends are pinned to the loop

  Scenario: A narrator can pin a station through the verb registry
    When I navigate to "/components/build_loop"
    And I wait for the page to be interactive
    And the narrator calls "pin" with "AI" on the loop
    Then 1 legend is pinned to the loop
    And the pinned legend mentions "partner"

  Scenario: A narrator can turn the hive to face a station
    When I navigate to "/components/build_loop"
    And I wait for the page to be interactive
    And the narrator calls "pin" with "AI" on the loop
    And the narrator calls "look_at" with "Need" on the loop
    Then the pinned legend follows its station

  Scenario: A narrator can clear every pinned legend
    When I navigate to "/components/build_loop"
    And I wait for the page to be interactive
    And the narrator calls "pin" with "AI" on the loop
    And the narrator calls "pin" with "Ship" on the loop
    Then 2 legends are pinned to the loop
    When the narrator calls "unpin" with "" on the loop
    Then 0 legends are pinned to the loop

  Scenario: A narrator can stop and restart the spin
    When I navigate to "/components/build_loop"
    And I wait for the page to be interactive
    And the narrator calls "spin" with "off" on the loop
    Then the build loop spin button offers to resume

  Scenario: An unknown station is refused, not guessed
    When I navigate to "/components/build_loop"
    And I wait for the page to be interactive
    Then the narrator verb "pin" with "Nope" is refused
    And 0 legends are pinned to the loop

  Scenario: The spin can be paused and resumed
    When I navigate to "/components/build_loop"
    And I wait for the page to be interactive
    And I click the build loop spin button
    Then the build loop spin button offers to resume
