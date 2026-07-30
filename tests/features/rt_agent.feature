Feature: The tutor on a runner render studies the course, not the runner
  knowledge: [self] used to resolve against location.pathname — on /run that
  is the runner shell, so the avatar answered about the vehicle instead of
  the content. Under a page-level render, self now means the RENDERED file
  plus the {: .embed } fragments it composes from, fetched from the render's
  own repo, and the bot cache keys per rendered source.

  Scenario: knowledge self pulls the rendered course and its embedded fragments
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a builder key is connected
    And a yaml shim declaring knowledge self is preinstalled
    And the GitHub contents API serves "docs/bots/tutor.md" with the document:
      """
      ```yaml
      knowledge: [self]
      ```
      You are the course tutor.
      """
    And the counting GitHub contents API serves "courses/demo/mod/_why.md" as "why"
    And the GitHub contents API serves "courses/demo/mod/index.md" with the document:
      """
      # Course

      [Why](/_why)
      {: .embed }

      ## One

      Alpha.
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/mod/index.md"
    And I wait for the page to be interactive
    And I note the fragment hit count for "why"
    And I inject a tutor agent into the render root
    Then the fragment "why" is fetched again as tutor knowledge
