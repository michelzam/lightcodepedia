Feature: Slides FAB and presentation mode

  Background:
    Given I have a clean browser page

  Scenario: Slides FAB is present on tutorial101
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    Then the slides FAB button is visible

  @mobile
  Scenario: Slides FAB popup opens on tap
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I tap the slides FAB button
    Then the FAB popup is visible
    And the popup contains a "Present" option
    And the popup contains an X-ray option

  @mobile
  Scenario: Tapping Present closes the popup
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I tap the slides FAB button
    And I click the Present option in the popup
    Then the FAB popup is not visible

  @mobile
  Scenario: Slides FAB is present on mobile
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    Then the slides FAB button is visible

  @mobile
  Scenario: FAB popup appears on tap on mobile
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I tap the slides FAB button
    Then the FAB popup is visible
