Feature: Avatar — speaking overlay instructor

  Background:
    Given I have a clean browser page

  Scenario: Avatar examples page loads without errors
    When I navigate to "/components/examples/avatar"
    And I wait for the page to be interactive
    Then the LC platform is loaded
    And there are no JS console errors

  Scenario: The avatar overlay character appears
    When I navigate to "/components/examples/avatar"
    And I wait for the page to be interactive
    Then the avatar overlay "prof_avatar" is visible

  Scenario: The trigger starts the avatar speaking
    When I navigate to "/components/examples/avatar"
    And I wait for the page to be interactive
    And I click the avatar trigger for "prof_avatar"
    Then the avatar trigger for "prof_avatar" shows the stop label
    And the avatar "prof_avatar" is in the "speaking" state

  Scenario: Clicking the trigger again stops the avatar
    When I navigate to "/components/examples/avatar"
    And I wait for the page to be interactive
    And I click the avatar trigger for "prof_avatar"
    And I click the avatar trigger for "prof_avatar"
    Then the avatar "prof_avatar" is in the "idle" state

  Scenario: A Rive state-machine character renders on canvas
    When I navigate to "/components/examples/avatar"
    And I wait for the page to be interactive
    Then the avatar overlay "riv_avatar" is visible
    And the avatar "riv_avatar" shows a "canvas.lc-avatar-rive" character

  Scenario: A Rive narrator guides the Lucky and Wanda playground
    When I navigate to "/components/examples/lucky3d"
    And I wait for the page to be interactive
    Then the avatar overlay "lucky_guide" is visible
    And the avatar "lucky_guide" shows a "canvas.lc-avatar-rive" character

  Scenario: X-ray identifies the Avatar component
    When I navigate to "/components/examples/avatar"
    And I wait for the page to be interactive
    And I hover over the avatar overlay "prof_avatar"
    Then an x-ray panel is visible
    And the x-ray panel mentions "Avatar"
