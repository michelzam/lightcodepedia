Feature: RT scores key to the rendered page, not the runner
  Quiz scores are sacred — the localStorage key must name the CONTENT. On
  /run the pathname is always /run.html, so before this every course rendered
  through the runner shared one commingled bucket ("the runner's points").
  A gh: render now keys as gh:owner/repo/path, the same key a folder card's
  href produces, so shelf cards decorate with the right page's score.

  Scenario: A runner render scores under its own gh: key
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Scored page

      ## One

      Alpha.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    Then the page score key is "gh:acme/demo/courses/demo/mod"
    And a card href to that render produces the same score key
