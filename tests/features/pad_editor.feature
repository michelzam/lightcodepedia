Feature: The pad types like a text field, painted
  Michel, 2026-10-08: colours in the pad's source so learners match the
  components — and the colours must not cost undo: a run of typing is one
  ⌘Z, as in the run editor (the mirror is patched, not rebuilt, per key).

  Background:
    Given I have a clean browser page
    When I navigate to "/components/text"
    And I wait for the page to be interactive
    And I wait for the selector "[data-lc-id='playground'] .lc-mdpad-in"

  Scenario: A run of typing undoes as one, and the mirror follows the text
    When I type "  # hello" at the end of the "playground" pad
    Then the "playground" pad ends with "  # hello"
    And the "playground" pad's mirror shows "# hello"
    When I undo in the "playground" pad
    Then the "playground" pad does not contain "# hello"
    And the "playground" pad's mirror does not show "# hello"

  Scenario: ✎ Hide folds the editor, ✎ Edit brings it back
    Michel, 2026-10-09, on the phone: "a small button to fold the editor so we
    can see the whole width of the preview side, and (un)fold".

    When I press "✎ Hide" on the "playground" pad
    Then the "playground" pad's source is folded away
    And the "playground" pad's preview spans the pad
    When I press "✎ Edit" on the "playground" pad
    Then the "playground" pad's source is shown again

  Scenario: A pad's seed keeps its decorations glued to their lines in the runner
    Michel, 2026-10-09: the runner put a blank line above every decoration,
    fences included, so a pad opened with a gap the lesson never had, and a
    learner copying that shape left a datagrid's decoration alone — it landed
    on the query above and the query vanished. Fences are verbatim now.

    Given the GitHub contents API serves "courses/demo/module_05/glued.md" with the document:
      """
      # Glued

      `````markdown
      # App

      ```
      family,dog
      Kaur,Scout
      ```
      {: .dataset #families }

      [Families](#)
      {: .datagrid source="families" }
      `````
      {: .mdpad #glued decorations="true" rows="10" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_05/glued.md"
    And I wait for the page to be interactive
    Then the "glued" pad's text keeps every decoration glued to its line

  Scenario: A decoration's line wears its component's icon in the gutter
    Michel, 2026-10-10: "to see the decoration's component emoji in the
    gutter: 🛢️ for dataset". The icons are the component model's, the ones
    the x-ray and the editor show; a decoration that names no component
    (an id alone) wears none.

    Given the GitHub contents API serves "courses/demo/module_04/icons.md" with the document:
      """
      # Icons

      `````markdown
      # App
      {: #top }

      ```
      family,dog
      Kaur,Scout
      ```
      {: .dataset #families }

      [Families](#)
      {: .datagrid #fam_grid source="families" }

      [The family](#)
      {: .form master="fam_grid" }
      `````
      {: .mdpad #icons decorations="true" rows="14" numbers="true" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_04/icons.md"
    And I wait for the page to be interactive
    Then the "icons" pad's gutter shows "🛢️" on line 8, "▦" on line 11 and "☷" on line 14
    And the "icons" pad's gutter shows no icon on line 2

  Scenario: A copy saved with the old gaps opens glued, ready to save
    Michel, 2026-10-10: "no useless empty lines before decorations" (modules
    4 and 5). Pads saved before the 2026-10-09 runner fix kept the gap above
    every decoration, and a gap moves a decoration onto the next block. A
    decorated pad glues them back on load, outside fences; the text differs
    from the saved one, so 💾 offers to keep it.

    Given a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/faces.md" with the document:
      """
      # Faces

      `````markdown
      # Meet a dog
      `````
      {: .mdpad #faces decorations="true" save="faces.md" rows="12" }
      """
    And a connected bench whose "courses/demo/mod/faces.md" holds the document
      """
      # Meet a dog

      [dogs](dogs.yaml)

      {: .dataset #dogs }

      [The dogs](#)


      {: .datagrid #dog_grid source="dogs" }

      ```markdown
      [kept](#)

      {: .verbatim }
      ```
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/faces.md"
    And I wait for the page to be interactive
    Then the pad is marked as the reader's own
    And the "faces" pad's text keeps every decoration glued to its line, fences aside
