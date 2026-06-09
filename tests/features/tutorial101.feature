Feature: Tutorial 101 interactive components

  Background:
    Given I have a clean browser page

  Scenario: Grid renders with data
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    Then a datagrid component is visible
    And the datagrid contains at least 5 rows

  Scenario: Chart renders
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    Then a chart component is visible

  Scenario: Map renders
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    Then a map component is visible

  Scenario: Video block renders
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    Then a video block is visible

  Scenario: Grid row selection updates the chart
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I click the first row in the datagrid
    Then the chart reflects a data update
