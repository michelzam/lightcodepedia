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

  # Michel, 2026-11-24, on a page whose every section folds (the pilot meeting):
  # "present and reel don't work". A folding heading becomes a panel, so the deck
  # found no section to cut on, counted one slide and refused both modes.
  Scenario: A page whose sections all fold still makes a deck, and a slide shows its section open
    Given I have a clean browser page
    And the GitHub contents API serves "courses/demo/mod/folds.md" with the document:
      """
      # Folding page

      Intro.

      ## 1 · First
      {: .accordion }

      Alpha content.

      ## 2 · Second
      {: .accordion }

      Beta content.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/folds.md"
    And I wait for the page to be interactive
    Then the runner render partitions into 3 slides
    When the page enters "present" mode
    Then the page is in "present" mode
    When the deck moves to slide 2
    Then the active slide shows "Alpha content."
    When the page enters "reel" mode
    Then the page is in "reel" mode
