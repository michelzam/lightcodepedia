Feature: Vitals and model integrity — the platform measures itself

  Background:
    Given I have a clean browser page

  Scenario: The vitals collector publishes live samples on the nodes page
    When I navigate to "/nodes"
    And I wait for the page to be interactive
    And I open the accordion section "📊 Vitals & model check"
    Then the vitals card shows at least 2 samples
    And the "page_vitals" bound grid shows at least 2 rows

  Scenario: The model check card finds no broken references on the nodes page
    When I navigate to "/nodes"
    And I wait for the page to be interactive
    And I open the accordion section "📊 Vitals & model check"
    Then the model check card reports no broken references

  Scenario: Model integrity holds on the tutorial data chain
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    Then the page passes the model integrity check

  Scenario: Model integrity holds on the avatar examples
    When I navigate to "/components/examples/avatar"
    And I wait for the page to be interactive
    Then the page passes the model integrity check

  Scenario: Model integrity holds on the Lucky and Wanda playground
    When I navigate to "/components/examples/lucky3d"
    And I wait for the page to be interactive
    Then the page passes the model integrity check
