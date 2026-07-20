Feature: The student course wizard (/courses/join)

  The dedicated student journey — distinct from /start (the builder journey).
  Account → course key → live access check against the vault → open the course.

  Background:
    Given I have a clean browser page

  Scenario: A fresh student sees step 1 active and the rest waiting
    When I open the course wizard
    Then join step 1 is active and steps 2 and 3 are off

  Scenario: A valid course key advances to the enrollment check
    Given a stubbed GitHub that accepts the key with repo scope
    When I open the course wizard
    And I confirm I have an account
    And I paste the course key "ghp_newkey" and check it
    Then join steps 1 and 2 are done and step 3 is active

  Scenario: An enrolled student gets the open-course door
    Given a stubbed GitHub that accepts the key with repo scope
    And the student can read the vault
    When I open the course wizard with a stored key
    Then the wizard says the student is in
    And the open-course door points at the vault entry

  Scenario: A not-yet-enrolled student is guided to their invitation
    Given a stubbed GitHub that accepts the key with repo scope
    When I open the course wizard with a stored key
    And I check my access
    Then the wizard guides to the invitation, not an error dump

  Scenario: Accepting the invitation in-app opens the course
    Given a stubbed GitHub that accepts the key with repo scope
    When I open the course wizard with a stored key
    And I accept my invitation in the wizard
    Then the wizard says the student is in
    And the open-course door points at the vault entry

  Scenario: An enrolled student with no bench is offered the fork
    Given a stubbed GitHub that accepts the key with repo scope
    And the student can read the vault
    When I open the course wizard with a stored key
    Then the bench step offers the fork

  Scenario: Forking creates the org bench, explicitly up to date
    Given a stubbed GitHub that accepts the key with repo scope
    And the student can read the vault
    When I open the course wizard with a stored key
    And I fork my bench
    Then my bench shows up to date with the hub

  Scenario: A bench behind the hub shows the gap and syncs
    Given a stubbed GitHub that accepts the key with repo scope
    And the student can read the vault
    And my bench exists and is 2 updates behind the hub
    When I open the course wizard with a stored key
    Then the bench shows 2 updates to sync
    When I sync my bench
    Then my bench shows up to date with the hub

  Scenario: Submitting freezes a snapshot tag on the bench
    Given a stubbed GitHub that accepts the key with repo scope
    And the student can read the vault
    And my bench exists and is 0 updates behind the hub
    When I open the course wizard with a stored key
    And I submit my work
    Then the wizard confirms a frozen submission snapshot
