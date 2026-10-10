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
    The FOR names the PERSONA — "Ana" — not her subtitle: the name is who
    the pitch serves, the role is how the card explains her (Michel,
    2026-08-24).

    When I navigate to "/components/pitch"
    And I wait for the page to be interactive
    Then the pitch "demo_pitch" reads "Ana"
    And the pitch "demo_pitch" shows "who" as calculated

  Scenario: A typed who is ignored while the knob is set
    When I navigate to "/components/pitch"
    And I wait for the page to be interactive
    Then the pitch "drifting" reads "Ana"
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

  Scenario: The drift warning names words the need could echo
    Michel, 2026-10-01: "why do I have this warning?" — a finding has to
    say where to look. The warning names words from the card's goal and
    frustrations.

    When I navigate to "/components/pitch"
    And I wait for the page to be interactive
    Then the pitch "drifting" shows a drift warning
    And the drift warning on "drifting" names words from the card

  Scenario: The editor offers a way back to the lesson's starter, and the versions
    Michel, 2026-10-01: "we lost the versioning and being able to reset the
    data". Under the editor: ↺ puts the starter back, 🕘 lists every saved
    version (hidden until a first save exists).

    When I navigate to "/components/persona"
    And I wait for the page to be interactive
    And the form "sam_src" field "name" is set to "Zed"
    Then the persona card "sam" shows the name "Zed"
    When I start over from the lesson's starter for "sam"
    Then the persona card "sam" shows the name "Sam"
    And the editor of "sam" carries a versions handle

  Scenario: The starter survives an editor that arrives late
    Pedia's full suite, 2026-10-03/04: ↺ put "Unnamed" on the card every other
    run, green on the rig every time. The card wires before the editor form has
    published (its grid library comes from a CDN), so the starter it remembered
    was its own placeholder fence, not the author's document. The seed must be
    the first value the source ever publishes, whenever that lands.

    Given I have a clean browser page
    And the editor's grid library arrives late
    When I navigate to "/components/persona"
    And I wait for the page to be interactive
    Then the persona card "sam" shows the name "Sam"
    When the form "sam_src" field "name" is set to "Zed"
    Then the persona card "sam" shows the name "Zed"
    When I start over from the lesson's starter for "sam"
    Then the persona card "sam" shows the name "Sam"

  Scenario: In the runner, a leaf link scrolls to its proof and keeps the page's address
    Michel, 2026-10-01: "the impact map has a link 'The count table' but it
    leads nowhere" — on /run.html the hash is the address, and a plain
    anchor replaced it. The map is also a document: a cell reads its goal.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/map.md" with the document:
      """
      # Map page

      ```yaml
      goal: No adoption fails after payment
      impacts:
        - how: She sees where families stop
          what: The count table
          feature: count_proof
      ```
      {: .impact_map #map }

      The goal reads: {= map.goal }

      Filler one. Filler two. Filler three. Filler four. Filler five.
      Filler six. Filler seven. Filler eight. Filler nine. Filler ten.
      Filler one. Filler two. Filler three. Filler four. Filler five.
      Filler six. Filler seven. Filler eight. Filler nine. Filler ten.
      Filler one. Filler two. Filler three. Filler four. Filler five.
      Filler six. Filler seven. Filler eight. Filler nine. Filler ten.
      Filler one. Filler two. Filler three. Filler four. Filler five.
      Filler six. Filler seven. Filler eight. Filler nine. Filler ten.
      Filler one. Filler two. Filler three. Filler four. Filler five.
      Filler six. Filler seven. Filler eight. Filler nine. Filler ten.
      Filler one. Filler two. Filler three. Filler four. Filler five.
      Filler six. Filler seven. Filler eight. Filler nine. Filler ten.

      ```gherkin
      Feature: The coordinator sees where families stop
        Scenario: The week's count
          Given fourteen families asked about a dog this week
          When the coordinator reads the week
          Then she sees how many went home, and where the others stopped
      ```
      {: .feature #count_proof visible="true" status="wanted" tags="app" }

      ```gherkin
      Feature: The chain holds
        Scenario: The leaf is a wanted app feature
          Given the map's leaves
          :::python
          self.features: list = self.page.map.features
          :::
          Then the one leaf names a wanted feature of the app, by its title
          :::python
          assert len(self.features) == 1
          assert self.features[0].exists and self.features[0].wanted
          assert "app" in self.features[0].tags
          assert self.features[0].title == "The coordinator sees where families stop"
          assert "Given fourteen families" in self.features[0].text
          :::
      ```
      {: .feature #chain_proof visible="true" status="pending" }

      ```yaml
      name: The judge
      placeholder: Does this map hold?
      system: You judge impact maps.
      ```
      {: .agent #judge bound="{= dict(goal=map.goal, impacts=map.impacts) }" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/map.md"
    And I wait for the page to be interactive
    Then the page reads "The goal reads: No adoption fails after payment"
    And the agent "judge" is named "The judge" and reads "map.goal"
    And the impact map "map" leaf "count_proof" reads "The coordinator sees where families stop 📝"
    When I run the feature "chain_proof"
    Then the feature "chain_proof" is green
    When I follow the impact map "map" leaf to "count_proof"
    Then the page's address still names "courses/demo/mod/map.md"
    And the proof "count_proof" is in view

  Scenario: A wanted feature shows its request and nothing to run
    Michel, 2026-10-01: the problem space writes the request in plain
    Given/When/Then; the solution implements the steps later. Until then
    the card is wanted — dashed, badged, no ▶ — and readable as a document.

    When I navigate to "/components/feature"
    And I wait for the page to be interactive
    Then the feature "wanted_demo" is wanted, with no run button
    And the page reads "says No payment before a visit"

  Scenario: A map leaf wears its feature's title and state
    When I navigate to "/components/impact_map"
    And I wait for the page to be interactive
    Then the impact map "shelter_map" leaf "visit_first" reads "Families meet the dog before they pay 📝"

  Scenario: The map collects the app's features, never the lesson's checks
    When I navigate to "/components/impact_map"
    And I wait for the page to be interactive
    Then the impact map "pulled_map" collects the proof "weekly_proof"
    And the impact map "pulled_map" does not collect "impact_map_proof"

  Scenario: A leaf whose feature lives elsewhere reads as words and says where it is
    Michel, 2026-10-10: the leaves are features — 🦄, the feature's own
    icon — named in words, not as ids; the person is 👤; and a leaf whose
    feature is on another page "leads to an empty new page". It says so
    under the leaf now, and the runner keeps its page.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/elsewhere.md" with the document:
      """
      # Elsewhere

      ```yaml
      goal: No adoption fails after payment
      who: The coordinator
      impacts:
        - how: She stops payments that come before a visit
          feature: no_payment_before_visit
      ```
      {: .impact_map #map }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/elsewhere.md"
    And I wait for the page to be interactive
    Then the impact map "map" leaf "no_payment_before_visit" reads "No payment before visit ⚪"
    And the impact map "map" shows "👤 The coordinator" and "🦄 No payment before visit"
    When I follow the impact map "map" leaf to "no_payment_before_visit"
    Then the page's address still names "courses/demo/mod/elsewhere.md"
    And the impact map "map" says "is not on this page" under the leaf
