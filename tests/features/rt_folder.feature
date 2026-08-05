Feature: Folder shelf — read posture and X-ray workbench
  The .folder component has two postures. READ (default): the listing minus
  every writing affordance — no ➕ New, underscore files hidden. X-RAY (the
  mode): the shelf becomes a workbench — ➕ New returns, every file shows,
  and each file card grows a ⚙️ menu with rename / move / trash. Trash is a
  move into _trash/ with a _deleted_<timestamp> suffix — recoverable.

  Scenario: Read posture lists pages with no writing affordances
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key is connected
    And the folder "courses/demo/mod" serves pages "alpha.md,_hidden.md"
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Shelf page

      [Browse](#)
      {: .folder }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    Then the shelf shows a card for "Alpha"
    And the shelf hides "Hidden" and every writing affordance

  Scenario: X-ray turns the shelf into a workbench
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key is connected
    And the viewer can push to the repo
    And the folder "courses/demo/mod" serves pages "alpha.md,_hidden.md"
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Shelf page

      [Browse](#)
      {: .folder }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    And the page enters X-ray mode
    Then the shelf shows a card for "Hidden"
    And the shelf offers New and a gear on each file card

  Scenario: Trash moves the file into _trash with a deleted-suffix name
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key is connected
    And the viewer can push to the repo
    And the folder "courses/demo/mod" serves pages "alpha.md,_hidden.md"
    And the folder file "courses/demo/mod/alpha.md" accepts moves
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Shelf page

      [Browse](#)
      {: .folder }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    And the page enters X-ray mode
    And I trash the "Alpha" card
    Then the file was moved to "courses/demo/mod/_trash/alpha_deleted_"
    And the trash folder was born with its index

  Scenario: An empty shelf speaks the language of its posture
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key is connected
    And the viewer can push to the repo
    And the folder "courses/demo/mod" is empty
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Shelf page

      [Browse](#)
      {: .folder }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    Then the empty shelf offers no New button
    When the page enters X-ray mode
    Then the empty shelf offers a New button

  Scenario: X-ray survives a refresh through the URL
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key is connected
    And the viewer can push to the repo
    And the folder "courses/demo/mod" serves pages "alpha.md,_hidden.md"
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Shelf page

      [Browse](#)
      {: .folder }
      """
    When I navigate to "/run.html?xray=1#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    Then the shelf shows a card for "Hidden"
    And the shelf offers New and a gear on each file card

  Scenario: X-ray on someone else's material stays a lens
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key is connected
    And the viewer cannot push to the repo
    And the folder "courses/demo/mod" serves pages "alpha.md,_hidden.md"
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Shelf page

      [Browse](#)
      {: .folder }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    And the page enters X-ray mode
    Then the shelf shows a card for "Alpha"
    And the shelf hides "Hidden" and every writing affordance

  Scenario: A subfolder card counts its files in the workbench
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key is connected
    And the viewer can push to the repo
    And the folder "courses/demo/mod" lists pages "alpha.md" plus subfolder "week1" with files "a.md,_b.md,deep/_c.md,deep/d.md"
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Shelf page

      [Browse](#)
      {: .folder }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    And the page enters X-ray mode
    Then the subfolder card shows the census "2/4"
    And the subfolder card offers a gear

  Scenario: An underscore subfolder hides from readers and shows in the workbench
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key is connected
    And the viewer can push to the repo
    And the folder "courses/demo/mod" lists pages "alpha.md" plus subfolder "_archive" with files "old.md"
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Shelf page

      [Browse](#)
      {: .folder }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    Then the shelf shows a card for "Alpha"
    And the shelf shows no card for "Archive"
    When the page enters X-ray mode
    Then the shelf shows a card for "Archive"

  @mobile
  Scenario: On touch, a tap on the gear opens the menu, not the lens
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key is connected
    And the viewer can push to the repo
    And the folder "courses/demo/mod" serves pages "alpha.md,_hidden.md"
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Shelf page

      [Browse](#)
      {: .folder }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    And the page enters X-ray mode
    And I tap the gear on the "Alpha" card
    Then the card menu is open

  Scenario: Open in the card menu lands in X-ray on the target
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key is connected
    And the viewer can push to the repo
    And the folder "courses/demo/mod" serves pages "alpha.md,_hidden.md"
    And the GitHub contents API serves "courses/demo/mod/alpha.md" with the document:
      """
      # Alpha page
      """
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Shelf page

      [Browse](#)
      {: .folder }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    And the page enters X-ray mode
    And I choose "open" on the "Alpha" card
    Then the page URL carries "xray=1" and "alpha.md"

  Scenario: Move offers the repo's folders as autocomplete and lands the file
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key is connected
    And the viewer can push to the repo
    And the folder "courses/demo/mod" lists pages "alpha.md" plus subfolder "week1" with files "a.md"
    And the folder file "courses/demo/mod/alpha.md" accepts moves
    And moves into "courses/demo/mod/week1" are accepted
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Shelf page

      [Browse](#)
      {: .folder }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    And the page enters X-ray mode
    And I choose "move" on the "Alpha" card
    Then the destination autocomplete offers "courses/demo/mod/week1"
    When I move it to "courses/demo/mod/week1"
    Then the file was moved to "courses/demo/mod/week1/alpha.md"

  Scenario: The course map charts the rendered folder, relative path included
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key is connected
    And course pages serve raw markdown
    And the folder "courses/demo/mod" lists pages "alpha.md" plus subfolder "week1" with files "a.md"
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Map page

      [Browse](.)
      {: .sitemap path="." height="300" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    Then the course map draws at least 2 nodes

  Scenario: A folder card wears its index page's score
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key is connected
    And the folder "courses/demo/mod" lists pages "alpha.md" plus subfolder "week1" with files "index.md"
    And the subfolder "courses/demo/mod/week1" carries an index with one quiz
    And the learner has earned some points on "gh:acme/demo/courses/demo/mod/week1"
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Shelf page

      [Browse](#)
      {: .folder }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    Then the folder card score chip reads "2/3"

  @mobile
  Scenario: On touch, the empty shelf's New button beats the lens
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key is connected
    And the viewer can push to the repo
    And the folder "courses/demo/mod" is empty
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Shelf page

      [Browse](#)
      {: .folder }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    And the page enters X-ray mode
    And I tap the empty shelf's New button
    Then the New dialog opens

  Scenario: Typing a name with .md creates exactly that file
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key is connected
    And the viewer can push to the repo
    And the folder "courses/demo/mod" is empty
    And new files land in "courses/demo/mod"
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Shelf page

      [Browse](#)
      {: .folder }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    And the page enters X-ray mode
    And I create a new page named "notes.md"
    Then the file "courses/demo/mod/notes.md" was created

  Scenario: Cards keep their real titles when a stale raw token 404s
    On a private repo the listing's download_url carries a SHORT-LIVED
    token. Served from cache, those tokens have expired — the raw fetch
    404s and every card silently degrades to its filename with no snippet,
    no tags, no dots: the same folder rendering differently between visits.
    The content must come through the door we are authenticated for.

    Given I have a clean browser page
    And a builder key is connected
    And the folder "courses/demo/mod" lists "01_adoption_day.md" whose raw token is stale
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    Then the shelf shows a card for "Adoption Day"

  Scenario: A subfolder card keeps its title when the raw token has expired
    The page cards were fixed for this; the SUBFOLDER half was missed. Its
    index.md was still read through download_url — an unauthenticated raw
    URL carrying a SHORT-LIVED token. Served from cache the token has aged
    out, the read 404s, so a module card degraded to its directory name
    ("Module 00") with no title, no snippet — differently from one visit to
    the next, which is why it was impossible to reproduce on demand.

    Given a stubbed private repo whose raw tokens have expired
    When I open a shelf listing that repo
    Then the subfolder card shows the index's own title

  Scenario: parent="true" offers the way up, out of the folder
    A reader who finished a module needs to climb one level before they can
    pick the next one, and a list of siblings cannot offer that. The knob is
    opt-in because "up" is not always somewhere useful — at the root it is
    nowhere at all.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key is connected
    And the folder "courses/demo/mod" serves pages "alpha.md"
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Shelf page

      [Browse](#)
      {: .folder parent="true" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    Then the shelf shows a card for "Alpha"
    And a way up to the folder above is offered
    And the way up is not a card in the grid
