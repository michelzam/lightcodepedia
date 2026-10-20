Feature: Two tabs, one server — a page serves a class and a function, another imports them
  Michel, 2026-10-20 (hq/architecture/distributed.md, "The simplest
  example"): reaching other running pages is an explicit intent, a line of
  its own — [the demo](lc://demo) {: .server #demo model="tally_model" }.
  A client imports with the same link on a .model, writes no Python, and
  its grid, gutter and buttons work as for a local class: the object acts
  where it lives, the rows come back. The server's id is a dataset of its
  requests. One server per name, one loop, in order; the browser's own
  channel is the wire.

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
      {: .model #tally_model }

      [the demo](lc://demo)
      {: .server #demo model="tally_model" }

      [the tally](#)
      {: .datagrid source="Tally" #server_grid }

      [what was asked](#)
      {: .datagrid source="demo.traffic" #traffic_grid }

      [who follows](#)
      {: .datagrid source="demo.clients" #clients_grid }

      [what is served](#)
      {: .datagrid source="demo.contract" #contract_grid }
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

      [what was imported](#)
      {: .datagrid source="m.contract" #contract }
      """

  Scenario: The client follows, bumps through the server, calls its function; a second client sees it; the server gone, the client says so
    The server is an explicit line, its id a dataset of requests (Michel,
    2026-10-20: "#traffic is a bit obscure… an explicit server with a knob to
    model… offering a #serverID we could use as a dataset").

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
    And in tab 2 the grid "grid" wears ↻ in its corner
    # born with the server: clients, contract — on both sides; the server as a python object
    And in tab 1 the grid "clients_grid" has 1 row, with 2 or more requests
    And in tab 1 the grid "contract_grid" lists "Tally.bump" and "function"
    And in tab 2 the grid "contract" lists "Tally.bump" and "function"
    And in tab 1 the python "Page().demo.traffic.count" gives "3"
    # a reload is the same tab, not a new client
    When I reload tab 2
    Then in tab 2 the grid "grid" shows "visits" with count "1"
    And in tab 1 the grid "clients_grid" has 1 row, with 2 or more requests
    When I open "/run.html#src=gh:acme/demo/courses/demo/dist/client.md" in tab 3
    Then in tab 3 the grid "grid" shows "visits" with count "1"
    When I close tab 1
    Then in tab 2 the grid "grid" says "nobody serves lc://demo"

  Scenario: A server re-rendered in a pad keeps one channel — a bump counts once; the heartbeat is not traffic
    Michel, 2026-10-20: "Why each bump from client adds 8?" — a pad or the
    editor re-renders its model block; every render had opened one more
    channel, and a verb ran once per stale listener. And "not clear who
    fills #traffic and when": the heartbeat was listed as a follow.

    Given the GitHub contents API serves "courses/demo/dist/server_pad.md" with the document:
      """
      # The server, in a pad

      `````markdown
      ```csv
      name,count
      visits,0
      ```
      {: .dataset #tally }

      ```python
      class Tally(Object, source="tally"):
          def bump(self):
              self.count += 1
      ```
      {: .model #tally_model }

      [the demo](lc://demo)
      {: .server #demo model="tally_model" }

      [the tally](#)
      {: .datagrid source="Tally" #server_grid }

      [what was asked](#)
      {: .datagrid source="demo.traffic" #traffic_grid }

      {= demo.
      `````
      {: .mdpad #srv decorations="true" rows="20" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/dist/server_pad.md"
    And I wait for the page to be interactive
    And I open "/run.html#src=gh:acme/demo/courses/demo/dist/client.md" in tab 2
    Then in tab 2 the grid "grid" shows "visits" with count "0"
    When in tab 1 I retype the model block of the "srv" pad three times
    And in tab 2 I press "bump" in the gutter of "visits" in "grid"
    Then in tab 1 the grid "server_grid" shows "visits" with count "1"
    And in tab 2 the grid "grid" shows "visits" with count "1"
    And after 9 seconds, in tab 1 the grid "traffic_grid" lists one "follow" and one "bump"
    # completion knows what hangs under a server (Michel, 2026-10-20: "code completion should help")
    And in tab 1 completion in the "srv" pad after "{= demo." offers "traffic, clients, contract"

  Scenario: A second server of the same name stands by — one server per name
    Michel, 2026-10-20: "a second server can listen as well… they are both
    propagated to the clients but not to each other". The rule: one owner
    per source. A newcomer claims the name; the holder says taken; the
    newcomer stands by and serves nothing.

    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/dist/server.md"
    And I wait for the page to be interactive
    And I open "/run.html#src=gh:acme/demo/courses/demo/dist/server.md" in tab 2
    Then in tab 2 the server "demo" stands by
    And in tab 2 the grid "traffic_grid" shows "stands by"
    When I open "/run.html#src=gh:acme/demo/courses/demo/dist/client.md" in tab 3
    And in tab 3 I press "bump" in the gutter of "visits" in "grid"
    Then in tab 1 the grid "server_grid" shows "visits" with count "1"
    And in tab 2 the grid "server_grid" shows "visits" with count "0"
