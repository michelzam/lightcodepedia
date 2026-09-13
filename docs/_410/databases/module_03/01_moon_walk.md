# 🧱 The Moon Walk

🌙 Twice now the shop's tables were handed to you, already shaped.
Today the shaping is yours: one table exists on your machine —
Customers, with Thomas in it — and the shop needs its **orders**. You
will walk backwards from the data to its structure, build the missing
table, tie it to Customers with a key, and walk back again to see what
the database now draws.

- [🔧 Setup — MySQL on your machine](00_setup.md)
{: .prerequisite }

Ask Doc for a tour!
{: .avatar_trigger target="guide" }

```
### 💾 0 · Backup first — just in case

[Server → Data Export](_slides/m03_03.jpg)
{: .embed image="true" width="100%" }

Before touching a database, make a copy of it. In Workbench:
**Server → Data Export**, tick your schema, *Export to Self-Contained
File*, **Start Export**. The way back is **Server → Data Import**.

Workbench's exporter misbehaves on some versions. If it errors, try
the other export option, or simply save your scripts — the point is
that a copy exists before you change anything. Builders back up;
gamblers do not.
```
{: .accordion #backup }

```
### 🌙 1 · Reverse engineer — from data to structure

[Database → Reverse Engineer: from the data to its model](_slides/m03_04.jpg)
{: .embed image="true" width="100%" }

You have data. Ask the database for its **structure**: in Workbench,
**Database → Reverse Engineer…**, pick your schema, next, next,
Execute. A diagram opens with one box: **Customers** — the entity —
listing its columns, and beside each column its **type**:

- `CustomerID INT` — a whole number 🔢, the primary key 🔑
- `CustomerName VARCHAR(100)` — text 🔤, up to 100 characters
- `City VARCHAR(50)`, `Country VARCHAR(50)` — text
- an `OrderDate DATE` is coming — a date 📆

A type says what a column can hold and how much room it gets. That
is the moon walk: the data was there first; the structure is what the
database reads back out of it.
```
{: .accordion #reverse }

````
### 🧱 2 · Build Orders — a table related to Customers

The shop needs orders, and every order belongs to a customer.

[Build a new table, related to Customers](_slides/m03_05.jpg)
{: .embed image="true" width="100%" }

Say it
in English first: *an order has a number, a date, and the customer who
placed it.* Now the SQL — paste it into a Workbench query tab with your
database as the default schema (double-click it in the left panel so
it turns bold), then press ⚡:

```sql
-- Create Orders with a FK to Customers
CREATE TABLE Orders (
  OrderID    INT AUTO_INCREMENT PRIMARY KEY,
  CustomerID INT NOT NULL,
  EmployeeID INT,
  OrderDate  DATE NOT NULL,
  ShipperID  INT,
  FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);
```

Line by line:

- `OrderID INT AUTO_INCREMENT PRIMARY KEY` — the order's identity.
  The database hands out the numbers itself: 1, 2, 3…
- `CustomerID INT NOT NULL` — every order **must** name a customer.
  No orphan orders.
- `FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)` — and
  the customer it names must **exist**. The database now refuses an
  order for customer 999 if there is no customer 999.
- `EmployeeID`, `ShipperID` — room for later, empty allowed.

Refresh the left panel: Orders is there, empty. Now fill it — with
**your own** CustomerID values, the ones your Customers table holds:

```sql
-- Insert orders tied to customers
INSERT INTO Orders (CustomerID, OrderDate)
VALUES
  (1, '2025-09-14'),
  (4, '2025-09-14');

-- Select Orders
SELECT * FROM Orders;

-- Select Orders and their Customers
SELECT * FROM Orders, Customers
WHERE Orders.CustomerID = Customers.CustomerID;
```

[The script, and Orders in the left panel](_slides/m03_06.jpg)
{: .embed image="true" width="100%" }

Three things to notice in the result grids: the OrderIDs you never
typed, the join from module 02 running on tables that are now yours,
and — try it — an insert with a CustomerID that does not exist. The
database says no. That refusal is the foreign key at work.
````
{: .accordion #build }

**Q:** Why does the script declare `CustomerID INT NOT NULL` in Orders?

- [ ] So the column is indexed and the join runs faster

  > The foreign key does earn an index, but NOT NULL is about meaning,
  > not speed: a value must be there.

- [x] Because every order is placed by exactly one customer — an order without one is not allowed

  > The English sentence, made into a rule the database enforces: an
  > order without a customer cannot exist. NOT NULL says "always one";
  > the FOREIGN KEY says "and a real one".

- [ ] Because primary keys are always declared NOT NULL

  > True of primary keys — but CustomerID is not the key of Orders.
  > It is a foreign key, and the rule was chosen, not inherited.
{: .quiz }

````
### 🔎 3 · Check the sentence on the page first

Here is a small copy of what your two tables should look like — a
Customers slice, and two orders pointing at it. The join runs live;
edit it, run it, and compare with your Workbench grid:

```json
[
  {"CustomerID": 1, "CustomerName": "UWM", "ContactName": "Michel Zam", "City": "Milwaukee", "Country": "USA"},
  {"CustomerID": 4, "CustomerName": "Around the Horn", "ContactName": "Thomas Hardy", "City": "London", "Country": "UK"},
  {"CustomerID": 5, "CustomerName": "Around the Horn", "ContactName": "Jay", "City": "Paris", "Country": "France"}
]
```
{: .dataset #Customers }

[your Customers](#)
{: .datagrid bind="Customers" rows="3" }

```json
[
  {"OrderID": 1, "CustomerID": 1, "EmployeeID": null, "OrderDate": "2025-09-14", "ShipperID": null},
  {"OrderID": 2, "CustomerID": 4, "EmployeeID": null, "OrderDate": "2025-09-14", "ShipperID": null}
]
```
{: .dataset #Orders }

[your Orders](#)
{: .datagrid bind="Orders" rows="2" }

```sql
SELECT OrderID, OrderDate, ContactName, City
FROM Orders, Customers
WHERE Orders.CustomerID = Customers.CustomerID
```
{: .query source="Orders,Customers" #q_orders editable="true" }

[each order with its customer](#)
{: .datagrid source="q_orders" rows="2" }

Two orders, two customers named, nobody orphaned. Jay in Paris placed
nothing yet — and the join, rightly, does not invent an order for him.
````
{: .block title="🔎 Your two tables — live" #check }

````
### 🌙 4 · Reverse engineer again — the model grows

Back to **Database → Reverse Engineer…**. The diagram now shows two
boxes and a line between them:

[Reverse engineer again: Orders joins the model, a diamond on its foreign key](_slides/m03_07.jpg)
{: .embed image="true" width="100%" }

Here is the same picture, drawn on the
page from a hidden declaration of your two tables:

```python
@component(icon="👤")
class Customer(Object):
    CustomerID   = Attr(int, hint="primary key")
    CustomerName = Attr(str)
    ContactName  = Attr(str)
    City         = Attr(str)
    Country      = Attr(str)

@component(icon="🧾")
class Order(Object):
    OrderID    = Attr(int, hint="primary key, AUTO_INCREMENT")
    CustomerID = Attr("Customer", hint="foreign key → Customers, NOT NULL")
    EmployeeID = Attr(int, hint="room for later")
    OrderDate  = Attr(str)
    ShipperID  = Attr(int, hint="room for later")
```
{: .model #two_tables_model }

[Customers and Orders — two entities, one relationship](#)
{: .diagram scope="Order" states="false" }

Read it:

- **Orders** is a new entity; its `CustomerID` wears a diamond ♦ in
  Workbench — the foreign key — and gained an index, since the
  database will look customers up by it all day.
- The line is a **relationship**, **1 : N**: one customer, many
  orders. A customer may place zero, one or many orders; each order is
  placed by exactly one customer. The crow's foot sits on the Orders
  side.
- Lay it out **parents above children**: Customers on top, Orders
  below — the picture above already does. The table with the primary
  key stands over the table that points at it. A diagram you can read
  top-down is a diagram you can reason about.

Two facts about tables sit under all of this. **Columns are fixed**:
the structure is decided at design time. **Rows are extensible**: the
data grows forever at runtime. So a thing that can repeat — an order,
another order — never becomes a column; it becomes a row in its own
table, pointing back with a foreign key.
````
{: .accordion #again }

**Q:** The reverse-engineered diagram draws Customers above Orders. What
does the layout say?

- [ ] Customers was created first, so it ranks higher

  > Creation order is history, not structure. Swap the dates and the
  > diagram should still read the same way.

- [x] Orders points at Customers: the foreign key side sits below the primary key side

  > Parents above children. The table holding the primary key stands
  > over the table whose foreign key references it — one customer,
  > many orders, read top-down.

- [ ] Customers has more rows, and bigger tables float up

  > Row counts are runtime; the model is design. Orders will outgrow
  > Customers within a week and still hang below it.
{: .quiz }

```
### 🏴‍☠️ 5 · Your quest — two more tables

The shop has shippers and employees, and Orders already saved a seat
for each: `ShipperID`, `EmployeeID`. Give them a table to point at:

1. **Shippers** — `ShipperID INT AUTO_INCREMENT PRIMARY KEY`,
   `ShipperName VARCHAR(100) NOT NULL`, `Phone VARCHAR(30)`. Insert
   Speedy Express, United Package, Federal Shipping.
2. Tie the seat to the table:
   `ALTER TABLE Orders ADD FOREIGN KEY (ShipperID) REFERENCES Shippers(ShipperID);`
   then update your two orders with a ShipperID each.
3. **Employees** the same way — `EmployeeID`, `LastName`, `FirstName`,
   `BirthDate DATE` — and the foreign key on `Orders.EmployeeID`.
4. Reverse engineer once more: **four entities**, three lines, every
   one 1 : N, every many side below its one side. Then one join that
   spans them: *each order with its customer's name and its shipper's
   name.*

English first, each time. The sentence tells you which side gets the
foreign key: the side that says *many*.
```
{: .accordion #quest }

```
### 🔬 Observations — what we just played

- 🌙 The moon walk: data first, then the structure the database reads
  out of it — and after every change, read it out again.
- 🔤 A column has a **type**: INT, VARCHAR(n), DATE — what it holds
  and how much room it gets.
- 🔑 A **primary key** gives a row its identity; the database can hand
  the numbers out itself.
- ♦ A **foreign key** makes a sentence a rule: every order names a
  customer, and a real one.
- 🖇️ One line in the diagram is a **relationship**, 1 : N, read
  parents above children.
- 🧱 Columns are fixed, rows are extensible: things that repeat become
  rows in a table of their own.

Next: the words for all of this, and three smell tests, on the design
page.
```
{: .accordion #observations }

Four words to keep from this page: a `type`[^type] says which values fit
a column; a `primary key`[^primary_key] gives a row its identity; a
`foreign key`[^foreign_key] makes "every order names a customer" a rule
the database enforces; the line between the two tables is a
`relationship`[^relationship]. The proof below reads the page's own copy
of your two tables:

```gherkin
Feature: Every order names a customer that exists
  Scenario: The foreign key values all answer to a primary key
    Given the Customers and Orders on this page
    :::python
    self.customers: Dataset = Dataset("Customers")
    self.orders: Dataset = Dataset("Orders")
    :::
    Then each order's CustomerID is a customer's CustomerID
    :::python
    keys: list[str] = self.customers.values("CustomerID")
    refs: list[str] = self.orders.values("CustomerID")
    assert refs and all(r in keys for r in refs), refs
    :::

  Scenario: The join names one customer per order and invents none
    Given the join over the two tables
    :::python
    self.joined: Query = self.page.q_orders
    self.orders: Dataset = Dataset("Orders")
    :::
    Then it returns exactly one line per order
    :::python
    assert self.joined.count == self.orders.count, self.joined.count
    names: list[str] = sorted(self.joined.values("ContactName"))
    assert names == ["Michel Zam", "Thomas Hardy"], names
    :::
```
{: .feature #moon_proof tags="type, primary key, foreign key, relationship" visible="true" status="passing" }

[Browse](#)
{: .folder parent="true" }

```yaml
bot: doc
voice: en-US
face:
  zoom: 1.2
script:
  - say: "Twice the tables were handed to you. Today you build one — and the database will draw you a picture of what you did. First, a copy."
  - at: backup
    do: open
    say: "Backup before anything. Server, Data Export, your schema, one file. Builders back up; gamblers do not."
  - at: reverse
    do: open
    say: "Reverse engineer: the database reads its own structure back out of the data. One entity, Customers, and beside every column its type — a whole number, text with a size, a date."
  - at: build
    do: open
    say: "Now the shop's orders. Say it in English: an order has a number, a date, and the customer who placed it. The script makes each half a rule — NOT NULL means always one customer, FOREIGN KEY means a real one. Then insert two orders with your own customer IDs, and join."
  - at: check
    do: open
    say: "Here is the same shape on the page, live. Two orders, two customers named, nobody orphaned — and Jay in Paris, who ordered nothing, gets no invented order."
  - at: again
    do: open
    say: "Reverse engineer again and the model has grown: two boxes, one line, one to many. Lay it out parents above children — the primary key over the foreign key that points at it."
  - at: quest
    do: open
    say: "Your quest: shippers, then employees, each a table for a seat Orders already saved. Four entities, three lines, every many side below its one side — and one join that spans them all."
stories:
  summarize the page:
    - 'You might wonder: summarize the page'
    - This page builds the shop's Orders table in your own MySQL, tied to your Customers table.
    - You back up first, reverse engineer to see the structure and types the database reads from your data.
    - The CREATE TABLE script gives Orders a primary key and a foreign key to Customers, then you insert and join.
    - The page carries a live copy of the two tables so the join can be checked before Workbench.
    - Reverse engineering again shows the model grow — two entities, one relationship, one to many, parents above children.
    - The quest adds Shippers and Employees the same way, four entities in all.
  what does the foreign key do:
    - 'You might wonder: what does the foreign key do'
    - It turns a sentence into a rule: every order names a customer, and that customer must exist.
    - Insert an order for a CustomerID that is not in Customers, and the database refuses it.
    - In the diagram it shows as a diamond on the column and a one-to-many line up to Customers.
```
{: .avatar #guide dock="true" size="115" }

[^type]: **type** — what a column can hold and how much room it gets:
    `INT` a whole number, `VARCHAR(100)` text up to 100 characters,
    `DATE` a calendar date.
[^primary_key]: **primary key** — the column that identifies a row and
    forbids duplicates; `AUTO_INCREMENT` lets the database number the
    rows itself.
[^foreign_key]: **foreign key** — a column that must hold a value found
    in another table's primary key. It makes the link a rule: no
    order for a customer who does not exist.
[^relationship]: **relationship** — the line the model draws between
    two entities tied by a foreign key; read with its cardinality, one
    to many, parents above children.
