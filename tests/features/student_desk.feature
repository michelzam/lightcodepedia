Feature: 🧑‍🎓 The triptych desk — one roster, three systems
  Navigate360, PAWS and Canvas refuse iframes (SSO walls), so the desk is
  a switchboard (Michel, 2026-08-25): fetch the class through the gate,
  pick a row, and named-tab launchers aim each system at that student.
  Zero student data at rest — facts die with the tab, the Navigate id
  lives in this browser only.

  Background:
    Given I have a clean browser page

  Scenario: The desk stands, empty and honest
    Given a connected author key on the triptych
    When I navigate to "/lab/students"
    And I wait for the page to be interactive
    Then the triptych offers fetch, card and roster
    And the HQ card links to the triptych

  Scenario: The roster lands and the card aims all three systems
    Given a connected author key and a stubbed facts gate
    When I navigate to "/lab/students"
    And I wait for the page to be interactive
    And I press the triptych fetch button
    And I pick "Lovelace" in the triptych roster
    Then the card shows the canvas facts "88" and "2026-08-20"
    And the "canvas" launcher aims at "/courses/10954/users/111"
    And the "paws" launcher aims at "EMPLID=123"
    And the "paws" launcher aims at "STRM=2259"
    And the "nav" launcher aims at "/home"

  Scenario: A typed Navigate id sticks to this browser, never the repo
    Given a connected author key and a stubbed facts gate
    When I navigate to "/lab/students"
    And I wait for the page to be interactive
    And I press the triptych fetch button
    And I pick "Lovelace" in the triptych roster
    And I type "8679020" as the Navigate id
    Then the "nav" launcher aims at "/students/8679020"
    And the Navigate id is kept in this browser only
