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

  Scenario: Subtitles say what each part of the program is, on hover and on tap
    Michel, 2026-10-27: "tooltips in that .run component to explicit what code
    parts are (variable, type, positional or named param, default value,
    conditionals, etc), based on an on/off option to add subtitles".
    When I wait for the selector "#lc-pyrun-subtitled .lc-pyrun-subs .lc-sub"
    Then the "subtitled" editor subtitles "name" as "a parameter"
    And the "subtitled" editor subtitles "times" as "a parameter with a default value"
    And the "subtitled" editor subtitles "str" as "a type hint"
    And the "subtitled" editor subtitles "hello" as "a variable"
    And the "subtitled" editor subtitles "i" as "the loop variable"
    And the "subtitled" editor subtitles "greet" as "the function's name"
    And the "subtitled" editor subtitles "for" as "for — repeats"
    When I tap the subtitle "times" in the "subtitled" editor
    Then the "subtitled" editor's subtitle line reads "times — a parameter with a default value"
    When I press 💬 Subtitles in the "subtitled" editor
    Then the "subtitled" editor is back to editing
    When I press 💬 Subtitles in the "first_run" editor
    Then the "first_run" editor shows its subtitles

  Scenario: The bar speaks softly — icons with tooltips, ▶ Run keeps its word, 💬 is a switch that shows its state
    Michel, 2026-10-27: "make the buttons more subtle (icons + tooltips for
    labels) except for ▶ Run; make the subtitles button more an on/off switch".
    Then the "first_run" editor's run button reads "▶ Run"
    And the "first_run" editor's "test" button is an icon with the tooltip "Test"
    And the "first_run" editor's clear button reads "Clear"
    And the "first_run" editor's subtitles switch is "false"
    When I press 💬 Subtitles in the "first_run" editor
    Then the "first_run" editor's subtitles switch is "true"

  Scenario: Ctrl+Space completes from the program and the runner; two letters open the list; Enter takes it
    Michel, 2026-10-27: "code completion, a bit like in mdpad".
    When I replace the "first_run" editor's program with:
      """
      greeting = "hello"
      pl
      """
    And I put the caret at the end of the "first_run" editor
    And I press Ctrl+Space in the "first_run" editor
    Then the "first_run" editor offers the name "play"
    When I accept the completion in the "first_run" editor
    Then the "first_run" editor ends with "play"
    When I type "." at the end of the "first_run" editor
    Then the "first_run" editor offers "tempo" and "wave"
    When I press Escape in the "first_run" editor
    And I type " gr" at the end of the "first_run" editor
    Then the "first_run" editor offers the name "greeting"

  Scenario: Selecting a word lights its other occurrences
    Michel, 2026-10-27: "flash the other occurrences of a given symbol when selected".
    When I replace the "first_run" editor's program with:
      """
      total = 0
      for n in [1, 2, 3]:
          total = total + n
      print(total)
      """
    And I select the word "total" in the "first_run" editor
    Then the "first_run" editor lights 3 other occurrences of "total"
    When I select the word "n" in the "first_run" editor
    Then the "first_run" editor lights 1 other occurrences of "n"

  Scenario: Under the captions the colours stay, keywords bold, and a block folds
    Michel, 2026-10-27: "when the captions are on, the syntax should remain
    colored; bold for python keywords; make the code foldable in caption_on mode".
    When I wait for the selector "#lc-pyrun-subtitled .lc-pyrun-subs .lc-sub"
    Then the "subtitled" editor's captions colour "def" as a bold keyword
    And the "subtitled" editor's captions colour "Lucky" as a string
    When I fold the block at "def" in the "subtitled" editor
    Then the "subtitled" editor hides 10 captioned lines
    And the "subtitled" editor's gutter numbers 2 lines
    When I fold the block at "def" in the "subtitled" editor
    Then the "subtitled" editor hides 0 captioned lines
    And the "subtitled" editor's gutter numbers 12 lines

  Scenario: The grip under the editor sets its height; a double-click gives it back
    Michel, 2026-10-27: "we also need a vertical resizing handle (like mdpad)".
    When I drag the "first_run" editor's grip down by 120 pixels
    Then the "first_run" editor grew by about 120 pixels
    When I double-click the "first_run" editor's grip
    Then the "first_run" editor is back to its own height

  Scenario: Captions add no lines of their own
    Michel, 2026-10-27, a snapshot: blank lines between every captioned line.
    When I wait for the selector "#lc-pyrun-subtitled .lc-pyrun-subs .lc-sub"
    Then the "subtitled" editor's captions count as many lines as the program
