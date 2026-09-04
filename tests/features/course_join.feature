Feature: The learner course wizard (/courses/join)

  The dedicated learner journey — distinct from /start (the builder journey).
  Account → course key → live access check against the vault → open the course.

  Background:
    Given I have a clean browser page

  Scenario: The content door forwards to the course root
    One short address for the LMS iframe (Michel, 2026-08-25) — the door
    rewrites /go into the runner's full incantation; the runner still
    demands the visitor's own key, so the door guards nothing.

    When I open the content door "/go"
    Then the runner is asked for "courses/micro_build_ai/index.md"

  Scenario: The content door forwards a named lesson, md optional
    When I open the content door "/go?p=module_00/00_welcome"
    Then the runner is asked for "courses/micro_build_ai/module_00/00_welcome.md"

  Scenario: The door bakes the learner flags
    Focus, the crumb and the open scope ride INSIDE the door — that is
    what keeps the LMS line short. A query param still overrides its own
    default.

    When I open the content door "/go"
    Then the runner carries the baked learner flags
    And the landing wears the learner chrome, not the platform
    And no retired pencil floats over the lesson

  Scenario: A course page in the frame offers no way into edit mode
    Course material in a teacher's frame is READ-ONLY — the editor opened
    on it empty and useless (2026-08-18). The door was baking editable=1,
    which is the one thing that overrides that rule, so a visitor with no
    key at all could still switch the Canvas view into edit mode (Michel,
    2026-08-30, Firefox). The door says nothing about editing now; the
    rule decides.

    When I open the content door "/go"
    Then the edit door is closed, and it says why

  Scenario: An explicit editable still opens the door
    The escape hatch survives: whoever writes ?editable=1 means it.

    When I open the content door "/go?editable=1"
    Then the edit door is open

  Scenario: The content door never climbs out of the course
    When I open the content door "/go?p=../../evil"
    Then the runner is asked for "courses/micro_build_ai/evil.md"

  Scenario: A fresh learner sees step 1 active and the rest waiting
    When I open the course wizard
    Then join step 1 is active and steps 2 and 3 are off

  Scenario: A valid course key advances to the enrollment check
    Given a stubbed GitHub that accepts the key with repo scope
    When I open the course wizard
    And I confirm I have an account
    And I paste the course key "ghp_newkey" and check it
    Then join steps 1 and 2 are done and step 3 is active

  Scenario: An enrolled learner is told they are in — and setup goes on
    Setup ends at setup (Michel, 2026-08-30). Two doors used to lead out of
    the middle of the wizard — one into the whole course at step 3, one into
    the bench at step 4 — both before the learner had their AI key, and the
    course one opened all eight modules at once. The wizard says where you
    stand and nothing else; the course is entered from the LMS.

    Given a stubbed GitHub that accepts the key with repo scope
    And the learner can read the vault
    When I open the course wizard with a stored key
    Then the wizard says the learner is in
    And the wizard offers no way out of setup

  Scenario: A not-yet-enrolled learner is guided to their invitation
    Given a stubbed GitHub that accepts the key with repo scope
    When I open the course wizard with a stored key
    And I check my access
    Then the wizard guides to the invitation, not an error dump

  Scenario: Accepting the invitation in-app opens the course
    Given a stubbed GitHub that accepts the key with repo scope
    When I open the course wizard with a stored key
    And I accept my invitation in the wizard
    Then the wizard says the learner is in
    And the wizard offers no way out of setup

  Scenario: A missing bench is a message, never a button
    The DESK is the one bench builder (A′, Michel 2026-08-25): the
    teacher's Sync forges the fork and the grants in one press. The
    wizard only ever finds, opens and refreshes a bench — so with none
    there yet, it says who builds it and asks GitHub for nothing.

    Given a stubbed GitHub that accepts the key with repo scope
    And the learner can read the vault
    When I open the course wizard with a stored key
    Then the bench step says the teacher's desk builds it
    And no repository was created by the wizard

  Scenario: Last term's session is never adopted
    The wizard used to take "the newest template in the org" for the class
    it was in. A teacher who taught last term (Michel, 2026-08-31) opened
    fall26's Module 00 in Canvas and got summer26: the dogs came back
    already repaired, from the OLD bench, and Save filed this year's work
    there without a word. The class is named — by the door, or by the
    page — never guessed.

    Given a stubbed GitHub that accepts the key with repo scope
    And the learner can read the vault
    And last term's session is still in the org
    And this device is still paired to last term's bench
    When I open the course wizard with a stored key
    Then the bench step names the session "build-ai-fall26"
    And this device is paired to no bench

  Scenario: Last term's bench is not usable on this session's page
    The pairing is stamped with the class it was made for, and every
    save="my/…" reads that stamp: a page framed for THIS session refuses a
    bench from another one instead of writing into it silently.

    Given this device is still paired to last term's bench
    When I open a saving lesson framed for "build-ai-fall26"
    Then the keep button says the bench for this session is not paired

  Scenario: A pairing from before the stamp is not this class's bench
    A pairing made before the stamp names no class — so against a page that
    names one it is exactly as unproven as another session's, and is refused
    the same way. On a page that names no class it still stands: refusing
    everything unstamped once cost 29 saves in one suite and the author his
    own bench (2026-09-02).

    Given this device carries a pairing from before the stamp
    When I open a saving lesson framed for "build-ai-fall26"
    Then the keep button says the bench for this session is not paired

  Scenario: A page that names no class keeps the bench it was given
    Given this device carries a pairing from before the stamp
    When I open a saving lesson with no session in its address
    Then the keep button is armed

  Scenario: A desk-built bench is found and named, with no door out of setup
    The wizard tells the learner their bench exists and is current. It does
    not open it: the ?go=bench forward below is the one that opens a bench —
    asked for by the bench menu, never offered mid-setup.

    Given a stubbed GitHub that accepts the key with repo scope
    And the learner can read the vault
    And my bench exists and is 0 updates behind the hub
    When I open the course wizard with a stored key
    Then my bench shows up to date with the hub
    And the wizard offers no way out of setup

  Scenario: A bench behind the hub shows the gap and syncs
    Given a stubbed GitHub that accepts the key with repo scope
    And the learner can read the vault
    And my bench exists and is 2 updates behind the hub
    When I open the course wizard with a stored key
    Then the bench shows 2 updates to sync
    When I sync my bench
    Then my bench shows up to date with the hub

  Scenario: The course door forwards a green learner into the bench
    Given a stubbed GitHub that accepts the key with repo scope
    And the learner can read the vault
    And my bench exists and is 0 updates behind the hub
    When I open the course door "?go=bench&hub=build-ai-fall26" with a stored key
    Then I am forwarded into my bench

  Scenario: A pending sync holds the door open on the wizard
    Given a stubbed GitHub that accepts the key with repo scope
    And the learner can read the vault
    And my bench exists and is 2 updates behind the hub
    When I open the course door "?go=bench&hub=build-ai-fall26" with a stored key
    Then the bench shows 2 updates to sync

  Scenario: The door names a session the learner cannot see
    Given a stubbed GitHub that accepts the key with repo scope
    And the learner can read the vault
    When I open the course door "?go=bench&hub=ghost-session" with a stored key
    Then the bench step explains the session is not visible

  Scenario: The door holds for refresh when the bench lacks the new root
    Given a stubbed GitHub that accepts the key with repo scope
    And the learner can read the vault
    And my bench exists and is 0 updates behind the hub
    And my bench has no index yet
    When I open the course door "?go=bench&hub=build-ai-fall26" with a stored key
    Then the bench step invites a refresh

  Scenario: The energy key gets a live check and a save-as-password moment
    Given a stubbed GitHub that accepts the key with repo scope
    And the learner can read the vault
    And the energy provider accepts the key
    When I open the course wizard with a stored key
    And I paste the energy key "AIzaTestKey" and check it
    Then the energy step confirms the key works and will follow the learner

  Scenario: A rejected energy key says rejected, not broken
    Given a stubbed GitHub that accepts the key with repo scope
    And the learner can read the vault
    And the energy provider rejects the key
    When I open the course wizard with a stored key
    And I paste the energy key "AIzaWrong" and check it
    Then the energy step reports the rejection with the status code

  Scenario: A resolved bench completes the connection pair
    Step 2 stores the key; the bench resolving is when its repo half
    becomes known. Without pairing them, every save="my/…" aimed at
    whatever repo was lying around from an earlier life — the author's
    site on a teacher's browser, nothing at all on a learner's — and the
    key answered 404 for a repo it was never meant to cover.

    Given a stubbed GitHub that accepts the key with repo scope
    And the learner can read the vault
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
    And the learner can read the vault
    And the energy provider will not let us test the key
    When I open the course wizard with a stored key
    And I paste the energy key "AIzaRestricted" and check it
    Then the energy step says the key is saved but untested
    And the energy key is on this device

  Scenario: A key is kept when the road is blocked, not thrown away
    An ad-blocker, VPN or firewall eating the request is not evidence
    against the key. Keep it — that is the whole point of saving it once.

    Given a stubbed GitHub that accepts the key with repo scope
    And the learner can read the vault
    And the energy provider cannot be reached at all
    When I open the course wizard with a stored key
    And I paste the energy key "AIzaBlockedRoad" and check it
    Then the energy step says the key is saved but untested
    And the energy key is on this device

  Scenario: A rejected key is NOT saved
    401 is the one answer that means the key itself is wrong. Saving it
    would send the learner to every desk in the course with a dud.

    Given a stubbed GitHub that accepts the key with repo scope
    And the learner can read the vault
    And the energy provider rejects the key
    When I open the course wizard with a stored key
    And I paste the energy key "AIzaWrong" and check it
    Then the energy step reports the rejection with the status code
    And no energy key is on this device

  Scenario: A returning learner is not asked for a key they already have
    The wizard reopened step 5 on every visit, whether or not the key was
    still on the device. From the learner's chair that IS being asked again.

    Given a stubbed GitHub that accepts the key with repo scope
    And the learner can read the vault
    And an energy key "AIzaAlreadyMine" is on this device
    When I open the course wizard with a stored key
    Then the energy step is already done

  Scenario: The wizard never creates the bay — that is the teacher's act
    Bays are provisioned from the classroom console with the org key
    (Michel, 2026-08-15: "WE create the public repo for each student").
    A learner-side creation would need the org to let every member create
    public repositories — a wide-open door so one repo could exist. So the
    wizard pairs the bench and asks GitHub for nothing else.

    Given a stubbed GitHub that accepts the key with repo scope
    And the learner can read the vault
    And my bench exists and is 0 updates behind the hub
    When I open the course wizard with a stored key
    Then no repository was created by the wizard

  Scenario: The seat is read from the key and written into the bench — nothing typed
    Nobody types a login: the key already says who they are (Michel,
    2026-09-04). With user:email on the key, the wizard reads the learner's
    verified address too, and once the bench is found it writes email ↔
    login into the bench as __seat.yml — the teacher's desk reads it back
    after any reload. The learner saw one extra scope in a link, and no field.

    Given a stubbed GitHub that accepts the key with repo scope
    And the learner can read the vault
    And GitHub knows the learner's verified email "zamm-student@uwm.edu"
    And my bench exists and is 0 updates behind the hub
    When I open the course wizard
    And I confirm I have an account
    And I paste the course key "ghp_valid" and check it
    Then the wizard says the learner is in
    And the seat field is not shown
    And the bench carries a seat file naming "zamm-student@uwm.edu" and "zamm-student"

  Scenario: Without the email scope the wizard asks once, then writes the seat
    A key made before the scope existed cannot tell the address, so step 3
    shows one field, the address the invitation came to, exactly once.

    Given a stubbed GitHub that accepts the key with repo scope
    And the learner can read the vault
    And GitHub will not tell the learner's email
    And my bench exists and is 0 updates behind the hub
    When I open the course wizard
    And I confirm I have an account
    And I paste the course key "ghp_valid" and check it
    Then the wizard says the learner is in
    And the seat field is shown
    When I type the seat email "zamm-student@uwm.edu" and save it
    Then the bench carries a seat file naming "zamm-student@uwm.edu" and "zamm-student"
