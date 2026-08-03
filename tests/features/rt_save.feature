Feature: One page, two repos — the fence seeds, the reader's bench persists
  A course page in the vault mixes the author's material with places where
  the learner contributes (a résumé pad, a repairable grid). The material
  and the contribution must live in DIFFERENT repos: save="my/…" makes the
  fence the author's seed and the learner's connected repo the truth. One
  writer per file — the author republishes forever, nothing ever collides.

  Background:
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/work.md" with the document:
      """
      # Work page

      ```markdown
      # Starter résumé — replace me
      ```
      {: .mdpad #cv save="my/cv.md" rows="6" }

      ```yaml
      - name: Rex
        campus: Milwauke
      ```
      {: .datagrid #dogs editable="true" save="my/dogs.yaml" height="160" }
      """

  Scenario: Without a key the page still teaches, and says how to join
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    Then the pad shows the author's starter
    And the pad's save button is disabled with a join hint

  Scenario: A joined learner with no saved copy starts from the seed
    Given a connected bench whose "my/cv.md" does not exist yet
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    Then the pad shows the author's starter
    And the pad is not marked as the reader's own

  Scenario: The saved copy wins over the seed on the next visit
    Given a connected bench whose "my/cv.md" holds "# Alice — WHS volunteer"
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    Then the pad shows "# Alice — WHS volunteer"
    And the pad is marked as the reader's own

  Scenario: Saving writes to the learner's repo, never the author's
    Given a connected bench whose "my/cv.md" does not exist yet
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    And I type "# Mine now" into the pad and save
    Then the bench received a commit to "my/cv.md" containing "# Mine now"
    And the author's repo received no commit

  Scenario: Start over restores the seed without touching the saved file
    Given a connected bench whose "my/cv.md" holds "# Alice — WHS volunteer"
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    And I press the pad's start-over button
    Then the pad shows the author's starter
    And the bench received no commit

  Scenario: The grid loads the reader's repaired rows over the broken seed
    Given a connected bench whose "my/dogs.yaml" holds "- name: Rex\n  campus: Milwaukee"
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    Then the dogs grid shows "Milwaukee"
    And the grid is marked as the reader's own

  Scenario: The grid's keep button writes rows to the learner's repo
    Given a connected bench whose "my/dogs.yaml" does not exist yet
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    And I press the grid's keep button
    Then the bench received a commit to "my/dogs.yaml" containing "Milwauke"
