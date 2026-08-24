Feature: Page editor — ✨ AI edit dialog

  The editor's ✨ button (top bar) opens a dialog scoped to the current
  selection, where the author asks for a change. This asserts the
  structural slice that needs no GitHub token: the button opens the
  dialog and reveals a prompt; and the editor has a Log tab.

  Background:
    Given I have a clean browser page

  Scenario: The ✨ button opens the AI edit dialog with a prompt
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the page editor
    And I click the editor "ed-agent-btn" button
    Then the editor agent pane shows a prompt box

  Scenario: A key GitHub refuses surfaces the sign-in instead of a dead picker
    # A stored key that GitHub no longer accepts (expired, revoked, rescoped)
    # made the file list error and the filename show ⚠️ — the picker "looked
    # broken" — while ⚙️ Connect stayed COLLAPSED (we only auto-expanded it when
    # no key was stored), so the way back in was invisible.
    Given a stored key that GitHub refuses
    When I navigate to "/nodes"
    And I wait for the page to be interactive
    And I open the page editor
    Then the sign-in panel is offered

  Scenario: The editor has a Log tab
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the page editor
    And I switch to the editor "log" tab
    Then the editor log pane is visible

  Scenario: The editor has a Features tab
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the page editor
    And I switch to the editor "features" tab
    Then the editor features pane is visible

  Scenario: The editor has a Diagram tab
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the page editor
    And I switch to the editor "diagram" tab
    Then the editor diagram pane is visible

  Scenario: The Diagram tab renders the page's class graph
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the page editor
    And I load sample components into the editor
    And I switch to the editor "diagram" tab
    Then the editor diagram renders a class graph

  Scenario: The Raw tab is the dark basement workshop
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the page editor
    And I switch to the editor "raw" tab
    Then the raw editor is dark themed

  Scenario: The Raw editor has a formatting toolbar
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the page editor
    And I switch to the editor "raw" tab
    Then the editor formatting toolbar is visible
    When I bold a selection with the toolbar
    Then the raw editor contains "**"

  Scenario: The Blocks-tab Content editor is dark too
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the page editor
    And I load sample components into the editor
    And I switch to the editor "blocks" tab
    And I select the first block
    Then the block content editor is dark themed

  Scenario: Ask AI reads the page's embedded fragments too
    Given a builder key is connected
    And the counting GitHub contents API serves "docs/_frag.md" as "frag"
    And the AI model endpoint is stubbed
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the page editor
    And the editor content is:
      """
      # Lesson

      [Why](/_frag)
      {: .embed }
      """
    And I click the editor "ed-agent-btn" button
    And I ask the editor AI to "generate a quiz from this page"
    Then the AI request carried the embedded fragment

  Scenario: editable=0 closes every editing door
    When I navigate to "/tutorial101?editable=0"
    And I wait for the page to be interactive
    And I press the edit hotkey
    Then the editor drawer stays closed
    And the pill offers no Edit item

  Scenario: A page of this site is edited in this site's repo, not the last bench paired
    lc_ed_repo is ONE browser-wide pairing and the last bench to connect
    wins it. After bench work, opening the editor on a plain site page
    connected it to the BENCH — which does not hold that page — so the
    site's own author could not edit his own site (Michel, 2026-08-19,
    lightcodepedia.org/events). The page you are on decides the repo.

    Given a browser still paired to a learner's bench
    When I navigate to "/events"
    And I wait for the page to be interactive
    And I press the edit hotkey
    Then the editor reads this site's own repo, not the bench

  Scenario: The Raw editor folds its fences, and never saves them folded
    A page is mostly fences; reading the prose between them meant
    scrolling through walls of yaml (Michel, 2026-08-23). Fold collapses
    every fenced block to one marker line — DISPLAY only: the value the
    save path reads stays the full source, and clicking a marker unfolds
    it in place.

    Given I open the editor on a page with two fenced blocks
    When I press the fold button
    Then the display shrinks to marker lines
    And the markers wear their block's icon and type
    But the full source is still what a save would read
    And the gutter numbers stay source-true across the folds
    When I click the first marker line
    Then that block is back in place
    When I refold it from the gutter arrow
    Then the display shrinks to marker lines

  Scenario: A loaded file arrives folded — the outline first
    Folded by default (Michel, 2026-08-23): a page opens as its outline,
    every fenced block one marker line, so the Raw tab reads modular and
    you unfold only what you touch. The virtual value stays the full
    source, so nothing about saving changes.

    Given I have a clean browser page
    And a connected editor whose repo serves a two-fence page
    When I navigate to "/events"
    And I wait for the page to be interactive
    And I open the page editor
    And the editor has loaded the page's own file
    And I switch to the editor "raw" tab
    Then the display shrinks to marker lines
    And the markers wear their block's icon and type
    But the full source is still what a save would read

  Scenario: The draft checker knows the classes the draft declares
    A grid binds a CLASS, not only a block id (bind="Student") — the
    checker read that as a broken reference and stamped ⚠ on an honest
    draft (Michel, 2026-08-23). Class names declared in python fences
    count as identifiers; a name nothing declares still warns.

    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I open the page editor
    And the editor content is:
      """
      # Demo

      ```python
      class Student(Object):
          name = Attr()
      ```
      {: .inspector #models }

      [grid](#)
      {: .datagrid #g1 bind="Student" }

      [ghost](#)
      {: .datagrid #g2 bind="Ghost" }
      """
    Then the draft checker warns only about "Ghost"

  Scenario: Closing and reopening the editor never amputates the folds
    The drawer used to re-wire the fold engine on every open: the value
    property rebound to a fresh empty fold map while the display still
    held the old session's markers — one save then committed marker
    lines to git, fences gone (Michel, 2026-08-24, classroom3). One
    wiring per page lifetime, plus a last gate: a save refuses content
    that still carries a fold token.

    Given I have a clean browser page
    And a connected editor whose repo serves a two-fence page
    When I navigate to "/events"
    And I wait for the page to be interactive
    And I open the page editor
    And the editor has loaded the page's own file
    And I close the page editor
    And I open the page editor
    Then the full source is still what a save would read
