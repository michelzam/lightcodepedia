Feature: Quiz grading

  Background:
    Given I have a clean browser page

  Scenario: Picking the right answer grades it correct
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I pick the quiz answer "Labrador Retriever"
    Then that quiz answer is marked correct

  Scenario: Picking a wrong answer reveals it as wrong
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I pick the quiz answer "Beagle"
    Then that quiz answer is marked wrong

  Scenario: A multi quiz keeps its ticks through Check, so the next click means what it shows
    Michel, 2026-09-16: after Check the boxes looked empty while the picks
    were still held — the next click on one silently unpicked it, the one
    after ticked it again, and Check graded what the learner could not
    see. The tick is the pick, the colour is the verdict; both stay.

    When I navigate to "/components/quiz"
    And I wait for the page to be interactive
    And I toggle the multi quiz option "for"
    And I toggle the multi quiz option "repeat"
    And I press Check on the multi quiz
    Then the multi quiz option "for" is ticked and marked correct
    And the multi quiz option "repeat" is ticked and marked wrong
    And the multi quiz says "Not quite"
    When I toggle the multi quiz option "repeat"
    Then the multi quiz option "repeat" is unticked, with no verdict colour
    When I toggle the multi quiz option "repeat"
    Then the multi quiz option "repeat" is ticked, with no verdict colour
    When I toggle the multi quiz option "repeat"
    And I toggle the multi quiz option "while"
    And I press Check on the multi quiz
    Then the multi quiz says "All correct"
