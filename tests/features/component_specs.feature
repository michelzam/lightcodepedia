Feature: Component specs run green

  Hidden .feature blocks embedded on component pages must pass when executed
  by the in-browser MicroPython step runner. This dogfoods the runtime: the
  component's own model classes drive its live demo and assert the behaviour.

  Scenario: Accordion spec passes
    Given I have a clean browser page
    When I navigate to "/components/accordion"
    And I wait for the page to be interactive
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: Tabs spec passes
    Given I have a clean browser page
    When I navigate to "/components/tabs"
    And I wait for the page to be interactive
    And I wait for the selector ".lc-tab-btn"
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: Radio spec passes
    Given I have a clean browser page
    When I navigate to "/components/radio"
    And I wait for the page to be interactive
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: Dropdown spec passes
    Given I have a clean browser page
    When I navigate to "/components/dropdown"
    And I wait for the page to be interactive
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: Cards spec passes
    Given I have a clean browser page
    When I navigate to "/components/cards"
    And I wait for the page to be interactive
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: Menu spec passes
    Given I have a clean browser page
    When I navigate to "/components/menu"
    And I wait for the page to be interactive
    And I wait for the selector ".lc-menu"
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: Carousel spec passes
    Given I have a clean browser page
    When I navigate to "/components/carousel"
    And I wait for the page to be interactive
    And I wait for the selector ".lc-carousel"
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: Button spec passes
    Given I have a clean browser page
    When I navigate to "/components/button"
    And I wait for the page to be interactive
    And I wait for the selector ".button"
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: Quiz spec passes
    Given I have a clean browser page
    When I navigate to "/components/quiz"
    And I wait for the page to be interactive
    And I wait for the selector ".lc-quiz"
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: Slides spec passes
    Given I have a clean browser page
    When I navigate to "/components/slides"
    And I wait for the page to be interactive
    And I wait for the selector ".lc-slide"
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: Grid spec passes
    Given I have a clean browser page
    When I navigate to "/components/grid"
    And I wait for the page to be interactive
    And I wait for the selector ".lc-grid-cell"
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: QR spec passes
    Given I have a clean browser page
    When I navigate to "/components/qr"
    And I wait for the page to be interactive
    And I wait for the selector ".lc-qr"
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: Map spec passes
    Given I have a clean browser page
    When I navigate to "/components/map"
    And I wait for the page to be interactive
    And I wait for the selector ".lc-map canvas"
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: Dataset spec passes
    Given I have a clean browser page
    When I navigate to "/components/dataset"
    And I wait for the page to be interactive
    And I wait for the selector ".lc-dg-table"
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: Datagrid spec passes
    Given I have a clean browser page
    When I navigate to "/components/datagrid"
    And I wait for the page to be interactive
    And I wait for 3 elements matching "[data-lc-id='editable_dogs'] .ag-center-cols-container .ag-row"
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: Chart spec passes
    Given I have a clean browser page
    When I navigate to "/components/chart"
    And I wait for the page to be interactive
    And I wait for the selector ".lc-chart canvas"
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: Form spec passes
    Given I have a clean browser page
    When I navigate to "/components/form"
    And I wait for the page to be interactive
    And I wait for the selector ".lc-form-grid .ag-row"
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: Query spec passes
    Given I have a clean browser page
    When I navigate to "/components/query"
    And I wait for the page to be interactive
    And I wait for the selector ".lc-dg-table"
    And I run the page's embedded features
    Then every embedded feature passes
