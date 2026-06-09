Feature: Core pages load without errors

  Background:
    Given I have a clean browser page

  Scenario: Home page loads
    When I navigate to "/"
    Then the page title contains "Lightcodepedia"
    And there are no JS console errors

  Scenario: Tutorial 101 loads
    When I navigate to "/tutorial101"
    Then the page title contains "Lightcodepedia"
    And there are no JS console errors

  Scenario: Components page loads
    When I navigate to "/components/"
    Then the page title contains "Lightcodepedia"
    And there are no JS console errors

  Scenario: Components examples page loads
    When I navigate to "/components/examples"
    Then the page title contains "Lightcodepedia"
    And there are no JS console errors

  Scenario: License page loads
    When I navigate to "/license"
    Then the page title contains "Lightcodepedia"
    And there are no JS console errors
