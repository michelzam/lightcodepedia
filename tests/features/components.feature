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

  Scenario: The markdown pad renders a live preview
    When I navigate to "/components/text"
    And I wait for the page to be interactive
    Then the markdown pad shows an editor and a rendered preview

  Scenario: The custom-class example shows a live Python editor
    When I navigate to "/components/examples/custom-class"
    And I wait for the page to be interactive
    Then a live Python editor is visible

  Scenario: A query aggregates a dataset into a bound grid
    When I navigate to "/components/query"
    And I wait for the page to be interactive
    Then the "by_breed" bound grid shows at least 3 rows

  Scenario: An editable query is a live SQL editor feeding a grid
    When I navigate to "/components/query"
    And I wait for the page to be interactive
    Then a live SQL editor is visible
    And the "live_q" bound grid shows at least 3 rows
