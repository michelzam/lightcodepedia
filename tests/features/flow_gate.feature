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

  Scenario: Module 04's first screen is red on arrival
    The learner's first part: a welcome page in a decorated pad, whose link
    they turn into a button with one line. Red until the title is finished
    plus the line typed: the smallest red-then-green in the course.

    Given the runner serves the course page "courses/micro_build_ai/module_04/01_first_screen.md"
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_04/01_first_screen.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's proof
    Then the lesson's proof is red

  Scenario: Module 04's first screen is green once the link is a button
    Given the runner serves the course page "courses/micro_build_ai/module_04/01_first_screen.md"
    And the learner has finished the welcome and turned its link into a button
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_04/01_first_screen.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's proof
    Then the lesson's proof is green
    And the pad's preview wears app chrome titled "Welcome to the shelter"

  Scenario: Module 04's dogs screen is red on arrival
    The second screen of the learner's app: the dog pile, declared in the
    pad with no face, until the learner types the datagrid line.

    Given the runner serves the course page "courses/micro_build_ai/module_04/02_dogs.md"
    And the runner serves the course file "courses/micro_build_ai/module_00/dogs.yaml"
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_04/02_dogs.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's proof
    Then the lesson's proof is red

  Scenario: Module 04's dogs screen is green once the pile wears a table
    Given the runner serves the course page "courses/micro_build_ai/module_04/02_dogs.md"
    And the runner serves the course file "courses/micro_build_ai/module_00/dogs.yaml"
    And the learner has given the dog pile a table
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_04/02_dogs.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's proof
    Then the lesson's proof is green
    And the pad's preview wears app chrome titled "Our dogs"

  Scenario: Module 04's three faces are red on arrival
    Given the runner serves the course page "courses/micro_build_ai/module_04/03_faces.md"
    And the runner serves the course file "courses/micro_build_ai/module_00/dogs.yaml"
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_04/03_faces.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's proof
    Then the lesson's proof is red

  Scenario: Module 04's three faces are green once the card and the chart are typed
    Given the runner serves the course page "courses/micro_build_ai/module_04/03_faces.md"
    And the runner serves the course file "courses/micro_build_ai/module_00/dogs.yaml"
    And the learner has given the pile a card and a chart
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_04/03_faces.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's proof
    Then the lesson's proof is green

  Scenario: Module 04's Essentials beat proof is red until the learner's beat is written
    Given the runner serves the course page "courses/micro_build_ai/module_04/04_concepts.md"
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_04/04_concepts.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's proof
    Then the lesson's proof is red

  Scenario: Module 04's Essentials beat proof is green once the beat is written
    Given the runner serves the course page "courses/micro_build_ai/module_04/04_concepts.md"
    And the learner has written the chart's beat
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_04/04_concepts.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's proof
    Then the lesson's proof is green
    And the story pad stacks its preview above its source

  Scenario: Module 05's playground is red on arrival
    Michel, 2026-10-09: Module 05 rebuilt in the pad — four pages, the builder
    one of them. The playground opens with a checklist and no component.

    Given the runner serves the course page "courses/micro_build_ai/module_05/01_builder.md"
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_05/01_builder.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's check "builder_check"
    Then the lesson's check "builder_check" is red

  Scenario: Module 05's playground is green once the datagrid and the button are added and ticked
    Given the runner serves the course page "courses/micro_build_ai/module_05/01_builder.md"
    And the learner has added the datagrid and the button
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_05/01_builder.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's check "builder_check"
    Then the lesson's check "builder_check" is green

  Scenario: Module 05's follow-up app is red on arrival
    The coordinator's app: the dataset and a checklist; the reasons (persona,
    pitch, map row) sit beside the pad, on the lesson page.

    Given the runner serves the course page "courses/micro_build_ai/module_05/02_list.md"
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_05/02_list.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's check "list_proof"
    Then the lesson's check "list_proof" is red

  Scenario: Module 05's follow-up app is green once its four components are built
    The proof presses the button once (Nguyen gets today's day, Okafor is
    selected); two more presses mark Okafor and Alvarez and select Brooks.
    No WHERE yet, so the marked families stay: still fourteen.

    Given the runner serves the course page "courses/micro_build_ai/module_05/02_list.md"
    And the learner has built the follow-up app
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_05/02_list.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's check "list_proof"
    Then the lesson's check "list_proof" is green
    When the coordinator presses the call button 2 times
    Then the selected family is "Brooks"
    And the pad's preview reads "14 families are waiting"

  Scenario: Module 05's follow-up app names a decoration with nothing above it
    Michel's pad, 2026-10-09: the datagrid's decoration typed alone after a
    blank line, with no link above it, landed on the query — the query became
    a grid of every reservation and the proof only said "no query yet". It
    now names the decoration that has nothing above it.

    Given the runner serves the course page "courses/micro_build_ai/module_05/02_list.md"
    And the learner has built the follow-up app with the datagrid's decoration alone
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_05/02_list.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's check "list_proof"
    Then the lesson's check "list_proof" is red
    And the lesson's check "list_proof" says "nothing right above {: .datagrid"

  Scenario: Module 05's proof page is red while fourteen families are in the list
    The story the page tells: two presses, and Alvarez is selected, who
    took Scout home on Saturday.

    Given the runner serves the course page "courses/micro_build_ai/module_05/03_proof.md"
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_05/03_proof.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And the coordinator presses the call button 2 times
    Then the selected family is "Alvarez"
    When I run the lesson's check "proof_proof"
    Then the lesson's check "proof_proof" is red

  Scenario: Module 05's proof page is green once the check is in the app and the query is fixed
    The check the learner types runs INSIDE their app: red with the five
    families who already met their dog, green after WHERE met = ''. Then
    each press takes the marked family out of the list: 9, 8, 7.

    Given the runner serves the course page "courses/micro_build_ai/module_05/03_proof.md"
    And the learner has written the check at the bottom of the page
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_05/03_proof.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's check "proof_proof"
    Then the lesson's check "proof_proof" is red
    When the learner runs the check inside the pad
    Then the check inside the pad is red
    When the learner fixes the question with WHERE met = ''
    And the learner runs the check inside the pad
    Then the check inside the pad is green
    When the coordinator presses the call button 2 times
    Then the selected family is "Ferraro"
    And the pad's preview reads "7 families are waiting"
    When I run the lesson's check "proof_proof"
    Then the lesson's check "proof_proof" is green

  Scenario: Module 05's own app is red on arrival
    Given the runner serves the course page "courses/micro_build_ai/module_05/04_concepts.md"
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_05/04_concepts.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's check "app_proof"
    Then the lesson's check "app_proof" is red

  Scenario: Module 05's own app is green once its five items are built
    Given the runner serves the course page "courses/micro_build_ai/module_05/04_concepts.md"
    And the learner has built an app of their own
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_05/04_concepts.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's check "app_proof"
    Then the lesson's check "app_proof" is green

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

  Scenario: A cell counts a table that lands after the first paint
    Pedia, 2026-09-19: "Everyone 3 and visited ." — the query's engine came
    off a slow CDN, the cell had already read an empty count, and nothing
    told it to look again. Data that lands late schedules a recompute.

    Given the GitHub contents API serves "courses/demo/mod/late.md" with the document:
      """
      # Late

      [late rows](/assets/late.csv)
      {: .dataset #late }

      Late {= late.count }.
      {: #tally }
      """
    And "/assets/late.csv" answers 3 seconds late with 2 rows
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/late.md"
    And I wait for the page to be interactive
    Then the tally reads "Late 2."

  Scenario: Module 04's card shows the dog's photo once a family clicks a row
    Given the runner serves the course page "courses/micro_build_ai/module_04/03_faces.md"
    And the runner serves the course file "courses/micro_build_ai/module_00/dogs.yaml"
    And the learner has given the pile a card and a chart
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_04/03_faces.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And a family clicks the first dog in the pad's table
    Then the card shows that dog's photo

  Scenario: Module 04's card wears the photo as soon as the learner types compute= on it
    Given the runner serves the course page "courses/micro_build_ai/module_04/03_faces.md"
    And the runner serves the course file "courses/micro_build_ai/module_00/dogs.yaml"
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_04/03_faces.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And the learner types the card under the table, compute= on it
    Then the card shows that dog's photo

  Scenario: Module 04's plain card shows the pic number, no face yet
    Given the runner serves the course page "courses/micro_build_ai/module_04/03_faces.md"
    And the runner serves the course file "courses/micro_build_ai/module_00/dogs.yaml"
    When I navigate to "/run.html#src=gh:acme/demo/courses/micro_build_ai/module_04/03_faces.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And the learner types the plain card under the table
    Then the card shows the pic number and no face

  Scenario: The Python class's first assignment opens with a tutor beside the program
    Michel, 2026-10-06: account-free pages for the Python class — a tutor in
    student mode bound to a run block, the student's own engine key. The
    page's proof is structural until the sealed brief lands.

    Given the runner serves the course page "courses/python/hidden_gems_activity.md"
    When I navigate to "/run.html#src=gh:acme/demo/courses/python/hidden_gems_activity.md"
    And I wait for the page to be interactive
    And I wait for the cells to settle
    And I run the lesson's check "assignment_proof"
    And I run the lesson's check "dod"
    Then the lesson's check "assignment_proof" is green
    And the lesson's check "dod" is red
