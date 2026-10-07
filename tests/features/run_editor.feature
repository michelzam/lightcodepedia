Feature: The run editor types like a text field
  Michel, 2026-10-07, on the 6a starter: "undo does NOT work in that editor",
  and "= in an f-string between curly brackets gives an error". The editor
  keeps the browser's undo — a run of typing is one ⌘Z, Tab and the tutor's
  piece are typed, not assigned — and CPython's f'{x = }' runs on MicroPython.

  Background:
    Given I have a clean browser page
    When I navigate to "/components/run"
    And I wait for the page to be interactive
    And I wait for the selector "#lc-pyrun-first_run .lc-pyrun-code"

  Scenario: A run of typing undoes as one
    When I type "  # hello" at the end of the "first_run" editor
    Then the "first_run" editor ends with "  # hello"
    When I undo in the "first_run" editor
    Then the "first_run" editor does not contain "# hello"

  Scenario: Tab indents and undoes
    When I type "x" at the end of the "first_run" editor
    And I press Tab in the "first_run" editor
    Then the "first_run" editor ends with "x    "
    When I undo in the "first_run" editor
    Then the "first_run" editor ends with "x"

  Scenario: An f-string with = runs as CPython reads it
    When I replace the "first_run" editor's program with:
      """
      a = 5
      print(f'{a = }, {a == 5}, {a = :>3}, {{a}}, {a=!s}')
      print(f"{a}=")
      """
    And I click Run in the "first_run" editor
    Then the "first_run" editor's output reads "a = 5, True, a =   5, {a}, a=5" then "5="

  Scenario: Tab on a selection indents the lines, Shift+Tab brings them back
    Michel, 2026-10-07: "when a text is selected, if I type a tab, it deletes
    it instead of indenting".

    When I replace the "first_run" editor's program with:
      """
      a = 1
      b = 2
      c = 3
      """
    And I select the lines "b = 2" to "c = 3" of the "first_run" editor
    And I press Tab in the "first_run" editor
    Then the "first_run" editor reads "a = 1\n    b = 2\n    c = 3"
    And the "first_run" editor's selection reads "    b = 2\n    c = 3"
    When I press Shift+Tab in the "first_run" editor
    Then the "first_run" editor reads "a = 1\nb = 2\nc = 3"
    When I undo in the "first_run" editor
    Then the "first_run" editor reads "a = 1\n    b = 2\n    c = 3"
