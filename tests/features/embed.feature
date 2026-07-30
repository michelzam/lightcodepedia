Feature: Folder-relative embeds — a course page composes from its siblings
  A render that advertises its source file via data-lc-src-path (the runner's
  bench/vault render, the editor preview of a file outside docs/) makes
  {: .embed } resolve against that file's OWN folder — "/x" and "x" both mean
  "my sibling x.md" — because courses/ and hubs/ never exist under docs/.
  Site pages keep the site-root meaning untouched.

  Scenario: An embed under a course render fetches the sibling fragment
    Given I have a clean browser page
    And the GitHub contents API serves "courses/demo/module_00/_why.md" with "## Sibling loaded"
    When I navigate to "/components/embed_page"
    And I wait for the page to be interactive
    And I inject an embed of "/_why" rendered from "courses/demo/module_00/index.md"
    Then the injected embed shows "Sibling loaded"

  Scenario: A parent-folder fragment resolves through ../
    Given I have a clean browser page
    And the GitHub contents API serves "courses/demo/_shared.md" with "## Shared fragment"
    When I navigate to "/components/embed_page"
    And I wait for the page to be interactive
    And I inject an embed of "../_shared" rendered from "courses/demo/module_00/index.md"
    Then the injected embed shows "Shared fragment"

  Scenario: An image embed under a course render becomes the image itself
    Given I have a clean browser page
    And the GitHub contents API serves the image "courses/demo/module_00/_logo.png"
    When I navigate to "/components/embed_page"
    And I wait for the page to be interactive
    And I inject an embed of "_logo.png" rendered from "courses/demo/module_00/index.md"
    Then the injected embed shows an image from a blob URL

  Scenario: A relative image in a runner render resolves through the builder key
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key is connected
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Pic page

      ![logo](pic.png)
      """
    And the GitHub contents API serves the image "courses/demo/mod/pic.png"
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    Then the runner's image resolves to a blob URL

  Scenario: A site-absolute image in a runner render loads from the site
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Banner page

      ![banner](/courses/AI-Builders.png)
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    Then the runner's image decodes from the site

  Scenario: A site-absolute image embed stays a site asset — with the height knob
    Given I have a clean browser page
    When I navigate to "/components/embed_page"
    And I wait for the page to be interactive
    And I inject a sized embed of "/courses/AI-Builders.png" height "400" rendered from "courses/demo/module_00/index.md"
    Then the injected embed shows the site image 400px tall

  Scenario: A quiz inside an embedded fragment becomes a live component
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the GitHub contents API serves "courses/demo/mod/_deal.md" with the document:
      """
      **Q:** Ready?

      - [x] Yes
      - [ ] No
      {: .quiz }
      """
    When I navigate to "/components/embed_page"
    And I wait for the page to be interactive
    And I inject an embed of "/_deal" rendered from "courses/demo/mod/index.md"
    Then the injected embed upgrades the quiz component
