Feature: ↔️ A form's labels fit, and the learner moves the line
  A card beside a datagrid showed its labels and almost nothing else: the
  label column was a fixed 160px, the values got 39 (Michel's pad, Module
  04 · Three Faces, 2026-10-10). The column now fits its labels — never more
  than half the card — and a grip on the line between labels and values
  drags it; the learner's width holds when the card follows another row.

  Background:
    Given I have a clean browser page
    When I navigate to "/components/form"
    And I wait for the page to be interactive
    And I click row 1 of the "narrow_grid" grid

  Scenario: The labels fit, and the values keep the rest
    Then the "narrow_form" form's labels are whole
    And the "narrow_form" form gives its values at least half its width

  Scenario: Dragging the line moves it, and it holds on the next row
    When I drag the "narrow_form" form's label line 40px to the right
    Then the "narrow_form" form's label column grew by 40px
    When I click row 2 of the "narrow_grid" grid
    Then the "narrow_form" form shows "Wanda"
    And the "narrow_form" form's label column kept its width
