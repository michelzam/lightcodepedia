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

  Scenario: In a teacher's frame, Edit grays out on a course page
    The editor opened empty on a lesson in Canvas — the file is the
    course's, not the learner's (Michel, 2026-08-18). The pill now says
    so quietly instead of opening a dead drawer, and the hotkey stays
    silent too.

    Given the GitHub contents API serves "courses/demo/mod/lesson.md" with the document:
      """
      # Lesson

      The prose here belongs to the course.
      """
    When I navigate to "/run.html?crumb=BUILD#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    Then the pill's Edit door is grayed with a reason
    And pressing Alt+E does not open the editor

  Scenario: In the same frame, the learner's own bench page stays editable
    Given a stubbed bench with a course page
    When I open the framed bench page "course/ex1.md"
    Then the pill's Edit door is open

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

  Scenario: In a Canvas-shaped frame, a link to the page on screen reaches its top
    Unframed, the browser quietly handles a self-link. In Canvas the
    lesson iframe is TALL — its own window never scrolls, the parent
    does — so the click's only effect was invisible and the learner's
    "🏠 Back to the lesson" bookmark was a dead button exactly where
    they first press it (Emmanuel, 2026-08-18). Only scrollIntoView
    crosses the frame boundary; the runner must use it.

    When I open the frame host page scrolled past the lesson's top
    And I click the framed runner link "Back to this page"
    Then the host page is scrolled back to the lesson's top

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
    for a learner, a fork tomorrow (Michel, 2026-08-12).

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
    And the embedded runner is inside a border of its own
    And the injected file's own title stays out of the lesson

  Scenario: title= turns the embed into a window, and title="" names it from the file
    A border says "another file"; a title bar says "an application" (Michel,
    2026-08-15). The dots are paint: nothing closes, minimises or zooms.

    Given the GitHub contents API serves "courses/demo/_app_dogs.md" with the document:
      """
      # 🐕 Adoption Day — Dogs

      Every dog in our care.
      """
    And the GitHub contents API serves "courses/demo/lesson.md" with the document:
      """
      # Lesson

      [Named](#)
      {: .runner src="_app_dogs.md" title="Adoption Day" }

      [From the file](#)
      {: .runner src="_app_dogs.md" title="" }

      [No window](#)
      {: .runner src="_app_dogs.md" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/lesson.md"
    And I wait for the page to be interactive
    Then the windowed embeds are titled "Adoption Day" and "🐕 Adoption Day — Dogs"
    And an embed with no title= stays a plain box
    And the window dots are decoration, not controls

  Scenario: A stale key names itself, instead of saying HTTP 401
    Michel opened a vault link in a second browser and read "⚠️ Could not
    load: HTTP 401" — which tells a learner nothing and a teacher less. 401
    is a key that no longer works, so it earns the same live diagnosis as a
    404: probe the key, then say what is actually wrong.

    Given a course key that GitHub rejects
    When I open the runner page on "gh:acme/demo-vault/courses/demo/mod/lesson.md"
    Then the runner says the key itself is the problem
    And the runner never shows a bare HTTP status

  Scenario: A framed learner with no key still has a door in
    Focus mode learned this once already: a private course tells the learner
    to connect a key, and hiding the one control that does it makes the
    instruction impossible to follow.

    When I navigate to "/components/text?crumb=BUILD-AI"
    And I wait for the page to be interactive
    Then the sign-in door is offered

  Scenario: With no key at all, the message is three steps, not a status
    Michel, 2026-08-13: "if the FF has no key, we should at least have a
    better message, and some directions". A missing key is not an error, it
    is a missing step — so the page says the steps, in order, with the door
    to make the key.

    Given a private vault that answers a stranger with 404
    When I open the runner page on "gh:acme/demo-vault/courses/demo/mod/lesson.md"
    Then the runner says the course is private
    And the runner offers a way to make a key
    And the runner names the Get started door

  Scenario: An accordion may hold a two-column block, and a local clip plays itself
    Two fixes in one page (Michel, 2026-08-13: "2 blocks inside the author
    accordion … inject the video in the second with self play in a loop, all
    this side by side"). A ### inside a NESTED fence is content, not a new
    section — the outer accordion used to eat those headings and come out
    empty. And an .mp4 that lives beside the page is our file, not somebody
    else's player: it becomes a real <video>, which is the only way to say
    loop and autoplay.

    Given the GitHub contents API serves "courses/demo/mod/who.md" with the document:
      """
      # Cover

      ````
      ### 👤 The Author

      ```
      ### 👤 Name
      Some prose about the author.

      ### 🎬 In motion
      [A word from the author](clip.mp4)
      {: .video autoplay="true" loop="true" }
      ```
      {: .blocks cols="2" }
      ````
      {: .accordion }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/who.md"
    And I wait for the page to be interactive
    And I open the "The Author" accordion
    Then the accordion holds two blocks side by side
    And the clip is a video element that loops and starts muted
