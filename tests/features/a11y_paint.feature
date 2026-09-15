Feature: What we paint ourselves reads, and names itself

  The private accessibility scan walks the live site and names its nodes;
  this is its rig-side twin for the things WE choose — a colour, a role, a
  hidden field — so a fix stays fixed. The course pages joined the scan on
  2026-09-13 and surfaced exactly these: a nameless hidden field on the
  join wizard (critical), grey numbers, faded links, a code comment and a
  placeholder all under AA, and footnotes wearing a role the standard
  retired. Each landed here first, red, then green.

  Background:
    Given I have a clean browser page

  Scenario: The form's numbers read at AA contrast
    When I navigate to "/components/form"
    And I wait for the page to be interactive
    Then the text in ".lc-form-num" reads at AA contrast

  Scenario: A code comment in the editor reads at AA contrast
    When I navigate to "/components/run"
    And I wait for the page to be interactive
    Then the text in ".lc-pyrun .token.comment" reads at AA contrast

  Scenario: Footnotes are list items, not a retired role
    When I navigate to "/components/run"
    And I wait for the page to be interactive
    Then no footnote carries a retired role

  Scenario: The chart's empty placeholder reads at AA contrast
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    Then the text in ".lc-chart > div" reads at AA contrast

  Scenario: The field the join wizard hides for password managers has a name
    A screen reader met a text field with no name at all on the energy-key
    step — axe's one critical finding across the course pages.

    When I navigate to "/courses/join"
    And I wait for the page to be interactive
    Then every field hidden for the password manager still carries a name

  Scenario: The runner's status line reads at AA contrast
    The line shows when a page is missing and names the paths it tried;
    the scan met it on a quiz folder the vault never receives.

    Given the GitHub API answers 404 for anything else
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/work.md" with the document:
      """
      # Work page

      Just a page.
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/missing.md"
    And I wait for the page to be interactive
    Then the text in ".lc-run-status code" reads at AA contrast


  Scenario: Every map marker has a role and says what it marks
    The map library stamps each dot "Map marker" on a box with no role — a
    name with nothing to hang it on. A dot is a button that opens its
    popup, and its name is what the popup says.

    When I navigate to "/components/map"
    And I wait for the page to be interactive
    Then every map marker carries a role and a name of its own

  Scenario: A grid's scroll region is reachable by keyboard
    When I navigate to "/components/datagrid"
    And I wait for the page to be interactive
    Then every grid scroll region is a tab stop

  Scenario: A quiz answer holds no second control
    When I navigate to "/components/datagrid"
    And I wait for the page to be interactive
    Then no quiz answer contains a focusable descendant
    And the footnote mark inside an answer still opens its popover


  Scenario: High contrast makes the help chips read at AA, and nothing on the page stays tiny
    The default keeps its look (Michel, 2026-09-15): under High contrast the
    "i" chips, the arrows and the hints darken and grow, for the learner who
    asked for more — one toggle, ⌥H, no impact on anyone else.

    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I press "Alt+KeyH"
    Then the page is in High contrast
    And the text in ".lc-help" reads at AA contrast
    And no visible text on the page is smaller than 11 pixels
