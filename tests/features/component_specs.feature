Feature: Component specs run green

  Hidden .feature blocks embedded on component pages must pass when executed
  by the in-browser MicroPython step runner. This dogfoods the runtime: the
  component's own model classes drive its live demo and assert the behaviour.

  Scenario: Accordion spec passes
    Given I have a clean browser page
    When I navigate to "/components/accordion"
    And I wait for the page to be interactive
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: Tabs spec passes
    Given I have a clean browser page
    When I navigate to "/components/tabs"
    And I wait for the page to be interactive
    And I wait for the selector ".lc-tab-btn"
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: Radio spec passes
    Given I have a clean browser page
    When I navigate to "/components/radio"
    And I wait for the page to be interactive
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: Dropdown spec passes
    Given I have a clean browser page
    When I navigate to "/components/dropdown"
    And I wait for the page to be interactive
    And I run the page's embedded features
    Then every embedded feature passes
