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
    And the bench door opens in the runner

  Scenario: A bench behind the hub shows the gap and syncs
    Given a stubbed GitHub that accepts the key with repo scope
    And the student can read the vault
    And my bench exists and is 2 updates behind the hub
    When I open the course wizard with a stored key
    Then the bench shows 2 updates to sync
    When I sync my bench
    Then my bench shows up to date with the hub

  Scenario: The course door forwards a green student into the bench
    Given a stubbed GitHub that accepts the key with repo scope
    And the student can read the vault
    And my bench exists and is 0 updates behind the hub
    When I open the course door "?go=bench&hub=build-ai-fall26" with a stored key
    Then I am forwarded into my bench

  Scenario: A pending sync holds the door open on the wizard
    Given a stubbed GitHub that accepts the key with repo scope
    And the student can read the vault
    And my bench exists and is 2 updates behind the hub
    When I open the course door "?go=bench&hub=build-ai-fall26" with a stored key
    Then the bench shows 2 updates to sync

  Scenario: The door names a session the student cannot see
    Given a stubbed GitHub that accepts the key with repo scope
    And the student can read the vault
    When I open the course door "?go=bench&hub=ghost-session" with a stored key
    Then the bench step explains the session is not visible

  Scenario: The door holds for refresh when the bench lacks the new root
    Given a stubbed GitHub that accepts the key with repo scope
    And the student can read the vault
    And my bench exists and is 0 updates behind the hub
    And my bench has no index yet
    When I open the course door "?go=bench&hub=build-ai-fall26" with a stored key
    Then the bench step invites a refresh

  Scenario: The energy key gets a live check and a save-as-password moment
    Given a stubbed GitHub that accepts the key with repo scope
    And the student can read the vault
    And the energy provider accepts the key
    When I open the course wizard with a stored key
    And I paste the energy key "AIzaTestKey" and check it
    Then the energy step confirms the key works and will follow the student

  Scenario: A rejected energy key says rejected, not broken
    Given a stubbed GitHub that accepts the key with repo scope
    And the student can read the vault
    And the energy provider rejects the key
    When I open the course wizard with a stored key
    And I paste the energy key "AIzaWrong" and check it
    Then the energy step reports the rejection with the status code

  Scenario: A resolved bench completes the connection pair
    Step 2 stores the key; the bench resolving is when its repo half
    becomes known. Without pairing them, every save="my/…" aimed at
    whatever repo was lying around from an earlier life — the author's
    site on a teacher's browser, nothing at all on a student's — and the
    key answered 404 for a repo it was never meant to cover.

    Given a stubbed GitHub that accepts the key with repo scope
    And the student can read the vault
    And my bench exists and is 0 updates behind the hub
    And an old author connection points at "michelzam/lightcodepedia"
    When I open the course wizard with a stored key
    Then my bench shows up to date with the hub
    And the connected repo is my bench

  Scenario: The course key never steals a username from the page
    Given a stubbed GitHub that accepts the key with repo scope
    When I open the course wizard
    And I confirm I have an account
    Then the course key is asked through a named credential form

  Scenario: A key the provider will not let us test is still saved
    A 403 on the check says the key is not allowed to make THAT call — it
    says nothing about whether the key is good. Discarding it meant a
    learner behind a website-restricted key or a corporate proxy could
    never get through the door at all, and pasted it again every refresh.

    Given a stubbed GitHub that accepts the key with repo scope
    And the student can read the vault
    And the energy provider will not let us test the key
    When I open the course wizard with a stored key
    And I paste the energy key "AIzaRestricted" and check it
    Then the energy step says the key is saved but untested
    And the energy key is on this device

  Scenario: A key is kept when the road is blocked, not thrown away
    An ad-blocker, VPN or firewall eating the request is not evidence
    against the key. Keep it — that is the whole point of saving it once.

    Given a stubbed GitHub that accepts the key with repo scope
    And the student can read the vault
    And the energy provider cannot be reached at all
    When I open the course wizard with a stored key
    And I paste the energy key "AIzaBlockedRoad" and check it
    Then the energy step says the key is saved but untested
    And the energy key is on this device

  Scenario: A rejected key is NOT saved
    401 is the one answer that means the key itself is wrong. Saving it
    would send the learner to every desk in the course with a dud.

    Given a stubbed GitHub that accepts the key with repo scope
    And the student can read the vault
    And the energy provider rejects the key
    When I open the course wizard with a stored key
    And I paste the energy key "AIzaWrong" and check it
    Then the energy step reports the rejection with the status code
    And no energy key is on this device

  Scenario: A returning student is not asked for a key they already have
    The wizard reopened step 5 on every visit, whether or not the key was
    still on the device. From the student's chair that IS being asked again.

    Given a stubbed GitHub that accepts the key with repo scope
    And the student can read the vault
    And an energy key "AIzaAlreadyMine" is on this device
    When I open the course wizard with a stored key
    Then the energy step is already done
