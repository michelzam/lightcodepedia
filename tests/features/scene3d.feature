Feature: Scene3D — Lucky & Wanda 3D playground

  Background:
    Given I have a clean browser page

  Scenario: 3D playground page loads without errors
    When I navigate to "/components/examples/lucky3d"
    And I wait for the page to be interactive
    Then the LC platform is loaded
    And there are no JS console errors

  Scenario: The 3D scene canvas renders
    When I navigate to "/components/examples/lucky3d"
    And I wait for the page to be interactive
    Then the 3D scene canvas is visible

  Scenario: Both objects expose their attribute panels
    When I navigate to "/components/examples/lucky3d"
    And I wait for the page to be interactive
    Then the scene shows an attribute panel for "lucky : Dog"
    And the scene shows an attribute panel for "wanda : Fish"

  Scenario: Calling a method logs the call to the scene console
    When I navigate to "/components/examples/lucky3d"
    And I wait for the page to be interactive
    And I call the "bark" method on the scene
    Then the scene console logs ">>> lucky.bark()"
    And the scene console logs "Woof! Woof!"

  Scenario: The console keeps the whole session and scrolls
    Michel, 2026-11-11: "I need to be able to scroll the content of the console, otherwise I lose
    the beginning after a while" — the console kept six lines.
    When I navigate to "/components/examples/lucky3d"
    And I wait for the page to be interactive
    And I call the scene methods 12 times, noting the first
    Then the scene console still holds its first line, and scrolls

  Scenario: Editing an attribute logs the assignment
    When I navigate to "/components/examples/lucky3d"
    And I wait for the page to be interactive
    And I change the dog colour to "Golden"
    Then the scene console logs "lucky.colour"

  Scenario: X-ray identifies the Scene3d component
    When I navigate to "/components/examples/lucky3d"
    And I wait for the page to be interactive
    And I hover over the scene3d component
    Then an x-ray panel is visible
    And the x-ray panel mentions "Scene3d"
