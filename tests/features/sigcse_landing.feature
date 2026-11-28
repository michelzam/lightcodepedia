Feature: The SIGCSE talk's address answers before the example opens
  Michel, 2026-11-28: the camera-ready abstract prints lightcodepedia.org/sigcse,
  and the working example is released with the proceedings. Until then the
  address must not be a 404: a short landing says what will open and when,
  and nothing else (Michel, same day: no links, no contact, no signature
  there). The example itself stays in the lab.

  Scenario: The landing names the talk and says when the example opens, nothing more
    Given I have a clean browser page
    When I navigate to "/sigcse"
    And I wait for the page to be interactive
    Then the page reads "Two Probabilistic Systems Walk into a Classroom"
    And the page reads "The working example of the SIGCSE TS 2027 lightning talk"
    And the page reads "It opens here with the proceedings of SIGCSE TS 2027, in February 2027"
    And the landing holds none of "Until then, karmicsoft, BUILD-AI, Michel Zam"
