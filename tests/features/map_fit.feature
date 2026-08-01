Feature: A map frames its own markers
  A map of three shelters should SHOW three shelters — and still should when
  a fourth arrives, with no hand-tuned centre-and-zoom to maintain. Fitting
  is the default with two or more markers; lat/lng/zoom is the fallback for
  none or one, and fit="false" keeps a deliberately framed view.

  (MapLibre's script and vector tiles come from CDNs this harness cannot
  reach, so a recording stub stands in for the map engine: the assertions
  are about what OUR component asks the engine to do.)

  Background:
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a recording map engine is preinstalled

  Scenario: Several markers are framed together
    Given the GitHub contents API serves "courses/demo/mod/shelters.md" with the document:
      """
      # Campuses

      ```csv
      name,lat,lng
      Milwaukee,43.0530,-87.9720
      Ozaukee,43.3839,-87.9403
      Racine,42.7261,-87.7828
      ```
      {: .map #campus_map height="320" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/shelters.md"
    And I wait for the page to be interactive
    Then the map was fitted around all 3 markers

  Scenario: One marker keeps the author's view
    Given the GitHub contents API serves "courses/demo/mod/one.md" with the document:
      """
      # One campus

      ```csv
      name,lat,lng
      Milwaukee,43.0530,-87.9720
      ```
      {: .map lat="43.06" lng="-87.88" zoom="9" height="300" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/one.md"
    And I wait for the page to be interactive
    Then the map was never fitted

  Scenario: fit="false" keeps the author's frame
    Given the GitHub contents API serves "courses/demo/mod/pinned.md" with the document:
      """
      # Pinned map

      ```csv
      name,lat,lng
      Far north,60.0,10.0
      Far south,-40.0,20.0
      ```
      {: .map lat="48.86" lng="2.35" zoom="12" height="300" fit="false" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/pinned.md"
    And I wait for the page to be interactive
    Then the map was never fitted
