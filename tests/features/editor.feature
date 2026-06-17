Feature: Page editor — ✨ AI edit dialog

  The editor's ✨ button (top bar) opens a dialog scoped to the current
  selection, where the author asks for a change. This asserts the
  structural slice that needs no GitHub token: the button opens the
  dialog and reveals a prompt; and the editor has a Log tab.

  Background:
    Given I have a clean browser page

  Scenario: The ✨ button opens the AI edit dialog with a prompt
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the page editor
    And I click the editor "ed-agent-btn" button
    Then the editor agent pane shows a prompt box

  Scenario: The editor has a Log tab
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the page editor
    And I switch to the editor "log" tab
    Then the editor log pane is visible

  Scenario: The editor has a Features tab
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the page editor
    And I switch to the editor "features" tab
    Then the editor features pane is visible

  Scenario: The editor has a Diagram tab
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the page editor
    And I switch to the editor "diagram" tab
    Then the editor diagram pane is visible

  Scenario: The Diagram tab renders the page's class graph
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the page editor
    And I load sample components into the editor
    And I switch to the editor "diagram" tab
    Then the editor diagram renders a class graph

  Scenario: The Raw tab is the dark basement workshop
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the page editor
    And I switch to the editor "raw" tab
    Then the raw editor is dark themed

  Scenario: The Raw editor has a formatting toolbar
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the page editor
    And I switch to the editor "raw" tab
    Then the editor formatting toolbar is visible
    When I bold a selection with the toolbar
    Then the raw editor contains "**"

  Scenario: The Blocks-tab Content editor is dark too
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the page editor
    And I load sample components into the editor
    And I switch to the editor "blocks" tab
    And I select the first block
    Then the block content editor is dark themed
