Feature: X-ray inspector

  Background:
    Given I have a clean browser page

  Scenario: X-ray panel appears on hover over a component
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I hover over the first grid component
    Then an x-ray panel is visible
    And the x-ray panel shows a component class name

  Scenario: X-ray panel identifies the bound chart component
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I hover over the chart component
    Then an x-ray panel is visible
    And the x-ray panel mentions "Chart"

  Scenario: X-ray panel identifies the map component
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I hover over the map component
    Then an x-ray panel is visible
    And the x-ray panel mentions "Map"

  Scenario: Keep commits the edited block when the builder is connected
    When I navigate to "/tutorial101"
    And I am connected as a builder with a stubbed repo
    And I wait for the page to be interactive
    And I open the x-ray editor on the local dog block
    And I change the block content to "Cute, huh — this committed dog?"
    And I keep the changes
    Then the stubbed repo received a commit containing "committed dog"
    And a green save toast confirms it

  Scenario: Keep invites anonymous learners to create an account
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the x-ray editor on the local dog block
    And I change the block content to "Cute, huh — a fleeting dog?"
    Then keeping the changes invites me to create an account

  Scenario: X-ray scene fits within viewport
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I hover over the first grid component
    Then an x-ray panel is visible
    And the x-ray panel is within the viewport bounds

  @mobile
  Scenario: X-ray is activatable via FAB popup on mobile
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I tap the slides FAB button
    Then the FAB popup is visible
    And the popup contains an X-ray option

  @mobile
  Scenario: Touch X-ray teaches its gestures on entry
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I tap the slides FAB button
    And I tap the X-ray option in the popup
    Then the touch gesture hint appears

  @mobile
  Scenario: X-ray activates on tap after enabling via FAB popup
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I tap the slides FAB button
    And I tap the X-ray option in the popup
    Then the FAB button has the xray-active style
    And I tap the first grid component
    Then an x-ray panel is visible

  @mobile
  Scenario: In x-ray mode a phone can still reach the rest of the page
    The lens used to swallow every touch on the page, so a phone in x-ray
    mode was frozen: you could inspect the part in front of you and never
    scroll to the next one. A finger that lands on nothing inspectable —
    a margin, a paragraph, whitespace — is scrolling, not asking.

    When I navigate to "/components/datagrid"
    And I wait for the page to be interactive
    And I tap the slides FAB button
    And I tap the X-ray option in the popup
    And I swipe up from a plain paragraph
    Then the page scrolled

  @mobile
  Scenario: A drag that starts on a part is still an inspection
    The escape hatch must not become the exit. A gesture beginning on a
    component belongs to the lens — it tracks the finger and the page stays
    put — or every inspection would slide out from under the reader.

    When I navigate to "/components/datagrid"
    And I wait for the page to be interactive
    And I tap the slides FAB button
    And I tap the X-ray option in the popup
    And I swipe up from the first grid component
    Then the page did not scroll

  @mobile
  Scenario: X-ray deactivates by tapping the FAB again
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I tap the slides FAB button
    And I tap the X-ray option in the popup
    Then the FAB button has the xray-active style
    And I tap the slides FAB button
    Then the FAB button does not have the xray-active style

  Scenario: Shift x-ray reveals the whole connected data chain
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I shift-hover over the chart component
    Then the x-ray scene mentions "Chart"
    And the x-ray scene mentions "Datagrid"
    And the x-ray scene mentions "Dataset"

  Scenario: Shift x-ray connects the trigger to its avatar
    When I navigate to "/components/examples/avatar"
    And I wait for the page to be interactive
    And I shift-hover over the avatar overlay "prof_avatar"
    Then the x-ray scene mentions "AvatarTrigger"

  Scenario: Shift x-ray labels a query result as Query, not its Dataset base
    When I navigate to "/components/query"
    And I wait for the page to be interactive
    And I shift-hover over the chart component
    Then the x-ray scene mentions "Query"

  Scenario: Resizing the editor keeps it open, and the text field grows with it
    A dialog's own resize corner and its backdrop both report the dialog as
    the click target, so letting go of the corner closed the editor, the
    edit gone with it. Position tells them apart: the backdrop is what lies
    OUTSIDE the box. The field must also take the new room; a taller box
    still showing a small slot is the wrong kind of resizable.

    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the x-ray editor on the local dog block
    And I drag the editor's resize corner
    Then the editor is still open
    And the text field grew with the box

  Scenario: The gear on a part inside a bench slot opens the part, not a div
    The lesson's repair happens on a component that is rendered INSIDE the
    learner's own slot — that is, after the page scan has already run. A
    subtree rendered late never reached the source snapshot, so lcSourceOf
    came back empty, the editor decided this was not a component, and the
    ⚙️ the whole exercise is built on opened a plain block with no knobs.

    Given a connected bench whose "courses/demo/mod/wiring.md" does not exist yet
    And the GitHub contents API serves "courses/demo/mod/lesson.md" with the document:
      """
      # Her screen, exactly as she left it

      The prose here belongs to the course.

      ````markdown
      ```csv
      campus,dogs_adopted
      Milwaukee,12
      Ozaukee,5
      ```
      {: .dataset #adoptions }

      ```csv
      ```
      {: .datagrid #wired source="ozaukee" height="160" empty="Nothing arrives here yet." }
      ````
      {: .embed save="wiring.md" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And I open the x-ray editor on the wired table
    Then the editor opened a component, not a plain block
    And the editor offers a "source" knob

  Scenario: Changing the wire commits the rewritten line to the learner's file
    The gesture the lesson asks for, end to end: read the real name with the
    lens, put it in source, keep it. It lands in the LEARNER'S file — the
    lesson stays the vault's — and the author's starter goes down first, so
    the very first change is readable in 🕘 as a change.

    Given a connected bench whose "courses/demo/mod/wiring.md" does not exist yet
    And the GitHub contents API serves "courses/demo/mod/lesson.md" with the document:
      """
      # Her screen, exactly as she left it

      ````markdown
      ```csv
      campus,dogs_adopted
      Milwaukee,12
      Ozaukee,5
      ```
      {: .dataset #adoptions }

      ```csv
      ```
      {: .datagrid #wired source="ozaukee" height="160" empty="Nothing arrives here yet." }
      ````
      {: .embed save="wiring.md" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And I open the x-ray editor on the wired table
    And I set the "source" knob to "adoptions"
    And I save, and the bench receives it
    Then the bench received 2 commits to "courses/demo/mod/wiring.md"
    And the first of them is the lesson's seed
    And the last of them wires source to adoptions
    And the author's repo received no commit

  Scenario: A name nothing answers to gets a bomb, not a part of its own
    The lens used to MATERIALISE the missing target: lcx_target falls back to
    constructing Dataset(id) when no element carries the id, so a source that
    named nothing drew a panel reading "id = ozaukee / loaded = false". A
    reader sweeping the lens — which is exactly what the lesson tells them to
    do — was told the part exists and is merely empty. That is the opposite
    of the truth, and no language materialises a variable because something
    mentioned its name. The broken thing is the REFERENCE, so it stays on the
    referrer and no wire leaves it.

    Given the GitHub contents API serves "courses/demo/ghost.md" with the document:
      """
      # Her screen

      ```csv
      campus,dogs_adopted
      Milwaukee,12
      ```
      {: .dataset #adoptions }

      ```csv
      ```
      {: .datagrid #wired source="ozaukee" height="160" empty="Nothing arrives here yet." }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/ghost.md"
    And I wait for the page to be interactive
    And I sweep the lens over the wired table
    Then the lens marks "source" as naming nothing
    And the lens draws no part called "ozaukee"
    And the lens draws no wire from it

  Scenario: A working wire beside a broken one is what makes the broken one legible
    The lesson's whole mechanism. A dataset alone draws no wire — only a
    bound VISUAL does — so a learner with nothing but a mis-wired part has
    no worked example to reason from and cannot guess what to change. Put a
    table that works next to a chart that does not: one wire lands, the
    other is a 💣, and the repair is read by analogy rather than explained.

    Given the GitHub contents API serves "courses/demo/pair.md" with the document:
      """
      # Her screen

      ```csv
      name,fee,campus
      Peanut,95,Milwaukee
      Bo,120,Ozaukee
      ```
      {: .dataset #dogs }

      ```csv
      ```
      {: .datagrid #wired source="dogs" height="160" }

      ```csv
      ```
      {: .chart #fees type="pie" x="name" y="fee" source="adoptions" height="200" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/pair.md"
    And I wait for the page to be interactive
    Then the table is showing "Peanut"
    When I sweep the lens over the chart
    Then the lens marks "source" as naming nothing
    And the lens draws no part called "adoptions"
