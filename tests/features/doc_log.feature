Feature: Doc's exchanges land in the learner's bench

  Michel, 2026-09-29: "when students use Doc to ask questions, can we store
  the Q&A as __notes in their bench? That would be great for the research."
  One file per lesson beside the margin, __<lesson>.doc.md, dunder so it
  never travels. It rides the roads the progress record takes: buffered in
  the browser, written with the next save or when the tab goes away — never
  a commit per question.

  Background:
    Given I have a clean browser page
    And a marked shim is preinstalled
    And an energy key "gem_stub" is already saved on this device
    And the "doc" bot is available
    And a connected bench whose "courses/demo/mod/__guide.doc.md" does not exist yet
    And the GitHub contents API serves "courses/demo/mod/guide.md" with the document:
      """
      # Guided page

      Some prose.

      ```yaml
      bot: doc
      script:
        - say: "Hello."
      stories:
        "Where is the gear?":
          - say: "Here. The gear on the corner of this table."
      ```
      {: .avatar #guide dock="true" size="115" }

      ```yaml
      name: Vet
      system: You are the shelter's vet. Answer in one line.
      ```
      {: .agent #vet }
      """

  Scenario: A live question and its answer are in the bench once the learner leaves
    Given the model endpoint answers in full with "The page introduces a course."
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/guide.md"
    And I wait for the page to be interactive
    And I ask the guide "Summarize this page"
    Then the bench received no commit
    When the learner leaves the page without saving
    Then the bench received a commit to "courses/demo/mod/__guide.doc.md" containing "**Q** Summarize this page"
    And the bench received a commit to "courses/demo/mod/__guide.doc.md" containing "The page introduces a course."
    And the bench received a commit to "courses/demo/mod/__guide.doc.md" containing "· live"

  Scenario: A kept story picked from the dock counts as an exchange too
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/guide.md"
    And I wait for the page to be interactive
    And I pick the guide's story "Where is the gear?"
    And the learner leaves the page without saving
    Then the bench received a commit to "courses/demo/mod/__guide.doc.md" containing "**Q** Where is the gear?"
    And the bench received a commit to "courses/demo/mod/__guide.doc.md" containing "· kept"

  Scenario: A page agent's exchange joins the same log, named after the agent
    Given the model endpoint answers in full with "She is healthy, just shy."
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/guide.md"
    And I wait for the page to be interactive
    And I ask the "vet" agent "Is Luna healthy?"
    Then the bench received no commit
    When the learner leaves the page without saving
    Then the bench received a commit to "courses/demo/mod/__guide.doc.md" containing "**Q** Is Luna healthy?"
    And the bench received a commit to "courses/demo/mod/__guide.doc.md" containing "She is healthy, just shy."
    And the bench received a commit to "courses/demo/mod/__guide.doc.md" containing "· agent Vet"
