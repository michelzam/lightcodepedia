Feature: Reel mode — Instagram-style vertical snap between titles

  Reuses the per-H2 .lc-slide sections the slides engine already builds. With
  reel mode on, the page becomes a full-viewport vertical scroll-snap
  container, one title per snap. ?reel=1 auto-enters; Esc / the FAB exits.

  Background:
    Given I have a clean browser page

  Scenario: ?reel=1 enters reel mode with a snap container
    When I navigate to "/tutorial101?reel=1"
    And I wait for the page to be interactive
    Then the page is in reel mode
    And the content is a vertical scroll-snap container

  Scenario: Reel mode can be exited
    When I navigate to "/tutorial101?reel=1"
    And I wait for the page to be interactive
    Then the page is in reel mode
    When I exit reel mode
    Then the page is not in reel mode
