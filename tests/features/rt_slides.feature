Feature: RT slides parity — Present and Reel work on a runner render
  The slides engine takes its deck census once, at page load, from the page's
  own direct children — so /run.html was flagged deckless before the fetched
  course ever rendered (nested inside the runner root), and Present/Reel went
  silently dead. After each page-level render the runner now calls
  lcSlidesRebuild(root): the deck re-partitions inside the render root and
  the modes come back. Embedded demos never hijack their host page's deck.

  @mobile
  Scenario: A rendered course partitions into slides and Present works
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Demo course

      ## First section

      Alpha content.

      ## Second section

      Beta content.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    Then the runner render partitions into 3 slides
    When I tap the slides FAB button
    Then the popup contains a "Present" option
    When I click the Present option in the popup
    Then the page is in present mode
    And the active slide shows "Demo course"

  @mobile
  Scenario: Reel mode snaps through the same rendered deck
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Demo course

      ## First section

      Alpha content.

      ## Second section

      Beta content.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    Then the runner render partitions into 3 slides
    When I tap the slides FAB button
    And I click the Reel option in the popup
    Then the page is in reel mode
    And the first rendered slide is visible

  Scenario: Present and Reel retire when the next render has no deck
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Demo course

      ## First section

      Alpha content.

      ## Second section

      Beta content.
      """
    And the GitHub contents API serves "courses/demo/flat.md" with the document:
      """
      # Flat page

      No sections here.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    Then the runner render partitions into 3 slides
    When the runner hash-navigates to "gh:acme/demo/courses/demo/flat.md"
    Then the Present and Reel options are hidden again
