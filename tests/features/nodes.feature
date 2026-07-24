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
    And I open the accordion section "Network map"
    Then the LightNode network map is visible

  Scenario: The UX results dataset renders the scenario grid
    When I navigate to "/nodes"
    And I wait for the page to be interactive
    And I open the accordion section "UX test results"
    Then the "uxtests" bound grid shows at least 20 rows

  Scenario: Results that predate this build are called stale, not shown as green
    # A CI run that dies before publishing (an infra 429 on the action download
    # aborted one before ANY step) leaves the old file in place, so the board
    # kept showing yesterday's numbers as if current. The gap between the data
    # and this build is the honest signal — a ✅ must not survive it.
    When I navigate to "/nodes"
    And I wait for the page to be interactive
    And I open the accordion section "Full Gherkin report"
    And the published results are from a run long before this build
    Then the totals stat says the results are stale
