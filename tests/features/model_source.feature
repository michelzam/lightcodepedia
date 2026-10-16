Feature: A class wears a dataset — the grid dresses the rows
  A class is a dataset (Michel, 2026-10-15): class Family(Object,
  source="calls") wraps the list's rows as objects, its columns as fields,
  and the grid on the class shows the state cell with a ⌄ of verbs, legal
  ones live and the others grey; edits and verbs go through the object and
  land in the list; New and Delete are born of Object.

  Background:
    Given I have a clean browser page
    When I navigate to "/components/dataset"
    And I wait for the page to be interactive

  Scenario: The dressed grid shows the list's columns, the state as a chip, no obj column
    Then the grid "family_grid" has the columns "family, dog, stage, since"
    And the stage cell of "Nguyen" in "family_grid" is a chip with a caret

  Scenario: The caret drops the row's verbs, legal ones live and the others grey
    When I open the verbs of "Nguyen" in "family_grid"
    Then the verb "meet" is live and "adopt" is grey, needing "met"
    And the menu ends with "Delete"

  Scenario: A grey verb says what it needs, a live one moves the row and the list
    When I open the verbs of "Nguyen" in "family_grid"
    And I press the verb "adopt"
    Then the grid "family_grid" says "needs met"
    When I open the verbs of "Nguyen" in "family_grid"
    And I press the verb "meet"
    Then the stage of "Nguyen" in "family_grid" reads "met"
    And the dataset "calls" has "Nguyen" at stage "met"

  Scenario: A typed cell edit goes through the object and the list recounts
    When I type "Wed" in the "since" cell of "Nguyen" in "family_grid"
    Then the dataset "calls" has "Nguyen" since "Wed"

  Scenario: New adds a row at its first stage; the form shows the verbs
    When I press New under "family_grid"
    Then the grid "family_grid" has 4 rows and the dataset "calls" has 4 rows
    When I click the row "Nguyen" in "family_grid"
    Then the form "family_card" shows the verbs "meet, adopt" with "adopt" grey

  Scenario: The page's own proof is green
    When I run the feature "class_source_proof"
    Then the feature "class_source_proof" is green

  Scenario: A grid on a class declared in the pad is wired, not broken
    Module 06 · 1bis on the live lab: the pad's broken-wire scan said
    "source «Family» — no such id on this page" over a working grid
    (Michel, 2026-10-16) — a class declared in the pad's own python is a
    dataset, so a wire to it holds.

    Given the GitHub contents API serves "courses/demo/module_06/dress.md" with the document:
      """
      # Dress

      `````markdown
      # The list, dressed

      ```csv
      family,dog,stage
      Nguyen,Biscuit,asked
      Diallo,Scout,met
      ```
      {: .dataset #calls }

      ```python
      class Family(Object, source="calls"):
          stage = State(["asked", "met", "home"])

          @transition(pre=["asked"], post="met")
          def meet(self):
              pass
      ```
      {: .model }

      [the families](#)
      {: .datagrid source="Family" #families }
      `````
      {: .mdpad #dress decorations="true" rows="20" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/dress.md"
    And I wait for the page to be interactive
    Then the "dress" pad shows the grid "families" dressed, with no broken wire
