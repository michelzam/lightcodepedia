Feature: LightNode network page

  Background:
    Given I have a clean browser page

  Scenario: Nodes page loads
    When I navigate to "/nodes"
    And I wait for the page to be interactive
    Then the LC platform is loaded

  Scenario: The network map renders
    When I navigate to "/nodes"
    And I wait for the page to be interactive
    Then the LightNode network map is visible

  Scenario: The UX results dataset renders the scenario grid
    When I navigate to "/nodes"
    And I wait for the page to be interactive
    And I open the accordion section "UX test results"
    Then the "uxtests" bound grid shows at least 20 rows
