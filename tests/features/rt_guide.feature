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

  Scenario: The page's presentation verbs fold accordions and drive modes
    Given I have a clean browser page
    When I navigate to "/components/accordion"
    And I wait for the page to be interactive
    Then the verb "close" folds every accordion section
    And the verb "open" with "started" unfolds the matching section only
    And the verb "open" targets the "started" section title as its subject
    And the verb "present" enters present mode

  Scenario: The xray verb lights the pipes for a beat, then hands the page back
    "Show the pipes going from datasources to grids for a few seconds while
    walking through a lesson" (Michel, 2026-08-18). The verb must hold, not
    toggle, when a later line calls it again — with seconds it comes home
    to read by itself, leaving nothing switched on.

    Given I have a clean browser page
    When I navigate to "/components/accordion"
    And I wait for the page to be interactive
    Then the verb "xray" turns the pipes on and stays on when asked again
    And the verb "xray" with seconds returns the page to read by itself

  Scenario: The xray verb draws the pipes itself — no pointer, no fingers
    "Tested, but I see NOTHING behind the scene: no ghosts, no pipes!"
    (Michel, 2026-08-18). The mode is a lens that paints only under a
    pointer, and a bare mouse move even wiped what was there — so the verb
    must draw the pipelines scene itself and hold it against pointer noise.

    Given I have a clean browser page
    When I navigate to "/components/dataset"
    And I wait for the page to be interactive
    Then the verb "xray" reveals the wiring scene and it survives a mouse move
    And the docked source ghost floats above the ghosts that use it
    And the verb "read" folds the wiring scene away

  Scenario: The select verb picks a datagrid row through the grid's own API
    Given I have a clean browser page
    When I navigate to "/components/accordion"
    And I wait for the page to be interactive
    And a stub datagrid holds rows for "Lucky" and "Wanda"
    Then the verb "select" with "Wanda" selects that row and stands at it

  Scenario: An action-only story line is a quick stage direction, not a dead beat
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a tour yaml shim with a stage direction is preinstalled
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Staged page

      <details><summary>Alpha section</summary>Hidden content.</details>

      ```yaml
      script: []
      ```
      {: .avatar #guide dock="true" size="115" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    And I play the guide's tour
    Then the section unfolds and the narration reaches "After the beat"

  Scenario: Voice-cue tags speak but never display, and a bare at: line just walks
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a tour yaml shim with a voice cue is preinstalled
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Cue page

      Some content to walk to.

      ```yaml
      script: []
      ```
      {: .avatar #guide dock="true" size="115" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    And I play the guide's tour
    Then the bubble narrates "Take a breath" without the cue tag
