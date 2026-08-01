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

  Scenario: The trophy's reset truly forgets the page's score
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Scored page

      **Q:** Ready?

      - [x] Yes
      - [ ] No
      {: .quiz }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    And I answer the quiz correctly
    And I open the trophy and reset the score
    Then the score store is empty
    When the runner page reloads
    Then the score store is empty

  Scenario: Two right answers make a quiz multi-select by themselves
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Multi page

      **Q:** Pick all that apply.

      - [x] Alpha
      - [x] Beta
      - [ ] Gamma
      {: .quiz }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    Then the quiz grades with a Check button
    When I select "Alpha" and "Beta" and check
    Then the trophy shows "1/1"

  Scenario: The trophy's progression bar fills when a point lands
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Bar page

      **Q:** Ready?

      - [x] Yes
      - [ ] No
      {: .quiz }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    And I answer the quiz correctly
    Then the trophy's progression bar is filling
