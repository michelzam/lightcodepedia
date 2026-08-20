Feature: 🎮 Join the game — the two-minute door into BUILD-AI
  A student in Canvas with no GitHub account, and a visitor who found the
  site alone, read the same page and need different last paragraphs
  (Michel, 2026-08-19). Nothing here asks for an account or a key: the app
  runs, the proof runs, the quiz scores. The ask comes after the win, and
  it says the one thing that makes an emailed invitation work.

  Background:
    Given I have a clean browser page

  Scenario: The app runs for someone who has nothing
    When I navigate to "/courses/build_ai/start"
    And I wait for the page to be interactive
    Then the shelter list shows 3 dogs
    And the fee chart is drawn
    And nothing on the page asked me to connect

  Scenario: The page's own promise starts red and names the gap
    A green check proves nothing to a newcomer. Nova's missing fee is the
    invitation to touch the data — and the check says her name.

    When I navigate to "/courses/build_ai/start"
    And I wait for the page to be interactive
    And I run the page's embedded features
    Then the proof is failing about "Nova"

  Scenario: The app wears a window, and its cells invite one tap
    "The grid looks r/o", and a page that calls something an app should
    frame it like one (Michel, 2026-08-20). Both were real: a dataset-bound
    grid ignored editable= entirely, and the app was loose prose on the
    page instead of a framed thing.

    When I navigate to "/courses/build_ai/start"
    And I wait for the page to be interactive
    Then the app is framed as a window titled "Shelter Desk"
    And the fee cells accept a tap

  Scenario: One tap fills the gap and the whole page follows
    On iPhone the double-click AG needs never arrived. A contenteditable
    cell takes ONE tap, which is what a phone actually does.

    When I navigate to "/courses/build_ai/start"
    And I wait for the page to be interactive
    And I tap Nova's fee and type "75"
    Then the dataset carries Nova's new fee
    And the page's own promise turns green

  Scenario: A visitor is invited to write in
    When I navigate to "/courses/build_ai/start"
    And I wait for the page to be interactive
    Then the page offers the enrolment address
    And the roster paragraph stays hidden

  Scenario: Inside Canvas, the student is told their invitation is coming
    The frame is the tell: a Canvas embed carries ?crumb=, a visitor's tab
    does not. Same page, different door — and the framed one must say
    "sign up with that same address", or the invitation will not match the
    account they create.

    When I navigate to "/courses/build_ai/start?crumb=BUILD-AI"
    And I wait for the page to be interactive
    Then the page tells me my invitation is coming to my university address
    And the page tells me to sign up with that same address
    And the page shows the way in when the mail never arrives
    And the enrolment address stays hidden

  Scenario: The cover is the visitor's first page, and it opens the door
    A page nobody links to does not exist. The cover is the only entry a
    visitor finds under /courses/, and it pointed at enrolment and at the
    key wizard — never at the two-minute app (Michel, 2026-08-20).

    When I navigate to "/courses/build_ai/"
    And I wait for the page to be interactive
    And I follow the cover's link into the game
    Then the shelter list shows 3 dogs
    And nothing on the page asked me to connect
