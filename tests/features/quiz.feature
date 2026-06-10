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
