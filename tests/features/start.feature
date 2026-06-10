Feature: Onboarding wizard

  Background:
    Given I have a clean browser page

  Scenario: Start page loads without errors
    When I navigate to "/start"
    And I wait for the page to be interactive
    Then the LC platform is loaded
    And there are no JS console errors

  Scenario: The wizard renders six steps with only the first active
    When I navigate to "/start"
    And I wait for the page to be interactive
    Then the wizard shows 6 steps
    And wizard step 1 is active
    And wizard steps 2 through 6 are locked

  Scenario: Confirming a GitHub account advances to the access-key step
    When I navigate to "/start"
    And I wait for the page to be interactive
    And I click the wizard button "I have an account"
    Then wizard step 1 is done
    And wizard step 2 is active

  Scenario: The access-key check requires a key first
    When I navigate to "/start"
    And I wait for the page to be interactive
    And I click the wizard button "I have an account"
    And I click the wizard button "Check key"
    Then the access-key result shows an error mentioning "access key"

  Scenario: Karma rewards are advertised on the wizard steps
    When I navigate to "/start"
    And I wait for the page to be interactive
    Then a wizard step advertises "+15 pts" karma
    And a wizard step advertises "+10 pts" karma
    And a wizard step advertises "+50 pts / friend" karma
