Feature: Everything a mouse can do, a keyboard can do

  A learner who cannot use a mouse must be able to take the course. This is
  WCAG 2.1.1 at Level A — the floor, not the polish. It lives in the gating
  suite rather than the axe scan on purpose: a static scan cannot tell that an
  element with a click handler has no keyboard path, so it scores a
  keyboard-dead quiz as perfect. Every keyboard fix from here to April lands
  with a scenario here, or it is not done.

  Background:
    Given I have a clean browser page

  Scenario: Every quiz answer is a tab stop
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    Then every quiz answer is reachable by keyboard

  Scenario: A quiz answer can be focused and read by assistive tech
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I tab to the quiz answer "Labrador Retriever"
    Then that quiz answer is the focused element
    And the quiz answer "Labrador Retriever" exposes the role "radio"

  Scenario: Enter answers the quiz, exactly as a click does
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I tab to the quiz answer "Labrador Retriever"
    And I press "Enter"
    Then that quiz answer is marked correct
    And the quiz answer "Labrador Retriever" is announced as checked

  Scenario: Space answers the quiz too
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I tab to the quiz answer "Beagle"
    And I press " "
    Then that quiz answer is marked wrong

  Scenario: Arrow keys walk the answers
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I tab to the quiz answer "Beagle"
    And I press "ArrowDown"
    Then that quiz answer is not the focused element
