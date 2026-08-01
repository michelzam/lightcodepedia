Feature: The course map draws the tree it is given
  A sitemap over a course must show the natural folder organisation without
  anybody declaring it: an index owns the pages beside it and the indexes of
  its subfolders. Prerequisites are a different relation — a constraint
  across the tree, not part of its shape — so they draw dashed and lighter.

  Scenario: Containment edges appear with no links written anywhere
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the course tree contains "courses/demo/index.md, courses/demo/module_01/index.md, courses/demo/module_01/lesson.md"
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/index.md"
    And I wait for the page to be interactive
    And I wait for the selector ".lc-sitemap svg"
    Then the map draws 2 "tree" edges
    And the map draws 0 "prereq" edges

  Scenario: A prerequisite draws dashed, over the tree
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the course tree contains "courses/demo/index.md, courses/demo/module_01/index.md, courses/demo/module_01/lesson.md"
    And "courses/demo/module_01/lesson.md" requires "index.md"
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/index.md"
    And I wait for the page to be interactive
    And I wait for the selector ".lc-sitemap svg"
    Then the map draws 1 "prereq" edges
    And the prerequisite edge is dashed and lighter than the tree
    And the map explains its arrows

  Scenario: The page you are on is a landmark on its own map
    Given I have a clean browser page
    And a marked shim is preinstalled
    And the course tree contains "courses/demo/index.md, courses/demo/module_01/index.md, courses/demo/module_01/lesson.md"
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/index.md"
    And I wait for the page to be interactive
    And I wait for the selector ".lc-sitemap svg"
    Then exactly one node is marked as here
    And the here node is bigger than the others

  Scenario: A link back up to the parent index draws no second arrow
    The tree already joins them; a return link would only add clutter (and
    a bidirectional curve). A prerequisite the same way is still kept.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And the course tree contains "courses/demo/index.md, courses/demo/module_01/index.md, courses/demo/module_01/lesson.md"
    And "courses/demo/module_01/lesson.md" links back to "index.md"
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/index.md"
    And I wait for the page to be interactive
    And I wait for the selector ".lc-sitemap svg"
    Then the map draws 2 "tree" edges
    And the map draws 0 "link" edges
