Feature: Component gallery behaviors

  Background:
    Given I have a clean browser page

  Scenario: Selecting a grid row fills the bound form
    When I navigate to "/components/form"
    And I wait for the page to be interactive
    And I click the grid row containing "Wanda"
    Then a form titled "Wanda" is visible

  Scenario: Accordion sections open on click
    When I navigate to "/components/accordion"
    And I wait for the page to be interactive
    And I open the first accordion section
    Then the accordion section body has content

  Scenario: Liquid build-time includes render on the help archive
    When I navigate to "/archive/help"
    And I wait for the page to be interactive
    Then an embedded iframe from "onlineide" is present
    And an embedded iframe from "pythontutor" is present

  Scenario: A bound grid drives a bound-to detail chart
    When I navigate to "/components/dataset"
    And I wait for the page to be interactive
    And I click the bound grid "monthly_grid" row containing "Feb"
    Then the detail chart bound to "monthly_grid" renders a canvas
