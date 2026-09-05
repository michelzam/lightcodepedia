# 📋 Query Concepts

The Treasure Hunt gave you the moves. This page gives you the words —
five ideas every query you will ever write is made of.

- [🗺️ The Treasure Hunt](01_hunt.md)
{: .prerequisite }

Ask Doc for a tour!
{: .avatar_trigger target="guide" }

````
### 🗣️ 1 · A query is a sentence

A small slice of the customers table, for the examples on this page:

```json
[
  {"CustomerID": 1, "ContactName": "Maria Anders", "City": "Berlin", "Country": "Germany"},
  {"CustomerID": 4, "ContactName": "Thomas Hardy", "City": "London", "Country": "UK"},
  {"CustomerID": 11, "ContactName": "Victoria Ashworth", "City": "London", "Country": "UK"},
  {"CustomerID": 34, "ContactName": "Mario Pontes", "City": "Rio de Janeiro", "Country": "Brazil"},
  {"CustomerID": 90, "ContactName": "Matti Karttunen", "City": "Helsinki", "Country": "Finland"}
]
```
{: .dataset #Customers }

[the slice](#)
{: .datagrid bind="Customers" rows="5" }

> "A query is a question asked of the database, in a language it
> understands."

English first, always: *"Select the London customers."* Then SQL —
**Structured Query Language** — the same sentence made precise:

~~~sql
SELECT * FROM Customers WHERE City = 'London';
~~~

Three clauses, three jobs: **SELECT** says which columns, **FROM**
says which tables, **WHERE** says which rows. If you cannot say it
in English, no syntax will save you.
````
{: .accordion #sentence }

```
### 🔤 2 · Select columns — or all of them with *

The word SELECT is about **columns**, nothing else. Name the columns
you want after it, and only those come back — for every row:

~~~sql
SELECT ContactName, City FROM Customers;
~~~
{: .query source="Customers" #q_columns }

[two columns, every row](#)
{: .datagrid #cols_grid source="q_columns" rows="3" }

`*` means *every column*, the whole width. A comma separates column
names; `AND` never does — `AND` joins conditions, not columns. And
nothing here narrowed the rows: that is the next clause's job.
```
{: .accordion #select_columns }

```
### 🎯 3 · Select rows — with WHERE

Rows are the WHERE's business. It keeps only the rows that pass a
test, and every column comes along because of the `*`:

~~~sql
SELECT * FROM Customers WHERE City = 'London';
~~~
{: .query source="Customers" #q_rows }

[every column, the London rows](#)
{: .datagrid source="q_rows" rows="3" }

The test compares a column with a **value** — and text values wear
quotes: `'London'`. Without them, `London` would be read as the name
of a column, and there is none. Columns after SELECT, rows after
WHERE: two clauses, two directions.
```
{: .accordion #select_rows }

**Q:** `SELECT ContactName, City FROM Customers` and
`SELECT * FROM Customers WHERE City = 'London'` — which does what?

- [ ] Both narrow the rows, in different ways

  > The first keeps every customer; only its width shrinks. Rows are
  > the WHERE's business, and the first query has none.

- [x] The first keeps fewer columns, the second fewer rows

  > Projection, then selection: name columns after SELECT to trim the
  > width, add a WHERE to trim the height. Most real queries do both.

- [ ] Both narrow the columns, since both name something

  > The second names a column only to test it — `City` in a WHERE
  > filters rows, and `*` still brings back every column.
{: .quiz }


```
### 🖇️ 4 · Cross product and join — two tables

Two tables in a FROM, separated by a comma, are **crossed**: every row
of one paired with every row of the other. Products × Categories =
77 × 8 = 616 lines, most of them nonsense.

~~~sql
SELECT ProductName, CategoryName
FROM Products, Categories
WHERE Products.CategoryID = Categories.CategoryID;
~~~

The WHERE on the keys — **primary key = foreign key** — keeps only the
pairs that belong together: 77 rows, one per product. That is a
**join**. A cross product with no key to tie it, like Shippers ×
Categories, stays nonsense: 24 lines and no sentence.
```
{: .accordion #join }

**Q:** Why does `WHERE Products.CategoryID = Categories.CategoryID`
turn 616 lines into 77?

- [ ] It removes the categories that have no products

  > An empty category adds no lines to begin with. The drop from 616
  > is about pairs, not about empty categories.

- [ ] It sorts the crossed lines so duplicates collapse

  > Sorting changes order, never count. The lines that vanish were
  > not duplicates — they were false pairs.

- [x] It keeps only the pairs whose keys agree

  > Each product carries one CategoryID; only the one category with
  > that ID survives beside it. 77 products, 77 rows: a join.
{: .quiz }


```
### 🪆 5 · A result is a table

Whatever a query returns has rows and columns — it is a table. So it
can be queried again, sitting in another query's FROM:

~~~sql
SELECT ProductName, Price
FROM (SELECT * FROM Products, Categories
      WHERE Products.CategoryID = Categories.CategoryID);
~~~

Tables in, tables out — that is why queries nest, why views exist,
and why one language covers the whole database.
```
{: .accordion #closure }

```
### 🗺️ The shop's keys — reading the map

| Table | Primary key | Points at |
|---|---|---|
| Customers | CustomerID | — |
| Employees | EmployeeID | — |
| Shippers | ShipperID | — |
| Suppliers | SupplierID | — |
| Categories | CategoryID | — |
| Orders | OrderID | CustomerID → Customers · EmployeeID → Employees · ShipperID → Shippers |
| OrderDetails | OrderDetailID | OrderID → Orders · ProductID → Products |
| Products | ProductID | SupplierID → Suppliers · CategoryID → Categories |

Every arrow is a foreign key, and every arrow is a sentence waiting:
*an order was placed by a customer, taken by an employee, shipped by
a shipper; an order line belongs to an order and names a product; a
product has a category and a supplier.* Eight tables, seven arrows,
one thread from Thomas to the supplier in São Paulo.
```
{: .accordion #keys }

````
### 🧬 The same map, as a diagram

The eight tables as **entities**: their columns, and the connections
between them. The picture is drawn from a declaration hidden on this
page, one box per table: every blue arrow is an arrow of the key table
above, labelled with the foreign key and pointing at the table it
references.

```python
@component(icon="👤")
class Customer(Object):
    CustomerID   = Attr(int, hint="primary key")
    CustomerName = Attr(str)
    ContactName  = Attr(str)
    City         = Attr(str)
    Country      = Attr(str)

@component(icon="🧑‍💼")
class Employee(Object):
    EmployeeID = Attr(int, hint="primary key")
    LastName   = Attr(str)
    FirstName  = Attr(str)
    BirthDate  = Attr(str)

@component(icon="🚚")
class Shipper(Object):
    ShipperID   = Attr(int, hint="primary key")
    ShipperName = Attr(str)
    Phone       = Attr(str)

@component(icon="🏭")
class Supplier(Object):
    SupplierID   = Attr(int, hint="primary key")
    SupplierName = Attr(str)
    ContactName  = Attr(str)
    City         = Attr(str)
    Country      = Attr(str)

@component(icon="🏷️")
class Category(Object):
    CategoryID   = Attr(int, hint="primary key")
    CategoryName = Attr(str)
    Description  = Attr(str)

@component(icon="📦")
class Product(Object):
    ProductID   = Attr(int, hint="primary key")
    ProductName = Attr(str)
    SupplierID  = Attr("Supplier", hint="foreign key → Suppliers")
    CategoryID  = Attr("Category", hint="foreign key → Categories")
    Unit        = Attr(str)
    Price       = Attr(float)

@component(icon="🧾")
class Order(Object):
    OrderID    = Attr(int, hint="primary key")
    CustomerID = Attr("Customer", hint="foreign key → Customers")
    EmployeeID = Attr("Employee", hint="foreign key → Employees")
    OrderDate  = Attr(str)
    ShipperID  = Attr("Shipper", hint="foreign key → Shippers")

@component(icon="🧮")
class OrderDetail(Object):
    OrderDetailID = Attr(int, hint="primary key")
    OrderID       = Attr("Order", hint="foreign key → Orders")
    ProductID     = Attr("Product", hint="foreign key → Products")
    Quantity      = Attr(int)
```
{: .model #shop_model }

[the shop — eight tables and seven connections](#)
{: .diagram scope="OrderDetail,Order,Product" states="false" }

Read it like the sentence: an **OrderDetail** names its Order and its
Product; an **Order** names its Customer, Employee and Shipper; a
**Product** names its Category and Supplier. Seven arrows, the same
seven as the table — one thread from Thomas to São Paulo.
````
{: .accordion #entities }

```
### ✅ Your move

Back to the Treasure Hunt with the words in hand: write the ladder —
a sentence over two tables, then three to six, then all eight — in
English first, then in SQL, on the full-size database. Name the
tables each one needs. Every value checked against the data, the way
the paper claim was.
```
{: .accordion #your_move }

Four words to keep from this page: `select`[^select] is about columns,
`where`[^where] is about rows, a `column`[^column] is one kind of fact
and a `row`[^row] is one thing. The proof below runs the page's two
queries over the customers slice and checks both directions:

```gherkin
Feature: Select columns, select rows
  Scenario: Naming columns keeps every row and trims the width
    Given the slice and the columns query
    :::python
    self.src: Dataset = Dataset("Customers")
    self.cols: Query = self.page.q_columns
    self.grid: Datagrid = self.page.cols_grid
    :::
    Then every customer is still there, two columns wide
    :::python
    assert self.cols.count == self.src.count, self.cols.count
    heads: list[str] = self.grid.headers
    assert heads == ["ContactName", "City"], heads
    :::

  Scenario: A WHERE keeps only the rows that pass the test
    Given the rows query
    :::python
    self.rows: Query = self.page.q_rows
    :::
    Then only the London customers come back, every column along
    :::python
    assert self.rows.count == 2, self.rows.count
    cities: list[str] = self.rows.values("City")
    assert cities == ["London", "London"], cities
    :::
```
{: .feature #concepts_proof tags="select, where, column, row" visible="true" status="passing" }

[Browse](#)
{: .folder parent="true" }

```yaml
bot: doc
voice: en-US
face:
  zoom: 1.2
script:
  - at: sentence
    do: open
    say: "A query is a question, asked precisely. Three clauses: SELECT for the columns, FROM for the tables, WHERE for the rows. English first, then the tie goes on."
  - at: select_columns
    do: open
    say: "SELECT is about columns, and only columns. Name the ones you want, separated by commas — never by AND, which is for conditions. Star means every column."
  - at: select_rows
    do: open
    say: "Rows are the WHERE's business. It tests each row against a value, and text values wear quotes. London in quotes is a value; London without them is a column that does not exist."
  - at: join
    do: open
    say: "Two tables in one FROM are crossed — every row with every row, six hundred sixteen lines of mostly nonsense. Primary key equals foreign key in the WHERE, and only the true pairs survive. That is a join."
  - at: closure
    do: open
    say: "The quiet superpower: a result is a table, so a query can read a query. One language, all the way down."
  - at: keys
    do: open
    say: "Here is the map of the shop's keys. Seven arrows, and each one is a sentence waiting to be written. Follow them from Thomas to the supplier in São Paulo, and you have crossed all eight tables."
  - at: entities
    do: open
    say: "The same map as a picture: eight tables, their columns, and seven connections — every foreign key an arrow pointing at the table it references. Same facts, other language."
  - at: your_move
    do: open
    say: "Words done, moves next: back to the hunt, the ladder of sentences over two tables, then more, then all eight. And check every value against the data."
stories:
  summarize the page:
    - 'You might wonder: summarize the page'
    - This page names the five ideas behind every query.
    - A query is a sentence with three clauses — SELECT for columns, FROM for tables, WHERE for rows.
    - SELECT picks columns, star means every column; WHERE picks rows.
    - Two tables in a FROM are crossed until a WHERE on the keys turns the cross product into a join.
    - A result is a table, so queries nest.
    - It closes with the map of the shop's keys, the same map as a diagram, and your next move back on the hunt.
  what is the difference between a cross product and a join:
    - 'You might wonder: what is the difference between a cross product and a join'
    - A cross product pairs every row of one table with every row of the other — all times all.
    - A join keeps only the pairs whose keys agree, primary key equal to foreign key.
    - Products crossed with Categories gives 616 lines; joined on CategoryID it gives 77, one per product.
```
{: .avatar #guide dock="true" size="115" }

[^select]: **select** — the SELECT clause names the **columns** that
    come back; `*` means every column. Its official name, from the
    maths of relations, is *projection*.
[^where]: **where** — the WHERE clause keeps only the **rows** that
    pass a test. Its official name is *selection* — which is why the
    word SELECT is such a trap.
[^column]: **column** — one kind of fact, named and typed, down the
    whole table: `City` is a column.
[^row]: **row** — one thing and all its facts across the columns:
    Thomas Hardy is a row. Also called a tuple.
