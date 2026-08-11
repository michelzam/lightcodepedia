Feature: The material board's pending count

  The board compares each course's blobs in the lab against the vault.
  It must count only what the publish gate would actually send, or the
  number is never zero and stops being read.

  Background:
    Given I have a clean browser page

  Scenario: A margin note is not pending — it never travels
    The gate rsyncs with --exclude '__*' --exclude '*.notes.md'
    --exclude 'course.yml'. Counting those made a course that was
    perfectly in sync report "3 pending" forever (Michel, 2026-08-11).

    Given the board's lab holds "index.md" "__pitch.md" "m0/__a.notes.md" "course.yml"
    And the board's vault holds "index.md"
    When I open the material board
    Then the course reads "✅ in sync"

  Scenario: A real difference is still counted
    Given the board's lab holds "index.md" "__pitch.md" "m0/lesson.md" "course.yml"
    And the board's vault holds "index.md"
    When I open the material board
    Then the course reads "⏳ 1 pending"
