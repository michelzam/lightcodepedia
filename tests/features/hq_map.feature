Feature: The HQ map — the lab's handoff as pitch, map and proof

  The lab's headquarters start on one page: a pitch, an impact map whose
  leaves are the topics, one topic page each, and a proof that turns red
  when a topic has not been touched for thirty days. hq/ is never rendered,
  so the map opens in the runner with the author key, from the lab desk,
  on any device.

  Background:
    Given I have a clean browser page

  Scenario: The lab desk offers the map as a door into the runner
    When I open the HQ landing
    Then the landing offers the HQ map in the runner

  Scenario: The map renders its pitch, eight topics and its own proof
    Given the HQ map is served from the lab, touched today
    When I open the runner page on "gh:michelzam/lightcodelab/hq/index.md"
    And I wait for the runner to render
    Then the pitch "hq_pitch" reads "the HQ map"
    And the impact map "hq_map" has 8 behaviour changes
    And the impact map "hq_map" leaf links to the proof "hq_proof"
    And the topic cards open in the runner

  Scenario: The map's proof is green while every topic is fresh
    Given the HQ map is served from the lab, touched today
    When I open the runner page on "gh:michelzam/lightcodelab/hq/index.md"
    And I wait for the runner to render
    And I run the feature "hq_proof"
    Then the feature "hq_proof" is green

  Scenario: A topic left for a month turns the map's proof red and names it
    Given the HQ map is served from the lab, with "cohorts" last touched 40 days ago
    When I open the runner page on "gh:michelzam/lightcodelab/hq/index.md"
    And I wait for the runner to render
    And I run the feature "hq_proof"
    Then the feature "hq_proof" is red and names "cohorts"

  Scenario: A topic page deep in hq lists a folder at the repo root
    Given the HQ map is served from the lab, touched today
    When I open the runner page on "gh:michelzam/lightcodelab/hq/topics/cohorts.md"
    And I wait for the runner to render
    Then the shelf "modules" was listed from the repo root folder "courses/micro_build_ai"

  Scenario: The map lists the lab's root, CLAUDE.md among the cards
    Given the HQ map is served from the lab, touched today
    When I open the runner page on "gh:michelzam/lightcodelab/hq/index.md"
    And I wait for the runner to render
    Then the shelf "root_cards" opens "CLAUDE.md" in the runner
    And the shelf "hq_cards" opens "hq/DECISION_REGISTER_20260718.md" in the runner
