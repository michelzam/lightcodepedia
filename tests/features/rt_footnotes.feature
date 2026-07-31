Feature: Page-level footnotes — defs at the file end, one global numbering
  Concept definitions used to be trapped inside the fence that referenced
  them: each block rendered its own little list, numbering restarted at 1,
  and a definition authored at the end of the file never met its reference
  inside a block. Now every chunk's notes settle into ONE list — the last
  one on the page, exactly where end-of-file defs land — with a single
  reading-order numbering and no injected title.

  Scenario: Defs at the file end serve refs inside blocks, numbered globally
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/concepts.md" with the document:
      """
      # Concepts page

      ```
      ### First
      One idea: `alpha`[^alpha].
      ```
      {: .block }

      ```
      ### Second
      Another idea: `beta`[^beta].
      ```
      {: .block }

      [^alpha]: **Alpha** — the first concept.
      [^beta]: **Beta** — the second concept.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/concepts.md"
    And I wait for the page to be interactive
    Then footnote "alpha" settles as number 1 and "beta" as number 2
    And the page shows a single footnote list with 2 visible entries

  Scenario: A legacy in-fence definition still resolves into the page list
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/legacy.md" with the document:
      """
      # Legacy page

      ```
      ### Legacy
      Inline: `gamma`[^gamma].
      [^gamma]: **Gamma** — defined right here in the fence.
      ```
      {: .block }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/legacy.md"
    And I wait for the page to be interactive
    Then footnote "gamma" settles as number 1
