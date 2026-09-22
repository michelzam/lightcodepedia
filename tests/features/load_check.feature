Feature: 🧠 Cognitive load check — four scores, their factors, and the change since the previous version
  Michel, 2026-09-22: "deterministic first, then LLM semantic help, step by
  step", and "compare scores with previous versions, since the improvement
  is the key". Coherence, load, friction and seduction, each from the page
  as rendered, each with its rows; every run remembered per page on the
  device, the cards saying what changed.

  Scenario: A loose form is friction, an orphan video is one hero, and the next version reads better
    Given I have a clean browser page
    And a builder key and editor repo are connected
    And the committable GitHub page "courses/demo/mod/load.md" serves:
      """
      # Load page

      ## One

      ```yaml
      fields:
        - name: title
      ```
      {: .form #f_one }

      The title is {= f_one.title }.

      ```gherkin
      Feature: One
        Scenario: reads the form
          Given nothing
      ```
      {: .feature #chk_one tags="learn" visible="true" }

      - What is one?
        - [x] one
        - [ ] two
      {: .quiz #q_one visible="= chk_one.passing" }

      ## Two

      ```yaml
      fields:
        - name: note
      ```
      {: .form #loose }

      [Clip](https://youtu.be/abc12345678)
      {: .video #vid }
      """
    And the commits API names the page's last commit "edit: drop the loose form"
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/load.md"
    And I wait for the page to be interactive
    And I open the page editor
    And I switch to the editor "a11y" tab
    And the load rule "kinds_per_section_max" is set to 2
    And I press the editor's load check
    Then the load card "friction" reads "1 loose control" and warns
    And clicking the section row "One" outlines that section on the page
    And the load card "seduction" reads "1 orphan media" and passes
    And the load card "coherence" reads "2 validations" and passes
    And the load rows name "form #loose"
    And the load rules are listed, "loose controls, at most" set to "0"
    When the page moves to a new version without the loose form
    And I press the editor's load check
    Then the load card "friction" reads "0 loose controls" and says "-1 vs previous"
    And the load history remembers 2 runs
    And the history grid marks "loose" as improved on the latest run, its headers explained
    And the latest version's tooltip names the commit "edit: drop the loose form"
