Feature: 🎬 Doc's pad verbs — type, save, and a music player's words for the film
  Michel, 2026-10-10: two scripts on one list of steps — "Build it with me"
  types each step into the pad and saves it with its line; "Watch it grow"
  plays the versions with their subtitles and moonwalks back. replay is from
  the beginning, play from here; Doc's save opens 💾 Save… with the line
  filled in on a learner's pad, and commits at once on the author's.

  Background:
    Given I have a clean browser page
    And the GitHub contents API serves "courses/demo/mod/faces.md" with the document:
      """
      # Faces

      `````markdown
      # Meet a dog

      [The dogs](#)
      {: .datagrid #dog_grid source="dogs" }
      `````
      {: .mdpad #faces decorations="true" save="faces.md" rows="12" comment="true" replay="0.3" }

      ```yaml
      bot: doc
      steps:
        - say: a card that follows the table
          lines: |
            [The dog](#)
            {: .form master="dog_grid" }
        - say: the card builds the photo
          find: '{: .form master="dog_grid" }'
          lines: |
            {: .form master="dog_grid" compute="photo = 'x' + str(pic)" }
      script: []
      stories:
        Build it with me:
          - do: type
            with: 1
            at: faces
          - do: save
            with: 1
            at: faces
      ```
      {: .avatar #guide }

      [🛠 Build it with me](#)
      {: .avatar_trigger target="guide" story="Build it with me" }
      """

  Scenario: Doc types a step, finds the next one's line, and never types a step twice
    Given a connected bench whose "courses/demo/mod/faces.md" does not exist yet
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/faces.md"
    And I wait for the page to be interactive
    And Doc does "type" with 1 on the "faces" pad
    Then the "faces" pad holds '{: .form master="dog_grid" }'
    When Doc does "type" with 1 on the "faces" pad
    Then the "faces" pad holds '[The dog](#)' once
    When Doc does "type" with 2 on the "faces" pad
    Then the "faces" pad holds 'compute="photo'
    And the "faces" pad holds '{: .form master="dog_grid"' once

  Scenario: Doc never types over the learner's own work
    Given a connected bench whose "courses/demo/mod/faces.md" holds "# My own page"
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/faces.md"
    And I wait for the page to be interactive
    And Doc does "type" with 1 on the "faces" pad
    Then the "faces" pad does not hold "[The dog](#)"

  Scenario: On a learner's pad, Doc's save offers the line and waits for the tap
    Given a connected bench whose "courses/demo/mod/faces.md" does not exist yet
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/faces.md"
    And I wait for the page to be interactive
    And I click the trigger "🛠 Build it with me"
    Then the "faces" pad offers to keep it as "a card that follows the table"
    And the bench received no commit
    When Doc does "type" with 2 on the "faces" pad
    Then the "faces" pad does not hold "compute="

  Scenario: On the author's own pad, Doc's save commits with the step's line
    Given a connected bench whose "courses/demo/mod/faces.md" does not exist yet
    And the key is paired as the author's own
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/faces.md"
    And I wait for the page to be interactive
    And I click the trigger "🛠 Build it with me"
    Then the bench received a commit titled "✍️ a card that follows the table"

  Scenario: replay plays the steps from the beginning; pause, frame and stop do what they say
    No history of its own: the film is the one Doc's steps make.

    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/faces.md"
    And I wait for the page to be interactive
    And Doc does "replay" on the "faces" pad with his steps
    Then the "faces" pad's film holds 3 frames
    And the "faces" pad's film ends on frame 3
    When Doc does "frame" with 2 on the "faces" pad
    Then the "faces" pad's film shows frame 2
    When Doc does "play" on the "faces" pad
    Then the "faces" pad's film ends on frame 3
    When Doc does "moonwalk" on the "faces" pad
    Then the "faces" pad's film ends on frame 1
    When Doc does "replay" on the "faces" pad
    Then the "faces" pad's film ends on frame 3
    When Doc does "stop" on the "faces" pad
    Then the "faces" pad's film is closed

  Scenario: On The Builder, each step turns its Then green, and the build goes on
    Michel, 2026-10-11: "features with steps containing assertions (thens)" —
    the page's own check drives the build. Each step names the Then it must
    turn green; typed, the check runs.

    Given the runner serves the course page "courses/micro_build_ai/module_05/01_builder.md"
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_05/01_builder.md"
    And I wait for the page to be interactive
    And Doc does "type" with 1 on the "follow_up" pad
    Then the check's step "a datagrid reads the reservations" is green
    And the "follow_up" pad is not held
    When Doc does "type" with 2 on the "follow_up" pad
    Then the check's step "a button is there to call the next family" is green
    And the check's step "nothing on the page is wired to nothing" is green

  Scenario: The Follow-Up List's TODOs, each replaced in place, turn its proof green
    Michel, 2026-10-13: the coordinator's TODO notes on the screen, the proof
    as the spec, and his app — every family in the table, one query that
    counts only the waiting ones. Each TODO goes when its part comes.

    Given the runner serves the course page "courses/micro_build_ai/module_05/02_list.md"
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_05/02_list.md"
    And I wait for the page to be interactive
    And Doc does "type" with 1 on the "follow_up" pad
    Then the check's step "all the families are in one table" is green
    When Doc does "type" with 2 on the "follow_up" pad
    Then the check's step "a query counts the families nobody met yet" is green
    When Doc does "type" with 3 on the "follow_up" pad
    Then the check's step "a sentence says how many are waiting" is green
    When Doc does "type" with 4 on the "follow_up" pad
    Then the check's step "no TODO is left on the screen" is green
    And the "follow_up" pad does not hold "TODO"
    When I run the lesson's check "list_proof"
    Then the lesson's check "list_proof" is green

  Scenario: The Proof — my own check goes red on Alvarez, the button's loop turns it green, the page's proof reads it
    Michel, 2026-10-13 ("B"): the button walks every row, so three presses
    select Alvarez, who already met Scout. The learner's own check, in the
    app, names him; a first loop in the button skips the met ones; the
    page's fixed proof checks the learner's check.

    Given the runner serves the course page "courses/micro_build_ai/module_05/03_proof.md"
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_05/03_proof.md"
    And I wait for the page to be interactive
    And Doc does "type" with 1 on the "follow_up" pad
    And I run the lesson's check "call_check"
    Then the lesson's check "call_check" is red
    And the lesson's check "call_check" says "Alvarez already met their dog"
    When Doc does "type" with 2 on the "follow_up" pad
    And I run the lesson's check "call_check"
    Then the lesson's check "call_check" is green
    When I run the lesson's check "proof_proof"
    Then the lesson's check "proof_proof" is green

  Scenario: A step its check finds red stops the build — nothing more is typed
    Given the runner serves the course page "courses/micro_build_ai/module_05/01_builder.md"
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_05/01_builder.md"
    And I wait for the page to be interactive
    And Doc types into the "follow_up" pad a step that forgets its decoration
    Then the "follow_up" pad is held, saying "no datagrid yet"
    And the "follow_up" pad does not hold "{: .button }"

  Scenario: Doc folds the editor away and shows it again
    Michel, 2026-10-11: "Fold/Show should also have verbs so the Doc can
    use them to demonstrate".

    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/faces.md"
    And I wait for the page to be interactive
    And Doc does "fold" on the "faces" pad
    Then the "faces" pad's source is folded away
    When Doc does "show" on the "faces" pad
    Then the "faces" pad's source is shown again

  Scenario: Doc's tour shows the pad's help, finder, list and fold — and changes nothing
    Michel, 2026-10-12: "a little tour/demo by Doc of the generic mdpad
    features listed in the help box" — show-only: the learner is working
    in that pad.

    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/faces.md"
    And I wait for the page to be interactive
    And I note the "faces" pad's text
    And Doc does "help" on the "faces" pad
    Then the "faces" pad's help mentions "F2" and "complete"
    When Doc does "dismiss" on the "faces" pad
    And Doc does "find" on 'dog' in the "faces" pad
    Then the "faces" pad's finder counts more than 1 match
    When Doc does "dismiss" on the "faces" pad
    And Doc does "caret_at" on '{: .' in the "faces" pad
    And Doc does "complete" on the "faces" pad
    Then the "faces" pad offers "datagrid" and "form"
    When Doc does "dismiss" on the "faces" pad
    Then the "faces" pad shows no help, no finder and no list
    And the "faces" pad's text is unchanged by the tour
