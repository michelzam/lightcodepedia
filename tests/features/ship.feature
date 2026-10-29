Feature: 🚀 Ship — the author-designed deployment component

  Shipping is a course element, not a platform permission (Michel,
  2026-08-15). The author places {: .ship app= files= bay= } on the
  assignment page; the learner's own key copies the named files into the
  public bay under <app>_<sha>/, writes the bay manifest, and a runner
  embed with src="ship:<app>" renders the deployed copy on the same page —
  the proof that deployment worked is the app itself, not a toast.

  Background:
    Given I have a clean browser page
    And a marked shim is preinstalled

  Scenario: Without a key the ship button stays disarmed, and says why
    Given the GitHub contents API serves "courses/demo/assignment.md" with the document:
      """
      # Assignment

      [Ship it](#)
      {: .ship app="spike_dogs" files="_ship_app.md" bay="acme/bay/bays" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/assignment.md"
    And I wait for the page to be interactive
    Then the ship button is disarmed with a reason

  Scenario: Pressing ship copies the files and writes the manifest
    Given I am signed in with a course key
    And the GitHub contents API serves "courses/demo/assignment.md" with the document:
      """
      # Assignment

      [Ship it](#)
      {: .ship app="spike_dogs" files="_ship_app.md" bay="acme/bay/bays" }
      """
    And the GitHub contents API serves "courses/demo/_ship_app.md" with the document:
      """
      # 🐕 Spike dogs

      Twelve dogs, none invisible.
      """
    And the bench HEAD commit is "cafebabe12345678"
    And the bay accepts writes
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/assignment.md"
    And I wait for the page to be interactive
    And I press the ship button
    Then the bay received "bays/spike_dogs_cafebabe12345678/_ship_app.md"
    And the bay manifest now points "spike_dogs" at "cafebabe12345678"
    And the ship button reports the shipped link

  Scenario: With comment="true", 🚀 Ship it… asks one line, and the ledger keeps it
    Michel, 2026-10-29: "the ship's time machine shows no comments for the
    commits — I would follow the mdpad example". The line rides the copy's
    commit and its ledger entry; the copies list shows it.

    Given I am signed in with a course key
    And the GitHub contents API serves "courses/demo/assignment.md" with the document:
      """
      # Assignment

      [Ship it](#)
      {: .ship app="spike_dogs" files="_ship_app.md" bay="acme/bay/bays" comment="true" }
      """
    And the GitHub contents API serves "courses/demo/_ship_app.md" with the document:
      """
      # 🐕 Spike dogs
      """
    And the bench HEAD commit is "cafebabe12345678"
    And the bay accepts writes
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/assignment.md"
    And I wait for the page to be interactive
    Then the ship button reads "🚀 Ship it…"
    When I press the ship button
    Then the ship asks for one line
    When I write the ship line "the tour pasted" and press Enter
    Then the bay's commit for "bays/spike_dogs_cafebabe12345678/_ship_app.md" ends with "— the tour pasted"
    And the bay manifest's "spike_dogs" history starts with the note "the tour pasted"

  Scenario: A picture beside a shipped page ships with it, and the saves since the last ship suggest the line
    Michel, 2026-10-29: Fern.jpg beside cv.md — public bay, private bench.
    Also: "I wish the comments of the saved versions could contribute too,
    suggested as default values".

    Given I am signed in with a course key
    And this browser is paired to the bench "acme/bench"
    And the GitHub contents API serves "courses/demo/assignment.md" with the document:
      """
      # Assignment

      [Ship it](#)
      {: .ship app="spike_dogs" files="_ship_app.md" bay="acme/bay/bays" comment="true" }
      """
    And the GitHub contents API serves "courses/demo/_ship_app.md" with the document:
      """
      # 🐕 Spike dogs

      ![Fern](Fern.jpg)
      """
    And the bench serves the picture "courses/demo/Fern.jpg"
    And the bench HEAD commit is "cafebabe12345678"
    And the bench's history for "courses/demo/_ship_app.md" reads "✍️ the tour pasted" then "✍️ the brag written"
    And the bay accepts writes
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/assignment.md"
    And I wait for the page to be interactive
    And I press the ship button
    Then the ship's line is pre-filled with "the brag written · the tour pasted"
    When I write the ship line "with Fern" and press Enter
    Then the bay received "bays/spike_dogs_cafebabe12345678/_ship_app.md"
    And the bay received "bays/spike_dogs_cafebabe12345678/Fern.jpg"

  Scenario: A pending bay invitation is accepted on the fly, and the ship completes
    A collaborator grant can land as a pending invitation instead of a
    direct one — the bay exists, push was granted, and the PUT still says
    404 (zamm-student, 2026-08-15). The learner's key can accept its own
    invitations, so the button must: sweep, accept, retry.

    Given I am signed in with a course key
    And the GitHub contents API serves "courses/demo/assignment.md" with the document:
      """
      # Assignment

      [Ship it](#)
      {: .ship app="spike_dogs" files="_ship_app.md" bay="acme/bay/bays" }
      """
    And the GitHub contents API serves "courses/demo/_ship_app.md" with the document:
      """
      # 🐕 Spike dogs

      Twelve dogs, none invisible.
      """
    And the bench HEAD commit is "cafebabe12345678"
    And the bay requires an accepted invitation before it takes writes
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/assignment.md"
    And I wait for the page to be interactive
    And I press the ship button
    Then the bay invitation was accepted
    And the bay received "bays/spike_dogs_cafebabe12345678/_ship_app.md"
    And the ship button reports the shipped link

  Scenario: A pairing from another org never invents a bay
    The bench pairing is browser-global and follows the LAST account that
    paired — an author-side lc_ed_repo of michelzam/lightcodepedia made
    ship derive "michelzam/lightcodepedia-bay" on a course page and fail
    as a 404 (2026-08-15). A derived bay is only trustworthy inside its
    own org; a foreign pairing disarms the button with the truth.

    Given I am signed in with a course key
    And this browser is paired to the bench "michelzam/lightcodepedia"
    And the GitHub contents API serves "courses/demo/assignment.md" with the document:
      """
      # Assignment

      [Ship it](#)
      {: .ship app="spike_dogs" files="_ship_app.md" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/assignment.md"
    And I wait for the page to be interactive
    Then the ship button is disarmed with a reason
    And the reason names the foreign pairing

  Scenario: A ship: embed renders the latest shipped copy, keyless
    Given the bay manifest points "spike_dogs" at "cafebabe12345678" with entry "_ship_app.md"
    And the bay serves "bays/spike_dogs_cafebabe12345678/_ship_app.md" with the document:
      """
      # 🐕 Spike dogs

      Twelve dogs, none invisible.
      """
    And the GitHub contents API serves "courses/demo/assignment.md" with the document:
      """
      # Assignment

      [My shipped app](#)
      {: .runner src="ship:spike_dogs" bay="acme/bay/bays" title="" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/assignment.md"
    And I wait for the page to be interactive
    Then the ship embed renders "Twelve dogs, none invisible"

  Scenario: Before any ship, the embed waits politely instead of erroring
    Given the bay has no manifest
    And the GitHub contents API serves "courses/demo/assignment.md" with the document:
      """
      # Assignment

      [My shipped app](#)
      {: .runner src="ship:spike_dogs" bay="acme/bay/bays" title="" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/assignment.md"
    And I wait for the page to be interactive
    Then the ship embed says nothing is shipped yet

  Scenario: A ship qr carries the deployed app's address
    Given the bay manifest points "spike_dogs" at "cafebabe12345678" with entry "_ship_app.md"
    And the GitHub contents API serves "courses/demo/assignment.md" with the document:
      """
      # Assignment

      ```
      Scan to open my app
      ```
      {: .qr ship="spike_dogs" bay="acme/bay/bays" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/assignment.md"
    And I wait for the page to be interactive
    Then the ship qr encodes "#src=gh:acme/bay/bays/spike_dogs_cafebabe12345678/_ship_app.md"

  Scenario: Before any ship, the qr waits instead of drawing a dead square
    Given the bay has no manifest
    And the GitHub contents API serves "courses/demo/assignment.md" with the document:
      """
      # Assignment

      ```
      Scan to open my app
      ```
      {: .qr ship="spike_dogs" bay="acme/bay/bays" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/assignment.md"
    And I wait for the page to be interactive
    Then the ship qr says nothing is shipped yet

  Scenario: Inside a shipped app, a part has no frame; a titled window keeps its own
    Given the bay manifest points "spike_dogs" at "cafebabe12345678" with entry "_ship_app.md"
    And the bay serves "bays/spike_dogs_cafebabe12345678/_ship_app.md" with the document:
      """
      # 🐕 Spike dogs

      [Part](#)
      {: .runner src="_part.md" }

      [Inner app](#)
      {: .runner src="_inner.md" title="Inner app" }
      """
    And the bay serves "bays/spike_dogs_cafebabe12345678/_part.md" with the document:
      """
      A part of the app.
      """
    And the bay serves "bays/spike_dogs_cafebabe12345678/_inner.md" with the document:
      """
      An app inside the app.
      """
    And the GitHub contents API serves "courses/demo/assignment.md" with the document:
      """
      # Assignment

      [My shipped app](#)
      {: .runner src="ship:spike_dogs" bay="acme/bay/bays" title="" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/assignment.md"
    And I wait for the page to be interactive
    Then the ship embed renders "An app inside the app."
    And inside the shipped app "A part of the app." has no frame and "An app inside the app." keeps its window

  Scenario: A shipped app opened on its own pins its title on top, the content scrolls under it
    Given the bay serves "bays/spike_dogs_cafebabe12345678/_ship_app.md" with the document:
      """
      # 🐕 Spike dogs

      Twelve dogs, none invisible.
      """
    When I navigate to "/run.html#src=gh:acme/bay/bays/spike_dogs_cafebabe12345678/_ship_app.md"
    And I wait for the page to be interactive
    Then the shipped app's title "Spike dogs" stays on top as the page scrolls
