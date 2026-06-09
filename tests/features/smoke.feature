Feature: Core pages load without errors

  Background:
    Given I have a clean browser page

  Scenario: Home page loads
    When I navigate to "/"
    And I wait for the page to be interactive
    Then the LC platform is loaded
    And there are no JS console errors

  Scenario: Tutorial 101 loads
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    Then the LC platform is loaded
    And there are no JS console errors

  Scenario: Components page loads
    When I navigate to "/components/"
    And I wait for the page to be interactive
    Then the LC platform is loaded
    And there are no JS console errors

  Scenario: Components examples page loads
    When I navigate to "/components/examples"
    And I wait for the page to be interactive
    Then the LC platform is loaded
    And there are no JS console errors

  Scenario: License page loads
    When I navigate to "/license"
    And I wait for the page to be interactive
    Then the LC platform is loaded
    And there are no JS console errors
