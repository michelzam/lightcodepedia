Feature: 🚀 Ship — the author-designed deployment component

  Shipping is a course element, not a platform permission (Michel,
  2026-08-15). The author places {: .ship app= files= bay= } on the
  assignment page; the learner's own key copies the named files into the
  public bay under <app>_<sha>/, writes the bay manifest, and a runner
  embed with src="ship:<app>" renders the deployed copy on the same page —
  the proof that deployment worked is the app itself, not a toast.

  Background:
    Given I have a clean browser page
    And a marked shim is preinstalled

  Scenario: Without a key the ship button stays disarmed, and says why
    Given the GitHub contents API serves "courses/demo/assignment.md" with the document:
      """
      # Assignment

      [Ship it](#)
      {: .ship app="spike_dogs" files="_ship_app.md" bay="acme/bay/bays" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/assignment.md"
    And I wait for the page to be interactive
    Then the ship button is disarmed with a reason

  Scenario: Pressing ship copies the files and writes the manifest
    Given I am signed in with a course key
    And the GitHub contents API serves "courses/demo/assignment.md" with the document:
      """
      # Assignment

      [Ship it](#)
      {: .ship app="spike_dogs" files="_ship_app.md" bay="acme/bay/bays" }
      """
    And the GitHub contents API serves "courses/demo/_ship_app.md" with the document:
      """
      # 🐕 Spike dogs

      Twelve dogs, none invisible.
      """
    And the bench HEAD commit is "cafebabe12345678"
    And the bay accepts writes
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/assignment.md"
    And I wait for the page to be interactive
    And I press the ship button
    Then the bay received "bays/spike_dogs_cafebabe12345678/_ship_app.md"
    And the bay manifest now points "spike_dogs" at "cafebabe12345678"
    And the ship button reports the shipped link

  Scenario: A pending bay invitation is accepted on the fly, and the ship completes
    A collaborator grant can land as a pending invitation instead of a
    direct one — the bay exists, push was granted, and the PUT still says
    404 (zamm-student, 2026-08-15). The learner's key can accept its own
    invitations, so the button must: sweep, accept, retry.

    Given I am signed in with a course key
    And the GitHub contents API serves "courses/demo/assignment.md" with the document:
      """
      # Assignment

      [Ship it](#)
      {: .ship app="spike_dogs" files="_ship_app.md" bay="acme/bay/bays" }
      """
    And the GitHub contents API serves "courses/demo/_ship_app.md" with the document:
      """
      # 🐕 Spike dogs

      Twelve dogs, none invisible.
      """
    And the bench HEAD commit is "cafebabe12345678"
    And the bay requires an accepted invitation before it takes writes
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/assignment.md"
    And I wait for the page to be interactive
    And I press the ship button
    Then the bay invitation was accepted
    And the bay received "bays/spike_dogs_cafebabe12345678/_ship_app.md"
    And the ship button reports the shipped link

  Scenario: A ship: embed renders the latest shipped copy, keyless
    Given the bay manifest points "spike_dogs" at "cafebabe12345678" with entry "_ship_app.md"
    And the bay serves "bays/spike_dogs_cafebabe12345678/_ship_app.md" with the document:
      """
      # 🐕 Spike dogs

      Twelve dogs, none invisible.
      """
    And the GitHub contents API serves "courses/demo/assignment.md" with the document:
      """
      # Assignment

      [My shipped app](#)
      {: .runner src="ship:spike_dogs" bay="acme/bay/bays" title="" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/assignment.md"
    And I wait for the page to be interactive
    Then the ship embed renders "Twelve dogs, none invisible"

  Scenario: Before any ship, the embed waits politely instead of erroring
    Given the bay has no manifest
    And the GitHub contents API serves "courses/demo/assignment.md" with the document:
      """
      # Assignment

      [My shipped app](#)
      {: .runner src="ship:spike_dogs" bay="acme/bay/bays" title="" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/assignment.md"
    And I wait for the page to be interactive
    Then the ship embed says nothing is shipped yet
