Feature: 🚦 A workflow ordered by its own values
  Module 02 teaches a reservation flow whose steps unlock each other: you
  cannot book a visit before you name a dog, and the dog cannot go home
  before a visit exists. The learner writes those rules as `visible="= …"`
  conditions over form fields — a spreadsheet skill, not code.

  These scenarios pin the three mechanics the lesson rests on, BEFORE the
  lesson is written. The reactive example page already shows `visible=` gating
  a paragraph; what it never shows is gating a FORM, which is the whole shape
  of the flow. Getting this wrong is how a lesson ends up red for ever.

  Background:
    Given I have a clean browser page
    And the GitHub contents API serves "courses/demo/mod/flow.md" with the document:
      """
      # A reservation

      ```yaml
      dog: ""
      ```
      {: .form #ask editable="true" title="1 Ask" }

      ```yaml
      when: ""
      ```
      {: .form #meet editable="true" title="2 Meet" visible="= ask.dog" }

      The dog goes home.
      {: .block #home visible="= meet.when" }
      """

  Scenario: A form can be gated by a condition over another form
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/flow.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    Then the step "ask" is open
    And the step "meet" is shut
    And the step "home" is shut

  Scenario: Filling a field opens the next step, and only the next one
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/flow.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I type "Biscuit" into the step "ask"
    Then the step "meet" is open
    And the step "home" is shut

  Scenario: The last step waits for the step before it
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/flow.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I type "Biscuit" into the step "ask"
    And I type "Thursday" into the step "meet"
    Then the step "home" is open

  Scenario: The lesson's own proof is red on arrival
    A proof that is green before the learner touches anything teaches nothing.
    One that stays red after the right edit is worse. Module 02 page 1 shipped
    red for ever because nobody ever ran it. These two scenarios run the REAL
    lesson file, both ways, so neither can happen again.

    Given the runner serves the course page "courses/micro_build_ai/module_02/02_gates.md"
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_02/02_gates.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's proof
    Then the lesson's proof is red

  Scenario: The lesson's own proof is green once the knob is fixed
    Given the runner serves the course page "courses/micro_build_ai/module_02/02_gates.md"
    And the learner has changed card 3 to follow the visit
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_02/02_gates.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's proof
    Then the lesson's proof is green

  Scenario: Page 3's check is red on arrival
    Given the runner serves the course page "courses/micro_build_ai/module_02/03_where_they_stop.md"
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_02/03_where_they_stop.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's proof
    Then the lesson's proof is red

  Scenario: Page 3's check is green once the card counts the query
    Given the runner serves the course page "courses/micro_build_ai/module_02/03_where_they_stop.md"
    And the learner has pointed the middle line at the visited query
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_02/03_where_they_stop.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's proof
    Then the lesson's proof is green

  Scenario: A cell can count a table, so no component is needed for one number
    Michel, 2026-08-06: "I am totally surprised by stat. Could it be rather
    done with a cell?" It could not — a formula reached forms, mdpads and
    feature status, but never a table, so counting rows needed its own
    component. Now `{= id.count }` reads any dataset or query, and a lesson can
    put one number on the screen with the mechanism it already taught.

    Given the GitHub contents API serves "courses/demo/mod/count.md" with the document:
      """
      # Counting

      ```csv
      family,met
      Nguyen,
      Alvarez,Wed
      Brooks,Tue
      ```
      {: .dataset #bookings }

      ```sql
      SELECT * FROM bookings WHERE met <> ''
      ```
      {: .query bind="bookings" #visited }

      Everyone {= bookings.count } and visited {= visited.count }.
      {: #tally }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/count.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    Then the tally reads "Everyone 3 and visited 2."
