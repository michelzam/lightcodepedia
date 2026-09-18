Feature: The agent's bound= knob — legacy pinned, expressions added
  bound= has meant "tie me to a .run editor" since the beginning: every Ask
  carries the editor's code and last output, and a python block in the reply
  grows an Apply button that writes back. Fleet pages depend on it, so the
  legacy path is PINNED here before any new meaning of bound ships. The new
  meaning — bound="{=expr}" evaluates a cell expression and hands the value
  to the model — must coexist without touching the old one.

  Scenario: Legacy — a bound agent carries the editor's code and applies fixes
    Given I have a clean browser page
    And a builder key is connected
    And the recording model endpoint replies with a python fix "print('fixed')"
    When I navigate to "/components/agent"
    And I wait for the page to be interactive
    And I connect the "tutor" agent with key "test-key"
    And I ask the "tutor" agent "help me fix it"
    Then the model request carried the editor code "print('hello'"
    When I apply the agent's fix
    Then the "buggy" editor now holds "print('fixed')"

  Scenario: After the first reply the box invites the next move, not the opening line
    Michel, 2026-09-18: a placeholder that still read Ask "what still
    drifts?" after the Agent had answered told a student to ask it again.
    From the second turn the box says what comes next.

    Given I have a clean browser page
    And a builder key is connected
    And the recording model endpoint replies with a python fix "print('fixed')"
    When I navigate to "/components/agent"
    And I wait for the page to be interactive
    And I connect the "tutor" agent with key "test-key"
    Then the "tutor" agent's box invites the opening line
    When I ask the "tutor" agent "help me fix it"
    Then the "tutor" agent's box invites the next move instead

  Scenario: Expression — bound reads a pad through a cell expression
    Given I have a clean browser page
    And a builder key is connected
    And the recording model endpoint replies with a python fix "ok"
    And the GitHub contents API serves "courses/demo/module_01/bind.md" with the document:
      """
      # Bind page

      ```markdown
      my resume draft, version one
      ```
      {: .mdpad #cv1 rows="4" }

      ```yaml
      system: Review what you are handed.
      ```
      {: .agent #desk bound="{=cv1.source}" rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/bind.md"
    And I wait for the page to be interactive
    And I connect the "desk" agent with key "test-key"
    And I ask the "desk" agent "review it"
    Then the model request carried the editor code "my resume draft, version one"

  Scenario: A provider error speaks its own sentence, even array-wrapped
    Google wraps error JSON in an array; the panel must surface the
    provider's message, not a bare status code.

    Given I have a clean browser page
    And the model endpoint rejects with an array-wrapped 404 saying "models/ghost is not found"
    And the GitHub contents API serves "courses/demo/module_01/err.md" with the document:
      """
      # Err page

      ```yaml
      system: Review.
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/err.md"
    And I wait for the page to be interactive
    And I connect the "desk" agent with key "test-key"
    And I ask the desk agent into the void "hello"
    Then the desk relays "models/ghost is not found"

  Scenario: The two 429 walls are told apart
    A per-minute limit refills by itself; the day's free allowance does not.
    A learner must know which wall they hit. (The day's wall is believed
    only when this browser really spent energy — the zero-spend case is
    the scenario below.)

    Given I have a clean browser page
    And this browser already spent AI energy today
    And the model endpoint answers 429 saying "Quota exceeded for quota metric 'Generate requests per day'"
    And the GitHub contents API serves "courses/demo/module_01/quota.md" with the document:
      """
      # Quota page

      ```yaml
      system: Review.
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/quota.md"
    And I wait for the page to be interactive
    And I connect the "desk" agent with key "test-key"
    And I ask the desk agent into the void "hello"
    Then the desk relays "come back tomorrow"

  Scenario: A day-quota wall over a zero meter is called a suspected spike
    Michel, 2026-08-28: "I used NO energy today!" — yet the desk read the
    day's allowance as spent. The free tier counts REQUESTS per project,
    shared by every device on the key — and demand spikes are shed
    through the same quota door, sometimes at a limit of zero. When our
    own meter reads zero, sentencing the learner to tomorrow is a
    misdiagnosis: say what is actually known.

    Given I have a clean browser page
    And the model endpoint answers 429 saying "Quota exceeded for quota metric 'Generate requests per day'"
    And the GitHub contents API serves "courses/demo/module_01/quota0.md" with the document:
      """
      # Quota page

      ```yaml
      system: Review.
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/quota0.md"
    And I wait for the page to be interactive
    And I connect the "desk" agent with key "test-key"
    And I ask the desk agent into the void "hello"
    Then the desk relays "spent nothing today"

  Scenario: A 403 keeps the key — pasting the same one again would not help
    Michel, 2026-08-05: "it asks every time after a refresh". A 403 means the
    key is valid but not allowed to make THIS call (limited to certain
    websites, service not switched on, a proxy in the way). The old code
    treated it like 401 and DELETED the key, so one 403 at any desk threw
    away what the join door had just saved.

    Given I have a clean browser page
    And an energy key "AIzaKeepMe" is already saved on this device
    And the model endpoint answers with status 403 saying "Requests from referer are blocked."
    And the GitHub contents API serves "courses/demo/module_01/ref.md" with the document:
      """
      # Ref page

      ```yaml
      system: Review.
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/ref.md"
    And I wait for the page to be interactive
    And I ask the desk agent into the void "hello"
    Then the desk relays "Requests from referer are blocked."
    And the energy key is still saved on this device
    And the desk is still connected

  Scenario: A 401 does drop the key, and says why on the form that asks again
    401 is the one answer that means "paste a different key". Dropping it is
    right — but the explanation used to be written into the chat status line,
    which the auth wall hides in the same tick, so the learner was left with
    a paste box carrying no reason at all.

    Given I have a clean browser page
    And an energy key "AIzaStale" is already saved on this device
    And the model endpoint answers with status 401 saying "API key not valid"
    And the GitHub contents API serves "courses/demo/module_01/dead.md" with the document:
      """
      # Dead page

      ```yaml
      system: Review.
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/dead.md"
    And I wait for the page to be interactive
    And I ask the desk agent into the void "hello"
    Then the energy key is gone from this device
    And the desk asks for a key and explains "401"

  Scenario: A saved key opens every desk connected, refresh after refresh
    The whole point of saving it: no paste ceremony on any page, any reload.

    Given I have a clean browser page
    And an energy key "AIzaSaved" is already saved on this device
    And the GitHub contents API serves "courses/demo/module_01/two.md" with the document:
      """
      # Two desks

      ```yaml
      system: One.
      ```
      {: .agent #desk rows="3" }

      ```yaml
      system: Two.
      ```
      {: .agent #desk2 rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/two.md"
    And I wait for the page to be interactive
    Then the desk is still connected
    And every desk on the page is connected
    When I reload the page
    And I wait for the page to be interactive
    Then every desk on the page is connected

  Scenario: The day's AI spend is counted once, wherever it was asked
    A free key is a budget, and until now each panel counted only its own
    session while the docked guide counted nothing — so a learner could burn
    a day across six pages and never see a number (Michel, 2026-08-13).

    Given I have a clean browser page
    And a builder key is connected
    And the recording model endpoint replies with a python fix "ok"
    When I navigate to "/components/agent"
    And I wait for the page to be interactive
    And I connect the "tutor" agent with key "test-key"
    And I ask the "tutor" agent "help me fix it"
    Then the day's ledger counted 1 question
    And the ledger's sentence warns that the free key is limited

  Scenario: A demand spike is ridden out, not handed to the learner
    "This model is currently experiencing high demand… (HTTP 503)" landed
    in front of a class often enough to be the lesson (Michel,
    2026-08-19). A spike lasts seconds; a retry the learner has to invent
    is a retry the desk should have made.

    Given I have a clean browser page
    And the model endpoint 503s once, then answers "the shelter list looks complete"
    And the GitHub contents API serves "courses/demo/module_01/busy.md" with the document:
      """
      # Busy page

      ```yaml
      system: Review.
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/busy.md"
    And I wait for the page to be interactive
    And I connect the "desk" agent with key "test-key"
    And I ask the desk agent into the void "hello"
    Then the desk answers "the shelter list looks complete"

  Scenario: When the spike holds, a second engine the learner already has answers
    The chain is the keys they HOLD — never the providers that exist, or a
    503 becomes a demand for a second signup mid-lesson.

    Given I have a clean browser page
    And the learner also holds an openrouter key
    And the model endpoint always 503s, but openrouter answers "openrouter took it"
    And the GitHub contents API serves "courses/demo/module_01/busy2.md" with the document:
      """
      # Busy page two

      ```yaml
      system: Review.
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/busy2.md"
    And I wait for the page to be interactive
    And I connect the "desk" agent with key "test-key"
    And I ask the desk agent into the void "hello"
    Then the desk offers the other engine and names whose key pays
    When I accept the other engine
    Then the desk answers "openrouter took it"
    And the desk says which engine answered

  Scenario: Nobody's key is spent without them saying so
    A fallback can be a PAID plan (Michel, 2026-08-19: "who might be
    paying?"). Retrying the first engine spends nothing new; switching
    engines is a spending decision, so it is asked — and a No spends
    nothing at all.

    Given I have a clean browser page
    And the learner also holds an openrouter key
    And the model endpoint always 503s, but openrouter answers "openrouter took it"
    And the GitHub contents API serves "courses/demo/module_01/busy3.md" with the document:
      """
      # Busy page three

      ```yaml
      system: Review.
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/busy3.md"
    And I wait for the page to be interactive
    And I connect the "desk" agent with key "test-key"
    And I ask the desk agent into the void "hello"
    And I decline the other engine
    Then no call reached the other engine

  Scenario: The ring lists the engines the repo declares, and any one key opens the desk
    Michel, 2026-09-16: a 503 from the one engine every learner was told
    about, often. The 🔑 is now a ring — every engine docs/bots/providers.yml
    declares, a key for any of them opens the desk.

    Given I have a clean browser page
    And the GitHub contents API serves "courses/demo/module_01/one.md" with the document:
      """
      # One desk

      ```yaml
      system: One.
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/one.md"
    And I wait for the page to be interactive
    Then the desk's ring offers "gemini", "openrouter" and "groq"
    When I paste "gsk_test" as the "groq" key on the desk
    Then the desk is connected through "api.groq.com"

  Scenario: The learner's ★ engine outranks the page's provider
    Given I have a clean browser page
    And keys for "gemini" and "groq" are saved on this device, "groq" answering first
    And every engine answers "hello" and records who was asked
    And the GitHub contents API serves "courses/demo/module_01/one.md" with the document:
      """
      # One desk

      ```yaml
      system: One.
      provider: gemini
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/one.md"
    And I wait for the page to be interactive
    And I ask the "desk" agent "hi"
    Then the question went to "api.groq.com" and never to "generativelanguage.googleapis.com"

  Scenario: A busy ★ engine is answered by the next key on the ring, and the desk says so
    Given I have a clean browser page
    And keys for "gemini" and "groq" are saved on this device, "gemini" answering first
    And "generativelanguage.googleapis.com" answers 503 while "api.groq.com" answers "hello"
    And the GitHub contents API serves "courses/demo/module_01/one.md" with the document:
      """
      # One desk

      ```yaml
      system: One.
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/one.md"
    And I wait for the page to be interactive
    And I ask the "desk" agent "hi", accepting the other engine when offered
    Then the agent says "api.groq.com answered"
    And the question went to "api.groq.com" and never to "generativelanguage.googleapis.com" for the answer

  Scenario: When the next key fails too, the desk says what every engine answered
    Michel, 2026-09-16: OpenRouter accepted, failed, and the desk moved on
    to Groq without a word; the final red line quoted Gemini alone. The
    trail now names every engine tried, in its own words.

    Given I have a clean browser page
    And keys for "gemini" and "groq" are saved on this device, "gemini" answering first
    And "generativelanguage.googleapis.com" answers 503 and "api.groq.com" answers 404 "The model does not exist"
    And the GitHub contents API serves "courses/demo/module_01/one.md" with the document:
      """
      # One desk

      ```yaml
      system: One.
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/one.md"
    And I wait for the page to be interactive
    And I ask the "desk" agent "hi", accepting the other engine, and it fails too
    Then the agent's trail names "generativelanguage.googleapis.com" and "api.groq.com: The model does not exist"

  Scenario: A model the ring names is gone: the engine's own list is asked, and the choice remembered
    Michel, 2026-09-16, the trail: OpenRouter "this model is unavailable for
    free", Groq "the model does not exist". Presets rot; the engine knows
    what it serves. A 404 asks /models once, takes the ring's next
    preference, and the desk says so.

    Given I have a clean browser page
    And keys for "gemini" and "groq" are saved on this device, "groq" answering first
    And "api.groq.com" serves only "llama-3.1-8b-instant" and answers "healed hello" on it
    And the GitHub contents API serves "courses/demo/module_01/one.md" with the document:
      """
      # One desk

      ```yaml
      system: One.
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/one.md"
    And I wait for the page to be interactive
    And I ask the "desk" agent "hi"
    Then the desk answered "healed hello" with the model "llama-3.1-8b-instant"
    And the agent says "llama-3.3-70b-versatile is gone; using llama-3.1-8b-instant"
    And the device remembers "llama-3.1-8b-instant" for "groq"
