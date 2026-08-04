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

  Scenario: A run's result is remembered like the score beside it
    status="…" in the page is the AUTHOR's declaration, one value for
    everyone. What a reader's own run produced is theirs — and it used to
    evaporate on reload while their quiz score survived, so the same page
    said "you scored 3/3" and "nothing has run here".

    When I navigate to "/components/quiz"
    And I wait for the page to be interactive
    And I run the page's embedded features
    Then every embedded feature passes
    When I reload the page
    Then a feature card is remembered as passing

  Scenario: A card shows the reader's own run, not the author's declaration
    lc_features already remembered what a run made of a .feature, and the
    PAGE showed it. The card did not: its dots came from the status= parsed
    out of the markdown, so a learner's run showed on the page while the
    card that leads there still carried the author's claim. One fact, two
    answers — the same inconsistency scores had, one level up.

    When I navigate to "/components/"
    And I wait for the page to be interactive
    And the run on page "/components/quiz" is remembered as "failing"
    And I reload the page
    Then a card shows a "failing" feature dot
    And that card is marked as remembering my run
