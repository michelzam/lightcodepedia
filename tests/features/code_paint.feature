Feature: 🎨 Code is painted wherever it shows — pad, card, a feature's steps
  Michel, 2026-10-10: "inside the editor, the sql should also be in colored
  syntax, and so on", and "the feature's stepdefs in python should also be
  in grayed background with colored syntax". One painter, no library: the
  pad's fences, the .code cards and a feature's step bodies wear the same
  token colours.

  Scenario: The pad paints the SQL inside its fence
    Given I have a clean browser page
    And the GitHub contents API serves "courses/demo/module_04/sql.md" with the document:
      """
      # SQL

      `````markdown
      ```sql
      SELECT campus, COUNT(*) AS dogs FROM dogs GROUP BY campus
      ```
      {: .query bind="dogs" #by_campus }
      `````
      {: .mdpad #sqlpad decorations="true" rows="8" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_04/sql.md"
    And I wait for the page to be interactive
    Then the "sqlpad" pad paints "SELECT" and "GROUP" as keywords

  Scenario: A feature's step code sits on the gray, painted
    Given I have a clean browser page
    When I navigate to "/components/impact_map"
    And I wait for the page to be interactive
    And I open the first step code of the feature "impact_map_proof"
    Then that step code is painted on the gray
