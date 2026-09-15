Feature: Everything a mouse can do, a keyboard can do

  A learner who cannot use a mouse must be able to take the course. This is
  WCAG 2.1.1 at Level A — the floor, not the polish. It lives in the gating
  suite rather than the axe scan on purpose: a static scan cannot tell that an
  element with a click handler has no keyboard path, so it scores a
  keyboard-dead quiz as perfect. Every keyboard fix from here to April lands
  with a scenario here, or it is not done.

  Background:
    Given I have a clean browser page

  Scenario: Every quiz answer is a tab stop
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    Then every quiz answer is reachable by keyboard

  Scenario: A quiz answer can be focused and read by assistive tech
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I tab to the quiz answer "Labrador Retriever"
    Then that quiz answer is the focused element
    And the quiz answer "Labrador Retriever" exposes the role "radio"

  Scenario: Enter answers the quiz, exactly as a click does
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I tab to the quiz answer "Labrador Retriever"
    And I press "Enter"
    Then that quiz answer is marked correct
    And the quiz answer "Labrador Retriever" is announced as checked

  Scenario: Space answers the quiz too
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I tab to the quiz answer "Beagle"
    And I press " "
    Then that quiz answer is marked wrong

  Scenario: Every field an agent asks for announces what it wants
    A screen reader gets nothing from a placeholder. The key panel is the
    one form on this site a learner MUST fill in to go further, and it grew
    a hidden keychain-identity field when the provider became configurable —
    six unnamed inputs, straight past the axe ratchet.

    When I navigate to "/components/agent"
    And I wait for the page to be interactive
    Then every agent form field has an accessible name

  Scenario: Arrow keys walk the answers
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I tab to the quiz answer "Beagle"
    And I press "ArrowDown"
    Then that quiz answer is not the focused element

  Scenario: Every code editor tells assistive tech what it is
    The Python editors, the REPL prompt and the markdown pad rendered as
    naked textareas — a screen reader announced bare "edit text" with no
    purpose, 15+ nodes across the site, and the axe ratchet stayed red on
    rule "label" for days (2026-08-10). The frame names the editor for the
    eye; it must name it for the reader too.

    When I navigate to "/components/run"
    And I wait for the page to be interactive
    Then every code editor on the page exposes an accessible name

  Scenario: A code editor's painted overlay is not a tab stop
    Behind every Python editor sits a painted copy of the code, hidden from
    assistive tech, that the syntax highlighter colours. The highlighter
    also makes any bare pre it touches a tab stop, so a keyboard user landed
    on an element a screen reader was told did not exist; the axe ratchet
    stayed red on aria-hidden-focus from 2026-09-03, two nodes per new
    example (2026-09-13). The overlay says "not a tab stop" itself, before
    the highlighter can say otherwise.

    When I navigate to "/components/run"
    And I wait for the page to be interactive
    Then no hidden code overlay on the page is a tab stop

  Scenario: Form fields carry the name their row shows
    When I navigate to "/components/form"
    And I wait for the page to be interactive
    Then every form control on the page exposes an accessible name


  Scenario: ⌥C shows every shortcut, Space closes the sheet and focus comes home
    Michel (2026-09-15): a hot key that displays all the key shortcuts, to
    document High contrast and the other options; closing with a space.

    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I focus the Modes pill
    And I press "Alt+KeyC"
    Then the shortcuts sheet is open with focus on its close button
    When I press " "
    Then the shortcuts sheet is closed and focus is back on the Modes pill

  Scenario: ⌥H turns High contrast on and off, and the sheet says which
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I press "Alt+KeyH"
    Then the page is in High contrast
    When I press "Alt+KeyC"
    Then the shortcuts sheet says High contrast is "now on"
    When I press "Escape"
    And I press "Alt+KeyH"
    Then the page is not in High contrast

  Scenario: The Modes pill opens from the keyboard, and Escape brings focus back
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I focus the Modes pill
    And I press "Enter"
    Then the modes popup is open with focus on its first item
    When I press "ArrowDown"
    Then focus is on the second item of the modes popup
    When I press "Escape"
    Then the modes popup is closed and focus is back on the Modes pill
