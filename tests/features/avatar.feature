Feature: Avatar — speaking overlay instructor

  Background:
    Given I have a clean browser page

  Scenario: Avatar examples page loads without errors
    When I navigate to "/components/examples/avatar"
    And I wait for the page to be interactive
    Then the LC platform is loaded
    And there are no JS console errors

  Scenario: The avatar overlay character appears
    When I navigate to "/components/examples/avatar"
    And I wait for the page to be interactive
    Then the avatar overlay "prof_avatar" is visible

  Scenario: The trigger starts the avatar speaking
    When I navigate to "/components/examples/avatar"
    And I wait for the page to be interactive
    And I click the avatar trigger for "prof_avatar"
    Then the avatar trigger for "prof_avatar" shows the stop label
    And the avatar "prof_avatar" is in the "speaking" state

  Scenario: Clicking the trigger again stops the avatar
    When I navigate to "/components/examples/avatar"
    And I wait for the page to be interactive
    And I click the avatar trigger for "prof_avatar"
    And I click the avatar trigger for "prof_avatar"
    Then the avatar "prof_avatar" is in the "idle" state

  Scenario: A Rive state-machine character renders on canvas
    When I navigate to "/components/examples/avatar"
    And I wait for the page to be interactive
    Then the avatar overlay "riv_avatar" is visible
    And the avatar "riv_avatar" shows a "canvas.lc-avatar-rive" character

  Scenario: A Rive narrator guides the Lucky and Wanda playground
    When I navigate to "/components/examples/lucky3d"
    And I wait for the page to be interactive
    Then the avatar overlay "lucky_guide" is visible
    And the avatar "lucky_guide" shows a "canvas.lc-avatar-rive" character

  Scenario: X-ray identifies the Avatar component
    When I navigate to "/components/examples/avatar"
    And I wait for the page to be interactive
    And I hover over the avatar overlay "prof_avatar"
    Then an x-ray panel is visible
    And the x-ray panel mentions "Avatar"

  Scenario: The guide asks for the AI key, not a GitHub token
    The docked guide shares the agents' brain, so it must ask for the same
    key under the same keychain identity — otherwise the browser cannot
    offer the one saved at the join door, and the learner is told to paste
    a GitHub token at a Google service.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/guide.md" with the document:
      """
      # Guided page

      Some prose.

      ```yaml
      bot: doc
      script:
        - say: "Hello."
      stories: {}
      ```
      {: .avatar #guide dock="true" size="115" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/guide.md"
    And I wait for the page to be interactive
    And I open the guide's ask panel
    Then the key prompt names the AI provider, not GitHub
    And the saved-password identity matches the agents'

  Scenario: A docked idle guide is untouchable, not just invisible
    The hidden big face kept its click handler while docked — an invisible
    circle floating over the page, and a Next button underneath started
    the tour instead of navigating. Invisible means untouchable.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/guide.md" with the document:
      """
      # Guided page

      Some prose.

      ```yaml
      bot: doc
      script:
        - say: "Hello."
      stories: {}
      ```
      {: .avatar #guide dock="true" size="115" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/guide.md"
    And I wait for the page to be interactive
    And I click where the hidden avatar face sits
    Then the avatar did not start playing
