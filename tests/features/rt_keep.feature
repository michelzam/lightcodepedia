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

  Scenario: The editor on a bench render edits the rendered file, preview included
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key and editor repo are connected
    And the committable GitHub page "courses/demo/mod/index.md" serves:
      """
      # Course

      [Why](/_why)
      {: .embed }

      ## One

      Alpha.
      """
    And the counting GitHub contents API serves "courses/demo/mod/_why.md" as "why"
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    And I open the page editor
    Then the editor is editing "courses/demo/mod/index.md"
    And the editor preview shows "building beats watching"

  Scenario: Save on a bench render commits the edit to the rendered file
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key and editor repo are connected
    And the editor repo "acme/demo" grants push
    And the committable GitHub page "courses/demo/mod/index.md" serves:
      """
      # Course

      ## One

      Alpha.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    And I open the page editor
    Then the editor is editing "courses/demo/mod/index.md"
    When I append "Edited-by-bdd." to the editor and save
    Then the rendered file's commit carries "Edited-by-bdd."
