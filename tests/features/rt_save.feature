Feature: One page, two repos — the fence seeds, the reader's bench persists
  A course page in the vault mixes the author's material with places where
  the learner contributes (a résumé pad, a repairable grid). The material
  and the contribution must live in DIFFERENT repos: save="my/…" makes the
  fence the author's seed and the learner's connected repo the truth. One
  writer per file — the author republishes forever, nothing ever collides.

  Background:
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/work.md" with the document:
      """
      # Work page

      ```markdown
      # Starter résumé — replace me
      ```
      {: .mdpad #cv save="cv.md" rows="6" }

      ```yaml
      - name: Rex
        campus: Milwauke
      ```
      {: .datagrid #dogs editable="true" save="dogs.yaml" height="160" }
      """

  Scenario: Without a key the page still teaches, and says how to join
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    Then the pad shows the author's starter
    And the pad's save button is disabled with a join hint

  Scenario: A joined learner with no saved copy starts from the seed
    Given a connected bench whose "courses/demo/mod/cv.md" does not exist yet
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    Then the pad shows the author's starter
    And the pad is not marked as the reader's own

  Scenario: The saved copy wins over the seed on the next visit
    Given a connected bench whose "courses/demo/mod/cv.md" holds "# Alice — WHS volunteer"
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    Then the pad shows "# Alice — WHS volunteer"
    And the pad is marked as the reader's own

  Scenario: Saving writes to the learner's repo, never the author's
    Given a connected bench whose "courses/demo/mod/cv.md" does not exist yet
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    And I type "# Mine now" into the pad and save
    Then the bench received a commit to "courses/demo/mod/cv.md" containing "# Mine now"
    And the author's repo received no commit

  Scenario: Start over restores the seed without touching the saved file
    Given a connected bench whose "courses/demo/mod/cv.md" holds "# Alice — WHS volunteer"
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    And I press the pad's start-over button
    Then the pad shows the author's starter
    And the bench received no commit

  Scenario: The grid loads the reader's repaired rows over the broken seed
    Given a connected bench whose "courses/demo/mod/dogs.yaml" holds "- name: Rex\n  campus: Milwaukee"
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    Then the dogs grid shows "Milwaukee"
    And the grid is marked as the reader's own

  Scenario: The grid's keep button writes rows to the learner's repo
    Given a connected bench whose "courses/demo/mod/dogs.yaml" does not exist yet
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    And I press the grid's keep button
    Then the bench received a commit to "courses/demo/mod/dogs.yaml" containing "Milwauke"

  Scenario: A derived view follows the repair, live
    The lesson shape: one dataset feeding an editable grid AND a query.
    The derived grid used to take the dataset once and never listen again,
    so repairing a row recomputed the query while the view below went on
    showing the old answer — a confident wrong number.

    Given a connected bench whose "courses/demo/mod/pets.yaml" does not exist yet
    And the GitHub contents API serves "courses/demo/mod/derived.md" with the document:
      """
      # Derived

      ```csv
      name,campus
      Rex,Milwauke
      Lucky,Milwaukee
      ```
      {: .dataset #pets }

      ```csv
      ```
      {: .datagrid source="pets" #pet_grid editable="true" save="pets.yaml" height="160" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/derived.md"
    And I wait for the page to be interactive
    And the dataset "pets" is repaired elsewhere
    Then the dogs grid shows "Milwaukee"
    And no grid cell still shows "Milwauke"

  Scenario: A dataset-backed repair keeps to the bench and re-derives the page
    Given a connected bench whose "courses/demo/mod/pets.yaml" holds "- name: Rex\n  campus: Fixed"
    And the GitHub contents API serves "courses/demo/mod/derived.md" with the document:
      """
      # Derived

      ```csv
      name,campus
      Rex,Milwauke
      ```
      {: .dataset #pets }

      ```csv
      ```
      {: .datagrid source="pets" #pet_grid editable="true" save="pets.yaml" height="160" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/derived.md"
    And I wait for the page to be interactive
    Then the dogs grid shows "Fixed"
    And the dataset "pets" now reads "Fixed"
    And the grid is marked as the reader's own

  Scenario: The class hub is framed, but the work goes home
    Canvas gives the whole class ONE url — the session hub. Prefer the repo
    the page renders from and every student's save aims at a shared repo
    none of them may write. Work always goes to the learner's OWN connected
    space: the page is where you stand; my/ is where you live.

    Given a learner connected to bench "stub/bench" reading the class hub "stub/hub"
    And the GitHub contents API serves "courses/demo/mod/work.md" with the document:
      """
      # Work page

      ```markdown
      # Starter résumé — replace me
      ```
      {: .mdpad #cv save="cv.md" rows="6" }
      """
    When I navigate to "/run.html#src=gh:stub/hub/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    And I type "# Mine now" into the pad and save
    Then the bench received a commit to "courses/demo/mod/cv.md" containing "# Mine now"
    And the repo "stub/hub" received no commit

  Scenario: The spelling picks the shelf — slash for the root, dots for the tree
    Relative lands beside the lesson under its FULL course path (two courses
    in one bench never collide); a leading slash is the bench root, for the
    personal files that outlive one lesson; ../ climbs the course tree the
    same way a prerequisite link does.

    Given a connected bench whose "my/scratch.md" does not exist yet
    And the GitHub contents API serves "courses/demo/mod/spell.md" with the document:
      """
      # Spellings

      ```markdown
      # root starter
      ```
      {: .mdpad #scratch save="/my/scratch.md" rows="4" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/spell.md"
    And I wait for the page to be interactive
    And I type "# Mine at the root" into the pad and save
    Then the bench received a commit to "my/scratch.md" containing "# Mine at the root"

  Scenario: A parent-relative path climbs to a shared course folder
    Given a connected bench whose "courses/demo/shared/notes.md" does not exist yet
    And the GitHub contents API serves "courses/demo/mod/climb.md" with the document:
      """
      # Climb

      ```markdown
      # shared starter
      ```
      {: .mdpad #notes save="../shared/notes.md" rows="4" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/climb.md"
    And I wait for the page to be interactive
    And I type "# Climbed" into the pad and save
    Then the bench received a commit to "courses/demo/shared/notes.md" containing "# Climbed"

  Scenario: A grid cell edit is data, not a credential
    The browser pairs a saved key with "the text field it saw" — a campus
    cell got offered a password-manager username mid-repair. An editor
    opened by a double-click must carry the opt-outs that keep every
    password manager away from the lesson's data.

    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    And I open a cell editor in the dogs grid
    Then the cell editor refuses autofill

  Scenario: The pad shows every version it ever saved
    The bench IS git, so the history already exists — it only lacked a
    door. Learners watch version control work before anyone says the word.
    An audit can also see that they iterated: no screenshot can fake that.

    Given a connected bench whose "courses/demo/mod/cv.md" holds "# Draft three"
    And the bench remembers two earlier versions of "courses/demo/mod/cv.md"
    And the GitHub contents API serves "courses/demo/mod/work.md" with the document:
      """
      # Work page

      ```markdown
      # Starter résumé — replace me
      ```
      {: .mdpad #cv save="cv.md" rows="6" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    And I open the pad's version list
    Then the list shows 2 saved versions
    When I compare the oldest version
    Then the difference is shown line by line

  Scenario: Bringing back an old version loads it without losing the new one
    Restoring is not a rollback. It drops the old text into the editor, so
    the next save is simply another commit. Nothing is ever lost, which is
    the lesson underneath.

    Given a connected bench whose "courses/demo/mod/cv.md" holds "# Draft three"
    And the bench remembers two earlier versions of "courses/demo/mod/cv.md"
    And the GitHub contents API serves "courses/demo/mod/work.md" with the document:
      """
      # Work page

      ```markdown
      # Starter résumé — replace me
      ```
      {: .mdpad #cv save="cv.md" rows="6" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    And I open the pad's version list
    And I bring back the oldest version
    Then the pad shows "# Draft one"
    And the bench received no commit

  Scenario: The grid offers the same versions panel as the pad
    One implementation, two call sites — the grid's repaired rows get the
    same history the résumé does. Removing the single attach call takes
    the feature out of the grid and leaves everything else untouched.

    Given a connected bench whose "courses/demo/mod/dogs.yaml" holds "- name: Rex\n  campus: Fixed"
    And the bench remembers two earlier versions of "courses/demo/mod/dogs.yaml"
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    And I open the grid's version list
    Then the list shows 2 saved versions

  Scenario: Saving commits the cell you are still typing in
    A grid cell editor holds its value until it closes. Typing a repair and
    reaching straight for 💾 saved the OLD value, so the learner's last
    change vanished with no sign it had. The editor closes before anything
    reads the rows.

    Given a connected bench whose "courses/demo/mod/dogs.yaml" does not exist yet
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    And I type "Milwaukee" into a grid cell without leaving it
    And I press the grid's keep button
    Then the bench received a commit to "courses/demo/mod/dogs.yaml" containing "Milwaukee"

  Scenario: The grid's difference is a grid of what actually moved
    Rows are not lines: a text diff of YAML is noise to a reader who thinks
    in dogs and campuses. Only the changed rows appear, as was/now pairs.

    Given a connected bench whose "courses/demo/mod/dogs.yaml" holds "- name: Rex\n  campus: Fixed"
    And the bench remembers two earlier versions of "courses/demo/mod/dogs.yaml"
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    And I open the grid's version list
    And I compare the oldest version
    Then the difference is a grid showing only the changed rows

  Scenario: The first save keeps the starter, so the first change can be read
    Otherwise version one IS the learner's text and the panel shows a single
    row that differs from nothing — the very change the lesson is about
    cannot be shown. Written on the first save only: a reader who never
    edits leaves no commits at all.

    Given a connected bench whose "courses/demo/mod/cv.md" does not exist yet
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    And I type "# Mine now" into the pad and save
    Then the bench received 2 commits to "courses/demo/mod/cv.md"
    And the first of them is the lesson's starter
    And the last of them holds "# Mine now"

  Scenario: A second save adds one version, not another starter
    Given a connected bench whose "courses/demo/mod/cv.md" holds "# Draft three"
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    And I type "# Draft four" into the pad and save
    Then the bench received 1 commits to "courses/demo/mod/cv.md"

  Scenario: The starter is named in the version list, not passed off as the learner's
    Given a connected bench whose "courses/demo/mod/cv.md" holds "# Draft three"
    And the bench remembers a starter and a change for "courses/demo/mod/cv.md"
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    And I open the pad's version list
    Then the oldest version is labelled as the lesson's starter

  Scenario: Changed values are coloured in the grid's difference
    Given a connected bench whose "courses/demo/mod/dogs.yaml" holds "- name: Rex\n  campus: Fixed"
    And the bench remembers two earlier versions of "courses/demo/mod/dogs.yaml"
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    And I open the grid's version list
    And I compare the oldest version
    Then the changed value is marked red where it was and green where it is

  Scenario: A bench slot is editable inside a read-only lesson
    The lesson stays the vault's; the framed region belongs to the learner.
    Read-only is nearest-wins now: uneditable unless a nearer source says
    otherwise, and inside the slot the nearer source is their own bench.

    Given a connected bench whose "courses/demo/mod/wiring.md" does not exist yet
    And the GitHub contents API serves "courses/demo/mod/lesson.md" with the document:
      """
      # Lesson

      The prose here belongs to the course.

      ```markdown
      Wire me.
      ```
      {: .embed save="wiring.md" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    Then the slot shows the lesson's seed
    And the slot commits to "courses/demo/mod/wiring.md"

  Scenario: The learner's own copy replaces the seed inside the slot
    Given a connected bench whose "courses/demo/mod/wiring.md" holds "Wired properly."
    And the GitHub contents API serves "courses/demo/mod/lesson.md" with the document:
      """
      # Lesson

      ```markdown
      Wire me.
      ```
      {: .embed save="wiring.md" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    Then the slot shows "Wired properly."
    And the slot is marked as the reader's own

  Scenario: A dataset reads the file the learner repaired in an earlier lesson
    The fence is the author's seed; the learner's file is the truth — the
    same contract the pad, the grid and the slot already follow. A dataset
    could not read a bench at all, so a lesson had no way to feed today's
    screen from the file its reader repaired yesterday. Watching your own
    earlier fix arrive somewhere new is the reason the next lesson is worth
    sitting through.

    Given a connected bench whose "courses/demo/mod/dogs.yaml" holds "- name: Rex\n  campus: Milwaukee"
    And the GitHub contents API serves "courses/demo/mod/feed.md" with the document:
      """
      # Feed

      ```yaml
      - name: Rex
        campus: Milwauke
      ```
      {: .dataset #dogs save="dogs.yaml" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/feed.md"
    And I wait for the page to be interactive
    Then the dataset "dogs" holds "Milwaukee"

  Scenario: The slot says whose file it is, and whether it is saved yet
    "Your own space" used to be carried by a 1px border nobody notices on
    a phone — the most important fact about the block was the least
    visible thing on the page. The stripe names the signed-in learner,
    not the repo owner: a class bench is forked INTO the org, so every
    student would otherwise see the same organisation logo over their own
    work.

    Given a connected bench whose "courses/demo/mod/wiring.md" does not exist yet
    And the signed-in learner is "ada"
    And the GitHub contents API serves "courses/demo/mod/lesson.md" with the document:
      """
      # Lesson

      ```markdown
      Wire me.
      ```
      {: .embed save="wiring.md" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    Then the slot's stripe names "@ada"
    And the slot's stripe says it is still the lesson's copy

  Scenario: The stripe reads draft once the learner has their own copy
    Given a connected bench whose "courses/demo/mod/wiring.md" holds "Mine now."
    And the signed-in learner is "ada"
    And the GitHub contents API serves "courses/demo/mod/lesson.md" with the document:
      """
      # Lesson

      ```markdown
      Wire me.
      ```
      {: .embed save="wiring.md" #work }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    Then the slot is in the "draft" state

  Scenario: Only the LESSON's check turns the slot green
    The learner owns the file, so a check inside it could be weakened or
    deleted. The card that grades a slot names it with grades= and lives
    in the vault, where the person being marked cannot reach it.

    Given a connected bench whose "courses/demo/mod/wiring.md" holds "Mine now."
    And the signed-in learner is "ada"
    And the GitHub contents API serves "courses/demo/mod/lesson.md" with the document:
      """
      # Lesson

      ```markdown
      Wire me.
      ```
      {: .embed save="wiring.md" #work }

      ```gherkin
      Feature: The marker
        Scenario: It holds
          Given nothing
      ```
      {: .feature #marker grades="work" visible="true" status="pending" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    Then the slot is in the "draft" state
    When the lesson's check on the slot passes
    Then the slot is in the "done" state

  Scenario: The slot's versions open the real panel, not an alert box
    The first cut printed commit messages into window.alert — no readable
    dates, no way to see what a version said, no way to bring it back
    (Michel, 2026-08-11). It is the same panel the pad and the grid use.

    Given a connected bench whose "courses/demo/mod/wiring.md" holds "# Draft three"
    And the bench remembers two earlier versions of "courses/demo/mod/wiring.md"
    And the GitHub contents API serves "courses/demo/mod/lesson.md" with the document:
      """
      # Lesson

      ```markdown
      Wire me.
      ```
      {: .embed save="wiring.md" #work }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    And I open the slot's menu
    And I choose "Every version I saved"
    Then the list shows 2 saved versions
    When I compare the oldest version
    Then the difference is shown line by line

  Scenario: A saved pad wears the same stripe as a page slot
    Michel, 2026-08-11: the bench indicator belongs everywhere a learner's
    own file is used — a cv pad, a dogs grid — not only on a page slot.
    Until now a pad wrote to the very same repo without saying so.

    Given a connected bench whose "courses/demo/mod/cv.md" holds "# Mine"
    And the GitHub contents API serves "courses/demo/mod/work.md" with the document:
      """
      # Work page

      ```markdown
      # Starter — replace me
      ```
      {: .mdpad #cv save="cv.md" rows="6" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    Then a bench stripe names "courses/demo/mod/cv.md"
    And that stripe reads "draft — yours"

  Scenario: Two devices converge, and neither undoes the other
    The merge is max-per-page, so a phone one lesson behind can never
    lower a laptop's record — which is why the sync needs no locking and
    no conflict resolution (Michel, 2026-08-11).

    Given a connected bench whose "courses/demo/mod/cv.md" does not exist yet
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    Then merging a behind device never lowers the record

  Scenario: A hand-edited progress file stops matching its own checksum
    Given a connected bench whose "courses/demo/mod/cv.md" does not exist yet
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/work.md"
    And I wait for the page to be interactive
    Then a progress file it wrote reads back intact
    And the same file with a typed-in line does not

  Scenario: The menu greys the transitions that do not apply
    Given a connected bench whose "courses/demo/mod/wiring.md" does not exist yet
    And the signed-in learner is "ada"
    And the GitHub contents API serves "courses/demo/mod/lesson.md" with the document:
      """
      # Lesson

      ```markdown
      Wire me.
      ```
      {: .embed save="wiring.md" #work }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    # the move that matters is a button, not a menu row (Michel, 2026-08-11)
    Then the slot offers "💾 Save to my space"
    When I open the slot's menu
    Then "Copy the starter into my space" is offered
    And "Start over from the lesson's copy" is greyed out
    # a starter has no file at that address yet, so the door would 404 and the
    # runner would offer a Refresh that can never bring it (Michel, 2026-08-11)
    And "Open it on its own" is greyed out
