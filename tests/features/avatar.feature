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

  Scenario: A tap on the playing face holds the tour, never kills it
    Michel, 2026-08-25: replace killing with pause. The face freezes at
    its line, the bubble stays, and the little remote floats in — prev,
    play, next, replay — gone again the moment it speaks. The trigger
    keeps its stop.

    When I navigate to "/components/examples/avatar"
    And I wait for the page to be interactive
    And I click the avatar trigger for "prof_avatar"
    And I tap the avatar face "prof_avatar"
    Then the avatar "prof_avatar" is in the "paused" state
    And the paused remote of "prof_avatar" offers prev, play, next and replay
    When I press "play" on the paused remote of "prof_avatar"
    Then the avatar "prof_avatar" is in the "speaking" state
    And the paused remote of "prof_avatar" is hidden

  Scenario: The remote steps the held tour forward
    When I navigate to "/components/examples/avatar"
    And I wait for the page to be interactive
    And I click the avatar trigger for "prof_avatar"
    And I tap the avatar face "prof_avatar"
    And I press "next" on the paused remote of "prof_avatar"
    Then the avatar "prof_avatar" is in the "speaking" state

  Scenario: The speaking guide outranks the platform chrome
    The bubble slid UNDER the topbar on a phone (Michel, 2026-08-25) —
    the guide is always foreground; only the editor drawer outranks it.

    When I navigate to "/components/examples/avatar"
    And I wait for the page to be interactive
    Then the avatar overlay "prof_avatar" rides above the topbar

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

  Scenario: A cut-off answer is spoken but never filed
    The model stopped at max_tokens, and 📌 kept the fragment anyway — a half
    sentence ("It outlines a") and the ⚠️ notice itself landed in the page's
    stories and got voiced (2026-08-07). Showing half an answer and FILING
    half an answer are different decisions.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And an energy key "gem_stub" is already saved on this device
    And the "doc" bot is available
    And the editor is connected as the author
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
    And the model endpoint stops mid-answer with "The page introduces a course. It outlines a"
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/guide.md"
    And I wait for the page to be interactive
    And I ask the guide "Summarize this page"
    Then the guide does not offer to keep the answer
    And the guide never says "cut off"

  Scenario: A complete answer is still offered for keeping
    The control for the scenario above: 📌 must disappear because the answer
    was truncated, not because keeping quietly broke.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And an energy key "gem_stub" is already saved on this device
    And the "doc" bot is available
    And the editor is connected as the author
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
    And the model endpoint answers in full with "The page introduces a course."
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/guide.md"
    And I wait for the page to be interactive
    And I ask the guide "Summarize this page"
    Then the guide offers to keep the answer

  Scenario: A wobbling model hands the guide a 🔁 chip, and one tap recovers
    Doc answered "high demand… (HTTP 503)" and stopped there (Michel,
    2026-08-26) — the learner's only road back was reopening the panel
    to retype the question. A retry the learner has to invent is a
    retry the button should have made (the publish button learned this
    2026-08-06): a wobble gets a 🔁 chip under the face; one tap asks
    the same question again. Real refusals (401/403) stay final.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And an energy key "gem_stub" is already saved on this device
    And the "doc" bot is available
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
    And the model endpoint wobbles out, then answers in full with "Nine families are waiting."
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/guide.md"
    And I wait for the page to be interactive
    And I ask the guide "Why the hurry?"
    Then the guide offers the retry chip with a warning
    When I tap the guide's retry chip
    Then the guide speaks "families" and the chip is gone

  Scenario: A quota wall over a zero meter gets the chip too
    Michel, 2026-08-28: "I used NO energy today!" — yet the guide read
    the day as spent. Demand spikes are shed through the quota door,
    sometimes at a limit of zero; with our own meter at zero the honest
    verdict is a suspected spike, and a suspected spike is worth a 🔁 —
    not a sentence to tomorrow.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And an energy key "gem_stub" is already saved on this device
    And the "doc" bot is available
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
    And the model endpoint answers the day-quota wall once, then in full with "Nine families are waiting."
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/guide.md"
    And I wait for the page to be interactive
    And I ask the guide "Why the hurry?"
    Then the guide speaks "spent nothing today"
    And the guide offers the retry chip with a warning
    When I tap the guide's retry chip
    Then the guide speaks "families" and the chip is gone

  Scenario: A recording made on one mount plays back on another
    The voice manifest keys recordings by the rendered file's MOUNT path.
    One course mounts at courses/… in the lab, at course/… on every learner
    bench, with older pathname islands like "micro_build_ai" alongside. So a
    voice recorded in the lab was unreachable from every bench: the mp3s sat
    in the repo while the guide spoke robot TTS (the volunteer bench,
    2026-08-08). Recordings are content-addressed by the line's text, so a
    slug miss must fall back to finding the line anywhere in the manifest.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "course/mod/guide.md" with the document:
      """
      # Bench page

      Some prose.

      ```yaml
      script:
        - say: "Hello builders."
      ```
      {: .avatar #guide }

      [▶ Play](#)
      {: .avatar_trigger target="guide" }
      """
    And the voice manifest maps "Hello builders." to "lc-test-voice.mp3" under the mount "courses-demo-mod-guide" for avatar "guide"
    And the studio file "lc-test-voice.mp3" is served
    When I navigate to "/run.html#src=gh:acme/demo/course/mod/guide.md"
    And I wait for the page to be interactive
    And I click the avatar trigger for "guide"
    Then the avatar "guide" speaks from the studio file "lc-test-voice.mp3"

  Scenario: A recording under the page's own mount still plays
    The control for the scenario above: exact-slug resolution must keep
    winning before any cross-mount fallback.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "course/mod/guide.md" with the document:
      """
      # Bench page

      Some prose.

      ```yaml
      script:
        - say: "Hello builders."
      ```
      {: .avatar #guide }

      [▶ Play](#)
      {: .avatar_trigger target="guide" }
      """
    And the voice manifest maps "Hello builders." to "lc-test-voice.mp3" under the mount "course-mod-guide" for avatar "guide"
    And the studio file "lc-test-voice.mp3" is served
    When I navigate to "/run.html#src=gh:acme/demo/course/mod/guide.md"
    And I wait for the page to be interactive
    And I click the avatar trigger for "guide"
    Then the avatar "guide" speaks from the studio file "lc-test-voice.mp3"

  Scenario: The guide says whose Doc is answering
    An editor key in the browser makes the guide answer as the AUTHOR's:
    direct, complete, nothing withheld (doctrine 7). Michel read that on a
    quiz page as the tutor leaking answers to learners — it was his own key.
    So the panel says which one is talking (Michel, 2026-08-13).

    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key is connected
    And the AI provider key is connected
    And the "doc" bot is available
    And the GitHub contents API serves "courses/demo/mod/guide2.md" with the document:
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
    And the viewer can push to "acme/demo"
    And the model endpoint answers in full with "1. Here you go."
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/guide2.md"
    And I wait for the page to be interactive
    And I open the guide's ask panel
    Then the ask panel says it is in author mode
    And the ask panel shows the day's AI spend
    When I ask "What is the answer?" in the open panel
    Then the question reached the model with the author's licence

  Scenario: A learner's own key does not make them the author
    Every learner holds an editor key — it is how their bench saves — so
    "a key is present" made every learner an author and handed them the
    direct answers. Michel, reading a course page in Canvas signed in as
    zamm-student, 2026-08-13: "I'm surprised to see I'm author". Ownership
    of the material decides, and it fails closed.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And a learner key is connected to their own bench
    And the AI provider key is connected
    And the "doc" bot is available
    And the viewer cannot push to "acme/demo"
    And the model endpoint answers in full with "1. What do you think?"
    And the GitHub contents API serves "courses/demo/mod/guide3.md" with the document:
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
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/guide3.md"
    And I wait for the page to be interactive
    And I open the guide's ask panel
    Then the ask panel is not in author mode
    And the ask panel shows the day's AI spend
    When I ask "What is the answer?" in the open panel
    Then the question reached the model without the author's licence
