Feature: The proof's reveal has a pace — checks land one at a time
  Michel, 2026-09-23: "artificially slow the display so learners see the
  green progression bar and the confetti… suspense, effort, expectation".
  The code runs as fast as it runs; the card shows its steps one at a time,
  300 ms apart by default, a thin bar filling with them. pace="0" is
  natural speed; an author may go slower.

  Scenario: By default the checks arrive one at a time, a bar filling with them
    Given I have a clean browser page
    When I navigate to "/components/feature"
    And I wait for the page to be interactive
    And the feature "temp_feature" is set to a pace of 600 ms
    And I run the feature "temp_feature"
    Then its checks arrive one at a time, about 600 ms apart, the bar filling with them

  Scenario: pace="0" shows the whole verdict at natural speed, no bar
    Given I have a clean browser page
    When I navigate to "/components/feature"
    And I wait for the page to be interactive
    And the feature "temp_feature" is set to a pace of 0 ms
    And I run the feature "temp_feature"
    Then its verdict lands at once, without a bar
