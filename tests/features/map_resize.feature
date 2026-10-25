Feature: A map drawn before its box had its size frames its markers again
  Michel, 2026-10-25: the shipped app's campuses map came up centred on the
  Caribbean, no pins — it was drawn while its box was still being laid out.
  When the box takes its size, the map takes it too and frames its markers
  again (unless the reader already moved it). A recording stub stands in for
  the map engine, as in map_fit.feature.

  Background:
    Given I have a clean browser page
    And a recording map engine is preinstalled

  Scenario: A map rendered folded away frames its markers once its panel opens
    Given the GitHub contents API serves "courses/demo/mod/folded.md" with the document:
      """
      # Campuses

      ````
      ### !🏠 The campuses
      ```csv
      name,lat,lng
      Milwaukee,43.0530,-87.9720
      Ozaukee,43.3839,-87.9403
      Racine,42.7261,-87.7828
      ```
      {: .map #campus_map height="320" }
      ````
      {: .accordion }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/folded.md"
    And I wait for the page to be interactive
    And I open the accordion section "The campuses"
    Then the map took its new size and framed its markers again
