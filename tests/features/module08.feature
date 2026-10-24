Feature: Module 08 — the front desk: a crew of three, one budget
  Michel, 2026-10-23: "go crew in a new 01bis page in module 7. Kiss." — moved to module 08 (2026-10-24: "AI in prod for the first time"). The
  learner's desk sits in a pad of their own: three members as rows, one
  .crew line with its bounds. Red on arrival — Sid sorts three alone, one
  easy message still costs an AI ask; one rule more and it is green. The
  check reads the log, so it holds with or without an AI key.

  Background:
    Given I have a clean browser page

  Scenario: As written, the desk runs and its proof asks for one more rule
    Given the module 08 lesson "01_the_front_desk.md" is served as written
    When I open the served lesson
    And I press ▶ Run on the crew "desk"
    Then the crew "desk" is done
    And the crew "desk" sorted "Lindqvist" as "OPEN" in 1 tries
    When I run the feature "desk_proof"
    Then the feature "desk_proof" is red and names "teach him one more rule in sort()"
    # the experiment waits for its line (Michel, 2026-10-24: "injection as a csv line")
    When I run the feature "experiment_proof"
    Then the feature "experiment_proof" is red and names "add one line to the inbox csv"
    # the lesson's tutor, as in module 06 (Michel, 2026-10-24: "the front desk has no chat zone … strange")
    And the lesson has "Bill the Builder" beside it, linked to "front_desk"

  Scenario: Sid taught one more rule: the easy message is free, the proof is green
    Given the module 08 lesson "01_the_front_desk.md" is served with Sid taught to see a visit
    When I open the served lesson
    And I press ▶ Run on the crew "desk"
    Then the crew "desk" is done
    And the crew "desk" sorted "Lindqvist" as "meet" in 0 tries
    When I run the feature "desk_proof"
    Then the feature "desk_proof" is green

  Scenario: With a key, the budget runs out: the last messages stay OPEN for a person, and the grid and the flow say why
    Michel, 2026-10-24: "how come Lindqvist were classified as CALL instead
    of visit? And how Ferraro who wants to pay are classified as visit??"
    Stages since (Michel: "stage instead of lane"): Ferraro's row says
    asked, and a family moves one stage at a time — met, not home.
    Ferraro's two rounds (read, check, read, check) take four of the six
    asks; Lindqvist's read and check the last two — Chuck refuses the read
    with no ask left for another; Moreau finds the budget spent. A stage is
    where the message moves its family: no visit yet for Ferraro, so met first.

    Given an energy key "AIza-crew-test" is already saved on this device
    And the AI answers as Rey and Chuck, Rey wrong the first time
    And the module 08 lesson "01_the_front_desk.md" is served as written
    When I open the served lesson
    And I press ▶ Run on the crew "desk"
    Then the crew "desk" is done
    And the crew "desk" says why "Ferraro" went "meet": "Chuck agreed"
    # Lindqvist: Rey's first read is checked and refused, and no ask is left for a second one
    And the crew "desk" says why "Lindqvist" went "OPEN": "budget spent"
    And the crew "desk" says why "Moreau" went "OPEN": "budget spent"
    # the flow says it too: the budget spent, then the message stays OPEN
    When I open the accordion section "event flow"
    Then the run's event flow "desk_flow" tells "Lindqvist / Chuck disagrees / budget spent / Lindqvist → 🧑 OPEN ⚠️ budget spent"
    And the crew "desk" asked the AI 6 times
    # a person is the dearest worker: two messages left OPEN cost more than every ask (Michel, 2026-10-24)
    And the desk's cost reads 1986: 6 rule runs, 6 AI asks, 2 left OPEN


  Scenario: The experiment — a line that gives orders, a budget to read it, and the desk answers it
    Michel, 2026-10-24: "injection as a csv line … Students should be
    instructed to BOTH inject a line in the csv and adjust the budget. But
    they're in charge, aware." The proof asks only for the row and for the
    AI to have read it within the budget; the quiz weighs the outcomes.

    Given an energy key "AIza-crew-test" is already saved on this device
    And the AI answers as Rey and Chuck, Rey wrong the first time
    And the module 08 lesson "01_the_front_desk.md" is served with an order in the inbox and a budget of 16
    When I open the served lesson
    And I press ▶ Run on the crew "desk"
    Then the crew "desk" is done
    And the crew "desk" says why "Dubois" went "meet": "Chuck agreed"
    When I run the feature "experiment_proof"
    Then the feature "experiment_proof" is green
