Feature: A crew — agents as the rows of a dataset, a loop with its bounds
  Michel, 2026-10-23: "data-driven dynamic instances initiated by a simple
  dataset … encapsulated, declarative, with clear bounds (costs, loops)" →
  "go crew". The members are rows; .crew runs them over an inbox: the rules
  first, then a reader checked by a checker, a disagreement sent back with
  the checker's words, at most tries= a message and budget= AI asks, and
  fallback= for what stays open. It writes <id>.sorted, <id>.flow and
  <id>.log only. Michel, 2026-10-24: "stage instead of lane, to remain
  consistent with the previous module" — each message's row carries its
  family's current_stage (asked, met, home); then "the semantics of next
  stage is recommendation" — the crew writes the action it recommends,
  module 06's verbs: meet, adopt, call.

  Scenario: The desk loops — Rey says adopt, Chuck disagrees, Rey says meet; the rules sort the rest for free
    Given I have a clean browser page
    And an energy key "AIza-crew-test" is already saved on this device
    And the AI answers as Rey and Chuck, Rey wrong the first time
    When I navigate to "/components/crew"
    # the page's proof is there to read and ▶ (Michel, 2026-10-24, on pedia: "the proof is empty…")
    Then the proof "crew_proof" can be read on the page
    And the proof "crew_proof" wears the tag "ai"
    # the whole inbox from the start, then a row at a time, the row at work selected (Michel, 2026-10-23)
    Then the crew "desk" shows its 3 messages, none sorted yet
    # who is an AI agent, at a glance (Michel, 2026-10-24: "it's not clear which one is a LLM agent, specially for chuck!")
    And the crew "desk" shows "Sid" as Python, "Rey" and "Chuck" as AI agents
    When I press ▶ Run on the crew "desk"
    Then the crew "desk" is done
    # the crew is an agent: its desk, closed while a key is held (Michel, 2026-10-24)
    And the crew "desk" shows its desk, closed
    And the grid of the crew "desk" has "Ferraro" selected
    And the crew "desk" sorted "Nguyen" as "meet" in 0 tries
    And the crew "desk" sorted "Okafor" as "adopt" in 0 tries
    And the crew "desk" sorted "Ferraro" as "meet" in 2 tries
    And the crew "desk" asked the AI 4 times
    # tokens, globally and by step (Michel, 2026-10-23: "show the token consumption")
    And the crew "desk" spent 48 tokens, 12 on each AI step
    # an agent's own token line, and the why of each stage (Michel, 2026-10-24)
    And the crew "desk" shows its tokens as an agent does: "Session: 48 tokens · this run: 48"
    And the crew "desk" says why "Nguyen" went "meet": "Sid's rule"
    And the crew "desk" says why "Ferraro" went "meet": "Chuck agreed"
    # one grid: each family's stage beside its next one (Michel, 2026-10-24: "why 2 grids for the families?")
    And in tab 1 the grid "desk_actions" lists "Okafor" and "adopt"
    # each message names its dog (Michel, 2026-10-24: "I see no dog name there?")
    And in tab 1 the grid "desk_actions" lists "Ferraro" and "Biscuit"
    # the reader reads the words; the checker checks them against the row — Chuck holds the stage, Rey does not
    And Rey read the words only, and Chuck checked them against the row
    # the workers, instantiated: each row a live agent with its own count, tokens, last answer (Michel, 2026-10-24: "go workers")
    When I open the accordion section "who does the job"
    Then the live agent "Rey" of the crew "desk" asked 2 times, 24 tokens, last said "VERDICT: meet"
    And the live agent "Sid" of the crew "desk" ran 3 times
    # the cost, three workers: 🐍 × 1, 🤖 × 30, 🧑 × 900 (Michel, 2026-10-24: "a nice global score for the costs")
    And the desk's cost reads 123: 3 rule runs, 4 AI asks, 0 left OPEN
    # the tokens beside the score, not in it: they move a little every run (Michel, 2026-10-24: "go for Tokens beside")
    And the desk's cost line says "beside it, 48 tokens"
    # a legend says what each action means, and who does it (Michel, 2026-10-24: "make it clear with a legend")
    And the desk's legend says "call a volunteer phones the family back"
    # the crew is an agent: the engine's 🔋 asks and tokens per unit of time, as under any agent (Michel, 2026-10-24)
    And the crew "desk" shows the engine's 🔋 asks left, as an agent does
    # the run reads as an event flow, each step's cost, each result ✅ sure or ⚠️ not; its legend shown (Michel, 2026-10-24)
    When I open the accordion section "event flow"
    # each beat names its worker by price: 🐍 Python, 🤖 the AI, 🧑 a person (Michel, 2026-10-24)
    Then the run's event flow "desk_flow" tells "🐍 Sid: meet / Nguyen → meet ✅ · free / Ferraro / 🤖 Rey proposes adopt · 12 tokens / 🤖 Chuck disagrees: the row says asked: no visit yet, and a family moves one stage at a time, so it cannot go home before it has met the dog / 🤖 Rey proposes meet / 🤖 Chuck agrees / Ferraro → meet ✅ · 48 tokens"
    And the event flow "desk_flow" shows its legend
    And the crew's log shows "Chuck" saying "DISAGREE"
    And Rey's second ask carried Chuck's words
    When I run the feature "crew_proof"
    Then the feature "crew_proof" is green
    # the same knobs, another answer — said on the cost only (Michel, 2026-10-24: "The change should be only on global score, to keep it simple")
    When I press ▶ Run on the crew "desk"
    Then the crew "desk" is done
    And the desk's cost line says "123 — = the last run"
    When the AI changes its mind: Rey now answers call
    And I press ▶ Run on the crew "desk"
    Then the crew "desk" is done
    And the desk's cost line says "63 — ≠ the last run: 123"

  Scenario: No key — the rules alone, the claim left OPEN for a person, nothing counted that was never sent
    Given I have a clean browser page
    When I navigate to "/components/crew"
    # no key: the crew's desk is open, as an agent's is (Michel, 2026-10-24)
    Then the crew "desk" shows its desk, open
    When I press ▶ Run on the crew "desk"
    Then the crew "desk" is done
    And the crew "desk" sorted "Okafor" as "adopt" in 0 tries
    And the crew "desk" sorted "Ferraro" as "OPEN" in 1 tries
    And the crew "desk" says why "Ferraro" went "OPEN": "no AI key"
    # an ask that never left the device is not counted against the budget
    And the crew "desk" asked the AI 0 times
    And the crew's log shows "Rey" saying "no AI key"

  Scenario: The agents are objects, their rows the storage — and the guide reads them as it speaks
    Michel, 2026-10-23: "can an avatar read some data from the page? For
    instance, personae's name" and "show agents are objects, storable as
    data". The members are a class built from the dataset's rows; a say:
    line with {= Member.first.name } is a cell, read as it is spoken.

    Given I have a clean browser page
    When I navigate to "/components/crew"
    # the workers — grid AND form — in their own accordion, above the messages (Michel, 2026-10-24)
    Then the accordion section "who does the job" comes before the grid "desk_actions"
    When I open the accordion section "who does the job"
    Then in tab 1 the grid "crew_grid" lists "Sid" and "Chuck"
    And picking "Rey" in the grid "crew_grid", the form "crew_form" shows its ai
    # one guide, the little docked one — no second, bigger Doc in the page (Michel, 2026-10-24)
    And the page has one guide, docked small in its corner
    When I press the trigger of the avatar "crew_guide"
    Then the guide speaks "3 members, one row each. Sid goes first"

  Scenario: A retired model heals — the crew asks as an agent panel does
    Michel, 2026-10-23, on his phone: Rey's step read "⚠️ The model
    `llama-3…` … not accessible". The crew asked the preset model with a
    request of its own; it now asks through the panel's whole path: the
    engine names what it serves, the next model on the ring answers.

    Given I have a clean browser page
    And a Groq key is saved on this device, and Groq has retired the preset model
    When I navigate to "/components/crew"
    And I press ▶ Run on the crew "desk"
    Then the crew "desk" is done
    And the crew "desk" sorted "Ferraro" as "meet" in 1 tries
    And the crew healed onto "llama-3.1-8b-instant"
    # a good run leaves the keys folded away (Michel, 2026-10-24: "once the run is done, the key panel is unfolded. WHY?? It makes noise")
    And the crew "desk" shows its desk, closed
    # and on a phone, the long columns read at the size of the others (2026-10-23: "font type strange")
    When I open the accordion section "who does the job"
    Then the grid "crew_grid" keeps its text at one size on a phone

  Scenario: An engine that does not answer — the crew says so and marks its 🔑, the keys stay folded
    Michel, 2026-10-24: Rey's step read "Couldn't reach
    generativelanguage.googleapis.com" and nothing on the crew let him fix
    the key — the crew is an agent, its 🔑 is where the key is fixed. Then:
    "once the run is done, the key panel is unfolded. WHY?? It makes noise":
    the 🔑 is marked, the keys unfold only when it is pressed.

    Given I have a clean browser page
    And an energy key is saved on this device, and its engine cannot be reached
    When I navigate to "/components/crew"
    Then the crew "desk" shows its desk, closed
    When I press ▶ Run on the crew "desk"
    Then the crew "desk" is done
    And the crew "desk" says "the AI did not answer"
    And the 🔑 of the crew "desk" is marked, its keys folded
    When I press the 🔑 of the crew "desk"
    Then the crew "desk" shows its desk, open


  Scenario: The bounds, played with — − on the budget, the gauge fills, what stays open says why
    Michel, 2026-10-24: "make visible the constraints … play with the knob's
    values: tries and budget, maybe with jauges", then "Steppers? I don't
    see them!". The bounds carry − and +; a gauge shows the budget spent.
    With a budget of 2, Ferraro's read and check spend it all: Chuck says
    no, no ask is left, Ferraro stays OPEN for a person.

    Given I have a clean browser page
    And an energy key "AIza-crew-test" is already saved on this device
    And the AI answers as Rey and Chuck, Rey wrong the first time
    When I navigate to "/components/crew"
    Then the crew "desk" shows its bounds: 2 tries, a budget of 6
    And the gauge of the crew "desk" reads "0 of 6 AI asks spent", low
    When I press "−" on the budget of the crew "desk" 4 times
    Then the crew "desk" shows its bounds: 2 tries, a budget of 2
    When I press ▶ Run on the crew "desk"
    Then the crew "desk" is done
    And the crew "desk" says why "Ferraro" went "OPEN": "budget spent"
    And the gauge of the crew "desk" reads "2 of 2 AI asks spent", spent
    When I open the accordion section "event flow"
    Then the run's event flow "desk_flow" tells "Ferraro / Chuck disagrees / budget spent / Ferraro → 🧑 OPEN ⚠️ budget spent"
    When I run the feature "crew_proof"
    Then the feature "crew_proof" is green
    # a try is a read and its check: the asks column adds up to the gauge (Michel, 2026-10-24: "the grid shows less")
    And the asks of the crew "desk" add up to its gauge: 2
    And the desk's cost reads 963: 3 rule runs, 2 AI asks, 1 left OPEN

  Scenario: A checker that runs out of words does not agree — every ask has an agent's allowance, said, and lowered only
    Michel, 2026-10-24, on Groq's gpt-oss (a model that thinks first): Ferraro
    went home with "Chuck agreed", Lindqvist spent a try on nothing. Each ask
    had 300 tokens, the thinking spent them, the replies came back empty or
    cut — and an empty check read as agreement. Now every ask has 2000, as
    any agent, and only a checker that says AGREE settles a message.

    Given I have a clean browser page
    And an energy key "AIza-crew-test" is already saved on this device
    And the AI answers as Rey, and Chuck runs out of words
    When I navigate to "/components/crew"
    # the cap is said, and lowered only (Michel, 2026-10-24: "display the token limit … lowering it (but not increasing it)")
    Then the crew "desk" allows 2000 tokens per ask, and no more
    When I press "−" on the max_tokens of the crew "desk" 4 times
    Then the crew "desk" allows 1000 tokens per ask
    When I press ▶ Run on the crew "desk"
    Then the crew "desk" is done
    And the crew "desk" says why "Ferraro" went "OPEN": "no agreement in 2 tries"
    And every ask of the crew allowed 1000 tokens
    # overloading is said: the cut answers, counted
    And the crew "desk" says "✂️ 2 answers cut at 1000 tokens per ask"
    When I open the accordion section "event flow"
    Then the run's event flow "desk_flow" tells "Ferraro / Rey proposes adopt / Chuck gives no verdict · 12 tokens ✂️ cut at 1000 / Ferraro → 🧑 OPEN ⚠️ no agreement in 2 tries"

  Scenario: A checker that says "Agreed." agrees
    Michel, 2026-10-24, on Groq: Ferraro spent all ten asks in five rounds, the
    others left OPEN — a Chuck who answers "Agreed." was read as no verdict.

    Given I have a clean browser page
    And an energy key "AIza-crew-test" is already saved on this device
    And the AI answers as Rey and Chuck, Rey wrong the first time, Chuck in his own words
    When I navigate to "/components/crew"
    And I press ▶ Run on the crew "desk"
    Then the crew "desk" is done
    And the crew "desk" sorted "Ferraro" as "meet" in 2 tries
    And the crew "desk" says why "Ferraro" went "meet": "Chuck agreed"

  Scenario: A checker in Python — an exact rule, free, the same every time
    Michel, 2026-10-24: "go python Chuck", then "just one agent? I would like
    to have 2": the lesson keeps Chuck an AI agent; the engine keeps a Python
    checker for a rule that is exact — a rules member named in checked_by.

    Given I have a clean browser page
    And an energy key "AIza-crew-test" is already saved on this device
    And the AI answers as Rey and Chuck, Rey wrong the first time
    And the module 08 lesson "01_the_front_desk.md" is served with a Python Chuck
    When I open the served lesson
    And I press ▶ Run on the crew "desk"
    Then the crew "desk" is done
    And the crew "desk" says why "Ferraro" went "meet": "Chuck agreed"
    # Chuck's checks are rule runs: Rey alone asks — Ferraro, Lindqvist, Moreau: two reads each
    And the crew "desk" asked the AI 6 times
    And the desk's cost reads 192: 12 rule runs, 6 AI asks, 0 left OPEN
    When I open the accordion section "event flow"
    Then the run's event flow "desk_flow" tells "Ferraro / 🤖 Rey proposes adopt / 🐍 Chuck disagrees: no visit yet: meet first / 🤖 Rey proposes meet / 🐍 Chuck agrees / Ferraro → meet ✅"

  Scenario: Answers as objects — the crew asks for JSON and reads it, the page's instructions say the role only
    Michel, 2026-10-24: "structured answers… objects instantiated from that
    json BUT encapsulated, so I don't want more complexity in the example".

    Given I have a clean browser page
    And an energy key "AIza-crew-test" is already saved on this device
    And the AI answers in JSON, Rey wrong the first time
    When I navigate to "/components/crew"
    And I press ▶ Run on the crew "desk"
    Then the crew "desk" is done
    And the crew "desk" sorted "Ferraro" as "meet" in 2 tries
    And the crew "desk" says why "Ferraro" went "meet": "Chuck agreed"
    And Rey was asked for an object: {"action": …, "why": …}
    And the crew's log reads Rey's first answer as the action "adopt", why "they want to pay"
    And Rey's second ask said "It allows meet."
    When I open the accordion section "event flow"
    Then the run's event flow "desk_flow" tells "Ferraro / 🤖 Rey proposes adopt / 🤖 Chuck disagrees: the stage is asked — allows meet / 🤖 Rey proposes meet / 🤖 Chuck agrees: one stage at a time / Ferraro → meet ✅"
