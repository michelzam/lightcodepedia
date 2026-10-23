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
    # the whole inbox from the start, then a row at a time, the row at work selected (Michel, 2026-10-23)
    Then the crew "desk" shows its 3 messages, none sorted yet
    When I press ▶ Run on the crew "desk"
    Then the crew "desk" is done
    And the grid of the crew "desk" has "Ferraro" selected
    And the crew "desk" sorted "Nguyen" as "VISIT" in 0 tries
    And the crew "desk" sorted "Okafor" as "PAY" in 0 tries
    And the crew "desk" sorted "Ferraro" as "VISIT" in 2 tries
    And the crew "desk" asked the AI 4 times
    # tokens, globally and by step (Michel, 2026-10-23: "show the token consumption")
    And the crew "desk" spent 48 tokens, 12 on each AI step
    And the crew's log shows "Chuck" saying "DISAGREE"
    And Rey's second ask carried Chuck's words
    When I run the feature "crew_proof"
    Then the feature "crew_proof" is green

  Scenario: No key — the rules alone, the claim to a person, nothing counted that was never sent
    Given I have a clean browser page
    When I navigate to "/components/crew"
    And I press ▶ Run on the crew "desk"
    Then the crew "desk" is done
    And the crew "desk" sorted "Okafor" as "PAY" in 0 tries
    And the crew "desk" sorted "Ferraro" as "CALL" in 1 tries
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
    And I open the accordion section "who can do what"
    Then in tab 1 the grid "crew_grid" lists "Sid" and "Chuck"
    When I press the trigger of the avatar "crew_guide"
    Then the guide speaks "3 members, one row each. Sid goes first"

