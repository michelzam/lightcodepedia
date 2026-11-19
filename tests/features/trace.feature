Feature: The paste trace — what was typed, pasted and applied, one row per save, counts only

  Michel, 2026-11-19: "count the number of characters pasted in the mdpad from elsewhere, while
  saving the info only on save … stay discrete but not penalize … match a paste with any part
  from that page, including agent's output, and keep the provenance … by page, in the progress
  record, in a less explicit way, but easy to collect for research by deterministic code".
  A row: <page>@<time>  c  1  typed  from-the-page  from-elsewhere  pastes  applied  from>to:n;…
  (`~` is elsewhere; `>` a paste, `=>` the page's own write)

  Background:
    Given I have a clean browser page
    And I am signed in with a course key
    And this browser knows me as "zamm"
    And this browser is paired to the bench "acme/bench"
    And my bench "acme/bench" holds nothing yet
    And my bench "acme/bench" takes saves
    And the GitHub contents API serves "courses/demo/mod/trace.md" with the document:
      """
      # A page that traces

      ```python
      def first_listing():
          return "Logo design, a simple two-color logo with one round of changes"
      ```
      {: .code #snippet title="snippet" bound="pad" }

      ```markdown
      # My notes
      ```
      {: .mdpad #pad save="notes.md" rows="6" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/trace.md"
    And I wait for the page to be interactive

  Scenario: A paste from elsewhere is counted, once, at the save — never its text
    When I type "Hello" in the pad "pad"
    And I paste 180 characters from elsewhere into the pad "pad"
    Then the progress record holds 0 trace rows
    When I press 💾 on the pad "pad"
    Then the progress record holds 1 trace rows
    And the last trace row says typed=5 page=0 ext=180 ext_n=1 applied=0 paths=~>pad:180

  Scenario: A paste of a part of the page keeps its provenance; the page's own writes are applied, not typed
    When I paste the lines of the code card "snippet" into the pad "pad"
    And I press ⬇ Add on the code card "snippet" for the trace
    And I press 💾 on the pad "pad"
    Then the last trace row says typed=0 page={card} ext=0 ext_n=0 applied={card} paths=snippet=>pad:{card};snippet>pad:{card}

  Scenario: A short paste and a save with nothing to count write no row
    When I paste 12 characters from elsewhere into the pad "pad"
    And I press 💾 on the pad "pad"
    Then the progress record holds 0 trace rows
