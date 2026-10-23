Feature: A crew — agents as the rows of a dataset, a loop with its bounds
  Michel, 2026-10-23: "data-driven dynamic instances initiated by a simple
  dataset … encapsulated, declarative, with clear bounds (costs, loops)" →
  "go crew". The members are rows; .crew runs them over an inbox: the rules
  first, then a reader checked by a checker, a disagreement sent back with
  the checker's words, at most tries= a message and budget= AI asks, and
  fallback= for what stays open. It writes <id>.lanes and <id>.log only.

  Scenario: The desk loops — Rey says PAY, Chuck disagrees, Rey says VISIT; the rules sort the rest for free
    Given I have a clean browser page
    And an energy key "AIza-crew-test" is already saved on this device
    And the AI answers as Rey and Chuck, Rey wrong the first time
    When I navigate to "/components/crew"
    And I press ▶ Run on the crew "desk"
    Then the crew "desk" is done
    And the crew "desk" sorted "Nguyen" as "VISIT" in 0 tries
    And the crew "desk" sorted "Okafor" as "PAY" in 0 tries
    And the crew "desk" sorted "Ferraro" as "VISIT" in 2 tries
    And the crew "desk" asked the AI 4 times
    And the crew's log shows "Chuck" saying "DISAGREE"
    And Rey's second ask carried Chuck's words
    When I run the feature "crew_proof"
    Then the feature "crew_proof" is green

  Scenario: Bounds hold — no key, the rules alone; a budget of 1 leaves the claim to a person
    Given I have a clean browser page
    When I navigate to "/components/crew"
    And I press ▶ Run on the crew "desk"
    Then the crew "desk" is done
    And the crew "desk" sorted "Okafor" as "PAY" in 0 tries
    And the crew "desk" sorted "Ferraro" as "CALL" in 1 tries
    And the crew "desk" asked the AI 1 times
    And the crew's log shows "Rey" saying "no AI key"
