Feature: Two tabs, one server — a page exports a class and a function, another imports them
  Michel, 2026-10-20 (hq/architecture/distributed.md, "The simplest
  example"): reaching other running pages is an explicit intent, one word
  on the model that offers itself — export="lc://demo". A client imports
  with a link, [the demo](lc://demo) {: .model #m }, writes no Python, and
  its grid, gutter and buttons work as for a local class: the object acts
  where it lives, the rows come back. One server, one loop, in order; the
  browser's own channel is the wire.

  Background:
    Given I have a clean browser page
    And the GitHub contents API serves "courses/demo/dist/server.md" with the document:
      """
      # The server

      ```csv
      name,count
      visits,0
      ```
      {: .dataset #tally }

      ```python
      class Tally(Object, source="tally"):
          def bump(self):
              self.count += 1

      def hello(name="world"):
          return "hello " + name
      ```
      {: .model export="lc://demo" }

      [the tally](#)
      {: .datagrid source="Tally" #server_grid }

      ```csv
      n,from,what
      ```
      {: .dataset #traffic }

      [what was asked](#)
      {: .datagrid source="traffic" #traffic_grid }
      """
    And the GitHub contents API serves "courses/demo/dist/client.md" with the document:
      """
      # A client

      [the demo](lc://demo)
      {: .model #m }

      [the tally](#)
      {: .datagrid source="m.Tally" #grid }

      [Say hello](#)
      {: .button #hi }
      ```python
      def on_click(button):
          m.hello("Michel")
      ```
      {: .onclick }

      [the answer](#)
      {: .datagrid source="m.hello" #answer }
      """

  Scenario: The client follows, bumps through the server, calls its function; a second client sees it; the server gone, the client says so
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/dist/server.md"
    And I wait for the page to be interactive
    And I open "/run.html#src=gh:acme/demo/courses/demo/dist/client.md" in tab 2
    Then in tab 2 the grid "grid" shows "visits" with count "0", and ⋯ offers "bump"
    When in tab 2 I press "bump" in the gutter of "visits" in "grid"
    Then in tab 1 the grid "server_grid" shows "visits" with count "1"
    And in tab 2 the grid "grid" shows "visits" with count "1"
    And in tab 1 the grid "traffic_grid" lists "follow" and "Tally.tally_1.bump()"
    When in tab 2 I press the button "hi"
    Then in tab 2 the grid "answer" shows "hello Michel"
    When I open "/run.html#src=gh:acme/demo/courses/demo/dist/client.md" in tab 3
    Then in tab 3 the grid "grid" shows "visits" with count "1"
    When I close tab 1
    Then in tab 2 the grid "grid" says "nobody serves lc://demo"
