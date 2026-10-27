Feature: Arcade jingles — a run block plays notes
  Michel, 2026-10-27: "generate sounds in the browser from our micropython
  examples so we can play a song". Every runner has play(): a note and its
  beats, queued one after the other, so a loop is a melody. The block
  records what it queued, so the page's proof and this suite hear nothing
  and check everything.

  Background:
    Given I have a clean browser page
    When I navigate to "/courses/python/jingles"
    And I wait for the page to be interactive
    And I wait for the selector "#lc-pyrun-coin .lc-pyrun-code"

  Scenario: The coin jingle queues its two notes, and the proof hears it
    When I run the page's embedded features
    Then the card "jingles_proof" comes out red
    When I click Run in the "coin" editor
    Then the "coin" editor played 2 notes, the last "E6"
    And the "coin" editor's output ends with "ping!"
    When I click Run in the "mine" editor
    And I run the page's embedded features
    Then the card "jingles_proof" comes out green

  Scenario: Objects, tuples and a whole list all play
    When I click Run in the "power" editor
    Then the "power" editor played 7 notes, the last "G6"
    When I click Run in the "scale" editor
    Then the "scale" editor played 16 notes, the last "C4"
