Feature: Frame flags are a scope, not a page setting
  A teacher frames ONE url in an LMS (?focus=1&navigable=0&open=…) and the
  learner clicks a folder card. Before this, the next page arrived with no
  flags at all — the full platform, in a new tab, outside the scope the
  teacher set up. The flags now ride every same-origin hop, and an
  allowlisted link stays inside the frame unless ?open_in=tab says otherwise.

  Background:
    Given I have a clean browser page

  Scenario: An ordinary internal link carries the frame flags forward
    A framed page that is still navigable (focus=1&navigable=1) keeps its
    scope on every hop — focus alone deliberately neutralises links, which
    is a different rule, tested below.

    When I navigate to "/components/text?focus=1&navigable=1&editable=0"
    And I wait for the page to be interactive
    And I follow the first internal link
    Then I actually left the page I was on
    And the page I land on still carries "focus=1"
    And the page I land on still carries "editable=0"

  Scenario: An allowlisted link stays in the frame, flags intact
    When I navigate to "/components/text?focus=1&navigable=0&open=/components/*"
    And I wait for the page to be interactive
    And I follow the first internal link to "/components/"
    Then I actually left the page I was on
    And no second tab was opened
    And the page I land on still carries "focus=1"
    And the page I land on still carries "navigable=0"

  Scenario: open_in=tab restores the side-by-side behaviour
    When I navigate to "/components/text?focus=1&navigable=0&open=/components/*&open_in=tab"
    And I wait for the page to be interactive
    And I follow the first internal link to "/components/"
    Then a second tab was opened carrying "focus=1"

  Scenario: An unframed page is left completely alone
    When I navigate to "/components/text"
    And I wait for the page to be interactive
    And I follow the first internal link
    Then the page I land on carries no frame flags
