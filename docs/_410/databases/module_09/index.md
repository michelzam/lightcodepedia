# 🤑 09 · TILT — Transactions, Integrity, Logic, and Trust

🛢️ Until now you mostly read data. This week you change it — safely.

Ask Doc for a tour!
{: .avatar_trigger target="guide" }

Welcome back! Databases tell living stories — not just what data **is**,
but how it **changes**. Reading (SELECT) shows the present. Changing
(INSERT, UPDATE, DELETE) shapes the future. **TILT** names the four
habits that keep those changes meaningful and safe: **Transactions,
Integrity, Logic, and Trust**.

This week happens mostly in **MySQL Workbench**, on a tiny new
database, **shopdb**: two tables, six rows, made to be broken and
repaired. Your **uwm** database stays exactly as you built it. Every
step says what to run and **what you should see**, so you can check
yourself at each line. Work in order, one step at a time.

Every step ends with a little quiz, just for you. Take your time. 🙂

> Why did the transaction break up with the database? It needed more
> commitment. 💍

````
### 🧰 Step 0 · Before you start: a small shop, just for this week

Open MySQL Workbench and your **Local instance**. This week we do not
touch your uwm database: changing data means making mistakes on
purpose, and those belong in a sandbox. Meet **shopdb** — two tables
from the dataquest shop, three customers, three orders.

```sql
CREATE DATABASE IF NOT EXISTS shopdb;
USE shopdb;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Customers;

CREATE TABLE Customers (
  CustomerID   INT NOT NULL,
  CustomerName VARCHAR(100),
  City         VARCHAR(50),
  PRIMARY KEY (CustomerID)
);

CREATE TABLE Orders (
  OrderID    INT NOT NULL,
  CustomerID INT NOT NULL,
  OrderDate  DATE,
  PRIMARY KEY (OrderID),
  FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

INSERT INTO Customers (CustomerID, CustomerName, City) VALUES
  (1, 'Alfreds Futterkiste', 'Berlin'),
  (2, 'Ana Trujillo Emparedados', 'México D.F.'),
  (3, 'Around the Horn', 'London');

INSERT INTO Orders (OrderID, CustomerID, OrderDate) VALUES
  (10248, 3, '2026-10-05'),
  (10249, 1, '2026-10-06'),
  (10250, 3, '2026-10-08');

SELECT COUNT(*) AS orders FROM Orders;
```

Run it all at once (⚡ the lightning bolt). **You should see:** a last
result of **3** orders, and **shopdb** in the Navigator's SCHEMAS (click
🔄 to refresh). Lost at any point this week? Run this script again: it
rebuilds shopdb from scratch, and only shopdb.

**Q:** Why practice on shopdb instead of your uwm database?

- [ ] Because uwm is read-only once a model has been forward engineered

  > Forward engineering does not lock anything. Your uwm can change —
  > we just do not want to break it.

- [x] Mistakes on purpose belong in a sandbox you can rebuild in one click

  > The setup script recreates shopdb from scratch, any time. Your uwm
  > keeps your own choices.

- [ ] Because transactions only work on databases with two tables

  > Transactions work on any InnoDB table. Small is simply easier to
  > check by eye.

- [ ] Because shopdb is faster, being named after a shop

  > Names do not make databases fast. Small does make them easy to
  > read.
{: .quiz }
````
{: .accordion #setup }

````
### 🤑 Step 1 · Reading and changing — what Workbench already did for you

[INSERT, as Workbench writes it](_slides/m09_04.jpg)
{: .embed image="true" width="100%" }

You have been changing data for weeks. Each time you typed a row in the
**Result Grid** and clicked **Apply**, Workbench showed you a script —
an INSERT or an UPDATE — and ran it for you. The grid is a friendly
face; underneath, it is always SQL.

This week we write the changes ourselves, and we learn to make them
**safe**:

- 🔄 **Transactions** make change reversible.
- ⚖️ **Integrity** makes relationships reliable.
- 🧩 **Logic** makes decisions deliberate.
- 💡 Together, they build **Trust**.

**Q:** You add a row in the Result Grid and click Apply. What reaches
the database?

- [ ] A picture of the grid, which the database copies cell by cell

  > Databases do not read pictures. They read statements.

- [x] An INSERT statement that Workbench wrote and showed you first

  > The Apply dialog shows the exact INSERT before it runs. The grid is
  > a way of writing SQL.

- [ ] Nothing until the next morning, when the database syncs on its own

  > Apply runs right away. Nothing waits for the morning.

- [ ] A SELECT, since the grid is only for reading

  > The grid reads AND writes: an edit becomes an UPDATE, a new row an
  > INSERT.
{: .quiz }
````
{: .accordion #changing }

````
### 🔄 Step 2 · Transactions — all or nothing

[Transactions — making change safely](_slides/m09_05.jpg)
{: .embed image="true" width="100%" }

Imagine a customer, Ana Trujillo, moves from México D.F. to Monterrey
**and** places a new order. Two changes that belong together: you want
**both** to happen — or **neither**. Half of it would leave the shop's
records telling a story that never happened.

A **transaction** groups several changes into one unit of work:

~~~sql
START TRANSACTION;   -- 🟩 begin: nothing is final from here
UPDATE ...;          -- 🟦 a change
INSERT ...;          -- 🟨 another change
COMMIT;              -- 🟩 make them all final, together
~~~

If something goes wrong before COMMIT, **ROLLBACK** cancels every change
since START TRANSACTION — as if nothing ever happened. That is
**atomicity**: all or nothing.

[ACID — the chemistry of reliability](_slides/m09_06.jpg)
{: .embed image="true" width="100%" }

Four letters, four promises, on the shop:

| | Promise | On shopdb |
|---|---|---|
| **A** | Atomicity — all or nothing | Ana's new city and her new order land together, or not at all |
| **C** | Consistency — from one valid state to another | No order for a customer that does not exist |
| **I** | Isolation — your unfinished work is invisible to others | Until you commit, a classmate's connection still sees the old rows |
| **D** | Durability — committed means kept | After COMMIT, Ana's change survives a crash or a restart |

**Q:** Between START TRANSACTION and COMMIT, the second of three changes
fails. With ROLLBACK, what stays in the database?

- [ ] The first change only, since it ran before the failure

  > That is "half of it" — exactly what a transaction prevents.
  > ROLLBACK cancels the first change too.

- [ ] The first and the third, skipping the one that failed

  > A transaction does not cherry-pick. One unit: all or nothing.

- [x] None of the three — the data is as it was before START TRANSACTION

  > Atomicity: ROLLBACK cancels everything since the transaction began.

- [ ] A note to the database administrator, apologizing for the trouble

  > Very polite, but the database keeps no apology notes.
{: .quiz }
````
{: .accordion #transactions }

````
### 🧪 Step 3 · Run it: a transaction that fails on purpose

Time to see atomicity with your own eyes, on shopdb.

**First, the two Workbench toggles.** In the SQL editor's toolbar, switch
**off** both of these:

[The two toggles — OFF × 2](_slides/m09_toggles.jpg)
{: .embed image="true" width="100%" }

- **Continue after failed statements** — off, so a script **stops** at
  its first error instead of running on blindly.
- **Autocommit** — off, so nothing is final until you say COMMIT.
  (START TRANSACTION also pauses autocommit — the toggle makes it the
  rule for the whole tab.)

**Then run the blocks below one at a time**: select the lines of one
block with the mouse, click ⚡ (it runs only the selection), read the
result, then go to the next block. Compare each result with **You should
see**.

**① Before** — look at the rows the transaction will touch:

```sql
USE shopdb;
SELECT COUNT(*) FROM Orders;
SELECT CustomerID, CustomerName, City FROM Customers WHERE CustomerID = 2;
```

You should see: **3** orders, and Ana Trujillo in **México D.F.**

**② The transaction** — Ana moves to Monterrey and places order 10251.
The last line is the mistake: order 10252 names customer 9, who does not
exist.

```sql
START TRANSACTION;
UPDATE Customers SET City = 'Monterrey' WHERE CustomerID = 2;
INSERT INTO Orders (OrderID, CustomerID, OrderDate) VALUES (10251, 2, '2026-10-26');
INSERT INTO Orders (OrderID, CustomerID, OrderDate) VALUES (10252, 9, '2026-10-26');
```

You should see: three green checks, then a red **Error Code: 1452.
Cannot add or update a child row: a foreign key constraint fails** in
the Output panel. Integrity said no.

**③ Inside, before deciding** — the error did **not** undo anything by
itself. Look:

```sql
SELECT COUNT(*) FROM Orders;
SELECT CustomerID, CustomerName, City FROM Customers WHERE CustomerID = 2;
```

You should see: **4** orders and Ana in **Monterrey**. Your session sees
its own unfinished work. Nobody else does yet — that is isolation.

**④ Roll back** — the plan failed halfway, so cancel all of it:

```sql
ROLLBACK;
SELECT COUNT(*) FROM Orders;
SELECT CustomerID, CustomerName, City FROM Customers WHERE CustomerID = 2;
```

You should see: **3** orders and Ana back in **México D.F.** All or
nothing — here, nothing. 🎉

Leave autocommit **off** for the rest of the week, and remember what it
means: from now on, a change you want to keep needs its **COMMIT**.

**If ④ shows 4 orders and Monterrey**, the changes were already
committed: autocommit was on, or START TRANSACTION was skipped. Each
statement became final as it ran, and ROLLBACK had nothing left to
cancel. Run the step 0 script to rebuild shopdb, switch autocommit off,
and try again.

**Q:** In block ③, why does your session already see 4 orders?

- [ ] Because the error rolled back the bad insert and committed the rest

  > An error inside a transaction cancels only the failing statement.
  > Nothing was committed: you decide, with COMMIT or ROLLBACK.

- [x] Your session sees its own changes before they are committed

  > Until COMMIT, the new row is yours alone. Others still count 3.
  > ROLLBACK makes it vanish for you too.

- [ ] Because Workbench caches the count and shows yesterday's number

  > Workbench counts fresh every time. The 4 is real — and not final.

- [ ] Because customer 9 was created automatically to save the day

  > No customer appears by magic. The failed insert left no row.
{: .quiz }
````
{: .accordion #run_it }

````
### ⚖️ Step 4 · Integrity — the database says no

[Integrity — keeping data honest](_slides/m09_07.jpg)
{: .embed image="true" width="100%" }

In step 3, the database refused an order for a customer who does not
exist. That is **referential integrity**: the primary and foreign keys
are guards, and the database checks them on every change.

Try two more refusals on shopdb, one block at a time (each one fails,
and changes nothing):

```sql
-- a) delete a customer who still has orders
DELETE FROM Customers WHERE CustomerID = 3;
```

You should see: **Error Code: 1451. Cannot delete or update a parent
row**. Around the Horn still has two orders.

```sql
-- b) a second order with an existing OrderID
INSERT INTO Orders (OrderID, CustomerID, OrderDate)
VALUES (10248, 1, '2026-10-26');
```

You should see: **Error Code: 1062. Duplicate entry '10248' for key
…PRIMARY**. A primary key never repeats.

A customer can exist without an order — Ana has none — but an order
cannot exist without its customer.

**Q:** Why is `DELETE FROM Customers WHERE CustomerID = 3` refused?

- [ ] Around the Horn is a premium customer, protected by the shop owner

  > No owner was consulted. The keys decide.

- [x] Two orders still point to customer 3 through their CustomerID

  > Deleting the parent would leave those orders pointing to nobody.
  > Integrity refuses.

- [ ] DELETE is forbidden in MySQL unless autocommit is on

  > DELETE works in both modes. This one breaks a key.

- [ ] Customers has no primary key, so no row can be found

  > CustomerID is its primary key. The row is found — and protected.
{: .quiz }
````
{: .accordion #integrity }

````
### 🧩 Step 5 · Logic — look first, act second

[Logic — thinking before changing](_slides/m09_08.jpg)
{: .embed image="true" width="100%" }

Before a risky UPDATE or DELETE, run a **SELECT with the same WHERE**.
It shows exactly the rows the change will touch. Look first, act second.

~~~sql
-- the change you plan:
DELETE FROM Orders WHERE CustomerID = 1;
-- look first, with the same WHERE:
SELECT * FROM Orders WHERE CustomerID = 1;
~~~

One row — order 10249. Now you know what the DELETE will do, before it
does it.

And the classic accident: an UPDATE or DELETE **without a WHERE** touches
**every row**. `SELECT * FROM Orders` shows what `DELETE FROM Orders`
would remove: all of them. 😱

You can practice the look-first habit right here, in the practice block
below: these are SELECTs, so nothing can break.

**Q:** You plan `UPDATE Customers SET City = 'Lyon' WHERE City = 'Berlin'`.
What do you run first?

- [ ] The UPDATE twice, just to be sure it really worked

  > The second run would find nobody left in Berlin — and the first may
  > already have moved too many.

- [ ] `SELECT * FROM Customers` — all of them, to be safe

  > That shows every row, not the ones the UPDATE will change. Use the
  > same WHERE.

- [x] `SELECT * FROM Customers WHERE City = 'Berlin'`

  > The same WHERE, as a SELECT: exactly the rows the UPDATE will
  > change.

- [ ] `ROLLBACK`, in case the UPDATE goes wrong later

  > ROLLBACK cancels what already happened in a transaction. Looking
  > first prevents the mistake.
{: .quiz }
````
{: .accordion #logic }

````
### 💡 Step 6 · Trust — what it all builds toward

Each layer of TILT reinforces the next:

- 🔄 **Transactions** make change reversible.
- ⚖️ **Integrity** makes relationships reliable.
- 🧩 **Logic** makes decisions deliberate.
- 💡 Together, they build **Trust** — in your data, and in yourself as
  its caretaker.

Your database becomes more than storage: a system that honors what is
true, even while it changes.

**Your routine for any change**, from now on, in your project too:

1. **Look** — SELECT with the WHERE you plan to use.
2. **Begin** — START TRANSACTION.
3. **Change** — the INSERTs, UPDATEs, DELETEs.
4. **Check** — SELECT again: is it what you meant?
5. **Decide** — COMMIT if yes, ROLLBACK if not.

**Q:** In that routine, when is the change final?

- [ ] As soon as the UPDATE line shows a green check

  > Green means it ran — inside the transaction, not yet for good.

- [ ] When you close Workbench for the day

  > Closing an open transaction does the opposite: unfinished work is
  > rolled back.

- [x] At COMMIT, after you checked the result

  > COMMIT is the decision. Before it, ROLLBACK can still cancel
  > everything.

- [ ] Never — a transaction can always be undone later

  > After COMMIT, durability takes over: the change is kept.
{: .quiz }
````
{: .accordion #trust }

````
### 🔎 Practice block — look first, here

The same shop as in Workbench — three customers, three orders. These are
SELECTs: look as much as you like, nothing changes.

```json
[
  {"CustomerID": 1, "CustomerName": "Alfreds Futterkiste", "City": "Berlin"},
  {"CustomerID": 2, "CustomerName": "Ana Trujillo Emparedados", "City": "México D.F."},
  {"CustomerID": 3, "CustomerName": "Around the Horn", "City": "London"}
]
```
{: .dataset #Customers }

```json
[
  {"OrderID": 10248, "CustomerID": 3, "OrderDate": "2026-10-05"},
  {"OrderID": 10249, "CustomerID": 1, "OrderDate": "2026-10-06"},
  {"OrderID": 10250, "CustomerID": 3, "OrderDate": "2026-10-08"}
]
```
{: .dataset #Orders }

**① Look first** — the rows `DELETE FROM Orders WHERE CustomerID = 1`
would remove:

```sql
SELECT * FROM Orders
WHERE Orders.CustomerID = 1
```
{: .query source="Orders" #q_look editable="true" }

[the rows the DELETE would remove](#)
{: .datagrid source="q_look" rows="1" }

**② The forgotten WHERE** — the rows `DELETE FROM Orders` would remove,
without a WHERE:

```sql
SELECT * FROM Orders
```
{: .query source="Orders" #q_all editable="true" }

[every order](#)
{: .datagrid source="q_all" rows="3" }

**✋ Your move** — you plan
`UPDATE Orders SET OrderDate = '2026-10-30' WHERE CustomerID = 3`.
Change this query so it shows **exactly the rows that UPDATE would
touch**, then press ▶ Run. Two orders should come back.

```sql
SELECT * FROM Orders
```
{: .query source="Orders" #q_mine editable="true" }

[your answer](#)
{: .datagrid source="q_mine" rows="3" }

The second check at the very bottom stays **red until you do it**.
````
{: .block title="🔎 Practice block" #live }

Three ideas to keep from this week: a transaction is all or nothing,
integrity lets the keys refuse what makes no sense, and
`look_first`[^look_first] runs the WHERE as a SELECT before any change.
The proof below runs the practice block's own queries:

```gherkin
Feature: Look first, act second
  Scenario: The same WHERE shows the rows a change will touch
    Given the orders and the look-first query
    :::python
    self.orders: Dataset = Dataset("Orders")
    self.look: Query = self.page.q_look
    :::
    When the WHERE of the planned DELETE runs as a SELECT
    Then one order comes back, number 10249
    :::python
    assert self.look.count == 1, self.look.count
    assert str(self.look.values("OrderID")[0]) == "10249", self.look.values("OrderID")
    :::

  Scenario: Without a WHERE, every row is touched
    Given the orders and the query with no WHERE
    :::python
    self.orders: Dataset = Dataset("Orders")
    self.all: Query = self.page.q_all
    :::
    When the planned DELETE forgets its WHERE
    Then all three orders would go
    :::python
    assert self.all.count == self.orders.count == 3, self.all.count
    :::
```
{: .feature #activity_proof tags="look_first" visible="true" status="passing" }

And one check that is **yours**. It reads your query in the practice
block and stays red while it still shows every order:

```gherkin
Feature: Your move — look before the UPDATE
  Scenario: The orders of customer 3, and only those
    Given your query in the practice block
    :::python
    self.mine: Query = self.page.q_mine
    :::
    When you press Run on your query
    Then it uses the UPDATE's own WHERE
    :::python
    flat: str = " ".join(self.mine.query.upper().split())
    assert "WHERE" in flat and "CUSTOMERID" in flat.split("WHERE")[-1], \
        "add the UPDATE's WHERE: WHERE Orders.CustomerID = 3, then press Run"
    :::
    And two orders come back, both for customer 3
    :::python
    assert self.mine.count == 2, self.mine.count
    assert {str(c) for c in self.mine.values("CustomerID")} == {"3"}, self.mine.values("CustomerID")
    :::
```
{: .feature #your_move_proof tags="look_first" visible="true" status="pending" celebration="true" }

[Browse](#)
{: .folder parent="true" }

```yaml
bot: doc
voice: en-US
face:
  zoom: 1.2
script:
  - say: "Welcome back! Until now you mostly read data. This week you change it, safely. TILT: transactions, integrity, logic, and trust. Most of it happens in Workbench, and every step tells you what you should see."
  - at: setup
    do: open
    say: "Step zero. One script builds shopdb, a tiny shop just for this week, so your uwm stays untouched. Run it all at once. You should see three orders."
  - at: changing
    do: open
    say: "Step one. Every time you clicked Apply in the grid, Workbench wrote an INSERT or an UPDATE for you. This week you write the changes yourself, and make them safe."
  - at: transactions
    do: open
    say: "Step two. A transaction groups changes into one unit: all or nothing. COMMIT makes them final together. ROLLBACK cancels them all."
  - at: run_it
    do: open
    say: "Step three. Switch off the two toggles, then run the blocks one at a time. The last insert fails on purpose. Look inside, then roll back. Three orders, and Ana back in Mexico City."
  - at: integrity
    do: open
    say: "Step four. The keys are guards. A missing parent, a parent still in use, a repeated key: three refusals, three error codes."
  - at: logic
    do: open
    say: "Step five. Look first, act second. Run the WHERE of your change as a SELECT, and see exactly what it will touch. And never forget the WHERE."
  - at: trust
    do: open
    say: "Step six. Trust is what the other three build. Your routine from now on: look, begin, change, check, decide."
  - at: live
    do: open
    say: "Here is the practice block, the same little shop. Look first, then see what a forgotten WHERE would touch. Your move: show exactly the orders of customer three. The last check stays red until you do."
stories:
  summarize the page:
    - 'You might wonder: summarize the page'
    - This week is about changing data safely, with four habits called TILT.
    - Transactions group changes so they happen all together or not at all.
    - Integrity lets the keys refuse changes that make no sense.
    - Logic means running the WHERE as a SELECT before any change.
    - Trust is what the three build, in your data and in yourself.
  why did the error not undo everything:
    - 'You might wonder: why did the error not undo everything'
    - Inside a transaction, an error cancels only the statement that failed.
    - The earlier changes wait, unfinished, until you decide.
    - COMMIT keeps them, ROLLBACK cancels them all.
  why does rollback do nothing:
    - 'You might wonder: why does rollback do nothing'
    - ROLLBACK only cancels changes that are not committed yet.
    - With autocommit on and no START TRANSACTION, each statement is final as it runs.
    - Run the step zero script to rebuild shopdb, switch autocommit off, and try again.
```
{: .avatar #guide dock="true" size="115" }

[^look_first]: **look_first** — running the WHERE of a planned UPDATE or
    DELETE as a SELECT, to see exactly which rows it will touch.
