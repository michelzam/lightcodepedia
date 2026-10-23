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

  Scenario: The simplest server serves pages — a shelf on the client, a tap lands where the server says, a folder gives its index, a server asks another server
    Michel, 2026-10-22: "the simplest case should be just: I serve some
    pages". pages= names rows of path and file; a folder's path answers with
    its index.md, like today's site; a file that is another server (lc://)
    is asked in turn. The client's shelf is a folder on s.pages — no repo, no
    manifest — and a tap asks the server where the page is. A refusal is a
    line under the shelf.

    Given the GitHub contents API serves "courses/demo/dist/site.md" with the document:
      """
      # The site

      ```csv
      path,file,title
      /,courses/demo/dist/site/,🏠 Home
      /walks,courses/demo/dist/site/walks.md,🐕 Walks
      /annex,lc://annex,📎 The annex
      ```
      {: .dataset #site_pages }

      ```csv
      page,count
      /,0
      ```
      {: .dataset #visits }

      ```python
      class Visit(Object, source="visits"):
          def bump(self):
              self.count += 1
      ```
      {: .model #site_model }

      [the site](lc://site)
      {: .server #site model="site_model" pages="site_pages" }

      [the pages served](#)
      {: .datagrid source="site.pages" #pages_grid }

      [what was asked](#)
      {: .datagrid source="site.traffic" #traffic_grid }
      """
    And the GitHub contents API serves "courses/demo/dist/annex.md" with the document:
      """
      # The annex

      ```csv
      path,file
      /,courses/demo/dist/annex/
      ```
      {: .dataset #annex_pages }

      [the annex](lc://annex)
      {: .server #annex pages="annex_pages" }

      [what was asked](#)
      {: .datagrid source="annex.traffic" #traffic_grid }
      """
    And the GitHub contents API serves "courses/demo/dist/visitor.md" with the document:
      """
      # A visitor

      [the site](lc://site)
      {: .model #s }

      [the pages](#)
      {: .folder source="s.pages" #shelf }

      [the visits](#)
      {: .datagrid source="s.Visit" #visits }
      """
    And the GitHub contents API serves "courses/demo/dist/site/index.md" with the document:
      """
      # Home of the site
      """
    And the GitHub contents API serves "courses/demo/dist/site/walks.md" with the document:
      """
      # The walks page
      """
    And the GitHub contents API serves "courses/demo/dist/annex/index.md" with the document:
      """
      # Home of the annex
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/dist/site.md"
    And I wait for the page to be interactive
    And I open "/run.html#src=gh:acme/demo/courses/demo/dist/annex.md" in tab 2
    And I open "/run.html#src=gh:acme/demo/courses/demo/dist/visitor.md" in tab 3
    Then in tab 1 the grid "pages_grid" lists "/walks" and "lc://annex"
    And in tab 3 the shelf "shelf" shows the cards "🏠 Home, 🐕 Walks, 📁 📎 The annex"
    And in tab 3 the grid "visits" shows "/" with count "0"
    # a page row: the server names the file, the browser lands on it
    When in tab 3 I tap the card "Walks" of "shelf"
    Then in tab 3 the page heading reads "The walks page"
    And in tab 1 the grid "traffic_grid" lists "follow" and "page /walks"
    # a folder row: / answers with its index.md
    When in tab 3 I go back
    And in tab 3 I tap the card "Home" of "shelf"
    Then in tab 3 the page heading reads "Home of the site"
    # a server row: the site asks the annex, the annex's folder answers
    When in tab 3 I go back
    And in tab 3 I tap the card "The annex" of "shelf"
    Then in tab 3 the page heading reads "Home of the annex"
    And in tab 1 the grid "traffic_grid" lists "page /annex" and "page /walks"
    And in tab 2 the grid "traffic_grid" lists "page /" and "page /"
    # the annex gone: the site says so, the shelf shows it
    When in tab 3 I go back
    And I close tab 2
    And in tab 3 I tap the card "The annex" of "shelf"
    Then in tab 3 the shelf "shelf" says "lc://annex answers nothing"
    And in tab 1 the python "Page().site.pages.count" gives "3"
    # the root folder row catches every path under it (found 2026-10-22 in run mode: it read "/" and caught nothing)
    And in tab 3 asking the site for "/deep" answers the file "courses/demo/dist/site/deep.md"
