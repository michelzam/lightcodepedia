Feature: The authored guide owns its page — the generic one yields
  The generic guide summons on a 900ms timer; a runner render arrives later.
  First-come-first-served let the generic squat the single guide seed while
  the authored avatar built its big face seedless and undocked — a stale
  char that ignored clicks, with the page's kept stories unreachable behind
  the generic menu (Canvas vault render, 2026-07-30). The authored fence
  must evict the generic and take the seed; no avatar face may ever float
  undocked while idle.

  Scenario: The authored guide evicts the generic squatter on a slow render
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a story yaml shim is preinstalled
    And the learner has the generic guide enabled
    And the GitHub contents API slowly serves "courses/demo/mod/index.md" with the document:
      """
      # Course

      ```yaml
      script: []
      ```
      {: .avatar #guide dock="true" size="115" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    Then the authored guide holds the only seed
    And no avatar face floats undocked
