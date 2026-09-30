Feature: 🎬 Short next walk — Doc walks, the page records itself
  Michel, 2026-09-20: one checkable line in Doc's menu, for the page's
  owner only. Tick it, play a tour or a story, and the walk is captured
  from its first line to its last inside a phone frame — the page itself
  becomes the 9:16 column, Doc in it, so what is on screen is the clip —
  reviewed in a dialog, uploaded unlisted on demand, and — if asked — embedded on the
  page in a folded "🎬 Shorts" accordion. The tick goes away after one
  walk. The tab capture and the upload are the browser's and YouTube's;
  the suite hands in a painted canvas and stub endpoints instead.

  Background:
    Given I have a clean browser page
    And the tab capture is stubbed with a painted canvas
    And the YouTube upload is stubbed

  Scenario: The owner ticks the line, walks a story, and the Short lands on the page
    Given a marked shim is preinstalled
    And a builder key and editor repo are connected
    And the viewer can push to "acme/demo"
    And the committable GitHub page "courses/demo/mod/short.md" serves:
      """
      # Walked page

      ## One

      Some prose.

      ## Two

      More prose.

      ```yaml
      bot: doc
      script: []
      stories:
        "Say hi":
          - say: "Hello there."
            pause: 1
          - say: "Bye now."
            pause: 1
      ```
      {: .avatar #guide dock="true" size="115" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/short.md"
    And I wait for the page to be interactive
    Then the guide's menu offers "🎬 Short next walk"
    When I tick "🎬 Short next walk" in the guide's menu
    Then the page is in reel mode
    And the page wears the phone frame
    When I pick "Say hi" from the guide's menu
    Then the voice was blessed before the capture prompt
    And the Short review dialog shows the clip
    And the take is held, an end card on offer for "/run.html#src=gh:acme/demo/courses/demo/mod/short.md"
    When I upload the Short, embedded on this page
    Then the Short went to YouTube unlisted
    And the Short's description says where to watch more
    And the take is released
    And "courses/demo/mod/short.md" now carries a folded Shorts accordion with Short 1
    When I close the Short dialog
    Then the phone frame is off
    And the guide's menu shows "🎬 Short next walk" unticked

  Scenario: A second Short joins the same accordion
    Given a marked shim is preinstalled
    And a builder key and editor repo are connected
    And the viewer can push to "acme/demo"
    And the committable GitHub page "courses/demo/mod/short2.md" serves:
      """
      # Walked page

      ## One

      Some prose.

      ## Two

      More prose.

      ```yaml
      bot: doc
      script: []
      stories:
        "Say hi":
          - say: "Hello there."
            pause: 1
          - say: "Bye now."
            pause: 1
      ```
      {: .avatar #guide dock="true" size="115" }

      ```
      ### 🎬 Short 1 · 2026-09-19

      [▶️ Short 1](https://youtu.be/first111)
      {: .video }

      ```
      {: .accordion #shorts }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/short2.md"
    And I wait for the page to be interactive
    And I tick "🎬 Short next walk" in the guide's menu
    And I pick "Say hi" from the guide's menu
    Then the Short review dialog shows the clip
    When I upload the Short, embedded on this page
    Then "courses/demo/mod/short2.md" now carries a folded Shorts accordion with Short 2

  Scenario: A learner never sees the line
    Every learner holds a key (their bench saves with it); the line is the
    owner's, and ownership is what author mode already checks.

    Given a marked shim is preinstalled
    And a builder key and editor repo are connected
    And the viewer cannot push to "acme/demo"
    And the committable GitHub page "courses/demo/mod/short3.md" serves:
      """
      # Walked page

      ## One

      Some prose.

      ## Two

      More prose.

      ```yaml
      bot: doc
      script: []
      stories:
        "Say hi":
          - say: "Hello there."
            pause: 1
          - say: "Bye now."
            pause: 1
      ```
      {: .avatar #guide dock="true" size="115" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/short3.md"
    And I wait for the page to be interactive
    Then the guide's menu does not offer "🎬 Short next walk"

  Scenario: The embedded accordion renders folded, the clip inside
    Given the GitHub contents API serves "courses/demo/mod/short4.md" with the document:
      """
      # Walked page

      Some prose.

      ```
      ### 🎬 Short 1 · 2026-09-20

      [▶️ Short 1](https://youtu.be/stub1234)
      {: .video }

      ```
      {: .accordion #shorts }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/short4.md"
    And I wait for the page to be interactive
    Then the Shorts accordion is folded
    When I unfold the Shorts accordion
    Then the Short plays inside it

  Scenario: A walk longer than a Short is not cut — it uploads as a video
    Michel, 2026-09-30, the four-minute slam: "Cut at 2:57" threw the take
    away. The limit is YouTube's word Short, not ours: the take keeps going,
    the review says it is longer than a Short, and it uploads unlisted as a
    regular video. The suite shortens the Short limit to two seconds.

    Given a marked shim is preinstalled
    And a builder key and editor repo are connected
    And the viewer can push to "acme/demo"
    And the Short limit is 2 seconds for this test
    And the committable GitHub page "courses/demo/mod/long.md" serves:
      """
      # Walked page

      ## One

      Some prose.

      ```yaml
      bot: doc
      script: []
      stories:
        "Say hi":
          - say: "Hello there."
            pause: 2
          - say: "Bye now."
            pause: 2
      ```
      {: .avatar #guide dock="true" size="115" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/long.md"
    And I wait for the page to be interactive
    And I tick "🎬 Short next walk" in the guide's menu
    And I pick "Say hi" from the guide's menu
    Then the Short review dialog shows the clip
    And the review says the clip is longer than a Short
    When I upload the Short, embedded on this page
    Then the upload was titled as a walk, not a Short

  Scenario: A share without tab audio is named, not discovered in the file
    Michel, 2026-09-30: "why is the sound not present anymore in those
    downloaded shorts?" Chrome records tab audio only for a tab with
    "Share tab audio" ticked. The suite's painted canvas carries no audio:
    the review must say so.

    Given a marked shim is preinstalled
    And a builder key and editor repo are connected
    And the viewer can push to "acme/demo"
    And the committable GitHub page "courses/demo/mod/mute.md" serves:
      """
      # Walked page

      ## One

      Some prose.

      ```yaml
      bot: doc
      script: []
      stories:
        "Say hi":
          - say: "Hello there."
            pause: 1
      ```
      {: .avatar #guide dock="true" size="115" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/mute.md"
    And I wait for the page to be interactive
    And I tick "🎬 Short next walk" in the guide's menu
    And I pick "Say hi" from the guide's menu
    Then the Short review dialog shows the clip
    And the review says the share had no tab audio

  Scenario: A share with tab audio is marked as such
    Given the tab capture is stubbed with a painted canvas and a tone
    And a marked shim is preinstalled
    And a builder key and editor repo are connected
    And the viewer can push to "acme/demo"
    And the committable GitHub page "courses/demo/mod/loud.md" serves:
      """
      # Walked page

      ## One

      Some prose.

      ```yaml
      bot: doc
      script: []
      stories:
        "Say hi":
          - say: "Hello there."
            pause: 1
      ```
      {: .avatar #guide dock="true" size="115" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/loud.md"
    And I wait for the page to be interactive
    And I tick "🎬 Short next walk" in the guide's menu
    And I pick "Say hi" from the guide's menu
    Then the Short review dialog shows the clip
    And the review says the share carried tab audio
