Feature: Homework — record karma and hand it in

  A page opened with a param chain (?homework_number=…&student_id=…&submit_info=…)
  starts a recorded homework session: the run is remembered in localStorage and
  every quiz result is logged, with a pill showing the running score and a
  Submit button.

  Background:
    Given I have a clean browser page

  Scenario: A homework param chain starts a recorded session
    When I navigate to "/tutorial101?homework_number=6a&student_id=93629601&submit_info=https://example.org/hand-in"
    And I wait for the page to be interactive
    Then the homework pill shows "6a"
    And the homework session is stored

  Scenario: A graded quiz is recorded into the homework karma
    When I navigate to "/tutorial101?homework_number=6a&student_id=93629601"
    And I wait for the page to be interactive
    And a quiz is graded correct
    Then the homework score is at least 1
