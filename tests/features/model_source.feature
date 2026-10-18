Feature: A class wears a dataset — the grid dresses the rows
  A class is a dataset (Michel, 2026-10-15): class Family(Object,
  source="calls") wraps the list's rows as objects, its columns as fields,
  and the grid on the class shows the state as a chip, the gutter ⋯ with
  the verbs, legal ones live and the others grey (the ⌄ on the chip went
  with the gutter, Michel 2026-10-18); edits and verbs go through the object and
  land in the list; New and Delete are born of Object.

  Background:
    Given I have a clean browser page
    When I navigate to "/components/dataset"
    And I wait for the page to be interactive

  Scenario: The dressed grid shows the list's columns, the state as a chip, no obj column
    Then the grid "family_grid" has the columns "family, dog, stage, since"
    And the stage cell of "Nguyen" in "family_grid" is a chip, with no caret
    # a class with stages wears the gutter too, as on page 3 (Michel, 2026-10-18: "Gutter?")
    And every row of "family_grid" wears the gutter, which opens its verbs

  Scenario: The gutter drops the row's verbs, legal ones live and the others grey
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

  Scenario: The stage chip sits on the row's text line
    Michel, 2026-10-16: the pill rode high, the ⌄ sank below the line.

    Then the chip and the family name of "Nguyen" in "family_grid" share one middle line

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

  Scenario: Every stage chip has the same width
    Then the stage chips of "family_grid" are all as wide

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

  Scenario: A class with no state offers its verbs from a light ⋯ in the row's gutter
    Michel, 2026-10-16: "if there is no state, there still should be
    actions to call". 2026-10-17: "I would prefer a gutter with a simple
    discrete/light but intuitive way to open the method picklist."

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
    Then the rows of "walkers" wear a faint ⋯ in a gutter, and the first column holds only the name
    When I open the ⋯ of "Ada" in "walkers"
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

  Scenario: sheet= names the tab the page reads
    Michel, 2026-10-16: "why don't you use the Sheet1 name anywhere?"

    Given a Google Sheet "SHEETID" holds the walks "Fern, Michel" and "Scout, Ada"
    And the GitHub contents API serves "courses/demo/module_06/gsheet.md" with the document:
      """
      # Sheet

      [the walk sheet](https://docs.google.com/spreadsheets/d/SHEETID/edit?usp=sharing)
      {: .dataset #walks sheet="Sheet1" }

      [the walks so far](#)
      {: .datagrid source="walks" #walk_list }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/gsheet.md"
    And I wait for the page to be interactive
    Then the grid "walk_list" shows "Fern" and "Scout"
    And the sheet was asked for its tab "Sheet1"

  Scenario: A class on a database table — empty grid, New, edit, delete, each saved by itself, once
    Michel, 2026-10-17: "I create the db myself, define the Family class,
    read the empty grid with the class, students add new objects (+New and
    a form), then save and refresh. They don't need to learn SQL." Then:
    "autosave should work as soon as it looks reasonable", with "a + round
    little button", a refresh "better visible on hovering" and "a similar,
    more stable and visual one for save" at the grid's top right corner.

    Given a database table "families" that is empty
    And the GitHub contents API serves "courses/demo/module_06/db.md" with the document:
      """
      # Families

      `````markdown
      [the families](https://demo.supabase.co/rest/v1/families)
      {: .dataset #families_db apikey="sb_publishable_test" }

      ```python
      class Family(Object, source="families_db"):
          family = Attr(str)
          dog = Attr(str)
          stage = State("asked", "met", "home")

          @transition("asked", "met")
          def meet(self):
              pass
      ```
      {: .model }

      [the families](#)
      {: .datagrid source="Family" #families }

      [the family](#)
      {: .form master="families" }
      `````
      {: .mdpad #db_pad decorations="true" rows="20" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/db.md"
    And I wait for the page to be interactive
    Then the grid "families" has the columns "family, dog, stage" and no row
    And Save under "families" is off
    And the corner of "families" holds ＋, ↻ and the save state, and no footer
    When I add a "Family" with New under "families"
    Then nothing is sent while the new row is blank
    When I type "Nguyen" and press Enter, without clicking
    Then the table "families" received an insert of "Nguyen" at stage "asked", with its key
    And the grid "families" shows the row "Nguyen" read back from the table
    When I double click the "dog" cell of "Nguyen" in "families" and type "Biscuit"
    Then the table "families" received an update of row 1 with dog "Biscuit"
    When I open the verbs of "Nguyen" in "families" and delete it
    Then the table "families" received a delete of row 1


  Scenario: A database that cannot be reached says so under the class grid, never as a row
    Michel, 2026-10-17 (page 3 before the real address): "Load failed"
    became a family at stage asked, in a ⚠️ column.

    Given a database "families" that cannot be reached
    And the GitHub contents API serves "courses/demo/module_06/db_down.md" with the document:
      """
      # Families

      [the families](https://demo.supabase.co/rest/v1/families)
      {: .dataset #families_db apikey="sb_publishable_test" }

      ```python
      class Family(Object, source="families_db"):
          family = Attr(str)
          dog = Attr(str)
          stage = State("asked", "met", "home")
      ```
      {: .model }

      [the families](#)
      {: .datagrid source="Family" #families }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/db_down.md"
    And I wait for the page to be interactive
    Then the grid "families" has the columns "family, dog, stage" and no row
    And the grid "families" says "the database cannot be reached", with no error column
    And the grid "families" still offers New, Save and Refresh

  Scenario: An unlisted table — the author's class makes it, a classmate reads and writes it by its name
    Michel, 2026-10-17: "I would like my class to create the table if not
    exists, even if I need to add a token in my browser, while letting
    others read or write data, just by sharing a special unlisted name."

    Given a database with the Lightcode setup and no author yet
    And the GitHub contents API serves "courses/demo/module_06/unl.md" with the document:
      """
      # Walks

      [the walks](https://demo.supabase.co/rest/v1/walks)
      {: .dataset #walks_db apikey="sb_publishable_test" unlisted="true" }

      ```python
      class Walk(Object, source="walks_db"):
          dog = Attr(str)
          walker = Attr(str)
          hour = Attr(str)
      ```
      {: .model }

      [the walks](#)
      {: .datagrid source="Walk" #walks }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/unl.md"
    And I wait for the page to be interactive
    Then the grid "walks" has the columns "dog, walker, hour" and no row
    And the grid "walks" asks for the list's unlisted name
    When I say I am the author under "walks", with no key yet
    Then the database has me as its author, and a table "walks" made of "dog, walker, hour"
    And the grid "walks" shows the name to share and my new author key
    When I copy my author key under "walks"
    Then the key leaves the grid "walks", and only the name to share stays
    When I add a "Walk" with New under "walks"
    And I type "Biscuit", the cell still open
    And I press Save under "walks" once, with the mouse
    Then the table "walks" holds "Biscuit", saved through its name
    When a classmate opens the page on another device and pastes the name under "walks"
    Then the grid "walks" shows the row "Biscuit" read back from the table
    And the grid "walks" has the columns "dog, walker, hour"
    And the grid "walks" offers no name to share
    When a stranger pastes "walks-000000000000" under "walks"
    Then the grid "walks" says "no list by that name", with no error column

  Scenario: A model on a .database — each class its table, the name in the page, the key in databases.yml
    Michel, 2026-10-17 (register P3): ".database to set the connection; a model
    with database= where class names match table names; the unlisted key in
    the starter code, students use it directly; the api-key not in the md."

    Given a database with the Lightcode setup and no author yet
    And the shelter database holds a "walk" table with "Biscuit"
    And the GitHub contents API serves "courses/demo/databases.yml" with the document:
      """
      shelter:
        url: https://demo.supabase.co
        key: sb_publishable_yml
      """
    And the GitHub contents API serves "courses/demo/module_06/model_db.md" with the document:
      """
      # Walks

      [the shelter](supabase://shelter)
      {: .database #shelter unlisted="5f2c9a01b7e3" }

      ```python
      class Walk(Object):
          dog = Attr(str)
          walker = Attr(str)
      ```
      {: .model source="shelter" }

      [the walks](#)
      {: .datagrid source="Walk" #walks }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/model_db.md"
    And I wait for the page to be interactive
    Then the grid "walks" shows the row "Biscuit" read back from the table
    And the page asked for nothing under "walks"
    And the database was read with the page's name and the key from databases.yml, never from the page

  Scenario: On the author's device, a .database without its name says which one to put
    Given a database with the Lightcode setup and no author yet
    And the GitHub contents API serves "courses/demo/databases.yml" with the document:
      """
      shelter:
        url: https://demo.supabase.co
        key: sb_publishable_yml
      """
    And the GitHub contents API serves "courses/demo/module_06/model_new.md" with the document:
      """
      # Walks

      [the shelter](supabase://shelter)
      {: .database #shelter }

      ```python
      class Walk(Object):
          dog = Attr(str)
          walker = Attr(str)
      ```
      {: .model source="shelter" }

      [the walks](#)
      {: .datagrid source="Walk" #walks }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/model_new.md"
    And I wait for the page to be interactive
    And I say I am the author under "walks", with no key yet
    Then the database has me as its author, and a table "walk" made of "dog, walker"
    And the author is told the database's name to put on the "shelter" line under "walks"

  Scenario: Writing the name on the .database line in a pad clears the author's hint
    Michel, 2026-10-17: "did that, but the grid is dirty with the key! even
    after copy!" — the pad redrew only the line he changed; the class's
    table kept the old, nameless line. And: "when I type speed, I would have
    multiple columns s, sp, spe, spee and speed" — columns wait for ↻. And
    "rows are twice!" — a redraw never sends a walk a second time.

    Given a database with the Lightcode setup and no author yet
    And the GitHub contents API serves "courses/demo/databases.yml" with the document:
      """
      shelter:
        url: https://demo.supabase.co
        key: sb_publishable_yml
      """
    And the GitHub contents API serves "courses/demo/module_06/model_pad.md" with the document:
      """
      # Walks

      `````markdown
      [the shelter](supabase://shelter)
      {: .database #shelter }

      ```python
      class Walk(Object):
          dog = Attr(str)
          walker = Attr(str)
      ```
      {: .model source="shelter" }

      [the walks](#)
      {: .datagrid source="Walk" #walks }
      `````
      {: .mdpad #walk_pad decorations="true" rows="20" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/model_pad.md"
    And I wait for the page to be interactive
    And I say I am the author under "walks", with no key yet
    Then the author is told the database's name to put on the "shelter" line under "walks"
    When I write the name the grid gave on the "shelter" line of the "walk_pad" pad
    Then the grid "walks" says nothing more about names
    When I add a "Walk" with New under "walks"
    And I type "Rex" and press Enter, without clicking
    And the "walk_pad" pad redraws its class twice while the walk is saving
    Then the table "walk" holds "Rex" once
    When the page's picture of the "walk" table is lost, and the grid saves
    Then no walk is sent again
    When I type the attribute "speed = Attr(str)" into the class in the "walk_pad" pad, letter by letter
    Then no column was made while typing, and 🔄 under "walks" offers "speed"
    When I apply the structure under "walks"
    Then the table "walk" gained the column "speed", and no other

  Scenario: A docstring's emoji is the icon of its class and its methods
    Michel, 2026-10-17 (register P4): "how to add icons/emojis to methods
    without loading too much the code?" — a one-line docstring; "add it also
    for the class, using it in button actions and in the grid's icon,
    replacing the grid generic emoji". A space before the emoji is fine.

    Given the GitHub contents API serves "courses/demo/module_06/icons.md" with the document:
      """
      # Walkers

      ```csv
      name,walks
      Ada,0
      Ben,2
      ```
      {: .dataset #volunteers }

      ```python
      class Walker(Object, source="volunteers"):
          '''🦮 A volunteer who walks the dogs.'''
          def walk(self):
              ''' 🐾 Count one more walk.'''
              self.walks = self.walks + 1
      ```
      {: .model }

      [the walkers](#)
      {: .datagrid source="Walker" #walkers }

      [the walker](#)
      {: .form master="walkers" #walker_card }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/icons.md"
    And I wait for the page to be interactive
    Then the title of "walkers" wears "🦮" instead of "▦", saying "A volunteer who walks the dogs."
    When I open the ⋯ of "Ada" in "walkers"
    Then the menu's "walk" reads "🐾 Walk", saying "Count one more walk."
    And the form "walker_card" has a button "🐾 Walk"

  Scenario: An attribute declared hidden shows in no grid and no form
    Michel, 2026-10-17: "when I declare an attribute as hidden, it should not
    appear anymore in the grid" — hour = Attr(str, hidden=True).

    Given the GitHub contents API serves "courses/demo/module_06/hidden.md" with the document:
      """
      # Walks

      ```csv
      dog,walker,hour
      Biscuit,Ana,08:00
      ```
      {: .dataset #walk_list }

      ```python
      class Walk(Object, source="walk_list"):
          dog = Attr(str)
          walker = Attr(str)
          hour = Attr(str, hidden=True)
      ```
      {: .model }

      [the walks](#)
      {: .datagrid source="Walk" #walks }

      [the walk](#)
      {: .form master="walks" #walk_card }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/hidden.md"
    And I wait for the page to be interactive
    Then the grid "walks" has the columns "dog, walker"
    And the form "walk_card" shows no "hour" field

  Scenario: A reference on a database — the walk's dog is picked from the dogs, by name, stored by id
    Michel, 2026-10-17: "should we also add a reference table? For instance
    for dogs? with a picklist in the grid and the proper icons in the column
    title?" — the author seeds the dogs, a walk picks one. The value shows
    plain, a ⌄ opens the dogs ("the picklist is a bit narrow"). And "an
    example of a computed column (@property?)".

    Given a database with the Lightcode setup and no author yet
    And the shelter database holds the dogs "Biscuit" and "Scout", and a walk of "Scout" by "Ben"
    And the GitHub contents API serves "courses/demo/databases.yml" with the document:
      """
      shelter:
        url: https://demo.supabase.co
        key: sb_publishable_yml
      """
    And the GitHub contents API serves "courses/demo/module_06/refs.md" with the document:
      """
      # Walks

      [the shelter](supabase://shelter)
      {: .database #shelter unlisted="5f2c9a01b7e3" }

      ```python
      class Dog(Object):
          '''🐕 A dog of the shelter.'''
          name = Attr(str)

      class Walk(Object):
          dog = Attr(Dog)
          walker = Attr(str)

          @property
          def who(self):
              return (self.dog.name if self.dog else "?") + " & " + self.walker
      ```
      {: .model source="shelter" }

      [the walks](#)
      {: .datagrid source="Walk" #walks }

      [the walk](#)
      {: .form master="walks" #walk_card }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/refs.md"
    And I wait for the page to be interactive
    Then the walk of "Ben" in "walks" names the dog "Scout", among "Biscuit, Scout"
    And the column "dog" of "walks" wears "🐕"
    When I pick the dog "Biscuit" for the walk of "Ben" in "walks"
    Then the table "walk" saved the walk of "Ben" with the dog's id 1
    And the form "walk_card" names the dog "Biscuit", never "dog_1"
    And the walk of "Ben" in "walks" shows "Biscuit & Ben" in its computed "who" column, read-only
    When I delete the walk by "Ben" in "walks", reading the question
    Then the question was "Delete this Walk: Biscuit · Ben · Biscuit & Ben?"
    And the table "walk" has no column "who"

  Scenario: A property with a setter is a column you edit — the setter writes the real attributes
    Michel, 2026-10-17: "what is happening if a property has a setter? Will
    it still work in a column to be updated in a grid?" — "go setter". A
    property alone stays read-only; with a setter its cell opens, the typed
    value goes through the setter, and only the real attributes are saved.

    Given a database with the Lightcode setup and no author yet
    And I am the shelter's author on this device
    And the shelter's "walk" table holds a walk by "Ben" at "9:00"
    And the GitHub contents API serves "courses/demo/databases.yml" with the document:
      """
      shelter:
        url: https://demo.supabase.co
        key: sb_publishable_yml
      """
    And the GitHub contents API serves "courses/demo/module_06/slots.md" with the document:
      """
      # Walks

      [the shelter](supabase://shelter)
      {: .database #shelter unlisted="5f2c9a01b7e3" }

      ```python
      class Walk(Object):
          walker = Attr(str)
          hour = Attr(str)

          @property
          def slot(self):
              return self.walker + " at " + self.hour

          @slot.setter
          def slot(self, text):
              self.walker, _, self.hour = str(text).partition(" at ")
      ```
      {: .model source="shelter" }

      [the walks](#)
      {: .datagrid source="Walk" #walks }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/slots.md"
    And I wait for the page to be interactive
    And I double click the "slot" cell of "Ben" in "walks" and type "Ana at 10:30"
    Then the table "walk" holds a walk by "Ana" at "10:30", and no "slot" column

  Scenario: A setter under another name leaves the column read-only, and says how to name it
    Michel, 2026-10-18, editing Who from the grid: "'Walk' object has no
    attribute 'who'" — his setter was def setwho under @who.setter, which
    Python makes a second property; who stayed read-only, yet its cells
    opened. They stay closed now, and the grid says how to name it.

    Given a database with the Lightcode setup and no author yet
    And I am the shelter's author on this device
    And the shelter's "walk" table holds a walk by "Ben" at "9:00"
    And the GitHub contents API serves "courses/demo/databases.yml" with the document:
      """
      shelter:
        url: https://demo.supabase.co
        key: sb_publishable_yml
      """
    And the GitHub contents API serves "courses/demo/module_06/badset.md" with the document:
      """
      # Walks

      [the shelter](supabase://shelter)
      {: .database #shelter unlisted="5f2c9a01b7e3" }

      ```python
      class Walk(Object):
          walker = Attr(str)
          hour = Attr(str)

          @property
          def who(self):
              return self.walker + " at " + self.hour

          @who.setter
          def setwho(self, value):
              self.walker = value
      ```
      {: .model source="shelter" }

      [the walks](#)
      {: .datagrid source="Walk" #walks }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/badset.md"
    And I wait for the page to be interactive
    Then the "who" cells of "walks" stay closed, and the grid says "who stays read-only: its setter is named setwho"

  Scenario: A column made while its attribute was text follows the class to a number
    Michel, 2026-10-18: "Refresh in a grid should also check the attribute
    types and operate the refactoring… laps was a str for a second before I
    made it int" — run() said "unsupported types for __add__: 'str', 'int'".
    The author's table retypes the column (a blank becomes none, a value
    that does not convert is named); a blank number reads as its default.

    Given a database with the Lightcode setup and no author yet
    And I am the shelter's author on this device
    And the shelter's "walk" table holds a text "laps" column, blank for "Sp" and "3" for "Ann"
    And the GitHub contents API serves "courses/demo/databases.yml" with the document:
      """
      shelter:
        url: https://demo.supabase.co
        key: sb_publishable_yml
      """
    And the GitHub contents API serves "courses/demo/module_06/laps.md" with the document:
      """
      # Walks

      [the shelter](supabase://shelter)
      {: .database #shelter unlisted="5f2c9a01b7e3" }

      ```python
      class Walk(Object):
          walker = Attr(str)

      class Sprint(Walk):
          '''🏃 A run with the dog.'''
          laps = Attr(int)

          def run(self):
              self.laps += 1
      ```
      {: .model source="shelter" }

      [the walks](#)
      {: .datagrid source="Walk" #walks }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/laps.md"
    And I wait for the page to be interactive
    Then the table "walk" made "laps" a number: none for "Sp", 3 for "Ann"
    When I run "run" on the walk by "Sp" in "walks"
    Then the table "walk" saved 1 laps for "Sp", and the grid says nothing wrong

  Scenario: A method that fails, pressed in the form, says why under the form
    Michel, 2026-10-18: "and when I click run in the form, there is no
    error message!" — the error went to grids bound to Sprint, and there
    were none: the walks grid is Walk's. It is said under the form, and
    under the base class's grid.

    Given a database with the Lightcode setup and no author yet
    And I am the shelter's author on this device
    And the shelter's "walk" table holds a text "laps" column, blank for "Sp" and "3" for "Ann"
    And the GitHub contents API serves "courses/demo/databases.yml" with the document:
      """
      shelter:
        url: https://demo.supabase.co
        key: sb_publishable_yml
      """
    And the GitHub contents API serves "courses/demo/module_06/fail.md" with the document:
      """
      # Walks

      [the shelter](supabase://shelter)
      {: .database #shelter unlisted="5f2c9a01b7e3" }

      ```python
      class Walk(Object):
          walker = Attr(str)

      class Sprint(Walk):
          '''🏃 A run with the dog.'''
          laps = Attr(int)

          def run(self):
              raise ValueError("too fast for the dog")
      ```
      {: .model source="shelter" }

      [the walks](#)
      {: .datagrid source="Walk" #walks }

      [the walk](#)
      {: .form master="walks" #walk_card }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/fail.md"
    And I wait for the page to be interactive
    And I click the row "Sp" in "walks"
    And I tap "Run" in the form "walk_card"
    Then the form "walk_card" says "too fast for the dog"

  Scenario: A dog picked on another row selects that row first; the form picks from the same list
    Michel, 2026-10-18: "When I click in the grid/dog column on another
    row, that row should be selected first before the picklist is open!" —
    also "In the form, the picklist for dogs is the old style. Why?"

    Given a database with the Lightcode setup and no author yet
    And the shelter database holds the dogs "Biscuit" and "Scout", a walk of "Scout" by "Ben" and one of "Biscuit" by "Ana"
    And the GitHub contents API serves "courses/demo/databases.yml" with the document:
      """
      shelter:
        url: https://demo.supabase.co
        key: sb_publishable_yml
      """
    And the GitHub contents API serves "courses/demo/module_06/pick.md" with the document:
      """
      # Walks

      [the shelter](supabase://shelter)
      {: .database #shelter unlisted="5f2c9a01b7e3" }

      ```python
      class Dog(Object):
          '''🐕 A dog of the shelter.'''
          name = Attr(str)

      class Walk(Object):
          dog = Attr(Dog)
          walker = Attr(str)
      ```
      {: .model source="shelter" }

      [the walks](#)
      {: .datagrid source="Walk" #walks }

      [the walk](#)
      {: .form master="walks" #walk_card }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/pick.md"
    And I wait for the page to be interactive
    And I click the row "Ana" in "walks"
    And I tap the dog of "Ben" in "walks"
    Then the row of "Ben" is selected in "walks" and the dogs are offered
    When I pick "Scout" in the open list
    Then the form "walk_card" shows "Ben"
    When I pick the dog "Biscuit" in the form "walk_card", from the same list as the grid's
    Then the table "walk" saved the walk of "Ben" with the dog's id 1

  Scenario: A table follows its class safely — a rename keeps its data, a leftover hides, 🧹 drops it
    Michel, 2026-10-17 (register P5): "what happens if an attribute is
    renamed? deleted? would that change the table's structure?" — never
    while typing; never dropped unasked; was= renames; 🧹 for the author.

    Given a database with the Lightcode setup and no author yet
    And I am the shelter's author on this device
    And the shelter database holds a "walk" table with an old "km" column, and "Biscuit" walked by "Ana"
    And the GitHub contents API serves "courses/demo/databases.yml" with the document:
      """
      shelter:
        url: https://demo.supabase.co
        key: sb_publishable_yml
      """
    And the GitHub contents API serves "courses/demo/module_06/tidy.md" with the document:
      """
      # Walks

      [the shelter](supabase://shelter)
      {: .database #shelter unlisted="5f2c9a01b7e3" }

      ```python
      class Walk(Object):
          dog = Attr(str)
          by = Attr(str, was="walker")
      ```
      {: .model source="shelter" }

      [the walks](#)
      {: .datagrid source="Walk" #walks }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/tidy.md"
    And I wait for the page to be interactive
    Then the table "walk" renamed "walker" to "by", keeping "Ana"
    And the grid "walks" has the columns "dog, by"
    And the corner of "walks" offers 🧹 for "km"
    When I tidy the table under "walks", confirming
    Then the table "walk" has no column "km", and no 🧹 is left under "walks"

  Scenario: A model's source= names a list or a database — one word
    Michel, 2026-10-17 (register P6): ".model should have 'source' as knob
    for db or dataset — more polymorphic, while reducing the cognitive load."

    Given the GitHub contents API serves "courses/demo/module_06/one_list.md" with the document:
      """
      # Walks

      ```csv
      dog,walker
      Lucky,Ana
      Fern,Ben
      ```
      {: .dataset #walk_list }

      ```python
      class Walk(Object):
          dog = Attr(str)
          walker = Attr(str)
      ```
      {: .model source="walk_list" #one_model }

      [the walks](#)
      {: .datagrid source="Walk" #walks }

      ```python
      class Dog(Object):
          name = Attr(str)

      class Walker(Object):
          name = Attr(str)
      ```
      {: .model source="walk_list" #two_model }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/one_list.md"
    And I wait for the page to be interactive
    Then the grid "walks" has the columns "dog, walker"
    And the grid "walks" shows "Lucky" and "Fern"
    And the model "two_model" asks which class wears "walk_list"

  Scenario: A new Sprint saves with its class — and a refused save says why, under the grid
    Michel, 2026-10-17: "2 new rows. A walk and a sprint. They are not
    saved. And refreshing would make them disappear" — the reason sat in
    the ⚠'s tooltip, which an iPad never shows. A refusal is now said
    under the grid; a blank cell goes to the table as null, never as ""
    (a number column refuses ""), and 🧹 never offers to drop a
    subclass's own column.

    Given a database with the Lightcode setup and no author yet
    And I am the shelter's author on this device
    And the GitHub contents API serves "courses/demo/databases.yml" with the document:
      """
      shelter:
        url: https://demo.supabase.co
        key: sb_publishable_yml
      """
    And the GitHub contents API serves "courses/demo/module_06/sprints.md" with the document:
      """
      # Walks

      [the shelter](supabase://shelter)
      {: .database #shelter unlisted="5f2c9a01b7e3" }

      ```python
      class Walk(Object):
          dog = Attr(str)
          walker = Attr(str)

      class Sprint(Walk):
          '''🏃 A run with the dog.'''
          speed = Attr(int)
      ```
      {: .model source="shelter" }

      [the walks](#)
      {: .datagrid source="Walk" #walks }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/sprints.md"
    And I wait for the page to be interactive
    And I add a "Sprint" with New under "walks"
    And I type "Max", the cell still open
    And I press "Enter"
    Then the table "walk" holds a "Sprint" of "Max"
    And the corner of "walks" says saved
    # the Sprint's speed is its own column, never a leftover to drop
    And the corner of "walks" offers no 🧹
    When the database refuses the next save with "no list by that name"
    And I add a "Walk" with New under "walks"
    And I type "Rex", the cell still open
    And I press "Enter"
    Then the grid "walks" says "not saved: no list by that name" under it, no hover needed

  Scenario: A subclass's rows keep their class in _sub — a renamed class takes its rows along, 🧹 clears the stale
    Michel, 2026-10-17: "we DO have a problem with inheritance: rows are
    twice! So maybe we need a _classname, including to be cleaned when the
    class is renamed" — both: a was= on the renamed class, and the 🧹. Then:
    "_sub, empty for the base class"; "the subclass icon in the grid's
    gutter for the instances of subclasses", still opening the methods.

    Given a database with the Lightcode setup and no author yet
    And I am the shelter's author on this device
    And the shelter's "walk" table holds a walk, a "Run" and a "Jog"
    And the GitHub contents API serves "courses/demo/databases.yml" with the document:
      """
      shelter:
        url: https://demo.supabase.co
        key: sb_publishable_yml
      """
    And the GitHub contents API serves "courses/demo/module_06/kinds.md" with the document:
      """
      # Walks

      [the shelter](supabase://shelter)
      {: .database #shelter unlisted="5f2c9a01b7e3" }

      ```python
      class Walk(Object):
          dog = Attr(str)
          walker = Attr(str)

      class Sprint(Walk):
          '''🏃 A run with the dog.'''
          was = "Run"
      ```
      {: .model source="shelter" }

      [the walks](#)
      {: .datagrid source="Walk" #walks }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_06/kinds.md"
    And I wait for the page to be interactive
    Then the walk by "Ben" is a "Sprint" in the grid "walks"
    And the row of "Ben" in "walks" wears "🏃" in its gutter, which opens its verbs
    # a tap in the gutter selects the row first, then opens its verbs (Michel, 2026-10-17)
    When I tap the gutter of "Cleo" in "walks"
    Then the row of "Cleo" is the selection of "walks", its verbs open
    And the table "walk" calls the walk by "Ben" a "Sprint"
    And the walk by "Cleo" is a "Walk" in the grid "walks"
    And the corner of "walks" offers 🧹 for "Jog"
    When I tidy the table under "walks", confirming
    Then the table "walk" calls the walk by "Cleo" by no class
    And the table "walk" holds "Lucky" once
