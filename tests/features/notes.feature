Feature: 💬 The reader's margin — one note per block, kept and versioned in the bench
  The lesson is the vault's; the margin is the reader's. Every block can
  carry ONE note, stored as a `## <anchor>` section in _lesson.notes.md in
  the LEARNER'S bench — underscored so the folder's cards never show it.
  The margin is a place, not a chute: reopening a block shows the note,
  editing rewrites its section, clearing deletes it, and git keeps the
  whole story. Under the x-ray, annotated blocks wear a 💬 at a glance.
  The teacher reads margins later through the roster, which already names
  every student's bench. (Questions-as-a-kind are parked — this could grow
  differently.)

  Background:
    Given I have a clean browser page
    And the GitHub contents API serves "courses/demo/mod/lesson.md" with the document:
      """
      # Lesson

      The prose here belongs to the course.

      ```csv
      campus,dogs
      Milwaukee,3
      ```
      {: .dataset #adoptions }
      """

  Scenario: A note on a vault block lands in the bench, under the block's own words
    Given a connected bench whose "courses/demo/mod/_lesson.notes.md" does not exist yet
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And I open the note composer on the lesson prose
    And I write the note "Why is it called source and not input?" and keep it
    Then the bench received a commit to "courses/demo/mod/_lesson.notes.md" containing "Why is it called source and not input?"
    And the margin holds 1 section for the block's own words
    And the author's repo received no commit

  Scenario: Reopening a noted block shows the note — the margin is a place, not a chute
    Given a connected bench whose "courses/demo/mod/_lesson.notes.md" holds "# 💬 notes\n\n## «The prose here belongs to the course.»\n\nFirst thought."
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And I open the note composer on the lesson prose
    Then the note area already holds "First thought."

  Scenario: Editing the note rewrites its section — one block, one note
    Given a connected bench whose "courses/demo/mod/_lesson.notes.md" holds "# 💬 notes\n\n## «The prose here belongs to the course.»\n\nFirst thought."
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And I open the note composer on the lesson prose
    And I write the note "Better thought." and keep it
    Then the bench received a commit to "courses/demo/mod/_lesson.notes.md" containing "Better thought."
    And the committed margin no longer contains "First thought."
    And the margin holds 1 section for the block's own words

  Scenario: Clearing the note removes it — and git remembers the story anyway
    Given a connected bench whose "courses/demo/mod/_lesson.notes.md" holds "# 💬 notes\n\n## «The prose here belongs to the course.»\n\nFirst thought."
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And I open the note composer on the lesson prose
    And I clear the note and keep it
    Then the committed margin no longer contains "First thought."
    And the margin holds 0 sections for the block's own words

  Scenario: Annotated blocks show their 💬 at a glance under the x-ray
    Given a connected bench whose "courses/demo/mod/_lesson.notes.md" holds "# 💬 notes\n\n## «The prose here belongs to the course.»\n\nFirst thought."
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And I sweep the x-ray over the lesson prose
    Then the noted block wears the margin mark

  Scenario: The vault's prose offers a margin, never an editor
    A read-only page used to refuse the gear entirely — correct about
    editing, but it also silenced the reader. Now the badge itself says
    what the tap will do: 💬, and what opens has no knobs, no Apply, no
    Save, not even a tab back to them.

    Given a connected bench whose "courses/demo/mod/_lesson.notes.md" does not exist yet
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And I open the note composer on the lesson prose
    Then the composer offers no editor controls

  Scenario: An editable block offers both tabs — the part, and my margin
    Given a connected bench whose "courses/demo/mod/wiring.md" does not exist yet
    And the GitHub contents API serves "courses/demo/mod/owned.md" with the document:
      """
      # Lesson

      ```markdown
      Wire me.
      ```
      {: .embed save="wiring.md" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/owned.md"
    And I wait for the page to be interactive
    And I open the x-ray editor on the slot's text
    Then the editor offers an edit tab and a notes tab
    When I switch to the notes tab
    Then the note area is ready to write
