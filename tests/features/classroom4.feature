Feature: 🧭 Classroom 4 — the onboarding desk, problem to solution
  The alignment set from classroom3, applied for real (Michel, 2026-08-24):
  personas → pitch → impact map → event flow → hidden model → data → the
  desk app in its window → runnable proofs → diagram → meta. One click
  invites the roster; the artifacts explain themselves.

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
    And the model is backstage and the diagram shows the managers

  Scenario: HQ offers the door
    When I navigate to "/lab/"
    And I wait for the page to be interactive
    Then the HQ card links to classroom 4

  Scenario: One click invites the whole roster (the simulation)
    The real ✉️ button fires the course-invite gate; this presses the
    SIMULATION of the same walk, safe on any machine.

    When I navigate to "/lab/classroom4"
    And I wait for the page to be interactive
    And I press "simulate_invites" on the "c4_mission" inspector
    Then the "c4_roster" grid shows "ada" in "invited"
    And the "c4_roster" grid shows "noor" in "invited"
    And the invitations grid gains rows

  Scenario: Every promise on the page turns green
    When I navigate to "/lab/classroom4"
    And I wait for the page to be interactive
    And I run every embedded feature
    Then all embedded features pass

  Scenario: The Plan button walks the real gate (stubbed) and seats arrive
    Dispatch → commit status → orphan blob: the console's own verdict
    channel, driven from the desk. The plan lists the Canvas roster; every
    NEW email becomes a seat, already-known ones are not duplicated.

    Given a connected author key and a stubbed roster gate
    When I navigate to "/lab/classroom4"
    And I wait for the page to be interactive
    And I press the desk button "c4_plan"
    Then the "c4_roster" grid shows "zik" in "in_canvas"
    And the roster holds exactly 5 seats

  Scenario: Sync reads the org's live facts (stubbed) and journeys advance
    Pending invitation = invited · member = in_org · pushed bench =
    building — each student walks the legal road to the fact, never past.

    Given a connected author key and a stubbed org
    When I navigate to "/lab/classroom4"
    And I wait for the page to be interactive
    And I press the desk button "c4_sync"
    Then the "c4_roster" grid shows "ada" in "invited"
    And the "c4_roster" grid shows "linus" in "in_org"
    And the "c4_roster" grid shows "noor" in "building"
