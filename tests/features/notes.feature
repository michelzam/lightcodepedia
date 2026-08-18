Feature: 💬 The reader's margin — one note per block, kept and versioned in the bench
  The lesson is the vault's; the margin is the reader's. Every block can
  carry ONE note, stored as a `## <anchor>` section in __lesson.notes.md in
  the LEARNER'S bench — underscored so the folder's cards never show it.
  The margin is a place, not a chute: reopening a block shows the note,
  editing rewrites its section, clearing deletes it, and git keeps the
  whole story. Under the x-ray, annotated blocks wear a 💬 at a glance.
  The teacher reads margins later through the roster, which already names
  every learner's bench. (Questions-as-a-kind are parked — this could grow
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
    Given a connected bench whose "courses/demo/mod/__lesson.notes.md" does not exist yet
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And I open the note composer on the lesson prose
    And I write the note "Why is it called source and not input?" and keep it
    Then the bench received a commit to "courses/demo/mod/__lesson.notes.md" containing "Why is it called source and not input?"
    And the margin holds 1 section for the block's own words
    And the author's repo received no commit

  Scenario: Reopening a noted block shows the note — the margin is a place, not a chute
    Given a connected bench whose "courses/demo/mod/__lesson.notes.md" holds "# 💬 notes\n\n## «The prose here belongs to the course.»\n\nFirst thought."
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And I open the note composer on the lesson prose
    Then the note area already holds "First thought."

  Scenario: Editing the note rewrites its section — one block, one note
    Given a connected bench whose "courses/demo/mod/__lesson.notes.md" holds "# 💬 notes\n\n## «The prose here belongs to the course.»\n\nFirst thought."
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And I open the note composer on the lesson prose
    And I write the note "Better thought." and keep it
    Then the bench received a commit to "courses/demo/mod/__lesson.notes.md" containing "Better thought."
    And the committed margin no longer contains "First thought."
    And the margin holds 1 section for the block's own words

  Scenario: Clearing the note removes it — and git remembers the story anyway
    Given a connected bench whose "courses/demo/mod/__lesson.notes.md" holds "# 💬 notes\n\n## «The prose here belongs to the course.»\n\nFirst thought."
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And I open the note composer on the lesson prose
    And I clear the note and keep it
    Then the committed margin no longer contains "First thought."
    And the margin holds 0 sections for the block's own words

  Scenario: Annotated blocks show their 💬 at a glance under the x-ray
    Given a connected bench whose "courses/demo/mod/__lesson.notes.md" holds "# 💬 notes\n\n## «The prose here belongs to the course.»\n\nFirst thought."
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And I sweep the x-ray over the lesson prose
    Then the noted block wears the margin mark

  Scenario: The vault's prose offers a margin, never an editor
    A read-only page used to refuse the gear entirely — correct about
    editing, but it also silenced the reader. Now the badge itself says
    what the tap will do: 💬, and what opens has no knobs, no Apply, no
    Save, not even a tab back to them.

    Given a connected bench whose "courses/demo/mod/__lesson.notes.md" does not exist yet
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

  Scenario: A margin written before the dunder rule is adopted, not orphaned
    Notes used to be `_lesson.notes.md`. A single underscore only hides a file
    from the folder's cards — it never stopped a publish — so the margin moved
    to `__lesson.notes.md`, which never travels. Anything already written under
    the old name must still open, or renaming the convention loses somebody's
    thinking.

    Given a connected bench whose "courses/demo/mod/_lesson.notes.md" holds "# 💬 notes\n\n## «The prose here belongs to the course.»\n\nWritten before the rename."
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And I open the note composer on the lesson prose
    Then the note area already holds "Written before the rename."

  Scenario: Saving an adopted margin writes the DUNDER name, never the old one
    The old file is left where it is — git keeps it, and the publish gate
    excludes both names — but from now on the writing goes to the new path.

    Given a connected bench whose "courses/demo/mod/_lesson.notes.md" holds "# 💬 notes\n\n## «The prose here belongs to the course.»\n\nWritten before the rename."
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And I open the note composer on the lesson prose
    And I write the note "Thought after the rename." and keep it
    Then the bench received a commit to "courses/demo/mod/__lesson.notes.md" containing "Thought after the rename."

  Scenario: The margin loads even when the x-ray wakes outside the render
    xray_edit handed e.target — whatever the pointer was over — to the code
    that resolves the margin's path, and that code walks up with .closest() to
    find the render root. Hover the topbar first and the path resolved
    somewhere else entirely; _notesTried had already latched, so the page's
    notes stayed invisible for the whole visit and no block ever wore its 💬.

    Given a connected bench whose "courses/demo/mod/__lesson.notes.md" holds "# 💬 notes\n\n## «The prose here belongs to the course.»\n\nWritten earlier."
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And the x-ray wakes up on the topbar, outside the render
    Then the margin still knows the page's notes
    And the noted block wears its 💬
    When I open the note composer on the lesson prose
    Then the note area already holds "Written earlier."

  Scenario: A note whose block was rewritten is listed, not lost
    The anchor for a block with no #id is its first sixty characters, so
    editing the prose orphans its note: the text stays in the file and nothing
    on the page can reach it. That happened to a real note when the module 02
    index was rewritten. Whatever the page cannot place, it shows.

    Given a connected bench whose "courses/demo/mod/__lesson.notes.md" holds "# 💬 notes\n\n## «A paragraph that used to be here»\n\nThe thinking I do not want to lose."
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And the x-ray wakes up on the topbar, outside the render
    Then the lost margin lists "The thinking I do not want to lose."
    And the lost margin lists "A paragraph that used to be here"

  Scenario: A margin that still matches its block shows no lost panel
    Given a connected bench whose "courses/demo/mod/__lesson.notes.md" holds "# 💬 notes\n\n## «The prose here belongs to the course.»\n\nStill attached."
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And the x-ray wakes up on the topbar, outside the render
    Then the noted block wears its mark in the left gutter
    And the lost margin is not shown

  Scenario: The marks appear the moment x-ray mode turns on — no hover needed
    decorate() was reachable only from an alt-pointermove, so turning the x-ray
    on with the ⚙️ pill loaded no notes and marked nothing. Marks appeared one
    at a time as the pointer swept each paragraph, and on a touch screen never
    at all. Michel: "the old icon only appears when I hoven the mouse over the
    paragraph."

    Given a connected bench whose "courses/demo/mod/__lesson.notes.md" holds "# 💬 notes\n\n## «The prose here belongs to the course.»\n\nMarked without a mouse."
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And the page enters X-ray mode
    Then the noted block wears its mark in the left gutter
    And the note area is reachable without ever hovering

  Scenario: The margin belongs to the page on screen, not the one before it
    Michel annotated the title of "🚶 A Long Walk" and his note landed in a
    file called __run.notes.md, headed "docs/run.md — notes" — the engine's own
    shell, not the lesson. Two faults, one cause. notesPathFor asked the
    element under the pointer for a render root instead of asking the page, and
    fell through to the runner's page path when it found none. And the loaded
    margin was cached with no idea which page it came from, so the FIRST page of
    a session named the file for every page after it. Nothing on the lesson
    could find the note again, and no block ever wore a mark.

    Given a connected bench whose "courses/demo/mod/__lesson.notes.md" does not exist yet
    And the GitHub contents API serves "courses/demo/mod/second.md" with the document:
      """
      # Second lesson

      The prose here belongs to the course.
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And the x-ray wakes up on the topbar, outside the render
    And I move to the runner source "gh:acme/demo-vault/courses/demo/mod/second.md"
    And I wait for the page to be interactive
    And I open the note composer on the lesson prose
    And I write the note "This one is about the second page." and keep it
    Then the bench received a commit to "courses/demo/mod/__second.notes.md" containing "This one is about the second page."
    And no margin was ever written for the runner's own shell

  Scenario: A note survives its block being reworded
    A note's whole purpose is to ask for an edit, and taking the advice used to
    put the note out of reach: Michel shortened a title from "The Long Walk" to
    "A Long Walk" and the note on it went lost. So a note the page cannot place
    exactly gets one more chance at the closest block still without one, and
    the match RENAMES its section, so the next save records the anchor that
    matches the page now.

    Given a connected bench whose "courses/demo/mod/__lesson.notes.md" holds "# 💬 notes\n\n## «The prose here belongs to this course.»\n\nWritten before the rewording."
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And the page enters X-ray mode
    Then the noted block wears its mark in the left gutter
    And the lost margin is not shown
    When I open the note composer on the lesson prose
    Then the composer shows "Written before the rewording."

  Scenario: Rewording is forgiving, but not blind
    The rescue must not hand a note to a paragraph that merely sits nearby.
    Two different sentences keep their own margins, and a note for a block that
    is really gone still goes to the lost list.

    Given a connected bench whose "courses/demo/mod/__lesson.notes.md" holds "# 💬 notes\n\n## «Adoption fees went up in March and nobody told us»\n\nThe thinking I do not want to lose."
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And the page enters X-ray mode
    Then the lost margin lists "The thinking I do not want to lose."

  Scenario: An absent margin is never asked for blindly
    Every page load read the margin file just in case, and the 404 for
    the note nobody wrote yet landed in the console of every demo
    (Michel, 2026-08-18). The bench's tree already says what exists —
    ask it once, quietly.

    Given a connected bench whose "courses/demo/mod/__lesson.notes.md" does not exist yet
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And the page flips into x-ray
    Then no read was issued for any notes file
