Feature: A dataset runs a SQL statement on a Databricks warehouse, with this device's token
  Michel, 2026-09-26, for George's data centre: "having keys in the users'
  browser is the perfect match with the CFO's need to not share strategic
  data with anyone else". The fence is SQL, dbx= names the warehouse, the
  statement goes through a same-origin proxy that forwards the browser's
  own token and stores nothing. Rows land on the bus like any dataset.

  Background:
    Given I have a clean browser page
    And the GitHub contents API serves "apps/arr.md" with the document:
      """
      # ARR by region

      ```sql
      SELECT region, SUM(arr_kusd) AS arr_kusd FROM finance.accounts GROUP BY region
      ```
      {: .dataset #arr dbx="wh-0123" }

      [ARR by region](#)
      {: .datagrid source="arr" #arr_grid height="200" }
      """
    And a Databricks warehouse behind "/dbx" that answers after one poll with the rows:
      | region | arr_kusd |
      | EMEA   | 120.5    |
      | AMER   | 98       |
      | APAC   | 41.25    |

  Scenario: With a token on this device, the statement runs and the grid fills
    Given a Databricks token "tok-1" on this device
    When I navigate to "/run.html#src=gh:acme/demo/apps/arr.md"
    And I wait for the page to be interactive
    Then the grid "arr_grid" shows 3 rows
    And the bar of "arr" reads "3 rows"
    And the warehouse was asked with the token "tok-1" for "wh-0123"
    And the number columns arrived as numbers

  Scenario: Without a token, the bar asks for one and the query runs once it is pasted
    When I navigate to "/run.html#src=gh:acme/demo/apps/arr.md"
    And I wait for the page to be interactive
    Then the bar of "arr" asks for a token
    And the warehouse was not asked
    When I paste the Databricks token "tok-2" in the bar of "arr"
    Then the grid "arr_grid" shows 3 rows
    And the warehouse was asked with the token "tok-2" for "wh-0123"

  Scenario: A refused token is said in the bar, not swallowed
    Given a Databricks token "dead" on this device
    And the warehouse refuses the token
    When I navigate to "/run.html#src=gh:acme/demo/apps/arr.md"
    And I wait for the page to be interactive
    Then the bar of "arr" reads "token refused"
