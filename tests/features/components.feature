Feature: Component gallery behaviors

  Background:
    Given I have a clean browser page

  Scenario: Selecting a grid row fills the bound form
    When I navigate to "/components/form"
    And I wait for the page to be interactive
    And I click the grid row containing "Wanda"
    Then a form titled "Wanda" is visible

  Scenario: Footnotes inside a fenced component block render
    # kramdown never looks inside a fence, so [^x] refs written in a .block
    # stayed raw AND their page-level definitions were dropped as unreferenced
    # (three of four footnotes vanished from the Build-AI cover). The client
    # pipeline now runs the same footnote pass the runner does, so a block
    # carries its own footnotes — refs and defs together, inside the fence.
    When I navigate to "/courses/build_ai_cover"
    And I wait for the page to be interactive
    Then every footnote on the page resolves

  Scenario: Accordion sections open on click
    When I navigate to "/components/accordion"
    And I wait for the page to be interactive
    And I open the first accordion section
    Then the accordion section body has content

  Scenario: Liquid build-time includes render on the help archive
    When I navigate to "/archive/help"
    And I wait for the page to be interactive
    Then an embedded iframe from "onlineide" is present
    And an embedded iframe from "pythontutor" is present

  Scenario: A bound grid drives a bound-to detail chart
    When I navigate to "/components/dataset"
    And I wait for the page to be interactive
    And I click the bound grid "monthly_grid" row containing "Feb"
    Then the detail chart bound to "monthly_grid" renders a canvas

  Scenario: The markdown pad renders a live preview
    When I navigate to "/components/text"
    And I wait for the page to be interactive
    Then the markdown pad shows an editor and a rendered preview

  Scenario: The custom-class example shows a live Python editor
    When I navigate to "/components/examples/custom-class"
    And I wait for the page to be interactive
    Then a live Python editor is visible

  Scenario: A query aggregates a dataset into a bound grid
    When I navigate to "/components/query"
    And I wait for the page to be interactive
    Then the "by_breed" bound grid shows at least 3 rows

  Scenario: An editable query is a live SQL editor feeding a grid
    When I navigate to "/components/query"
    And I wait for the page to be interactive
    Then a live SQL editor is visible
    And the "live_q" bound grid shows at least 3 rows

  Scenario: Inline IAL colour classes tint text
    When I navigate to "/components/text"
    And I wait for the page to be interactive
    Then a red coloured word is rendered

  Scenario: Colour classes also work in the mdpad live preview
    When I navigate to "/components/text"
    And I wait for the page to be interactive
    Then the mdpad preview shows a red word
    And the mdpad italic text is not coloured

  # The lab and every fork serve under /<repo>/, where a component that injects
  # a root-absolute path ("/assets/lab.jpg") 404s unless the scan pipeline heals
  # it. The suite serves at a domain root, so this drives the real pipeline with
  # a project base forced on. Guards the block/runner base-path regression.
  Scenario: A scanned component's root-absolute media heals under a project base
    When I navigate to "/components/block"
    And I wait for the page to be interactive
    Then a scanned subtree's root-absolute image resolves under the base path

  # End-to-end counterpart: under the base-path harness (BASE_URL .../lightcodelab)
  # the block's injected image must actually download — an unhealed /assets path
  # 404s and this fails. At a domain root it passes trivially (nothing to heal).
  Scenario: The block component's injected image actually loads
    When I navigate to "/components/block"
    And I wait for the page to be interactive
    Then the block component's image is loaded, not broken

  # The lab repo is private, so the GitHub Contents API 404s for anonymous
  # visitors. The gallery must enumerate from the build-time manifest
  # (assets/pages_index.json) with no API call — guards the .folder private-repo
  # regression (the red "HTTP 404" the API path produced on the lab).
  Scenario: The component gallery lists cards without the GitHub API
    When I navigate to "/components"
    And I wait for the page to be interactive
    Then the folder gallery shows at least 20 cards
    And the folder gallery shows no error card

  # Same private-repo fix for the sibling .sitemap graph (the "Component Map").
  Scenario: The sitemap graph builds without the GitHub API
    When I navigate to "/components/sitemap"
    And I wait for the page to be interactive
    Then the sitemap graph shows at least 20 nodes
    And clicking a sitemap node opens its page

  Scenario: A table wired to a name nothing answers to says so, and stops waiting
    An unresolved source= used to wait forever: the bind promise settles on
    the dataset's arrival alone, and nothing timed it out. So the page read
    as still loading rather than as the wiring mistake it is, and the sliver
    of "loading grid…" left almost nothing to aim a thumb at.

    Given a table gives its dataset 800ms to arrive
    And the GitHub contents API serves "courses/demo/wire.md" with the document:
      """
      # Her screen

      ```csv
      campus,dogs_adopted
      Milwaukee,12
      Ozaukee,5
      ```
      {: .dataset #adoptions }

      ```csv
      ```
      {: .datagrid #wired source="ozaukee" height="160" empty="Nothing arrives here yet." }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/wire.md"
    And I wait for the page to be interactive
    Then the waiting table comes to rest on "Nothing arrives here yet."
    And that message is a tappable target

  Scenario: A chart whose source names nothing stops pretending to load
    Michel, 2026-08-05: "it should not show Loading". A chart bound to a part
    that does not exist sat on "⏳ Loading…" for ever, which reads as "the page
    is slow" rather than "this wire is broken" — exactly backwards on the page
    that teaches wiring. The title paints too, so the reader can see what
    SHOULD have been here.

    Given a table gives its dataset 800ms to arrive
    And the GitHub contents API serves "courses/demo/chartwire.md" with the document:
      """
      # Her screen

      ```csv
      name,fee
      Scout,180
      ```
      {: .dataset #dogs }

      ```csv
      ```
      {: .chart #fees type="bar" x="name" y="fee" source="adoptions" height="200" title="💵 Adoption fee, dog by dog" empty="Nothing arrives here yet." }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/chartwire.md"
    And I wait for the page to be interactive
    Then the waiting chart comes to rest on "Nothing arrives here yet."
    And the waiting chart still shows its title

  Scenario: A chart whose source does resolve draws, title and all
    Given the GitHub contents API serves "courses/demo/chartok.md" with the document:
      """
      # Her screen

      ```csv
      name,fee
      Scout,180
      Biscuit,150
      ```
      {: .dataset #dogs }

      ```csv
      ```
      {: .chart #fees type="bar" x="name" y="fee" source="dogs" height="200" title="💵 Adoption fee, dog by dog" empty="Nothing arrives here yet." }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/chartok.md"
    And I wait for the page to be interactive
    Then the chart "fees" has drawn its bars
    And the waiting chart still shows its title

  Scenario: A page wears its own tags beside its title
    # The tags were on the folder card only, so a reader standing ON the page
    # saw nothing. They now ride inside the h1 — decoration, not a new line.
    When I navigate to "/components/build_loop"
    And I wait for the page to be interactive
    Then the page title shows the tags "learn, media, lifecycle"
    And the tags sit inside the page title

  Scenario: A page with no tagged feature keeps a bare title
    When I navigate to "/components/examples/spreadsheet"
    And I wait for the page to be interactive
    Then the page title shows no tags

  Scenario: A QR can carry the page you are on
    Present mode's share button encodes location.href; here="true" gives a
    fenced .qr the same thing, so a page hands out its own address without
    anyone typing a URL (Michel, 2026-08-12).

    When I navigate to "/components/qr"
    And I wait for the page to be interactive
    Then a QR on the page encodes this page's address

  Scenario: An image embed can be a round portrait
    A face on a cover is a portrait, not a poster (Michel, 2026-08-12), and
    a page may not carry CSS of its own — so the roundness is a knob.

    When I navigate to "/components/embed_page"
    And I wait for the page to be interactive
    Then a round image embed is on the page

  Scenario: An inline chart never claims it drew nothing
    The bound chart draws SVG, so a proof counts its rects. An inline chart
    draws the same bars into a canvas — and reported zero, which failed a
    page's own check on a chart everyone could see (Michel, 2026-08-13).

    Given the GitHub contents API serves "courses/demo/mod/cost.md" with the document:
      """
      # Cost

      ```csv
      way,energy
      A rule you wrote,1
      An old prediction,2
      An AI answer,30
      ```
      {: .chart #energy_chart type="bar" x="way" y="energy" height="240" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/cost.md"
    And I wait for the page to be interactive
    Then the chart "energy_chart" reports 3 bars

  Scenario: On paper a page is a document, not a screenshot of an app
    A printed page carries the prose and the evidence; nothing you could
    press belongs on it, and nothing may be folded away — a closed accordion
    prints as a hole (Michel, 2026-08-13: "export all the public pages of a
    module as pdf files").

    Given I have a clean browser page
    When I navigate to "/components/accordion"
    And I wait for the page to be interactive
    And the page is shown as it would print
    Then no button is offered on paper
    And every accordion is open on paper

  Scenario: Columns may be given proportions, not just a count
    Michel, 2026-08-13: "cols=2;1 should mean the first column is twice as
    large as the second". Prose beside a picture or a clip is rarely a
    fifty-fifty page.

    Given I have a clean browser page
    When I navigate to "/components/block"
    And I wait for the page to be interactive
    Then a weighted block splits its width two to one
    And a plain "cols" block still splits evenly

  Scenario: A panel keeps the id its author gave it
    A tour that finds a panel by the words in its summary breaks the day the
    wording changes. `{: .accordion #author }` is an address (Michel,
    2026-08-13: "you can define ids and use them in the avatar's script").

    Given I have a clean browser page
    When I navigate to "/components/accordion"
    And I wait for the page to be interactive
    Then an accordion given an id can be opened by that id

  Scenario: A rule with a label becomes a border that says which register starts
    A page speaks in registers — the lesson, the app, the course's tools.
    A beginner cannot infer a frame nobody gave them (Michel, 2026-08-13),
    so the seam is a thematic break with a name on it: the label is the
    border, the colour only decorates.

    Given I have a clean browser page
    When I navigate to "/components/seam"
    And I wait for the page to be interactive
    Then each seam says its register out loud
    And a seam is still a rule, for a screen reader

  Scenario: A card can wear the register it belongs to
    The seam names a register out loud; tone is the same three worn quietly
    by a card, so a reader who skimmed past the line still feels the change.
    Three values and no more — an unknown word keeps the plain card
    (Michel, 2026-08-14).

    Given I have a clean browser page
    When I navigate to "/components/block"
    And I wait for the page to be interactive
    Then each tone reaches its own cards
    And an unknown tone leaves the card plain
