Feature: X-ray inspector

  Background:
    Given I have a clean browser page

  Scenario: X-ray panel appears on hover over a component
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I hover over the first grid component
    Then an x-ray panel is visible
    And the x-ray panel shows a component class name

  Scenario: X-ray panel shows bound-to association for a chart
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I hover over the chart component
    Then an x-ray panel is visible
    And the x-ray panel mentions "bound_to"

  Scenario: X-ray panel shows on_click handler for a button
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I hover over a button component
    Then an x-ray panel is visible
    And the x-ray panel shows a code block

  Scenario: X-ray scene fits within viewport
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I hover over the first grid component
    Then an x-ray panel is visible
    And the x-ray panel is within the viewport bounds

  @mobile
  Scenario: X-ray is activatable via FAB popup on mobile
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I tap the slides FAB button
    Then the FAB popup is visible
    And the popup contains an X-ray option

  @mobile
  Scenario: X-ray activates on tap after enabling via FAB popup
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I tap the slides FAB button
    And I tap the X-ray option in the popup
    Then the FAB button has the xray-active style
    And I tap the first grid component
    Then an x-ray panel is visible

  @mobile
  Scenario: X-ray deactivates by tapping the FAB again
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I tap the slides FAB button
    And I tap the X-ray option in the popup
    Then the FAB button has the xray-active style
    And I tap the slides FAB button
    Then the FAB button does not have the xray-active style
