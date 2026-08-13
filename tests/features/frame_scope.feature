Feature: Frame flags are a scope, not a page setting
  A teacher frames ONE url in an LMS (?focus=1&navigable=0&open=…) and the
  learner clicks a folder card. Before this, the next page arrived with no
  flags at all — the full platform, in a new tab, outside the scope the
  teacher set up. The flags now ride every same-origin hop, and an
  allowlisted link stays inside the frame unless ?open_in=tab says otherwise.

  Background:
    Given I have a clean browser page

  Scenario: A focused learner can still walk the course
    Focus once implied navigable=0, so a framed learner tapping a folder
    card got nothing at all — every card link neutralised, the course
    unwalkable. Staying in the teacher's scope is the flags riding along,
    not the links dying. Only an explicit navigable=0 locks a page now.

    When I navigate to "/components/folder?focus=1"
    And I wait for the page to be interactive
    And I follow the first folder card link
    Then I actually left the page I was on
    And the page I land on still carries "focus=1"

  Scenario: An ordinary internal link carries the frame flags forward
    When I navigate to "/components/text?focus=1&navigable=1&editable=0"
    And I wait for the page to be interactive
    And I follow the first internal link
    Then I actually left the page I was on
    And the page I land on still carries "focus=1"
    And the page I land on still carries "editable=0"

  Scenario: An allowlisted link stays in the frame, flags intact
    When I navigate to "/components/text?focus=1&navigable=0&open=/components/*"
    And I wait for the page to be interactive
    And I follow the first internal link to "/components/"
    Then I actually left the page I was on
    And no second tab was opened
    And the page I land on still carries "focus=1"
    And the page I land on still carries "navigable=0"

  Scenario: open_in=tab restores the side-by-side behaviour
    When I navigate to "/components/text?focus=1&navigable=0&open=/components/*&open_in=tab"
    And I wait for the page to be interactive
    And I follow the first internal link to "/components/"
    Then a second tab was opened carrying "focus=1"

  Scenario: An unframed page is left completely alone
    When I navigate to "/components/text"
    And I wait for the page to be interactive
    And I follow the first internal link
    Then the page I land on carries no frame flags

  Scenario: In crumb mode the bar says where you are, and nothing else
    A learner inside a Canvas iframe already has Canvas's navigation. Ours
    only has to answer "where am I?" — course, module, page — and "am I
    signed in as me?" (Michel, 2026-08-13).

    Given the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # 📦 02·A Long Walk

      🚶 It works. People don't.
      """
    And the GitHub contents API serves "courses/demo/mod/lesson.md" with the document:
      """
      # 🚦 Gates

      ⛔ They paid. Never met it.
      """
    When I navigate to "/run.html?crumb=BUILD-AI#src=gh:acme/demo-vault/courses/demo/mod/lesson.md"
    And I wait for the page to be interactive
    Then the crumb reads "BUILD-AI" then "02·A Long Walk" then "Gates"
    And the menu links are gone
    And the runner never names the file
    And the trail sits left and the meters sit right, before my face
    And the module name leads to the module's own cover
    And the page begins right under the bar
    And the about bubble credits the content, the platform and the AI


  Scenario: The crumb survives the hop into a module
    Michel, 2026-08-13: "when I navigate to a given module, the
    'Lightcodepedia' full menu comes back". A scope that only holds on the
    page the teacher pasted is not a scope — crumb and up ride along like
    every other flag.

    When I navigate to "/components/folder?crumb=BUILD-AI&up=0"
    And I wait for the page to be interactive
    And I follow the first folder card link
    Then I actually left the page I was on
    And the page I land on still carries "crumb=BUILD-AI"
    And the page I land on still carries "up=0"
    And the menu links are gone

  Scenario: In crumb mode the face is a statement, not a menu
    Read-only means the account chip too (Michel, 2026-08-13: "the avatar
    drop down menu opens a lot of options, and I prefer not!"). Every row
    behind it — HQ, publish, disconnect — is a door out of the module.

    Given I am signed in with my face already cached
    When I navigate to "/components/text?crumb=BUILD-AI"
    And I wait for the page to be interactive
    Then my face is shown
    And tapping it opens nothing
