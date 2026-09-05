# 🗺️ The Treasure Hunt

🏴‍☠️ The paper hunt ended with a claim: *"Thomas Hardy placed an order
on 7/8/96."* Written by hand, from memory, on a Friday. Is it true?
Nobody knows — until someone asks the **database**. That is this page:
eight tables, live, and the tool that reads them without scrolling.

- [🏆 The Data Quest](../module_01/02_data_quest.md)
- [📋 Databases & RDBMS Concepts](../module_01/03_rdbms_concepts.md)
{: .prerequisite }

Ask Doc for a tour!
{: .avatar_trigger target="guide" }

````
### 🗺️ Eight tables — the map

The shop's whole world, in the dimensions that matter. These are
slices of the real thing: the full-size database on
[w3schools SQL editor](https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all)
holds **91** customers, **196** orders, **518** order lines, **77**
products, **8** categories, **29** suppliers, **3** shippers and
**10** employees. Same names, same columns — so every query you
write here runs there unchanged.

```json
[
  {"CustomerID": 1, "CustomerName": "Alfreds Futterkiste", "ContactName": "Maria Anders", "City": "Berlin", "Country": "Germany"},
  {"CustomerID": 3, "CustomerName": "Antonio Moreno Taquería", "ContactName": "Antonio Moreno", "City": "México D.F.", "Country": "Mexico"},
  {"CustomerID": 4, "CustomerName": "Around the Horn", "ContactName": "Thomas Hardy", "City": "London", "Country": "UK"},
  {"CustomerID": 11, "CustomerName": "B's Beverages", "ContactName": "Victoria Ashworth", "City": "London", "Country": "UK"},
  {"CustomerID": 34, "CustomerName": "Hanari Carnes", "ContactName": "Mario Pontes", "City": "Rio de Janeiro", "Country": "Brazil"},
  {"CustomerID": 84, "CustomerName": "Vins et alcools Chevalier", "ContactName": "Paul Henriot", "City": "Reims", "Country": "France"},
  {"CustomerID": 90, "CustomerName": "Wilman Kala", "ContactName": "Matti Karttunen", "City": "Helsinki", "Country": "Finland"}
]
```
{: .dataset #Customers }

[A · Customers](#)
{: .datagrid bind="Customers" rows="4" }

```json
[
  {"OrderID": 10248, "CustomerID": 90, "EmployeeID": 5, "OrderDate": "1996-07-04", "ShipperID": 3},
  {"OrderID": 10250, "CustomerID": 34, "EmployeeID": 4, "OrderDate": "1996-07-08", "ShipperID": 2},
  {"OrderID": 10251, "CustomerID": 84, "EmployeeID": 3, "OrderDate": "1996-07-08", "ShipperID": 1},
  {"OrderID": 10355, "CustomerID": 4, "EmployeeID": 6, "OrderDate": "1996-11-15", "ShipperID": 1},
  {"OrderID": 10365, "CustomerID": 3, "EmployeeID": 3, "OrderDate": "1996-11-27", "ShipperID": 1},
  {"OrderID": 10383, "CustomerID": 4, "EmployeeID": 8, "OrderDate": "1996-12-16", "ShipperID": 3}
]
```
{: .dataset #Orders }

[C · Orders](#)
{: .datagrid bind="Orders" rows="4" }

```json
[
  {"OrderDetailID": 10, "OrderID": 10251, "ProductID": 22, "Quantity": 6},
  {"OrderDetailID": 11, "OrderID": 10251, "ProductID": 57, "Quantity": 15},
  {"OrderDetailID": 12, "OrderID": 10251, "ProductID": 65, "Quantity": 20},
  {"OrderDetailID": 285, "OrderID": 10355, "ProductID": 24, "Quantity": 25},
  {"OrderDetailID": 286, "OrderID": 10355, "ProductID": 57, "Quantity": 25}
]
```
{: .dataset #OrderDetails }

[D · OrderDetails](#)
{: .datagrid bind="OrderDetails" rows="4" }

```json
[
  {"ProductID": 1, "ProductName": "Chais", "SupplierID": 1, "CategoryID": 1, "Unit": "10 boxes x 20 bags", "Price": 18},
  {"ProductID": 2, "ProductName": "Chang", "SupplierID": 1, "CategoryID": 1, "Unit": "24 - 12 oz bottles", "Price": 19},
  {"ProductID": 22, "ProductName": "Gustaf's Knäckebröd", "SupplierID": 9, "CategoryID": 5, "Unit": "24 - 500 g pkgs.", "Price": 21},
  {"ProductID": 24, "ProductName": "Guaraná Fantástica", "SupplierID": 10, "CategoryID": 1, "Unit": "12 - 355 ml cans", "Price": 4.5},
  {"ProductID": 39, "ProductName": "Chartreuse verte", "SupplierID": 18, "CategoryID": 1, "Unit": "750 cc per bottle", "Price": 18},
  {"ProductID": 57, "ProductName": "Ravioli Angelo", "SupplierID": 26, "CategoryID": 5, "Unit": "24 - 250 g pkgs.", "Price": 19.5},
  {"ProductID": 65, "ProductName": "Louisiana Fiery Hot Pepper Sauce", "SupplierID": 2, "CategoryID": 2, "Unit": "32 - 8 oz bottles", "Price": 21.05}
]
```
{: .dataset #Products }

[H · Products](#)
{: .datagrid bind="Products" rows="4" }

```json
[
  {"CategoryID": 1, "CategoryName": "Beverages", "Description": "Soft drinks, coffees, teas, beers, and ales"},
  {"CategoryID": 2, "CategoryName": "Condiments", "Description": "Sweet and savory sauces, relishes, spreads, and seasonings"},
  {"CategoryID": 3, "CategoryName": "Confections", "Description": "Desserts, candies, and sweet breads"},
  {"CategoryID": 4, "CategoryName": "Dairy Products", "Description": "Cheeses"},
  {"CategoryID": 5, "CategoryName": "Grains/Cereals", "Description": "Breads, crackers, pasta, and cereal"},
  {"CategoryID": 6, "CategoryName": "Meat/Poultry", "Description": "Prepared meats"},
  {"CategoryID": 7, "CategoryName": "Produce", "Description": "Dried fruit and bean curd"},
  {"CategoryID": 8, "CategoryName": "Seafood", "Description": "Seaweed and fish"}
]
```
{: .dataset #Categories }

[F · Categories](#)
{: .datagrid bind="Categories" rows="4" }

```json
[
  {"SupplierID": 1, "SupplierName": "Exotic Liquid", "ContactName": "Charlotte Cooper", "City": "Londona", "Country": "UK"},
  {"SupplierID": 2, "SupplierName": "New Orleans Cajun Delights", "ContactName": "Shelley Burke", "City": "New Orleans", "Country": "USA"},
  {"SupplierID": 9, "SupplierName": "PB Knäckebröd AB", "ContactName": "Lars Peterson", "City": "Göteborg", "Country": "Sweden"},
  {"SupplierID": 10, "SupplierName": "Refrescos Americanas LTDA", "ContactName": "Carlos Diaz", "City": "São Paulo", "Country": "Brazil"},
  {"SupplierID": 18, "SupplierName": "Aux joyeux ecclésiastiques", "ContactName": "Guylène Nodier", "City": "Paris", "Country": "France"},
  {"SupplierID": 26, "SupplierName": "Pasta Buttini s.r.l.", "ContactName": "Giovanni Giudici", "City": "Salerno", "Country": "Italy"}
]
```
{: .dataset #Suppliers }

[G · Suppliers](#)
{: .datagrid bind="Suppliers" rows="4" }

```json
[
  {"ShipperID": 1, "ShipperName": "Speedy Express", "Phone": "(503) 555-9831"},
  {"ShipperID": 2, "ShipperName": "United Package", "Phone": "(503) 555-3199"},
  {"ShipperID": 3, "ShipperName": "Federal Shipping", "Phone": "(503) 555-9931"}
]
```
{: .dataset #Shippers }

[E · Shippers](#)
{: .datagrid bind="Shippers" rows="3" }

```json
[
  {"EmployeeID": 3, "LastName": "Leverling", "FirstName": "Janet", "BirthDate": "1963-08-30"},
  {"EmployeeID": 4, "LastName": "Peacock", "FirstName": "Margaret", "BirthDate": "1958-09-19"},
  {"EmployeeID": 5, "LastName": "Buchanan", "FirstName": "Steven", "BirthDate": "1955-03-04"},
  {"EmployeeID": 6, "LastName": "Suyama", "FirstName": "Michael", "BirthDate": "1963-07-02"},
  {"EmployeeID": 8, "LastName": "Callahan", "FirstName": "Laura", "BirthDate": "1958-01-09"}
]
```
{: .dataset #Employees }

[B · Employees](#)
{: .datagrid bind="Employees" rows="4" }
````
{: .block title="🛢️ The shop — eight tables, live" #map }

````
### 🗣️ Say it in English, then run it

Every query starts as a sentence. *"Show me the customers — every
column."* Now the same sentence with its tie on — and this editor is
**real**: change the SQL, press ▶ Run, and the grid below obeys.

```sql
SELECT * FROM Customers
```
{: .query source="Customers" #q_customers editable="true" }

[what came back](#)
{: .datagrid source="q_customers" rows="4" }

Read it right, because the word is a trap: **SELECT** does not pick
rows. It picks **columns** — the `*` means *every column*. **FROM**
names the table. Nothing here narrows the rows, so every customer
comes back.

Three edits, three sentences — run each one:

1. *Show me the contact names and cities of the customers* —
   `SELECT ContactName, City FROM Customers`. Fewer **columns**: you
   named two instead of `*`.
2. *Show me the customers in London* —
   `SELECT * FROM Customers WHERE City = 'London'`. Fewer **rows**:
   that is the **WHERE**'s job, never SELECT's. The quotes matter:
   `'London'` is a value; `London` would be a column that does not
   exist.
3. *Show me the contact names of the London customers* — both at
   once: columns after SELECT, rows after WHERE.

🔗 Now the full-size table: paste each query into the
[w3schools SQL editor](https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all)
and read **Number of Records** each time. Every customer: 91. London
customers: fewer — how many?
````
{: .accordion #say_it }

````
### 🖇️ Two tables, one sentence — and the claim

Thomas Hardy is a row in **Customers**. His orders are rows in
**Orders**, each carrying his `CustomerID`. Put both tables in the
FROM, tie them by key equality, and one sentence spans both:

```sql
SELECT ContactName, OrderID, OrderDate
FROM Customers, Orders
WHERE Customers.CustomerID = Orders.CustomerID
  AND ContactName = 'Thomas Hardy'
```
{: .query source="Customers,Orders" #q_thomas editable="true" }

[Thomas Hardy's orders](#)
{: .datagrid source="q_thomas" rows="3" }

There is the verdict on the paper claim. Thomas ordered on
**1996-11-15** and **1996-12-16** — never on 7/8/96. The hand-written
hunt was wrong; the database was right. That is the whole reason it
exists: **one place where the facts are kept, and asked.**

Run the same query on [w3schools](https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all): same two rows, out of 196 orders.
````
{: .accordion #two_tables }

**Q:** The paper hunt said Thomas ordered on 7/8/96. What settled it?

- [ ] Reading the Orders grid until his name appeared

  > Orders carry a CustomerID, not a name — you would scroll 196
  > rows and never see "Thomas". The link runs through the key.

- [ ] Asking Doc, who remembers every order

  > Doc runs queries; he does not keep the facts. Nobody should —
  > that is what the database is for.

- [x] A query joining Customers and Orders on CustomerID

  > Two tables, key equality, one name in the WHERE: his two real
  > orders came back, dated November and December. The claim fell.
{: .quiz }


````
### 🚨 Crossed tables — the trap

Drop the WHERE and see what a comma really does. *"Select product
names with their category names"* — a beginner writes:

```sql
SELECT ProductName, CategoryName
FROM Products, Categories
```
{: .query source="Products,Categories" #q_crossed editable="true" }

[every product with every category](#)
{: .datagrid source="q_crossed" rows="4" }

Chais is a Beverage — and a Condiment, a Confection, a Seafood…
**Every row of the first table paired with every row of the second**:
7 products × 8 categories = 56 lines here, and **77 × 8 = 616** on
w3schools. All × All. Is that what you wanted?

Add the key equality and the pairs that belong together survive:
`WHERE Products.CategoryID = Categories.CategoryID` — 7 rows here,
**77** on w3schools, one per product. Try it in the editor above.

Same trap, other tables: `SELECT ShipperName, CategoryName FROM
Shippers, Categories` — 3 × 8 = **24** lines that mean nothing, on
the page and on w3schools alike. Shippers and categories share no key;
no sentence ties them.
````
{: .accordion #crossed }

**Q:** `SELECT ProductName, CategoryName FROM Products, Categories`
returns 616 lines on w3schools. Why so many?

- [ ] The two tables were copied once per category

  > Nothing is copied. The tables are untouched; the *result* is
  > what grew.

- [x] Each product was paired with every category

  > All × All: 77 products times 8 categories. A comma between two
  > tables crosses them, and only a WHERE on the keys keeps the
  > pairs that belong together.

- [ ] The database added the categories that had no products

  > A category with no products would add zero lines, not hundreds.
  > The count is a multiplication, not an addition.
{: .quiz }


````
### 🪆 A result is a table — so query it again

What a query returns *looks like a table* — and it **is** one. So it
can sit inside another query's FROM:

```sql
SELECT ProductName, Price
FROM (SELECT * FROM Products, Categories
      WHERE Products.CategoryID = Categories.CategoryID)
```
{: .query source="Products,Categories" #q_nested editable="true" }

[names and prices, from the joined result](#)
{: .datagrid source="q_nested" rows="4" }

The inner SELECT builds the related pairs; the outer one keeps two
columns of them. Queries nest like Russian dolls, because a result
is always a table. Still 7 rows here, still 77 on w3schools.
````
{: .accordion #nested }

```
### 🏴‍☠️ Your quest

Back to the treasure map, this time with the tool. On
[w3schools](https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all), with the
full-size tables:

1. Write a sentence relying on data from **2** tables — then its SQL.
   Example: *Thomas Hardy placed order 10355 on 1996-11-15.*
   (Customers, Orders)
2. Then **3, 4, 5, 6** tables. Follow the keys: an order has an
   employee and a shipper; an order line has a product; a product has
   a category and a supplier.
3. Then **all eight**. One sentence, one thread through the whole shop.
4. **Name each table** your sentence needs — the naming is the skill
   the Canvas check asks for.

Every sentence in English first. Verify every value against the data:
the paper hunt already showed what memory does to dates.
```
{: .accordion #quest }

```
### 🔬 Observations — what we just played

- 🗣️ English first, then SQL — same sentence, tie on.
- 🔤 Fewer columns: name them after SELECT. Fewer rows: WHERE.
- 🖇️ Two tables in a FROM are **crossed** — All × All — until a
  WHERE on the keys (P🔑 = F🔑) keeps the pairs that belong.
- 🪆 A result is a table, so a query can read another query.
- 🧾 The database beat the paper: 1996-11-15, not 7/8/96.

Next: the words for all of this, on the concepts page.
```
{: .accordion #observations }

Four words to keep from this page: a `table`[^table] holds the facts;
`select`[^select] picks the columns you want; `where`[^where] picks the
rows; a `key`[^key] ties one table's rows to another's. The proof below
runs the page's own queries and checks what came back:

```gherkin
Feature: The database answers the claim
  Scenario: Two tables tied by a key give Thomas his real orders
    Given the query joining Customers and Orders on CustomerID
    :::python
    self.q: Query = self.page.q_thomas
    :::
    Then it returns his two orders, neither in July
    :::python
    assert self.q.count == 2, self.q.count
    dates: list[str] = self.q.values("OrderDate")
    assert dates == ["1996-11-15", "1996-12-16"], dates
    :::

  Scenario: A comma crosses tables, the key equality relates them
    Given the crossed and the nested queries
    :::python
    self.crossed: Query = self.page.q_crossed
    self.related: Query = self.page.q_nested
    self.products: Dataset = Dataset("Products")
    self.categories: Dataset = Dataset("Categories")
    :::
    Then the cross product is all times all, the join is one row per product
    :::python
    assert self.crossed.count == self.products.count * self.categories.count, self.crossed.count
    assert self.related.count == self.products.count, self.related.count
    :::
```
{: .feature #hunt_proof tags="table, select, where, key" visible="true" status="passing" }

[Browse](#)
{: .folder parent="true" }

```yaml
bot: doc
voice: en-US
face:
  zoom: 1.2
script:
  - say: "The paper hunt made a claim about Thomas Hardy and a date. Claims are cheap. Let us ask the one place that actually knows."
  - at: map
    do: open
    say: "Eight tables, and they are live — slices of the real shop. Customers, orders, order lines, products, categories, suppliers, shippers, employees. The full-size versions wait on TryIt with the same names, so what you write here runs there."
  - at: map
    do: select
    with: "Thomas Hardy"
    say: "There he is, customer four, London. Finding him by hand worked on five rows. On ninety-one, you want a better tool."
  - at: say_it
    do: open
    say: "The tool is the query. Say it in English — show me the customers, every column — then in SQL. This editor is real: change the SQL, press Run, and the grid obeys. And mind the trap: SELECT picks columns, star means every column. Rows are the WHERE's job."
  - at: two_tables
    do: open
    say: "Now two tables. Customers and Orders, tied by key equality, and Thomas's name in the WHERE. Two orders come back — November and December. Never July. The paper was wrong; the database was right."
  - at: crossed
    do: open
    say: "Here is the trap every beginner falls into once. A comma between two tables pairs every row with every row — seventy-seven products times eight categories, six hundred sixteen lines. Add the key equality and only the pairs that belong together survive."
  - at: nested
    do: open
    say: "One more trick: a result is a table, so a query can read another query. Build the related pairs inside, keep two columns outside. Russian dolls."
  - at: quest
    do: open
    say: "Your quest: one sentence over two tables, then three, four, five, six, then all eight. Follow the keys, name each table, and check every value against the data."
stories:
  summarize the page:
    - 'You might wonder: summarize the page'
    - The paper hunt claimed Thomas Hardy ordered on 7/8/96, and the page checks it against the database.
    - Eight tables are live on the page — slices of the full-size w3schools database with the same names.
    - You run real queries in an editor: SELECT picks columns, star means every column, and WHERE picks rows.
    - Two tables tied by key equality answer the claim — Thomas ordered in November and December, never in July.
    - A comma between tables crosses them, All times All, until a WHERE on the keys keeps the pairs that belong.
    - A result is a table, so queries nest, and your quest is one sentence over two tables, then more, then all eight.
  was the claim true:
    - 'You might wonder: was the claim true'
    - No. The paper hunt said Thomas Hardy ordered on 7/8/96.
    - Joining Customers and Orders on CustomerID shows his two real orders, dated 1996-11-15 and 1996-12-16.
    - The database keeps the facts in one place, and a query is how you ask.
  why 616 rows:
    - 'You might wonder: why 616 rows'
    - A comma between Products and Categories pairs every product with every category.
    - Seventy-seven products times eight categories makes six hundred sixteen lines.
    - Add WHERE Products.CategoryID equals Categories.CategoryID and only the seventy-seven true pairs remain.
```
{: .avatar #guide dock="true" size="115" }

[^table]: **table** — a named rectangle of facts: one row per thing,
    one column per kind of fact. Customers, Orders, Products are tables.
[^select]: **select** — the SELECT clause names the **columns** you
    want back; `*` means every column. It never narrows the rows.
[^where]: **where** — the WHERE clause keeps only the **rows** that
    pass a test, such as `City = 'London'` or a key equality.
[^key]: **key** — the column that identifies a row (primary key) or
    points at another table's row (foreign key). Tables relate by key
    equality, primary = foreign.
