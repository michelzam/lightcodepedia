Feature: Blocks gate on feature state through cells
  A feature card with an id publishes {id: {status, passing}} into the page's
  cell scopes, and any block can wear visible="= id.passing". No new
  component: the cells engine already owned visibility — features just
  joined the data. Reinforcement quizzes hide until the proof turns green.

  Scenario: A gated paragraph opens the moment the run turns green
    Given I have a clean browser page
    And the GitHub contents API serves "courses/demo/module_01/gate.md" with the document:
      """
      # Gate page

      ```gherkin
      Feature: The gate
        Scenario: It opens honestly
          Given a working page
          :::python
          assert True
          :::
      ```
      {: .feature #gate visible="true" status="pending" }

      Reward unlocked — you earned this paragraph.
      {: visible="= gate.passing" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/gate.md"
    And I wait for the page to be interactive
    Then the text "Reward unlocked" is hidden
    When I run the page's embedded features
    Then every embedded feature passes
    And the text "Reward unlocked" becomes visible

  Scenario: celebration="true" bursts on the first honest red-to-green
    Given I have a clean browser page
    And the GitHub contents API serves "courses/demo/module_01/party.md" with the document:
      """
      # Party page

      ```gherkin
      Feature: Worth celebrating
        Scenario: earned
          Given the work is done
          :::python
          assert True
          :::
      ```
      {: .feature #party visible="true" status="pending" celebration="true" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/party.md"
    And I wait for the page to be interactive
    And I run the page's embedded features
    Then every embedded feature passes
    And a confetti burst appears

  Scenario: confetti is a verb any component can speak from a step
    Given I have a clean browser page
    And the GitHub contents API serves "courses/demo/module_01/verb.md" with the document:
      """
      # Verb page

      ```markdown
      seed
      ```
      {: .mdpad #pad rows="3" }

      ```gherkin
      Feature: The authored celebration
        Scenario: the page decides
          Given the pad
          :::python
          self.page.pad.confetti()
          :::
      ```
      {: .feature #author visible="true" status="pending" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/verb.md"
    And I wait for the page to be interactive
    And I run the page's embedded features
    Then every embedded feature passes
    And a confetti burst appears

  Scenario: A second repair celebrates again; a re-run does not
    Every run dips through "pending", so the question is what the card's
    last SETTLED state was. Break it, fix it, and the second repair is
    worth exactly as much as the first — but pressing Run on a card that
    is already green earned nothing.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/module_01/again.md" with the document:
      """
      # Again page

      ```markdown
      no
      ```
      {: .mdpad #pad rows="3" }

      ```gherkin
      Feature: Say ok
        Scenario: the pad says ok
          Given the pad
          :::python
          assert self.page.pad.source.strip() == "ok", self.page.pad.source
          :::
      ```
      {: .feature #again visible="true" status="pending" celebration="true" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/again.md"
    And I wait for the page to be interactive
    And I run the page's embedded features
    Then the embedded feature ends red
    When I retype the pad "pad" with:
      """
      ok
      """
    And I run the page's embedded features
    Then every embedded feature passes
    And a confetti burst appears
    When the confetti has cleared
    And I run the page's embedded features
    Then every embedded feature passes
    And no confetti burst appears
    When I retype the pad "pad" with:
      """
      no
      """
    And I run the page's embedded features
    Then the embedded feature ends red
    When I retype the pad "pad" with:
      """
      ok
      """
    And I run the page's embedded features
    Then every embedded feature passes
    And a confetti burst appears

  Scenario: A gate rewritten from the x-ray keeps listening
    Michel, 2026-09-24, Module 02: the learner changes card 3's gate from
    ask.dog to meet.when in the x-ray. The card shuts (no visit yet) — and
    must open again the moment a visit is booked. It stayed shut: the
    re-rendered card was never wired to the cells again.

    Given I have a clean browser page
    And the GitHub contents API serves "courses/demo/module_02/gates.md" with the document:
      """
      # Gates

      ```yaml
      dog: Biscuit
      ```
      {: .form #ask editable="true" title="1 Ask" }

      ```yaml
      when: ""
      ```
      {: .form #meet editable="true" title="2 Meet" visible="= ask.dog" }

      ```yaml
      paid: ""
      ```
      {: .form #home editable="true" title="3 Home" visible="= ask.dog" }

      Tail paragraph.
      """
    And a key that may keep edits to "acme/demo"
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_02/gates.md"
    And I wait for the page to be interactive
    Then the card "home" is open
    When I rewrite the gate of "home" to "= meet.when" in the x-ray
    Then the card "home" is shut
    When the form "meet" gets "when" = "Thu"
    Then the card "home" is open
    When the form "meet" gets "when" cleared
    Then the card "home" is shut

  Scenario: A shut gate is still a block to the x-ray
    The reader sees nothing; the author, x-ray on, sees the shut card as a
    ghost named by its formula, and the gear finds it.

    Given I have a clean browser page
    And the GitHub contents API serves "courses/demo/module_02/shut.md" with the document:
      """
      # Gates

      ```yaml
      when: ""
      ```
      {: .form #meet editable="true" title="2 Meet" }

      ```yaml
      paid: ""
      ```
      {: .form #home editable="true" title="3 Home" visible="= meet.when" }

      Tail paragraph.
      """
    And a key that may keep edits to "acme/demo"
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_02/shut.md"
    And I wait for the page to be interactive
    Then the card "home" is shut
    When the x-ray looks at the page
    Then the card "home" stands as a ghost
    And the gear can be summoned on "home"
