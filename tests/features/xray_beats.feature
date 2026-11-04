Feature: X-ray beats for a tour — the loupe, then the pipes, without the guide's own fan
  Michel, 2026-11-04, on the adopter teaser: "I wish I could see the xray
  for 1 component (the loupe), then 2 with pipes, then disclose the mdpad".
  `do: xray, with: lens` draws one ghost and no pipes; `do: xray` draws the
  pipes; and while the guide performs, its node stays out of the scene —
  before, every at: of the script came along and flooded the page.

  Background:
    Given I have a clean browser page
    When I navigate to "/components/xray"
    And I wait for the page to be interactive

  Scenario: The lens is one ghost, no pipes
    When Doc does "xray" with "lens" on the part "xray_sales_grid"
    Then the x-ray shows one ghost and no pipes
    And the x-ray scene mentions "Datagrid"

  Scenario: The pipes, while the guide performs, leave the guide out
    When the guide "xray_doc" is performing
    And Doc does "xray" with "pipes" on the part "xray_sales_grid"
    Then the x-ray scene mentions "Dataset"
    And the x-ray scene never mentions "Avatar"

  Scenario: The pipes, with the guide idle, show that it points at the part
    When Doc does "xray" with "pipes" on the part "xray_sales_grid"
    Then the x-ray scene mentions "Dataset"
    And the x-ray scene mentions "Avatar"
