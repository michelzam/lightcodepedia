Feature: X-ray inspector

  Background:
    Given I have a clean browser page

  Scenario: X-ray panel appears on hover over a component
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I hover over the first grid component
    Then an x-ray panel is visible
    And the x-ray panel shows a component class name

  Scenario: X-ray panel identifies the bound chart component
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I hover over the chart component
    Then an x-ray panel is visible
    And the x-ray panel mentions "Chart"

  Scenario: X-ray panel identifies the map component
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I hover over the map component
    Then an x-ray panel is visible
    And the x-ray panel mentions "Map"

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

  Scenario: Shift x-ray reveals the whole connected data chain
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I shift-hover over the chart component
    Then the x-ray scene mentions "Chart"
    And the x-ray scene mentions "Datagrid"
    And the x-ray scene mentions "Dataset"

  Scenario: Shift x-ray connects the trigger to its avatar
    When I navigate to "/components/examples/avatar"
    And I wait for the page to be interactive
    And I shift-hover over the avatar overlay "gatin_avatar"
    Then the x-ray scene mentions "AvatarTrigger"
