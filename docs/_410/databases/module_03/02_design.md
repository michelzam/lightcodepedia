# 📐 Good Design

The Moon Walk gave you the moves. This page gives you the words —
and three smell tests, because a table can look perfectly fine and
still burn you later.

- [🧱 The Moon Walk](01_moon_walk.md)
{: .prerequisite }

Ask Doc for a tour!
{: .avatar_trigger target="guide" }

```
### 🧭 1 · From table to entity — the model

A **database** is tables, rows, columns, data, types — the thing that
runs. A **model** is its picture: more abstract, fewer details, and it
catches the decisions with foundational consequences. Change a row and
nothing happens; change the model and every query, form and report
downstream feels it.

The building blocks of the model:

- **Entity** — a table, seen as a *kind of thing*: Customer, Order.
- **Column** — one fact about it, with a type.
- **Primary key** 🔑 — the fact that identifies one of them.
- **Foreign key** ♦ — the fact that names another entity's row.
- **Relationship** — the line a foreign key draws between two entities.
- **Cardinality** — how many on each end of the line: 1 : 1, 1 : N.

Module 02 taught English → SQL. This page adds English → ER: from a
sentence to an entity-relationship picture.
```
{: .accordion #blocks }

```
### 🗣️ 2 · English to ER — cardinality

> *A customer may place zero, one, or many orders, and each order is
> placed by exactly one customer.*

That sentence is the whole design of the Customers–Orders line:

- **many** on the Orders side → Orders carries the foreign key;
- **exactly one** on the Customers side → `CustomerID NOT NULL` in
  Orders;
- **zero** allowed → a customer with no orders is fine; Jay in Paris
  is a customer.

Read as **1 : N**, one to many. A **1 : 1** line — each employee has
exactly one badge, each badge exactly one employee — is rarer, and
often a sign the two belong in one table. Whichever the cardinality,
lay the model out **parents above children**: the *one* side over the
*many* side, so a diagram reads top-down like the sentence.
```
{: .accordion #cardinality }

**Q:** *"An order holds many order lines; each line belongs to exactly
one order."* Where does the foreign key go?

- [ ] In Orders, one column per line: Line1, Line2, Line3…

  > Columns are fixed, rows are extensible. The moment an order needs a
  > fourth line, the design is broken. Things that repeat become rows.

- [x] In OrderDetails, an OrderID column pointing up at Orders

  > The side that says *many* carries the foreign key. Orders above,
  > OrderDetails below, one to many — exactly the shop's map.

- [ ] In both tables, so the link works in both directions

  > One foreign key already works in both directions: the join reads
  > it either way. Two copies of a link are two chances to disagree.
{: .quiz }

````
### 🖼️ 3 · The picture — two entities

Customers and Orders, as the model draws them: two entities, one
relationship, the foreign key an arrow pointing at the table it
references — the *one* side. The declaration behind the picture is
hidden on this page; the picture is what design looks like.

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
{: .model #shop_model }

[Customers and Orders — two entities, one relationship](#)
{: .diagram scope="Order" states="false" }

Order is the child: it carries the foreign key, and the picture puts it
below the table it points at. The arrow is the sentence with *many* on
the Orders end. After your quest, Shippers and Employees hang the same
way — each one above Orders, each arrow a foreign key.
````
{: .accordion #picture }

````
### 👃 4 · Three smell tests — poor design looks fine at first

A skyscraper in London once melted a parked car with the sunlight its
curved glass focused on the street. The design looked good; the side
effect came later. Tables do the same. Three smells, each with the
poor table and the good one, live:

#### 1NF — a primary key, atomic columns, no repeating groups

Two phone numbers in one cell: how do you search for one? Or three
Phone columns: what happens to the fourth number?

```json
[
  {"StudentID": 1, "Name": "Alex", "PhoneNumbers": "414-555-1234, 414-555-6789"},
  {"StudentID": 2, "Name": "Jamie", "PhoneNumbers": "262-555-4321"}
]
```
{: .dataset #phones_poor }

[poor — two numbers in one cell](#)
{: .datagrid bind="phones_poor" rows="2" }

```json
[
  {"StudentID": 1, "PhoneID": 1, "PhoneNumber": "414-555-1234"},
  {"StudentID": 1, "PhoneID": 2, "PhoneNumber": "414-555-6789"},
  {"StudentID": 2, "PhoneID": 1, "PhoneNumber": "262-555-4321"},
  {"StudentID": 3, "PhoneID": 1, "PhoneNumber": "920-555-2468"}
]
```
{: .dataset #phones_good }

[good — one number per row, in its own table](#)
{: .datagrid bind="phones_good" rows="4" }

Things that repeat become rows. Every cell holds one value; every row
has a key; no column comes in numbered copies.

#### 2NF — every non-key column depends on the whole key

OrderDetails is keyed by *OrderID + ProductID*. CustomerName depends
on OrderID alone; ProductName and UnitPrice on ProductID alone. Change
a product's price and you must hunt down every line that copied it:

```json
[
  {"OrderID": 101, "ProductID": "P10", "OrderDate": "2025-09-10", "CustomerName": "Alex Kim", "ProductName": "Mug", "UnitPrice": 9.99},
  {"OrderID": 101, "ProductID": "P11", "OrderDate": "2025-09-10", "CustomerName": "Alex Kim", "ProductName": "Spoon", "UnitPrice": 2.49},
  {"OrderID": 102, "ProductID": "P10", "OrderDate": "2025-09-12", "CustomerName": "Jamie Lee", "ProductName": "Mug", "UnitPrice": 9.99}
]
```
{: .dataset #details_poor }

[poor — facts about the order and the product, copied per line](#)
{: .datagrid bind="details_poor" rows="3" }

The cure is the shop's own map: OrderDate and the customer live in
**Orders**, ProductName and the price in **Products**, and
OrderDetails keeps only the keys and the quantity.

#### 3NF — no non-key column depends on another non-key column

MajorName depends on MajorID, not on the student. Rename a major and
you edit every student who takes it — and one day two rows disagree:

```json
[
  {"StudentID": 1, "StudentName": "Alex", "MajorID": "M01", "MajorName": "Computer Sci", "DepartmentHead": "Prof. Smith"},
  {"StudentID": 2, "StudentName": "Jamie", "MajorID": "M02", "MajorName": "Math", "DepartmentHead": "Prof. Patel"},
  {"StudentID": 3, "StudentName": "Morgan", "MajorID": "M01", "MajorName": "Computer Sci", "DepartmentHead": "Prof. Smith"}
]
```
{: .dataset #students_poor }

[poor — the major's facts ride along on every student](#)
{: .datagrid bind="students_poor" rows="3" }

The cure: a **Majors** table — MajorID, MajorName, DepartmentHead —
and Students keeps MajorID as a foreign key. One fact, one place.

All three smells share a cure: split, key, point. And note what they
are about — the **structure** of the tables, never the display. A query
may show a student with the major's name beside them all day; it is
the *table* that must not store it twice.
````
{: .block title="👃 Three smell tests — the tables, live" #smells }

**Q:** Orders stores the customer's City on every order, copied from
Customers. Which smell is that?

- [ ] 1NF — City is not atomic

  > "London" is one value in one cell; atomicity is fine. The problem
  > is where the value lives, not its shape.

- [x] 3NF — City depends on CustomerID, a non-key column, not on the order

  > The city belongs to the customer. Stored per order it will drift:
  > Thomas moves, and half his orders still say London. One fact, one
  > place — Customers.

- [ ] No smell — the join would need it anyway

  > The join *reads* the city from Customers whenever a query wants it.
  > Storing a copy buys nothing and costs consistency.
{: .quiz }

```
### ✅ Your move

Back to Workbench with the words: your four entities, laid out parents
above children, and one join that spans them. Then read your own
tables with the three smells in mind — a numbered column, a copied
name, a fact that belongs to another table. Split, key, point.
```
{: .accordion #your_move }

Four words to keep from this page: an `entity`[^entity] is a table seen
as a kind of thing; a `relationship`[^relationship] is the line a
foreign key draws; its `cardinality`[^cardinality] says how many on each
end; a `normal form`[^normal_form] is a smell test a table passes or
fails. The proof below reads the smell-test tables on this page:

```gherkin
Feature: The good table passes the smell test the poor one fails
  Scenario: 1NF — one value per cell
    Given the two phone tables
    :::python
    self.poor: Dataset = Dataset("phones_poor")
    self.good: Dataset = Dataset("phones_good")
    :::
    Then the poor one packs two numbers in a cell and the good one never does
    :::python
    poor: list[str] = self.poor.values("PhoneNumbers")
    good: list[str] = self.good.values("PhoneNumber")
    assert any("," in v for v in poor), poor
    assert all("," not in v for v in good), good
    :::

  Scenario: 3NF — a fact stored twice is a fact that can disagree
    Given the poor students table
    :::python
    self.students: Dataset = Dataset("students_poor")
    :::
    Then the same major's name is stored on more than one student
    :::python
    majors: list[str] = self.students.values("MajorName")
    assert len(majors) > len(set(majors)), majors
    :::
```
{: .feature #design_proof tags="entity, relationship, cardinality, normal form" visible="true" status="passing" }

[Browse](#)
{: .folder parent="true" }

```yaml
bot: doc
voice: en-US
face:
  zoom: 1.2
script:
  - at: blocks
    do: open
    say: "A database runs; a model is its picture. Fewer details, bigger consequences. Entity, column, primary key, foreign key, relationship, cardinality — six words, and the whole design is made of them."
  - at: cardinality
    do: open
    say: "One sentence designs the line: a customer may place zero, one or many orders, each order by exactly one customer. Many means the foreign key; exactly one means not null; zero means Jay in Paris is still a customer."
  - at: picture
    do: open
    say: "Here is what you built, as a picture. Two entities, one arrow, and Order below Customers — it carries the foreign key, so it hangs under the table it points at."
  - at: smells
    do: open
    say: "Three smells. Two phone numbers in one cell. A product's price copied on every order line. A major's name riding along on every student. Same cure each time: split, key, point."
  - at: your_move
    do: open
    say: "Words done, moves next: back to Workbench, four entities parents above children, one join across them — and a sniff at your own tables."
stories:
  summarize the page:
    - 'You might wonder: summarize the page'
    - This page names the building blocks of a data model — entity, column, primary key, foreign key, relationship, cardinality.
    - One English sentence with zero, one and many designs a one-to-many line, and the many side carries the foreign key.
    - Customers and Orders are drawn as a picture: two entities, one relationship, Order below the table it points at.
    - Three smell tests show poor design beside good design — one value per cell, no facts copied per line, no fact riding on another non-key column.
    - It closes with your move back in Workbench.
  what is cardinality:
    - 'You might wonder: what is cardinality'
    - Cardinality is how many on each end of a relationship — one to one, or one to many.
    - A customer may place zero, one or many orders, and each order is placed by exactly one customer: one to many.
    - The side that says many carries the foreign key, and sits below the one side in the diagram.
```
{: .avatar #guide dock="true" size="115" }

[^entity]: **entity** — a table seen as a kind of thing the shop cares
    about: Customer, Order, Shipper. One row is one of them.
[^relationship]: **relationship** — the line a foreign key draws
    between two entities in the model.
[^cardinality]: **cardinality** — how many on each end of a
    relationship: 1 : 1, or 1 : N (one to many). *Many* is the side
    that carries the foreign key.
[^normal_form]: **normal form** — a test a table's structure passes or
    fails. 1NF: a key, one value per cell, no numbered columns. 2NF:
    every non-key column depends on the whole key. 3NF: no non-key
    column depends on another non-key column.
