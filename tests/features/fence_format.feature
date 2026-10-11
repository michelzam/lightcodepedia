Feature: 🏷️ A data fence names its format, and the name is obeyed
  Michel, 2026-10-11: "wherever there is some data in a fence, explicit the
  name of the format (csv, yaml…)" — for learners to read it. A ```yaml
  dataset used to be read as CSV unless format="yaml" was added too; the
  fence's own word now decides, for a dataset, a grid and a form.

  Scenario: A yaml dataset and a csv grid read as what they say
    Given I have a clean browser page
    And the GitHub contents API serves "courses/demo/mod/formats.md" with the document:
      """
      # Formats

      ```yaml
      - name: Lucky
        breed: Beagle
      - name: Wanda
        breed: Poodle
      ```
      {: .dataset #dogs }

      [The dogs](#)
      {: .datagrid #dog_grid source="dogs" }

      ```csv
      name,breed
      Hazel,Lab mix
      ```
      {: .datagrid #csv_grid }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/formats.md"
    And I wait for the page to be interactive
    Then the "dog_grid" grid shows the cell "Wanda"
    And the "csv_grid" grid shows the cell "Hazel"
