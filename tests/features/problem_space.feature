Feature: Problem space — persona, pitch, impact map

  The three documents every product carries, as components. The persona
  renders an empathy card, the pitch assembles its two sentences and
  checks itself against the persona it reads, the impact map traces
  features back to the goal and collects the page's proofs.

  Background:
    Given I have a clean browser page

  Scenario: The persona page loads without errors
    When I navigate to "/components/persona"
    And I wait for the page to be interactive
    Then the LC platform is loaded
    And there are no JS console errors

  Scenario: A persona renders as an empathy card
    When I navigate to "/components/persona"
    And I wait for the page to be interactive
    Then the persona card "maria" shows the name "Maria"
    And the persona card "maria" has 4 empathy sections

  Scenario: A minimal persona hides what it was not given
    When I navigate to "/components/persona"
    And I wait for the page to be interactive
    Then the persona card "sam" shows the name "Sam"
    And the persona card "sam" has 0 empathy sections

  Scenario: The pitch assembles its sentences from the blanks
    When I navigate to "/components/pitch"
    And I wait for the page to be interactive
    Then the pitch "demo_pitch" reads "adoption tracker"
    And the pitch "demo_pitch" reads "the paper binder"

  Scenario: The form is the persona's editor
    When I navigate to "/components/persona"
    And I wait for the page to be interactive
    Then the persona card "sam" shows the name "Sam"
    When the form "sam_src" field "name" is set to "Samantha"
    Then the persona card "sam" shows the name "Samantha"

  Scenario: The form is the pitch's editor
    When I navigate to "/components/pitch"
    And I wait for the page to be interactive
    Then the pitch "live_pitch" reads "Shelter Desk"
    When the form "pitch_form" field "product" is set to "MoonDesk"
    Then the pitch "live_pitch" reads "MoonDesk"

  Scenario: The pitch wires itself to the persona it serves
    When I navigate to "/components/pitch"
    And I wait for the page to be interactive
    Then the pitch "demo_pitch" links to the persona "ana"
    And the pitch "demo_pitch" shows no drift warning

  Scenario: A pitch that forgets its persona is warned, not stopped
    When I navigate to "/components/pitch"
    And I wait for the page to be interactive
    Then the pitch "drifting" shows a drift warning


  Scenario: A read-only document offers no save button
    A save= without a source= is the LATER page showing back what an
    earlier one built. A 💾 there would offer to save a document nobody
    can edit — and on an empty card, to write the seed over real work.

    When I navigate to "/components/persona"
    And I wait for the page to be interactive
    Then the persona card "recap" shows no save button
    And the persona card "recap" says nothing is saved yet

  Scenario: The save button sits with the editor, not the view
    A card is a rendering; the form is where the typing happens. A 💾
    under a read-only card reads as "save the view".

    When I navigate to "/components/persona"
    And I wait for the page to be interactive
    Then the save button for "sam" sits inside the form "sam_src"

  Scenario: The who is calculated from the persona the pitch reads
    When I navigate to "/components/pitch"
    And I wait for the page to be interactive
    Then the pitch "demo_pitch" reads "Shelter coordinator"
    And the pitch "demo_pitch" shows "who" as calculated

  Scenario: A typed who is ignored while the knob is set
    When I navigate to "/components/pitch"
    And I wait for the page to be interactive
    Then the pitch "drifting" reads "Shelter coordinator"
    And the pitch "drifting" shows a drift warning

  Scenario: The pitch reads as a form — one blank per line
    Michel, 2026-08-12: *"the display should show them in different lines
    to make the reading and checking easy."* The pitch is a sentence, but
    it is checked blank by blank, and a missing one must be findable at a
    glance instead of hunted inside a paragraph.

    When I navigate to "/components/pitch"
    And I wait for the page to be interactive
    Then the pitch "demo_pitch" shows 7 lines
    And the pitch line "benefit" of "demo_pitch" reads "no family pays before meeting the dog"

  Scenario: A tag reads as words, and keeps its name
    Names are snake_case (doctrine 2) and readers are not. The chip shows
    the reader's version; data-tag keeps the author's, so a filter still
    matches. Served through the runner because the catalog itself now
    speaks in single words — the rule outlives the vocabulary.

    Given the GitHub contents API serves "courses/demo/tagged.md" with the document:
      """
      # Tagged

      ```gherkin
      Feature: A named thing
        Scenario: It is named
          Given nothing
      ```
      {: .feature #named_proof visible="true" tags="impact_map" status="pending" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/tagged.md"
    And I wait for the page to be interactive
    Then the proof "named_proof" shows the tag "impact map"
    And the proof "named_proof" carries the tag name "impact_map"

  Scenario: The impact map renders all four levels
    When I navigate to "/components/impact_map"
    And I wait for the page to be interactive
    Then the impact map "shelter_map" shows the goal "no adoption fails"
    And the impact map "shelter_map" has 2 behaviour changes

  Scenario: An empty goal fills itself from the pitch it reads
    When I navigate to "/components/impact_map"
    And I wait for the page to be interactive
    Then the impact map "pulled_map" shows the goal "no family pays"
    And the impact map "pulled_map" links to the pitch "map_pitch"

  Scenario: A map row can name the proof that implements it
    When I navigate to "/components/impact_map"
    And I wait for the page to be interactive
    Then the impact map "shelter_map" leaf links to the proof "weekly_proof"

  Scenario: A proof missing from the map is collected, not ignored
    When I navigate to "/components/impact_map"
    And I wait for the page to be interactive
    Then the impact map "pulled_map" collects the proof "weekly_proof"
