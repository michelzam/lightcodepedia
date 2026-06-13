Feature: Page editor — AI agent tab

  The editor drawer offers a third tab, after Blocks and Raw, where the
  author types a prompt to change the page. This asserts the structural
  slice that needs no GitHub token: the tab exists and reveals a prompt.

  Background:
    Given I have a clean browser page

  Scenario: The editor offers an Agent tab that reveals a prompt
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the page editor
    And I switch to the editor "agent" tab
    Then the editor agent pane shows a prompt box
