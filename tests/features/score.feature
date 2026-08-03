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

  Scenario: A card follows the score as it changes, with no reload
    A shelf can carry a card for the very page you are standing on. The
    badge was written once and latched, so the card kept the old number
    while the trophy two inches above it showed the new one. Two numbers
    for one fact is worse than one number.

    When I navigate to "/"
    And I wait for the page to be interactive
    And I store a score "1/5" for page "/tutorial103"
    And I reload the page
    Then a card score tag shows "1/5"
    When the score for page "/tutorial103" becomes "4/5"
    Then a card score tag shows "4/5"
    And no card still shows "1/5"
