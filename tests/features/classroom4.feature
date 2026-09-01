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
    And I open every section
    Then both personas face each other
    And the pitch serves the instructor
    And the impact map pulls its goal from the pitch
    And the flow declares the one-click cast
    And the desk and the join wizard wear their windows
    And the model is backstage and the diagram shows the desk

  Scenario: The page opens on the desk, the rest folded away
    Seven sections is a scroll, and the desk is the one the instructor
    came for (Michel, 2026-08-31: "an accordion for each of the sections,
    keep the desk open" — the accordion itself, no new component type).
    A shut section still HOLDS its content: the proofs and the diagram
    exist from page load, folded or not.

    When I navigate to "/lab/classroom4"
    And I wait for the page to be interactive
    Then the page wears 7 section accordions
    And the "5--the-desk" section is open
    And the "6--proof-running" section is folded
    And the "7--the-picture" section is folded
    And the folded sections still hold their content
    When I open the "6--proof-running" section
    Then the "6--proof-running" section is open

  Scenario: The legend is the dimmer — a chip folds its kind away
    The cast strip is structure, not ink; the reader tunes the level of
    detail by clicking legend chips (Michel, 2026-08-25). A second click
    brings the kind back.

    When I navigate to "/lab/classroom4"
    And I wait for the page to be interactive
    And I open every section
    Then the "c4_flow" flow shows its "event" notes
    When I click the "event" legend chip on "c4_flow"
    Then the "c4_flow" flow hides its "event" notes
    And the "c4_flow" flow shows its "command" notes
    When I click the "event" legend chip on "c4_flow"
    Then the "c4_flow" flow shows its "event" notes

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
    And the desk offers exactly the verbs "plan, invite, sync"

  Scenario: Every promise on the page turns green
    When I navigate to "/lab/classroom4"
    And I wait for the page to be interactive
    And I open every section
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

  Scenario: A class-sized plan is echoed to the last name
    The echo stopped at twelve lines and said nothing about the rest, so
    fall26's first Plan showed eight of nineteen students and looked
    finished (Michel, 2026-08-31). A roster is read to the end, or the
    teacher invites people they never saw.

    Given a connected author key and a class-sized roster gate
    When I navigate to "/lab/classroom4"
    And I wait for the page to be interactive
    And I press "plan" on the "c4_mission" inspector
    Then the verdict echo names every seat, first "Conner, Jay" to last "Zamora, Iris"
    And all 19 seats stand on the roster, page after page

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

  Scenario: An existing bench never reads as a permissions failure
    GitHub refuses a fork whose NAME already stands with a 403 — the
    same status as a missing grant. Field-caught (2026-08-25): three
    healthy benches reported "the org key cannot create repos", and the
    reconciler bailed before team and bay. It now asks the bench itself
    before blaming the key, and finishes the kit.

    Given a connected author key and a stubbed roster gate
    And an org where ada accepts between two syncs
    And a bench factory where the bench already stands
    When I navigate to "/lab/classroom4"
    And I wait for the page to be interactive
    And I press "plan" on the "c4_mission" inspector
    And I press "sync" on the "c4_mission" inspector
    And I press "sync" on the "c4_mission" inspector
    Then the factory teamed "adalove" and built the bay "build-ai-fall26-adalove-bay"
    And the "c4_roster" grid shows "ada" in "benched"

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
    And the factory built "build-ai-fall26-zaralove" and granted "zaralove"

  Scenario: Sync forges the whole kit, the instant a login is known
    No Benches button anywhere (A′, Michel 2026-08-25): the same Sync
    that binds a login FORKS the hub into the org as <session>-<login>
    — a fork, never a template copy (register §18) — grants push on it
    plus read on the hub, puts the member on the SESSION TEAM (the
    vault rides it; org removal kills it and a re-invite does not
    restore it — the field lesson), creates the public bay, and walks
    the row onto its bench. Idempotent: one Sync makes a re-added
    student whole.

    Given a connected author key and a stubbed roster gate
    And an org where ada accepts between two syncs
    And a bench factory that records what it builds
    When I navigate to "/lab/classroom4"
    And I wait for the page to be interactive
    And I press "plan" on the "c4_mission" inspector
    And I press "sync" on the "c4_mission" inspector
    And I press "sync" on the "c4_mission" inspector
    Then the factory built "build-ai-fall26-adalove" and granted "adalove"
    And the factory teamed "adalove" and built the bay "build-ai-fall26-adalove-bay"
    And the "c4_roster" grid shows "ada" in "benched"
