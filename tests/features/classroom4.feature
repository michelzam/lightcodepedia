Feature: 🧭 Classroom 4 — the onboarding desk, problem to solution
  The alignment set, applied for real and then RETRO-DESIGNED bottom-up
  (Michel, 2026-08-24): two classes only. The Desk is an object — org,
  session, course, a phase machine — and its four verbs ARE the buttons,
  rendered by the inspector and gated by state. Students are rows that
  GitHub facts walk. The muscle lives in the console bridge (lcDeskRun).

  Background:
    Given I have a clean browser page

  Scenario: The whole problem-solution ladder stands on the page
    When I navigate to "/lab/classroom4"
    And I wait for the page to be interactive
    Then both personas face each other
    And the pitch serves the instructor
    And the impact map pulls its goal from the pitch
    And the flow declares the one-click cast
    And the desk and the join wizard wear their windows
    And the model is backstage and the diagram shows the desk

  Scenario: HQ offers the door
    When I navigate to "/lab/"
    And I wait for the page to be interactive
    Then the HQ card links to classroom 4

  Scenario: The desk's verbs are gated by its phase
    A fresh desk offers Plan and nothing else — the other two verbs
    render disabled until their preconditions hold. The buttons ARE the
    state machine (Michel, 2026-08-24).

    Given a connected author key and a stubbed roster gate
    When I navigate to "/lab/classroom4"
    And I wait for the page to be interactive
    Then the "plan" verb on the "c4_mission" inspector is enabled
    And the "sync" verb on the "c4_mission" inspector is disabled
    And the "invite" verb on the "c4_mission" inspector is disabled
    When I press "plan" on the "c4_mission" inspector
    Then the "sync" verb on the "c4_mission" inspector is enabled

  Scenario: Every promise on the page turns green
    When I navigate to "/lab/classroom4"
    And I wait for the page to be interactive
    And I run every embedded feature
    Then all embedded features pass

  Scenario: Plan walks the real gate (stubbed) and seats arrive
    Dispatch → commit status → orphan blob: the console's verdict channel,
    driven by the Desk's own verb. Every email becomes a seat, once; a
    skip bullet's tail is a REASON, never a name, and "already invited"
    walks that seat to invited on the spot.

    Given a connected author key and a stubbed roster gate
    When I navigate to "/lab/classroom4"
    And I wait for the page to be interactive
    And I press "plan" on the "c4_mission" inspector
    Then the "c4_roster" grid shows "zik" in "in_canvas"
    And the "c4_roster" grid shows "mk" in "invited"
    And the roster holds exactly 4 seats
    And no seat is named after a skip reason

  Scenario: Sync reads the org's live facts (stubbed) and journeys advance
    Pending invitation = invited · member = in_org · pushed bench =
    building — each student walks the legal road to the fact, never past.

    Given a connected author key and a stubbed roster gate
    And a stubbed org
    When I navigate to "/lab/classroom4"
    And I wait for the page to be interactive
    And I press "plan" on the "c4_mission" inspector
    And I press "sync" on the "c4_mission" inspector
    Then the "c4_roster" grid shows "ada" in "invited"
    And the "c4_roster" grid shows "zik" in "building"
    And no bay twin became a student

  Scenario: An acceptance between two syncs binds the login by itself
    GitHub never links a member to an email — but the desk sees TIME:
    exactly one pending email gone while exactly one member arrived IS
    the binding. No typing (Michel, 2026-08-24: "it should be automatic").

    Given a connected author key and a stubbed roster gate
    And an org where ada accepts between two syncs
    When I navigate to "/lab/classroom4"
    And I wait for the page to be interactive
    And I press "plan" on the "c4_mission" inspector
    And I press "sync" on the "c4_mission" inspector
    And I press "sync" on the "c4_mission" inspector
    Then the "c4_roster" grid shows "ada" in "in_org"
    And the "c4_roster" grid shows "ada" with login "adalove"

  Scenario: Sync matches members to seats by their names
    A member whose login tokens all prefix a seat's own words IS that
    seat — bound, walked, benched if the bench already stands. egbas
    matches nobody and honestly stays unclaimed.

    Given a connected author key and a stubbed roster gate
    And an org whose members wear their names
    When I navigate to "/lab/classroom4"
    And I wait for the page to be interactive
    And I press "plan" on the "c4_mission" inspector
    And I press "sync" on the "c4_mission" inspector
    Then the "c4_roster" grid shows "Onaivi" in "building"
    And the "c4_roster" grid shows "Onaivi" with login "Emmanuel-Onaivi"

  Scenario: A guest invited by hand becomes a seat, walks, and gets a bench
    People beyond Canvas — a TA, a colleague — are invited from the org's
    People page. GitHub's own pending invitation IS the seat record:
    nothing stored anywhere, the seat expires with the invitation it
    mirrors. Sync adopts it, witnesses the acceptance, forges the bench.

    Given a connected author key and a stubbed roster gate
    And an org where guest zara is invited by hand and then accepts
    And a bench factory that records what it builds
    When I navigate to "/lab/classroom4"
    And I wait for the page to be interactive
    And I press "plan" on the "c4_mission" inspector
    And I press "sync" on the "c4_mission" inspector
    Then the "c4_roster" grid shows "zara" in "invited"
    When I press "sync" on the "c4_mission" inspector
    Then the "c4_roster" grid shows "zara" with login "zaralove"
    And the "c4_roster" grid shows "zara" in "benched"
    And the factory built "build-ai-summer26-zaralove" and granted "zaralove"

  Scenario: Sync forges the benches itself, the instant a login is known
    No Benches button anywhere (A′, Michel 2026-08-25): the same Sync
    that binds a login FORKS the hub into the org as <session>-<login>
    — a fork, never a template copy (register §18: the fork link carries
    refresh, roster and the privacy guard) — grants the student push on
    it plus read on the hub, and walks the row onto its bench.

    Given a connected author key and a stubbed roster gate
    And an org where ada accepts between two syncs
    And a bench factory that records what it builds
    When I navigate to "/lab/classroom4"
    And I wait for the page to be interactive
    And I press "plan" on the "c4_mission" inspector
    And I press "sync" on the "c4_mission" inspector
    And I press "sync" on the "c4_mission" inspector
    Then the factory built "build-ai-summer26-adalove" and granted "adalove"
    And the "c4_roster" grid shows "ada" in "benched"
