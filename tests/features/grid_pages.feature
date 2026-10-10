Feature: ▦ A paged datagrid wears a title bar, and a new page takes its form along
  Michel, 2026-10-10, on Three Faces: "the grid's header should be as big as
  the Form one", and "when the grid goes to the next page, and the first
  line gets selected, any detail form should follow".

  Background:
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/pages.md" with the document:
      """
      # Pages

      ```
      name,breed
      Lucky,Beagle
      Wanda,Poodle
      Hazel,Lab mix
      Peanut,Chihuahua
      Bo,Terrier
      ```
      {: .dataset #dogs }

      [The dogs](#)
      {: .datagrid #dog_grid source="dogs" rows="3" }

      [The dog](#)
      {: .form master="dog_grid" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/pages.md"
    And I wait for the page to be interactive

  Scenario: The grid's title bar names it like the form's does
    Then the "dog_grid" grid's title bar reads "▦ The dogs"
    And the form shows "Lucky"

  Scenario: The next page selects its first row, and the form follows
    When I turn the "dog_grid" grid to its next page
    Then the "dog_grid" grid has "Peanut" selected
    And the form shows "Peanut"
