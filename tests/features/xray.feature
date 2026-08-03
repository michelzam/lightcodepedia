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

  Scenario: Keep commits the edited block when the builder is connected
    When I navigate to "/tutorial101"
    And I am connected as a builder with a stubbed repo
    And I wait for the page to be interactive
    And I open the x-ray editor on the local dog block
    And I change the block content to "Cute, huh — this committed dog?"
    And I keep the changes
    Then the stubbed repo received a commit containing "committed dog"
    And a green save toast confirms it

  Scenario: Keep invites anonymous learners to create an account
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the x-ray editor on the local dog block
    And I change the block content to "Cute, huh — a fleeting dog?"
    Then keeping the changes invites me to create an account

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
  Scenario: Touch X-ray teaches its gestures on entry
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I tap the slides FAB button
    And I tap the X-ray option in the popup
    Then the touch gesture hint appears

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
  Scenario: In x-ray mode a phone can still reach the rest of the page
    The lens used to swallow every touch on the page, so a phone in x-ray
    mode was frozen: you could inspect the part in front of you and never
    scroll to the next one. A finger that lands on nothing inspectable —
    a margin, a paragraph, whitespace — is scrolling, not asking.

    When I navigate to "/components/datagrid"
    And I wait for the page to be interactive
    And I tap the slides FAB button
    And I tap the X-ray option in the popup
    And I swipe up from a plain paragraph
    Then the page scrolled

  @mobile
  Scenario: A drag that starts on a part is still an inspection
    The escape hatch must not become the exit. A gesture beginning on a
    component belongs to the lens — it tracks the finger and the page stays
    put — or every inspection would slide out from under the reader.

    When I navigate to "/components/datagrid"
    And I wait for the page to be interactive
    And I tap the slides FAB button
    And I tap the X-ray option in the popup
    And I swipe up from the first grid component
    Then the page did not scroll

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
    And I shift-hover over the avatar overlay "prof_avatar"
    Then the x-ray scene mentions "AvatarTrigger"

  Scenario: Shift x-ray labels a query result as Query, not its Dataset base
    When I navigate to "/components/query"
    And I wait for the page to be interactive
    And I shift-hover over the chart component
    Then the x-ray scene mentions "Query"
