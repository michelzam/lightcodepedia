Feature: The material shelf — .folder scans unrendered material

  /lab/material lists courses/ and hubs/<session>/ with the SAME .folder
  component the site uses everywhere — open="runner" points its cards at
  unrendered material through the runner.

  Background:
    Given I have a clean browser page

  Scenario: Without an author key the shelf stays locked
    When I open the material page without a key
    Then the shelf asks for the author key

  Scenario: A node variable steers the shelf's folder
    Given a stubbed lab tree where COURSE_PATH is "curriculum"
    When I open the material page
    Then a "curriculum" card opens in the runner

  Scenario: Unset node variables fall back to the gentle default
    Given a stubbed lab tree with no node variables
    When I open the material page
    Then a "courses" card opens in the runner

  Scenario: The topbar carries the HQ door on the lab
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    Then the topbar offers the HQ door

  Scenario: The HQ landing shows the cockpit cards
    When I open the HQ landing
    Then the landing offers doors to classroom and material

  Scenario: Inside the lab branch the menu switches to HQ rails
    When I open the HQ landing
    Then the topbar menu lists the classroom and the shelf
