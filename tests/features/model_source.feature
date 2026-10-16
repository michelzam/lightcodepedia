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

  Scenario: New adds a row at its first stage; the form shows the object, its state last as a chip, the verbs as buttons
    When I add a "Family" with New under "family_grid"
    Then the grid "family_grid" has 4 rows and the dataset "calls" has 4 rows
    When I click the row "Nguyen" in "family_grid"
    Then the form "family_card" shows the verbs "meet, adopt" with "adopt" grey
    And the form "family_card" shows the state "asked" as a chip, in its last row

  Scenario: Deleting the selected row moves the selection on, and the form follows
    When I click the row "Nguyen" in "family_grid"
    And the selected object of "family_grid" is deleted in code
    Then the grid "family_grid" has 2 rows and the dataset "calls" has 2 rows
    And the selected row of "family_grid" is "Diallo", and the form "family_card" shows "Diallo"

  Scenario: The last row's verbs are not clipped by the grid's frame
    When I open the verbs of "Alvarez" in "family_grid"
    Then the verbs menu is fully on screen

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

  Scenario: A row is always selected, from the first paint on
    Michel, 2026-10-16: "a line should always be selected in a grid after
    refresh, on opening, etc." — a grid with no id selected nothing.

    Then the grid "family_grid" has exactly one selected row

  Scenario: New offers the class and its subclasses, and selects the one it made
    Michel, 2026-10-16: "+New should select the new created line" and
    "+New should propose all subclasses of the grid's source class".

    When I press New under "family_grid"
    Then the New menu offers "Family, Foster"
    When I pick "Foster" in the New menu
    Then the grid "family_grid" has 4 rows and the dataset "calls" has 4 rows
    And the selected row of "family_grid" is the new one, at stage "asked"
    And its verbs offer "give_back" beside "meet"

  Scenario: A double click opens a cell with its value selected, and typing replaces it
    Michel, 2026-10-16: "data should be updatable in the grid (double click
    to enter a field?)" — a class grid edits by default; a single tap only
    selects.

    When I click the row "Diallo" in "family_grid"
    Then the "since" cell of "Nguyen" in "family_grid" is closed for typing
    When I double click the "since" cell of "Diallo" in "family_grid" and type "Mon"
    Then the dataset "calls" has "Diallo" since "Mon"

  Scenario: The stage chip and its caret sit on the row's text line
    Michel, 2026-10-16: the pill rode high, the ⌄ sank below the line.

    Then the chip, the caret and the family name of "Nguyen" in "family_grid" share one middle line

  Scenario: The pad marks errors in its gutter, the python fence's included
    Michel, 2026-10-16: "check that errors (syntax, etc) are detected and
    displayed in the gutter, including inside the py fence".

    Given the GitHub contents API serves "courses/demo/module_06/broken.md" with the document:
      """
      # Broken

      `````markdown
      # The list

      ```csv
      family,stage
      Nguyen,asked
      ```
      {: .dataset #calls }

      ```python
      class Family(Object, source="calls"):
          stage = State("asked", "met")

          def meet(self)
              pass
      ```
      {: .model }

      [the families](#)
      {: .datagrid source="Family" #families
      `````
      {: .mdpad #broken decorations="true" numbers="true" rows="20" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/broken.md"
    And I wait for the page to be interactive
    Then the "broken" pad marks lines "13, 19" as errors
    And the "broken" pad's line 19 says "a decoration closes with }" on itself, in no column of its own

  Scenario: A click on a TODO blank takes it whole, and typing replaces it
    Michel, 2026-10-16: "when a todo value is selected, the editor should
    replace it when the learner types, not insert characters".

    Given the GitHub contents API serves "courses/demo/module_06/blank.md" with the document:
      """
      # Blank

      `````markdown
      [the families](#)
      {: .datagrid source="TODO_YOUR_LIST" }
      `````
      {: .mdpad #blank rows="6" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/blank.md"
    And I wait for the page to be interactive
    And I click inside "TODO_YOUR_LIST" in the "blank" pad and type "calls"
    Then the "blank" pad reads 'source="calls"'

  Scenario: New leaves the caret in the new row's first cell, ready to type
    Michel, 2026-10-16: "when new is clicked in the grid, the cursor should
    be in the first cell ready to type a value".

    When I add a "Family" with New under "family_grid"
    And I type "Proof" and press Enter, without clicking
    Then the dataset "calls" has "Proof" at stage "asked"

  Scenario: Every stage chip has the same width, so the carets line up
    Then the stage chips of "family_grid" are all as wide, their carets in one column

  Scenario: A card on a dressed grid in a pad shows the lit row from the start
    Michel, 2026-10-16: the card said "(no data)" under a lit row — the
    class published an empty list first, and the grid never announced its
    first row again once the rows came.

    Given the GitHub contents API serves "courses/demo/module_06/card.md" with the document:
      """
      # Card

      `````markdown
      ```csv
      family,dog,stage
      Nguyen,Biscuit,asked
      Diallo,Scout,met
      ```
      {: .dataset #reservations }

      ```python
      class Family(Object, source="reservations"):
          stage = State("asked", "met", "home")

          @transition("asked", "met")
          def meet(self):
              pass
      ```
      {: .model }

      [the families](#)
      {: .datagrid source="Family" #families }

      [Title](#)
      {: .form master="families" }
      `````
      {: .mdpad #card decorations="true" rows="20" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/card.md"
    And I wait for the page to be interactive
    Then the card in the "card" pad shows "Nguyen"

  Scenario: Typing in a pad does not pile up listeners
    Michel, 2026-10-16: "when I have multiple classes and code, the typing
    is slow" — every pause re-rendered the preview, while each replaced
    grid or class kept its dataset listener: one more per pause.

    Given the GitHub contents API serves "courses/demo/module_06/card.md" with the document:
      """
      # Card

      `````markdown
      Families.

      ```csv
      family,dog,stage
      Nguyen,Biscuit,asked
      ```
      {: .dataset #reservations }

      ```python
      class Family(Object, source="reservations"):
          stage = State("asked", "met")
      ```
      {: .model }

      [the families](#)
      {: .datagrid source="Family" #families }
      `````
      {: .mdpad #card decorations="true" rows="20" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/card.md"
    And I wait for the page to be interactive
    And I type in the "card" pad three times, pausing after each
    Then the lists "reservations, Family" keep at most 2 listeners each

  Scenario: A subclass's card shows its own fields too
    Michel, 2026-10-16: "when an instance of a subclass is selected in the
    form, all the attributes should be displayed".

    When I add a "Foster" with New under "family_grid"
    And I type "Proof" and press Enter, without clicking
    Then the form "family_card" shows a field "Until"
    And the grid "family_grid" has the columns "family, dog, stage, since"

  Scenario: A diagram in a section accordion draws the class the pad declares
    Michel, 2026-10-16: "a diagram scoped to the Family class in an
    accordion later in the page" — a heading accordion moves its parts, so
    the diagram stays live and redraws when the pad's class runs.

    Given the GitHub contents API serves "courses/demo/module_06/drawn.md" with the document:
      """
      # Drawn

      `````markdown
      ```csv
      family,stage
      Nguyen,asked
      ```
      {: .dataset #reservations }

      ```python
      class Family(Object, source="reservations"):
          stage = State("asked", "met")

          @transition("asked", "met")
          def meet(self):
              pass


      class Company(Family):
          address = Attr(str)
      ```
      {: .model }
      `````
      {: .mdpad #drawn_pad decorations="true" rows="20" }

      ## The class, drawn
      {: .accordion }

      [the families, drawn](#)
      {: .diagram scope="Family" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/drawn.md"
    And I wait for the page to be interactive
    Then the diagram in the section accordion names "Family, Company, address, meet"

  Scenario: The x-ray draws the grid, its class and the class's list together
    Michel, 2026-10-16: "sometimes we see the model, other times the
    dataset — they should both be there (the model has Family using the
    dataset)".

    When I shift-hover over the grid "family_grid"
    Then the x-ray scene mentions "Model"
    And the x-ray scene mentions "calls"

  Scenario: A class renamed in a pad leaves no ghost behind
    Michel, 2026-10-16: the diagram kept Compan, Company, Companyy… one
    ghost per pause — the registries kept every class ever declared.

    Given the GitHub contents API serves "courses/demo/module_06/ghost.md" with the document:
      """
      # Ghost

      `````markdown
      ```csv
      family,stage
      Nguyen,asked
      ```
      {: .dataset #reservations }

      ```python
      class Family(Object, source="reservations"):
          stage = State("asked", "met")


      class Company(Family):
          address = Attr(str)
      ```
      {: .model }
      `````
      {: .mdpad #ghost_pad decorations="true" rows="20" }

      [the families, drawn](#)
      {: .diagram scope="Family" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/ghost.md"
    And I wait for the page to be interactive
    And in the "ghost_pad" pad I rename "Company" to "Partner", a letter at a time
    Then the class "Company" is gone from the page, "Partner" is there

  Scenario: A new row in the card swaps its values, not its table
    Michel, 2026-10-16: "changing lines in the grid is too slow — it
    rebuilds the form?" — it did, a whole table per click.

    When I click the row "Diallo" in "family_grid"
    Then the card "family_card" shows "Diallo" in the same table after I click the row "Alvarez"

  Scenario: The verbs and New wear the page's action blue
    Then the button New under "family_grid" and the verbs of "family_card" are filled blue

  Scenario: Typing prose in a pad keeps its live parts
    Michel, 2026-10-16: "never slow down interaction" — the preview now
    rebuilds only the block that changed.

    Given the GitHub contents API serves "courses/demo/module_06/card.md" with the document:
      """
      # Card

      `````markdown
      Families.

      ```csv
      family,stage
      Nguyen,asked
      ```
      {: .dataset #reservations }

      [the families](#)
      {: .datagrid source="reservations" #families }
      `````
      {: .mdpad #card decorations="true" rows="20" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/card.md"
    And I wait for the page to be interactive
    And I mark the grid "families" and type in the "card" pad three times, pausing after each
    Then the grid "families" is the one I marked

  Scenario: Stage labels sit centred in pills of one width; a column resizes and stays
    Michel, 2026-10-16: "state labels justified in the pill", "columns
    should be resizable".

    Then the stage labels of "family_grid" are centred
    When I widen the column "dog" of "family_grid" by 80 pixels
    And I open the verbs of "Nguyen" in "family_grid"
    And I press the verb "meet"
    Then the column "dog" of "family_grid" is still at least 70 pixels wider

  Scenario: The pad's busy mark shows on a dark title too
    Michel, 2026-10-16: "when the preview's title is black, the temporary
    refresh sign is not visible".

    Given the GitHub contents API serves "courses/demo/module_06/card.md" with the document:
      """
      # Card

      `````markdown
      # A title

      Families.
      `````
      {: .mdpad #card decorations="true" rows="8" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/card.md"
    And I wait for the page to be interactive
    Then the "card" pad's busy mark is a white disc

  Scenario: A class with no state still offers its verbs, from the row's first cell
    Michel, 2026-10-16: "if there is no state, there still should be
    actions to call — maybe the first column should have the ⌄".

    Given the GitHub contents API serves "courses/demo/module_06/walkers.md" with the document:
      """
      # Walkers

      `````markdown
      ```csv
      name,walks
      Ada,0
      Ben,2
      ```
      {: .dataset #volunteers }

      ```python
      class Walker(Object, source="volunteers"):
          def walk(self):
              self.walks = self.walks + 1
      ```
      {: .model }

      [the walkers](#)
      {: .datagrid source="Walker" #walkers }
      `````
      {: .mdpad #walk_pad decorations="true" rows="20" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/walkers.md"
    And I wait for the page to be interactive
    And I open the first-cell verbs of "Ada" in "walkers"
    Then the menu offers "walk" and ends with "Delete"
    When I press the verb "walk"
    Then the dataset "volunteers" has "Ada" with 1 walks

  Scenario: A Google Sheet's own link reads as rows; a web page says it is not rows
    Michel, 2026-10-16: the grid stayed empty on a sheet's …/edit?usp=sharing
    link — the editor's web page, not the rows.

    Given a Google Sheet "SHEETID" holds the walks "Fern, Michel" and "Scout, Ada"
    And the GitHub contents API serves "courses/demo/module_06/gsheet.md" with the document:
      """
      # Sheet

      [the walk sheet](https://docs.google.com/spreadsheets/d/SHEETID/edit?usp=sharing)
      {: .dataset #walks }

      [the walks so far](#)
      {: .datagrid source="walks" #walk_list }

      [a web page](https://example.org/page.html)
      {: .dataset #page }

      [not rows](#)
      {: .datagrid source="page" #page_list }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/gsheet.md"
    And I wait for the page to be interactive
    Then the grid "walk_list" shows "Fern" and "Scout"
    And the grid "page_list" reads "a web page, not rows"

  Scenario: A list read from a sheet is read again by its ↻, and on coming back to the page
    Michel, 2026-10-16: "how to refresh the grid after a change made
    directly in the sheet?"

    Given a Google Sheet "SHEETID" holds the walks "Fern, Michel" and "Scout, Ada"
    And the GitHub contents API serves "courses/demo/module_06/gsheet.md" with the document:
      """
      # Sheet

      [the walk sheet](https://docs.google.com/spreadsheets/d/SHEETID/edit?usp=sharing)
      {: .dataset #walks }

      [the walks so far](#)
      {: .datagrid source="walks" #walk_list }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/gsheet.md"
    And I wait for the page to be interactive
    Then the grid "walk_list" shows "Fern" and "Scout"
    When the sheet "SHEETID" gains the walk "Nova, Cleo" and I press ↻ on "walk_list"
    Then the grid "walk_list" shows "Nova" and "Fern"
    When the sheet "SHEETID" gains the walk "Biscuit, Ben" and I come back to the page
    Then the grid "walk_list" shows "Biscuit" and "Nova"

