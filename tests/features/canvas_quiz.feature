Feature: 📝 The Canvas quiz desk — a quiz nobody can pass by pattern
  Michel wants an autograded check per module that someone who skipped the
  material — human or AI, expert or not — cannot pass, while staying fair
  to the learner who did the work (2026-08-19). He then caught the leak in
  the drafts himself: "the right answer is the longest and sometimes with
  some bold 🤭". So the desk judges the spec before Canvas ever sees it,
  and the same six rules run in tools/canvas_quiz.py.

  Background:
    Given I have a clean browser page
    And a stubbed Canvas course

  Scenario: A clean spec passes and offers the push
    Given the spec "hq/quizzes/demo.yaml" is the module 05 quiz
    When I open the canvas desk for that spec
    And I press the quiz desk's Lint button
    Then the desk reports no tells
    And the push button is offered

  Scenario: The longest bolded key is refused, and so is the push
    Given the spec "hq/quizzes/demo.yaml" has a key that is longest and bold
    When I open the canvas desk for that spec
    And I press the quiz desk's Lint button
    Then the desk names the longest-option tell
    And the desk names the decoration tell
    And the push button stays out of reach

  Scenario: A question that names nothing of ours is refused
    An expert who never opened the module could answer it, which is the
    whole failure this quiz exists to prevent.

    Given the spec "hq/quizzes/demo.yaml" asks a generic SQL question
    When I open the canvas desk for that spec
    And I press the quiz desk's Lint button
    Then the desk says the question names nothing from the module

  Scenario: Reading the course lists what Canvas already holds
    Given the spec "hq/quizzes/demo.yaml" is the module 05 quiz
    When I open the canvas desk for that spec
    And I press the quiz desk's Read Canvas button
    Then the desk lists the course's quizzes

  Scenario: A published quiz with questions is never rewritten
    Learners may have sat it. Rewriting it silently would edit somebody's
    exam, so the desk stops and says to unpublish it first.

    Given the spec "hq/quizzes/demo.yaml" is the module 05 quiz
    And the course already holds that quiz, published, with questions
    When I open the canvas desk for that spec
    And I press the quiz desk's Lint button
    And I press the quiz desk's Push button
    Then the desk refuses to touch the published quiz
