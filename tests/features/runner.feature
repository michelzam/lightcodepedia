Feature: The instant runner (RT) — Phase A parity

  Renders raw markdown into live components using the same client-side pipeline
  as the editor preview. Behaviour parity with Jekyll, not identical DOM.

  Background:
    Given I have a clean browser page

  Scenario: The /run page renders markdown text from a hash source
    When I open the runner page on "/run_samples/probe.txt"
    And I wait for the runner to render
    Then the runner shows a heading "RT probe page"
    And the runner shows bold text

  Scenario: The runner upgrades a component the way Jekyll does
    When I open the runner page on "/run_samples/probe.txt"
    And I wait for the runner to render
    Then the runner contains a ".lc-block" element
    And the rendered block mentions "Lucky"

  Scenario: A missing source shows a clear message, not a blank page
    When I open the runner page on "/run_samples/does-not-exist.txt"
    Then the runner reports it could not load

  Scenario: A component inside an RT render keeps its editable fence source
    When I open the runner page on "/components/block.md"
    And I wait for the runner to render
    Then a rendered component carries an editable source snapshot

  Scenario: Kramdown footnotes render in an RT render
    When I open the runner page on "/components/datagrid.md"
    And I wait for the runner to render
    Then footnote refs and their definitions render, none left raw

  Scenario: The bar replaces the page title and names the source
    When I open the runner page on "/run_samples/probe.txt"
    And I wait for the runner to render
    Then the runner bar names the source "probe.txt"
    And the runner page title is hidden

  Scenario: A bench flips the topbar into bench mode
    Given a stubbed bench with a course page
    When I open the bench page "course/ex1.md"
    Then the topbar switches to bench mode

  Scenario: A bench menu takes over the topbar links
    Given a stubbed bench with a course page
    And the bench ships a menu
    When I open the bench page "course/ex1.md"
    Then the topbar switches to bench mode
    And the topbar menu comes from the bench

  Scenario: Relative links in a rendered page stay in the repo
    Given a stubbed bench with a course page
    When I open the bench page "index.md"
    Then the link "Exercise 1" opens gh path "course/ex1.md"

  Scenario: Parent-relative links resolve within the repo
    Given a stubbed bench with a course page
    When I open the bench page "course/ex1.md"
    Then the link "Back to the bench" opens gh path "index.md"

  Scenario: A bare .folder inside a render lists the current folder
    # {: .folder } with no path knob defaults to the folder it lives in, and
    # runner mode is implied inside a render — "just show what's here".
    Given a stubbed bench with a course page
    When I open the bench page "shelf.md"
    Then the shelf lists a card opening gh path "lesson_a.md"

  Scenario: The runtime opens the rich page editor bound to the rendered source
    # /run.html has no page of its own to edit — the same rich editor must
    # target the RENDERED file (gh:repo/path the runner stamped), so course
    # material and benches are editable with the full Blocks/Raw/preview drawer.
    Given a stubbed bench with a course page
    When I open the bench page "course/ex1.md"
    And I open the page editor
    Then the page editor is editing "course/ex1.md"
    And the raw editor contains "Solve it your way"

  Scenario: A dot fence renders as a live diagram inside a runner page
    The Essentials' mindmap is a ```dot fence. The renderer only walked
    the static page once, at load — a fence arriving with a runner render
    stayed a wall of DOT source. The scan registry walks re-scans too.

    Given the GitHub contents API serves "courses/demo/mod/mindmap.md" with the document:
      """
      # Map

      ```dot
      digraph g { a -> b; }
      ```
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/mindmap.md"
    And I wait for the page to be interactive
    Then a rendered diagram replaces the dot source

  Scenario: A dot diagram fits the page instead of scrolling it
    A concept map wider than the page used to arrive at natural size and
    make the reader scroll sideways before reading anything. Fences fit by
    default; zoom= is the author's opt-out.

    Given the GitHub contents API serves "courses/demo/mod/wide.md" with the document:
      """
      # Wide

      ```dot
      digraph g { rankdir=LR; a->b->c->d->e->f->g->h->i->j->k->l->m->n->o; }
      ```
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/wide.md"
    And I wait for the page to be interactive
    Then a rendered diagram replaces the dot source
    And the diagram is no wider than the page

  Scenario: A second page's block opens its OWN source, not the last page's
    Michel opened the ⚙️ on a two-column .blocks in a lesson and got an
    .accordion from a completely different file (2026-08-06). The runner names
    id-less fences run_1, run_2 … with a counter that restarts at 1 on every
    render, and the source registry is keyed by that name and was never
    cleared. So the module's index claimed run_1 first, and the lesson's first
    fence inherited the index's markup for the rest of the session. A
    positional name is only unique inside one render, so the registry has to be
    emptied at the start of one too.

    Given the GitHub contents API serves "courses/demo/mod/first.md" with the document:
      """
      # First

      ```
      ### From the FIRST file
      ```
      {: .accordion }
      """
    And the GitHub contents API serves "courses/demo/mod/second.md" with the document:
      """
      # Second

      ```
      ### From the SECOND file
      ```
      {: .blocks cols="2" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/first.md"
    And I wait for the page to be interactive
    And I move to the runner source "gh:acme/demo/courses/demo/mod/second.md"
    And I wait for the page to be interactive
    Then the block editor on the rendered fence shows "From the SECOND file"
    And no snapshot still carries "From the FIRST file"

  Scenario: A card click lands at the top of the next page
    Inside the runner a link only changes the hash and the document is
    re-rendered in place, so the browser never scrolls. A reader who
    clicked a card near the bottom of a long module arrived half-way
    down a page they had never seen (2026-08-11).

    When I open the runner page on "/run_samples/tall.txt"
    And I wait for the runner to render
    And I scroll the runner to the bottom
    And the runner navigates to "/run_samples/probe.txt"
    Then the runner is scrolled to the top
    And the runner shows a heading "RT probe page"

  Scenario: Re-rendering the same page keeps the reader's place
    A save, a refresh or a repeated hash must not throw the reader back
    to the top of what they were already reading.

    When I open the runner page on "/run_samples/tall.txt"
    And I wait for the runner to render
    And I scroll the runner to the bottom
    And the runner navigates to "/run_samples/tall.txt"
    Then the runner is still scrolled down

  Scenario: A page rendered by the runner wears its own tags
    Course material arrives through the runner, so at page load its h1 does
    not exist yet — the tags are painted on the render instead (Michel,
    2026-08-12: "how to have them on the course material too?").

    When I open the runner page on "/components/code.md"
    And I wait for the runner to render
    Then the page title shows the tags "code"
    And the tags sit inside the page title

  Scenario: An embedded runner reads the file beside the page
    A course page must not name its own vault: `src="_setup.md"` means the
    file beside me, and "me" is the lab copy while authoring, the org vault
    for a student, a fork tomorrow (Michel, 2026-08-12).

    Given the GitHub contents API serves "courses/demo/_setup.md" with the document:
      """
      # Setup

      Collect your key.
      """
    And the GitHub contents API serves "courses/demo/cover.md" with the document:
      """
      # Cover

      [Setup](#)
      {: .runner src="_setup.md" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/cover.md"
    And I wait for the page to be interactive
    Then the embedded runner shows a heading "Setup"
