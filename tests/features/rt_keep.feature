Feature: 📌 Keep & voice files the story in the rendered page
  The keep flow used to commit a kept answer's dialogue to the page named by
  location.pathname — on a runner render that is docs/run.md, the vehicle:
  audio played (content-addressed) while the story text vanished from the
  author's view. A keep on a page-level render must commit to the RENDERED
  file in the rendered repo, and never touch docs/run.md.

  Scenario: A keep on a runner render commits to the rendered file
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a yaml shim is preinstalled
    And a builder key and editor repo are connected
    And the committable GitHub page "courses/demo/mod/index.md" serves:
      """
      # Course

      ## One

      Alpha.
      """
    And commits to "docs/run.md" are watched
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    And the guide holds an unsaved answer
    And I click the guide's Keep & voice
    Then the story is committed to "courses/demo/mod/index.md"
    And nothing was committed to "docs/run.md"
