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
