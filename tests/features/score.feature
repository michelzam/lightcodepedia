Feature: Per-page score memory

  Quiz scores are saved per page in localStorage: the 🏆 badge shows your
  remembered score when you reopen a page, and a card linking to a scored page
  shows that score as a corner tag.

  Background:
    Given I have a clean browser page

  Scenario: A page remembers your score on revisit
    When I navigate to "/components/text"
    And I wait for the page to be interactive
    And I record quiz answers "1/2" and reload
    Then the score badge shows "1/2"

  Scenario: A card shows the remembered score for the page it links to
    When I navigate to "/"
    And I wait for the page to be interactive
    And I store a score "3/5" for page "/tutorial103"
    And I reload the page
    Then a card score tag shows "3/5"
