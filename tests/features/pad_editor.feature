Feature: The pad types like a text field, painted
  Michel, 2026-10-08: colours in the pad's source so learners match the
  components — and the colours must not cost undo: a run of typing is one
  ⌘Z, as in the run editor (the mirror is patched, not rebuilt, per key).

  Background:
    Given I have a clean browser page
    When I navigate to "/components/text"
    And I wait for the page to be interactive
    And I wait for the selector "[data-lc-id='playground'] .lc-mdpad-in"

  Scenario: Ctrl+Space after a class offers that component's knobs — live on the database line
    Michel, 2026-10-20: "check the ctrl-space in the editor to offer the right
    knobs in the right components. For instance, live should be offered in
    database, right?" — the knobs ride the registry, one list for the pad's
    completion, the x-ray and the editor; the three lines that had none
    (database, server, diagram) have theirs.

    When I type "\n[the shelter](supabase://shelter)\n{: .database " at the end of the "playground" pad
    Then completion in the "playground" pad after "{: .database " offers "beside, live, unlisted"
    When I type "\n{: .mdpad " at the end of the "playground" pad
    Then completion in the "playground" pad after "{: .mdpad " offers "beside, comment, decorations, demo, folded, layout, numbers, piano, replay, rows, save"
    When I type "\n{: .datagrid " at the end of the "playground" pad
    Then completion in the "playground" pad after "{: .datagrid " offers "autocomplete, beside, columns, editable, empty, filter, format, height, hints, master, save, sort, source, title"
    When I type "\n{: .server " at the end of the "playground" pad
    Then completion in the "playground" pad after "{: .server " offers "beside, model"

  Scenario: A run of typing undoes as one, and the mirror follows the text
    When I type "  # hello" at the end of the "playground" pad
    Then the "playground" pad ends with "  # hello"
    And the "playground" pad's mirror shows "# hello"
    When I undo in the "playground" pad
    Then the "playground" pad does not contain "# hello"
    And the "playground" pad's mirror does not show "# hello"

  Scenario: ⇥ hides the editor, ✎ brings it back — small pills, 🔍 only while editing
    Michel, 2026-10-11: "Hide/Edit are displayed on top of the text. They
    should be more like an icon on a semi-transparent small pill", and the
    search button "visible only when the cursor is in the editor".

    Michel, 2026-10-09, on the phone: "a small button to fold the editor so we
    can see the whole width of the preview side, and (un)fold".

    Then the "playground" pad shows no 🔍 pill
    When I put the caret at the start of the "playground" pad
    Then the "playground" pad shows its 🔍 pill
    When I press "⇥" on the "playground" pad
    Then the "playground" pad's source is folded away
    And the "playground" pad's preview spans the pad
    And the "playground" pad shows no splitter
    # no editor, nothing to explain (Michel, 2026-10-18: "no need to show the ? button")
    And the "playground" pad shows no ? pill, even hovered
    When I press "✎" on the "playground" pad
    Then the "playground" pad's source is shown again
    And the "playground" pad's splitter is back

  Scenario: ⇥ slides the preview over a still editor; ✎ slides it back
    Michel, 2026-10-17 (register P1), after a regression nothing caught: "the
    right edge of the editor stays still, while the left side slides to the
    RIGHT to join the right edge, covering the md and bringing the preview on
    top. Uncovering does the opposite, revealing the md." Measured during the
    slide, not only at its end.

    When I fold the "playground" pad, watching it slide
    Then the editor stood still while the preview's right edge swept over it, left to right
    When I unfold the "playground" pad, watching it slide
    Then the editor stood still while the preview's right edge swept back, right to left

  Scenario: A pad's seed keeps its decorations glued to their lines in the runner
    Michel, 2026-10-09: the runner put a blank line above every decoration,
    fences included, so a pad opened with a gap the lesson never had, and a
    learner copying that shape left a datagrid's decoration alone — it landed
    on the query above and the query vanished. Fences are verbatim now.

    Given the GitHub contents API serves "courses/demo/module_05/glued.md" with the document:
      """
      # Glued

      `````markdown
      # App

      ```
      family,dog
      Kaur,Scout
      ```
      {: .dataset #families }

      [Families](#)
      {: .datagrid source="families" }
      `````
      {: .mdpad #glued decorations="true" rows="10" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_05/glued.md"
    And I wait for the page to be interactive
    Then the "glued" pad's text keeps every decoration glued to its line

  Scenario: A decoration's line wears its component's icon in the gutter
    Michel, 2026-10-10: "to see the decoration's component emoji in the
    gutter: 🛢️ for dataset". The icons are the component model's, the ones
    the x-ray and the editor show; a decoration that names no component
    (an id alone) wears none.

    Given the GitHub contents API serves "courses/demo/module_04/icons.md" with the document:
      """
      # Icons

      `````markdown
      # App
      {: #top }

      ```
      family,dog
      Kaur,Scout
      ```
      {: .dataset #families }

      [Families](#)
      {: .datagrid #fam_grid source="families" }

      [The family](#)
      {: .form master="fam_grid" }
      `````
      {: .mdpad #icons decorations="true" rows="14" numbers="true" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_04/icons.md"
    And I wait for the page to be interactive
    Then the "icons" pad's gutter shows "🛢️" on line 8, "▦" on line 11 and "☷" on line 14
    And the "icons" pad's gutter shows no icon on line 2
    And the "icons" pad paints the dataset's columns in turns

  Scenario: A copy saved with the old gaps opens glued, ready to save
    Michel, 2026-10-10: "no useless empty lines before decorations" (modules
    4 and 5). Pads saved before the 2026-10-09 runner fix kept the gap above
    every decoration, and a gap moves a decoration onto the next block. A
    decorated pad glues them back on load, outside fences; the text differs
    from the saved one, so 💾 offers to keep it.

    Given a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/faces.md" with the document:
      """
      # Faces

      `````markdown
      # Meet a dog
      `````
      {: .mdpad #faces decorations="true" save="faces.md" rows="12" }
      """
    And a connected bench whose "courses/demo/mod/faces.md" holds the document
      """
      # Meet a dog

      [dogs](dogs.yaml)

      {: .dataset #dogs }

      [The dogs](#)


      {: .datagrid #dog_grid source="dogs" }

      ```markdown
      [kept](#)

      {: .verbatim }
      ```
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/faces.md"
    And I wait for the page to be interactive
    Then the pad is marked as the reader's own
    And the "faces" pad's text keeps every decoration glued to its line, fences aside

  Scenario: The pad's grip resizes it for the visit, and a double-click gives the height back
    Michel, 2026-10-10: "a non persistent way to be resized vertically (by
    drag & drop), so, during work or demos we can decide different layouts".

    When I drag the "playground" pad's grip 150px down
    Then the "playground" pad's editor and preview grew by about 150px
    When I drag the "playground" pad's grip 300px up
    Then the "playground" pad's editor and preview are shorter than at first
    When I double-click the "playground" pad's grip
    Then the "playground" pad is back to its own height

  Scenario: The caret on an id lights every wire that names it
    Michel, 2026-10-11: "highlight all occurrences of an id when the cursor is
    there (prefixed by # or inside quotes or even inside a sql from/join
    clause) so learners can see the wires faster". A word that is only prose
    lights nothing.

    Given the GitHub contents API serves "courses/demo/module_05/wires.md" with the document:
      """
      # Wires

      `````markdown
      # Dogs per campus

      ```
      name,campus
      Lucky,Milwaukee
      ```
      {: .dataset #dogs }

      ```sql
      SELECT campus, COUNT(*) AS dogs FROM dogs GROUP BY campus
      ```
      {: .query bind="dogs" #by_campus }

      [The dogs](#)
      {: .datagrid #dog_grid source="dogs" }

      [The dog](#)
      {: .form master="dog_grid" }
      `````
      {: .mdpad #wires decorations="true" rows="20" numbers="true" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_05/wires.md"
    And I wait for the page to be interactive
    And I put the caret in "dogs" of 'source="dogs"' in the "wires" pad
    Then the "wires" pad lights 4 wires of "dogs"
    When I put the caret in "dog_grid" of 'master="dog_grid"' in the "wires" pad
    Then the "wires" pad lights 2 wires of "dog_grid"
    When I put the caret in "campus" of 'Dogs per campus' in the "wires" pad
    Then the "wires" pad lights no wire

  Scenario: Side by side, the splitter shares the width for the visit; a double-click gives the halves back
    Michel, 2026-10-11: "a resizable splitter between preview and editor,
    similar to the vertical one".

    When I drag the "playground" pad's splitter 120px to the right
    Then the "playground" pad's preview grew by about 120px
    When I double-click the "playground" pad's splitter
    Then the "playground" pad's preview is back to its own width

  Scenario: ⌘F floats a finder; ↓ and ↑ walk the matches, Esc leaves the caret there
    Michel, 2026-10-11: "a find function in the editor, with a floating
    finder, and up/down arrows helping to find the values".

    When I press ⌘F in the "playground" pad and look for "bullet"
    Then the "playground" pad's finder counts more than 1 match
    And the "playground" pad's mirror lights the current match
    When I press ↓ in the "playground" pad's finder
    Then the "playground" pad's finder is on match 2
    When I press ↑ in the "playground" pad's finder
    Then the "playground" pad's finder is on match 1
    When I press Escape in the "playground" pad's finder
    Then the "playground" pad's finder is gone
    And the "playground" pad's selection reads "bullet"

  Scenario: ⌘-click on a wire jumps to its id; on the id, it walks the uses
    Michel, 2026-10-11: "ctrl-click on an id ref to jump to the id".

    Given the GitHub contents API serves "courses/demo/module_05/wires.md" with the document:
      """
      # Wires

      `````markdown
      # Dogs per campus

      ```
      name,campus
      Lucky,Milwaukee
      ```
      {: .dataset #dogs }

      ```sql
      SELECT campus, COUNT(*) AS dogs FROM dogs GROUP BY campus
      ```
      {: .query bind="dogs" #by_campus }

      [The dogs](#)
      {: .datagrid #dog_grid source="dogs" }

      [The dog](#)
      {: .form master="dog_grid" }
      `````
      {: .mdpad #wires decorations="true" rows="20" numbers="true" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_05/wires.md"
    And I wait for the page to be interactive
    And I put the caret in "dogs" of 'source="dogs"' in the "wires" pad
    And I ⌘-click the caret in the "wires" pad
    Then the "wires" pad selects "dogs" on the line "{: .dataset #dogs }"
    When I ⌘-click the caret in the "wires" pad
    Then the "wires" pad selects "dogs" on the line "SELECT campus, COUNT(*) AS dogs FROM dogs GROUP BY campus"

  Scenario: F2 renames an id in every wire, prose untouched, one undo
    Michel, 2026-10-11: "a refactor/rename of an ID with propagation to
    other usages".

    Given the GitHub contents API serves "courses/demo/module_05/wires.md" with the document:
      """
      # Wires

      `````markdown
      # Dogs per campus

      ```
      name,campus
      Lucky,Milwaukee
      ```
      {: .dataset #dogs }

      ```sql
      SELECT campus, COUNT(*) AS dogs FROM dogs GROUP BY campus
      ```
      {: .query bind="dogs" #by_campus }

      [The dogs](#)
      {: .datagrid #dog_grid source="dogs" }

      [The dog](#)
      {: .form master="dog_grid" }
      `````
      {: .mdpad #wires decorations="true" rows="20" numbers="true" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_05/wires.md"
    And I wait for the page to be interactive
    And I put the caret in "dogs" of '#dogs' in the "wires" pad
    And I rename it to "pets" with F2 in the "wires" pad
    Then the "wires" pad holds "#pets", 'bind="pets"', "FROM pets" and 'source="pets"'
    And the "wires" pad holds "AS dogs"
    And the "wires" pad does not contain "#dogs"
    When I undo in the "wires" pad
    Then the "wires" pad holds "#dogs", 'bind="dogs"', "FROM dogs" and 'source="dogs"'
    When I put the caret in "dogs" of '#dogs' in the "wires" pad
    And I try F2 to "dog_grid" in the "wires" pad
    Then the "wires" pad's rename box says "#dog_grid is taken"

  Scenario: ⌥↓ and ⌥↑ move a whole block; ⌃⌥→ puts it beside the one above, ⌃⌥← takes it out
    Michel, 2026-10-11: "shortcuts to move/jump up/down (reverse order) and
    another to put it beside next/previous" — for all blocks.

    Given the GitHub contents API serves "courses/demo/module_05/wires.md" with the document:
      """
      # Wires

      `````markdown
      # Dogs per campus

      ```
      name,campus
      Lucky,Milwaukee
      ```
      {: .dataset #dogs }

      ```sql
      SELECT campus, COUNT(*) AS dogs FROM dogs GROUP BY campus
      ```
      {: .query bind="dogs" #by_campus }

      [The dogs](#)
      {: .datagrid #dog_grid source="dogs" }

      [The dog](#)
      {: .form master="dog_grid" }
      `````
      {: .mdpad #wires decorations="true" rows="20" numbers="true" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_05/wires.md"
    And I wait for the page to be interactive
    And I put the caret in "by_campus" of '#by_campus' in the "wires" pad
    And I press "Alt+ArrowDown" in the "wires" pad
    Then in the "wires" pad "#dog_grid" comes before "#by_campus"
    And the "wires" pad's caret is still in "#by_campus"
    When I press "Alt+ArrowUp" in the "wires" pad
    Then in the "wires" pad "#by_campus" comes before "#dog_grid"
    When I put the caret in "dog_grid" of 'master="dog_grid"' in the "wires" pad
    And I press "Control+Alt+ArrowRight" in the "wires" pad
    Then the "wires" pad holds '{: .form master="dog_grid" beside="true" }'
    When I press "Control+Alt+ArrowLeft" in the "wires" pad
    Then the "wires" pad holds '{: .form master="dog_grid" }'

  Scenario: On an empty line, a part completes; Tab flies over its blanks, each offering what fits
    Michel, 2026-10-11: "if it's an empty line and I start typing 'for', it
    should propose a {: .form }, and suggest with tabs to fly over all the
    sections". The part is the catalogue's; the ids offered are the pad's.

    Given the GitHub contents API serves "courses/demo/module_05/wires.md" with the document:
      """
      # Wires

      `````markdown
      # Dogs per campus

      ```
      name,campus
      Lucky,Milwaukee
      ```
      {: .dataset #dogs }

      ```sql
      SELECT campus, COUNT(*) AS dogs FROM dogs GROUP BY campus
      ```
      {: .query bind="dogs" #by_campus }

      [The dogs](#)
      {: .datagrid #dog_grid source="dogs" }

      [The dog](#)
      {: .form master="dog_grid" }
      `````
      {: .mdpad #wires decorations="true" rows="20" numbers="true" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_05/wires.md"
    And I wait for the page to be interactive
    And I type "fo" on a new line at the end of the "wires" pad
    Then the "wires" pad offers "form" first
    When I accept the offer in the "wires" pad
    Then the "wires" pad selects "Title"
    When I press "Tab" in the "wires" pad
    Then the "wires" pad selects "TODO_YOUR_GRID"
    And the "wires" pad offers "dog_grid" first
    When I accept the offer in the "wires" pad
    Then the "wires" pad holds '{: .form master="dog_grid" }'

  Scenario: Once the caret leaves a part, Tab in a fence indents — it no longer flies to the part's blanks
    Michel, 2026-10-18: "When I'm in the python code, a tab should add 4
    spaces, not jump to the next knob… Fences should behave differently!"
    — a form part inserted earlier kept its blanks for Tab, wherever the
    caret went next.

    Given the GitHub contents API serves "courses/demo/module_05/wires.md" with the document:
      """
      # Wires

      ```sql
      SELECT campus, COUNT(*) AS dogs FROM dogs GROUP BY campus
      ```
      {: .query bind="dogs" #by_campus }

      `````markdown
      # Dogs per campus

      ```
      name,campus
      Lucky,Milwaukee
      ```
      {: .dataset #dogs }

      ```sql
      SELECT campus, COUNT(*) AS dogs FROM dogs GROUP BY campus
      ```
      {: .query bind="dogs" #by_campus }

      [The dogs](#)
      {: .datagrid #dog_grid source="dogs" }
      `````
      {: .mdpad #wires decorations="true" rows="20" numbers="true" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_05/wires.md"
    And I wait for the page to be interactive
    And I type "fo" on a new line at the end of the "wires" pad
    And I accept the offer in the "wires" pad
    Then the "wires" pad selects "Title"
    When I click at the start of "SELECT campus" in the "wires" pad and press Tab
    Then the "wires" pad indented "SELECT campus" by four spaces, nothing selected

  Scenario: In a decoration, the class, its knobs and their values complete
    Michel, 2026-10-11: "for component type names, for attribute names, for
    values inside knobs, with picklist" — and a source offers the pad's
    datasets, an x the source's columns.

    Given the GitHub contents API serves "courses/demo/module_05/wires.md" with the document:
      """
      # Wires

      `````markdown
      # Dogs per campus

      ```
      name,campus
      Lucky,Milwaukee
      ```
      {: .dataset #dogs }

      ```sql
      SELECT campus, COUNT(*) AS dogs FROM dogs GROUP BY campus
      ```
      {: .query bind="dogs" #by_campus }

      [The dogs](#)
      {: .datagrid #dog_grid source="dogs" }

      [The dog](#)
      {: .form master="dog_grid" }
      `````
      {: .mdpad #wires decorations="true" rows="20" numbers="true" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_05/wires.md"
    And I wait for the page to be interactive
    And I type "{: .ch" on a new line at the end of the "wires" pad
    Then the "wires" pad offers "chart" first
    When I accept the offer in the "wires" pad
    And I type "sou" in the "wires" pad
    Then the "wires" pad offers "source" first
    When I accept the offer in the "wires" pad
    Then the "wires" pad offers "dogs" and "by_campus"
    When I accept the offer in the "wires" pad
    And I type " x" in the "wires" pad
    And I accept the offer in the "wires" pad
    Then the "wires" pad offers "name" and "campus"
    When I accept the offer in the "wires" pad
    Then the "wires" pad holds '{: .chart source="dogs" x="name"}'

  Scenario: The caret in a part the page does not show marks where it sits
    Michel, 2026-10-11: "an horizontal line with a short semi-transparent
    caption saying '🛢️ Dataset (invisible)'".

    Given the GitHub contents API serves "courses/demo/module_05/wires.md" with the document:
      """
      # Wires

      `````markdown
      # Dogs per campus

      ```
      name,campus
      Lucky,Milwaukee
      ```
      {: .dataset #dogs }

      ```sql
      SELECT campus, COUNT(*) AS dogs FROM dogs GROUP BY campus
      ```
      {: .query bind="dogs" #by_campus }

      [The dogs](#)
      {: .datagrid #dog_grid source="dogs" }

      [The dog](#)
      {: .form master="dog_grid" }
      `````
      {: .mdpad #wires decorations="true" rows="20" numbers="true" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_05/wires.md"
    And I wait for the page to be interactive
    And I put the caret in "Lucky" of 'Lucky,Milwaukee' in the "wires" pad
    Then the "wires" pad's preview marks "🛢️ Dataset (invisible)"

  Scenario: ? lists what the editor can do
    Michel, 2026-10-11: "a small help button to list all the features".

    When I press the "playground" pad's ? pill
    Then the "playground" pad's help mentions "F2" and "complete"

  Scenario: Tab walks what can be customized, like a form; in a fence it indents; Esc then Tab leaves
    Michel, 2026-10-12: "unless the cursor is in a fence, tab should jump
    between knobs and ids, just like in a form … and the class names too,
    everything that can be customized".

    Given the GitHub contents API serves "courses/demo/module_05/wires.md" with the document:
      """
      # Wires

      `````markdown
      # Dogs per campus

      ```
      name,campus
      Lucky,Milwaukee
      ```
      {: .dataset #dogs }

      ```sql
      SELECT campus, COUNT(*) AS dogs FROM dogs GROUP BY campus
      ```
      {: .query bind="dogs" #by_campus }

      [The dogs](#)
      {: .datagrid #dog_grid source="dogs" }

      [The dog](#)
      {: .form master="dog_grid" }
      `````
      {: .mdpad #wires decorations="true" rows="20" numbers="true" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_05/wires.md"
    And I wait for the page to be interactive
    And I put the caret at the start of the "wires" pad
    And I press "Tab" in the "wires" pad
    Then the "wires" pad selects "dataset"
    When I press "Escape" in the "wires" pad
    And I put the caret at the start of the "wires" pad
    And I press "Tab" in the "wires" pad
    And I press "Tab" in the "wires" pad
    Then the "wires" pad selects "dogs"
    When I press "Tab" in the "wires" pad
    Then the "wires" pad selects "query"
    When I press "Tab" in the "wires" pad
    Then the "wires" pad selects "dogs"
    And the "wires" pad offers "dogs" and "by_campus"
    When I press "Tab" in the "wires" pad
    Then the "wires" pad selects "by_campus"
    When I press "Tab" in the "wires" pad
    Then the "wires" pad selects "The dogs"
    When I press "Shift+Tab" in the "wires" pad
    Then the "wires" pad selects "by_campus"
    When I put the caret at the start of the line holding "SELECT campus" in the "wires" pad
    And I press "Tab" in the "wires" pad
    Then the "wires" pad holds "    SELECT campus"
    When I press "Shift+Tab" in the "wires" pad
    Then the "wires" pad does not contain "    SELECT campus"
    When I press "Escape" in the "wires" pad
    And I press "Tab" in the "wires" pad
    Then the "wires" pad's editor has let the focus go

  Scenario: Hovering a decoration's icon for a second names the component
    Michel, 2026-10-11: "hovering the gutter should show the component type
    (emoji and type name) after one second in a tooltip".

    Given the GitHub contents API serves "courses/demo/module_05/tip.md" with the document:
      """
      # Tip

      `````markdown
      # App

      ```csv
      family,dog
      Kaur,Scout
      ```
      {: .dataset #families }

      [Families](#)
      {: .datagrid source="families" }
      `````
      {: .mdpad #tip decorations="true" rows="12" numbers="true" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_05/tip.md"
    And I wait for the page to be interactive
    And I rest the pointer on the gutter of line 10 in the "tip" pad
    Then after a second the "tip" pad's gutter says "▦ datagrid"

  Scenario: A saved copy longer than the starter still lights its current block
    Michel, 2026-10-11: the blue bar "works well in some cases but not in
    others" — the blocks were mapped from the lesson's starter, so a saved
    copy's later blocks never lit.

    Given the GitHub contents API serves "courses/demo/mod/longer.md" with the document:
      """
      # Longer

      `````markdown
      # Meet a dog
      `````
      {: .mdpad #longer decorations="true" save="longer.md" rows="12" numbers="true" }
      """
    And a connected bench whose "courses/demo/mod/longer.md" holds the document
      """
      # Meet a dog

      [The dogs](#)
      {: .datagrid #grid source="dogs" }

      [The dog](#)
      {: .form master="grid" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/longer.md"
    And I wait for the page to be interactive
    And I put the caret in "form" of '.form master' in the "longer" pad
    Then the "longer" pad's current block holds "[The dog](#)" and ".form"

  Scenario: In a cell, the ids complete, then what each one offers; Tab lands on its name; a sentence stands beside too
    Michel, 2026-10-13: "the tab shortcut or code completion doesn't work
    there for cell expressions" — and ⌃⌥→ on the cell's sentence said
    "Beside needs a decoration" in red.

    Given the GitHub contents API serves "courses/demo/module_05/cells.md" with the document:
      """
      # Cells

      `````markdown
      # Calls

      ```
      family,met
      Nguyen,
      Alvarez,Wed
      ```
      {: .dataset #reservations }

      ```sql
      SELECT family FROM reservations WHERE met = ""
      ```
      {: .query bind="reservations" #to_call }

      [Families](#)
      {: .datagrid #call_list source="reservations" }
      `````
      {: .mdpad #cells decorations="true" rows="20" numbers="true" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_05/cells.md"
    And I wait for the page to be interactive
    And I type "{= to" on a new line at the end of the "cells" pad
    Then the "cells" pad offers "to_call" first
    When I accept the offer in the "cells" pad
    And I type "." in the "cells" pad
    Then the "cells" pad offers "count" and "empty"
    When I accept the offer in the "cells" pad
    And I type " } families are waiting." in the "cells" pad
    Then the "cells" pad holds "{= to_call.count } families are waiting."
    When I put the caret at the start of the line holding "families are waiting" in the "cells" pad
    And I press "Tab" in the "cells" pad
    Then the "cells" pad selects "to_call"
    When I press "Escape" in the "cells" pad
    And I put the caret at the start of the line holding "families are waiting" in the "cells" pad
    And I press "Control+Alt+ArrowRight" in the "cells" pad
    Then the "cells" pad holds '{: beside="true" }'
    When I press "Control+Alt+ArrowLeft" in the "cells" pad
    Then the "cells" pad does not contain "beside"
