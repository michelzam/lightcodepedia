# 🔧 Setup — MySQL on your machine

🖥️ Until now the database lived on someone else's server. Today one
runs on **yours**: MySQL Server, and Workbench to talk to it. Fourteen
steps, one picture each, in the order you will click them. At the end
you own a database with a Customers table and Thomas Hardy in it — the
starting point of the Moon Walk.

- [🗺️ The Treasure Hunt](../module_02/01_hunt.md)
- [📋 Query Concepts](../module_02/02_concepts.md)
{: .prerequisite }

Ask Doc for a tour!
{: .avatar_trigger target="guide" }

````
### 🏛️ 1 · Two pieces of software, two roles

[Client and server](_setup/setup_02.jpg)
{: .embed image="true" width="100%" }

**MySQL Server** is the software that manages databases: it keeps
them on persistent storage — big and slow, the disk — and serves them
from memory — small and fast. It is installed on a *server*, a
machine or a virtual one; on your laptop, that machine is your laptop.
It can be running or stopped.

**MySQL Workbench** is the **client**: the window you type SQL into.
It talks to the server, the server talks to the database. Two
programs, one conversation — the double arrow in the picture.
````
{: .accordion #architecture }

**Q:** You type `SELECT * FROM Customers;` in Workbench and a grid
appears. Which piece read the table?

- [ ] Workbench — it holds the database file and shows its rows

  > Workbench holds nothing. It is the client: it sends your sentence
  > and paints what comes back.

- [x] MySQL Server — Workbench only sent the sentence and painted the answer

  > Client asks, server answers. The server owns the database, on disk
  > and in memory; the client is the window.

- [ ] The database itself — it runs the query it receives

  > A database is data, not a program. The server is the program that
  > reads it for you.
{: .quiz }

````
### 📦 2 · Which versions — and which to avoid

[The two components](_setup/setup_03.jpg)
{: .embed image="true" width="100%" }

Two components, both free:

- **MySQL Community Server 8.x** — take the latest **LTS** (long-term
  support) release. **Not 9.x**: the course, the textbook and your
  classmates run 8.
- **MySQL Workbench 8.x**.

On Windows the **MySQL Installer — All MySQL Products** brings both in
one package. Already have an older 8.x installed? Keep it.
````
{: .accordion #versions }

````
### 🌐 3 · The download page

[dev.mysql.com/downloads](_setup/setup_04.jpg)
{: .embed image="true" width="100%" }

Go to [dev.mysql.com/downloads](https://dev.mysql.com/downloads/) and
pick **MySQL Community Server** and **MySQL Workbench** — the two
entries boxed in red. The page offers a login; the *No thanks, just
start my download* link at the bottom skips it.
````
{: .accordion #download }

````
### ⬇️ 4 · The installer

[Server and Workbench downloads](_setup/setup_05.jpg)
{: .embed image="true" width="100%" }

Left, the server's download page: pick your operating system, take
the recommended installer. Right, Workbench 8.0.34 for Windows — the
highlighted MSI. Run each installer with its defaults. When the
server asks for a **root password**, choose one and **write it down**:
Workbench will ask for it at every connection, and nobody can recover
it for you.
````
{: .accordion #installer }

````
### 🧭 5 · Workbench — find your way around

[Workbench, first look](_setup/setup_06.jpg)
{: .embed image="true" width="100%" }

Open Workbench and click your **Local instance**. The left panel has
two tabs: **Administration** — the server's health, start and stop —
and **Schemas** — the databases the server holds. *Instance* is the
running server; *schema* is MySQL's word for a database. The big
button on the Administration page says whether the server is running.
If it says stopped, start it here.
````
{: .accordion #workbench }

````
### 🛢️ 6 · Create your database

[create database testdb](_setup/setup_07.jpg)
{: .embed image="true" width="100%" }

Open a SQL tab — the first icon in the toolbar, *Create a new SQL tab
for executing queries* — and type:

```sql
create database testdb;
```

Press the ⚡ lightning to run it. The Action Output at the bottom says
*1 row(s) affected*; refresh the Schemas panel and **testdb** is there.
**Lowercase only** in a database name: MySQL treats names differently
on Windows and on Mac or Linux, and lowercase works everywhere.
````
{: .accordion #create_db }

**Q:** Why does the page insist on `testdb`, not `TestDB`?

- [ ] Uppercase letters are not allowed in SQL

  > SQL keywords do not care about case, and column names carry
  > capitals all over the shop. This is about *database* names.

- [x] Database names are case-sensitive on some systems and not on others — lowercase works everywhere

  > A script written on a Mac with TestDB can fail on Linux looking for
  > testdb. Lowercase names never hit that wall.

- [ ] Workbench only shows lowercase schemas in its panel

  > It shows them all. The trap is the file system underneath, not the
  > panel.
{: .quiz }

````
### 🧱 7 · Create the table — five clicks

[Create table, steps 1 to 5](_setup/setup_08.jpg)
{: .embed image="true" width="100%" }

Follow the numbers:

1. **Make testdb the current database**: double-click it in the
   Schemas panel — it turns **bold**. Or right-click → *Set as Default
   Schema*. Skip this and the table lands nowhere.
2. **Paste the script** — the one in the next step — into the SQL tab.
3. **Run it** with ⚡.
4. **Read the Action Output**: a green tick and *CREATE TABLE
   Customers … 0 row(s) affected*. Zero rows is right — you built a
   shape, not data.
5. **Refresh the Schemas panel**: testdb → Tables → **Customers**,
   with its columns, its PRIMARY index, and empty Foreign Keys for now.
````
{: .accordion #create_table }

````
### 📜 8 · The script — Customers

[CREATE TABLE Customers](_setup/setup_09.jpg)
{: .embed image="true" width="100%" }

```sql
CREATE TABLE Customers (
    CustomerID   INT NOT NULL AUTO_INCREMENT,
    CustomerName VARCHAR(100) NOT NULL,
    ContactName  VARCHAR(100),
    Address      VARCHAR(150),
    City         VARCHAR(50),
    PostalCode   VARCHAR(20),
    Country      VARCHAR(50),
    PRIMARY KEY (CustomerID)
);
```

Same columns as the w3schools table you queried in module 02 — on
purpose, so every query you already know runs here unchanged. Each
column has a **type**: `INT` a whole number, `VARCHAR(100)` text up to
100 characters. `NOT NULL` means the value is required;
`AUTO_INCREMENT` lets the database number the rows itself; `PRIMARY
KEY` names the column that identifies a customer.
````
{: .accordion #script }

````
### 🔎 9 · Select — an empty table is still a table

[SELECT on the empty table](_setup/setup_10.jpg)
{: .embed image="true" width="100%" }

```sql
SELECT * FROM Customers;
```

Run it. The Result Grid shows the seven column names and one row of
NULLs — the placeholder Workbench offers for typing a new row. No
customers yet: the shape exists, the data does not.
````
{: .accordion #select_empty }

````
### ✍️ 10 · Insert a row — by hand, in the grid

[Insert through the grid](_setup/setup_11.jpg)
{: .embed image="true" width="100%" }

Click the NULL under CustomerName, type **UWM**, press Enter, then
**Apply** at the bottom right. Workbench shows you the SQL it wrote for
you — `INSERT INTO testdb.Customers (CustomerName) VALUES ('UWM')` —
and asks you to Apply once more. That is the deal with Workbench: every
click becomes SQL, and it shows you the SQL before running it.
````
{: .accordion #insert_grid }

````
### 🔁 11 · Select again — check the CustomerID

[The first row](_setup/setup_12.jpg)
{: .embed image="true" width="100%" }

Run the SELECT again. UWM is there — and its CustomerID says **1**,
a number you never typed. `AUTO_INCREMENT` at work: the database hands
out identities. Every other column reads NULL, allowed because only
CustomerName was declared NOT NULL.
````
{: .accordion #select_again }

````
### 🧾 12 · Insert a row — by SQL, and it is Thomas

[INSERT Thomas Hardy](_setup/setup_13.jpg)
{: .embed image="true" width="100%" }

The grid is for one row. SQL is for any number, and for choosing the
key yourself:

```sql
INSERT INTO Customers
  (CustomerID, CustomerName, ContactName, Address,
   City, PostalCode, Country)
VALUES
  (4, 'Around the Horn', 'Thomas Hardy',
   '120 Hanover Sq.', 'London', 'WA1 1DP', 'UK');
```

CustomerID **4** on purpose: the same number he wears in the w3schools
shop, so the queries of module 02 find him here too. Text values wear
quotes; the number does not.
````
{: .accordion #insert_sql }

````
### ✅ 13 · Run it, read the output, select again

[1 row(s) affected](_setup/setup_14.jpg)
{: .embed image="true" width="100%" }

⚡ Run. The Action Output answers *1 row(s) affected* with a green
tick. Then the check, always the same:

[Two customers](_setup/setup_15.jpg)
{: .embed image="true" width="100%" }

```sql
SELECT * FROM Customers;
```

Two rows: UWM at 1, Around the Horn — Thomas Hardy, London — at 4.
The gap between 1 and 4 is fine: a key identifies, it does not count.
````
{: .accordion #verify }

````
### 🔄 14 · The learning loop

[Add, save, refresh, observe, repeat](_setup/setup_16.jpg)
{: .embed image="true" width="100%" }

Add more rows — a customer in Paris, one in Milwaukee. Save. Refresh
the grid. Observe what the database did with your input. Repeat. Every
table you will ever build follows this loop; the Moon Walk starts on
the far side of it.
````
{: .accordion #loop }

````
### 🎯 What your grid should show

The same two rows, live on the page — compare with your Workbench
Result Grid before moving on:

```json
[
  {"CustomerID": 1, "CustomerName": "UWM", "ContactName": null, "Address": null, "City": null, "PostalCode": null, "Country": null},
  {"CustomerID": 4, "CustomerName": "Around the Horn", "ContactName": "Thomas Hardy", "Address": "120 Hanover Sq.", "City": "London", "PostalCode": "WA1 1DP", "Country": "UK"}
]
```
{: .dataset #Customers }

[your Customers, expected](#)
{: .datagrid bind="Customers" rows="2" }

```sql
SELECT CustomerID, ContactName, City FROM Customers WHERE Country = 'UK'
```
{: .query source="Customers" #q_uk editable="true" }

[the UK customer](#)
{: .datagrid source="q_uk" rows="1" }
````
{: .block title="🎯 Expected — your Customers table" #expected }

Four words to keep from this page: the `server`[^server] runs the
database, the `client`[^client] is the window you type in, a
`schema`[^schema] is MySQL's word for a database, and `insert`[^insert]
is how a row gets in. The proof below reads the expected grid:

```gherkin
Feature: The shop starts with two customers, and Thomas is number four
  Scenario: The expected table matches the slides
    Given the expected Customers grid on this page
    :::python
    self.customers: Dataset = Dataset("Customers")
    :::
    Then it holds UWM at 1 and Thomas Hardy at 4
    :::python
    ids: list[str] = self.customers.values("CustomerID")
    names: list[str] = self.customers.values("ContactName")
    assert ids == ["1", "4"], ids
    assert names[1] == "Thomas Hardy", names
    :::

  Scenario: A query from module 02 already runs on it
    Given the UK query
    :::python
    self.uk: Query = self.page.q_uk
    :::
    Then it finds exactly Thomas
    :::python
    assert self.uk.count == 1, self.uk.count
    assert self.uk.values("City") == ["London"]
    :::
```
{: .feature #setup_proof tags="server, client, schema, insert" visible="true" status="passing" }

[Browse](#)
{: .folder parent="true" }

```yaml
bot: doc
voice: en-US
face:
  zoom: 1.2
script:
  - say: "Until now the database lived on somebody else's server. Today one runs on yours. Fourteen steps, one picture each — and at the end, Thomas Hardy lives on your machine."
  - at: architecture
    do: open
    say: "Two programs, two roles. The server manages the databases — on disk for keeps, in memory for speed. Workbench is the client, the window you type in. It asks; the server answers."
  - at: versions
    do: open
    say: "Version eight, the long-term support release — not nine. Server and Workbench both. On Windows, the installer brings the two in one package."
  - at: download
    do: open
    say: "The download page: Community Server and Workbench, the two boxed in red. No account needed — the small link at the bottom just starts the download."
  - at: installer
    do: open
    say: "Run each installer with its defaults. When the server asks for a root password, write it down. Workbench will ask for it every time, and nobody can recover it for you."
  - at: workbench
    do: open
    say: "Workbench, first look: Administration for the server's health, Schemas for its databases. Instance means the running server; schema means a database. If the big button says stopped, start it."
  - at: create_db
    do: open
    say: "A SQL tab, one line: create database testdb, all lowercase, then the lightning. Lowercase because some systems care about case and some do not — lowercase works everywhere."
  - at: create_table
    do: open
    say: "Five clicks, in order. Make testdb the current database — it turns bold. Paste the script. Run. Read the output: zero rows affected is right, you built a shape. Refresh, and Customers is there."
  - at: script
    do: open
    say: "The script is the w3schools Customers table, on purpose: every query you know already fits. Each column has a type. NOT NULL means required; AUTO_INCREMENT means the database numbers the rows; PRIMARY KEY names the identity."
  - at: select_empty
    do: open
    say: "Select star on an empty table: seven column names and a row of NULLs. The shape exists; the data does not. Yet."
  - at: insert_grid
    do: open
    say: "Type UWM in the grid, apply, and watch: Workbench shows you the INSERT it wrote before running it. Every click becomes SQL."
  - at: select_again
    do: open
    say: "Select again. UWM has CustomerID one — a number you never typed. The database hands out identities."
  - at: insert_sql
    do: open
    say: "Now by SQL, and choose the key yourself: four, so Thomas wears the same number as in the w3schools shop. Text in quotes, the number bare."
  - at: verify
    do: open
    say: "Run, read one row affected, select again. UWM at one, Thomas at four. The gap is fine — a key identifies, it does not count."
  - at: loop
    do: open
    say: "Add rows, save, refresh, observe, repeat. That loop is every table you will ever build. The Moon Walk starts on the far side of it."
  - at: expected
    do: open
    say: "Here is what your grid should show, live. Compare, then move on."
stories:
  summarize the page:
    - 'You might wonder: summarize the page'
    - This page installs MySQL Server and Workbench and builds your first database, in fourteen pictured steps.
    - Server and client are two programs with two roles — the server manages the data, Workbench is the window you type in.
    - You take version 8, create a lowercase database, and create the w3schools Customers table with a script.
    - You insert one row in the grid and one by SQL — Thomas Hardy at CustomerID 4 — and select to verify after each step.
    - The page ends with the expected grid, live, and the learning loop: add, save, refresh, observe, repeat.
  which version should I install:
    - 'You might wonder: which version should I install'
    - MySQL Community Server 8, the latest long-term support release, and MySQL Workbench 8.
    - Not version 9 — the course, the textbook and your classmates run 8.
    - On Windows, the MySQL Installer brings both in one package.
  I forgot my root password:
    - 'You might wonder: I forgot my root password'
    - Nobody can recover it, but a fresh install can set a new one.
    - Uninstall the server, keep Workbench, run the server installer again and write the password down this time.
    - Your tables live in the database files, so back them up first if they matter.
```
{: .avatar #guide dock="true" size="115" }

[^server]: **server** — MySQL Server, the program that manages the
    databases: keeps them on disk, serves them from memory, answers
    queries. Running or stopped.
[^client]: **client** — MySQL Workbench, the program you type SQL into.
    It sends your sentence to the server and paints the answer.
[^schema]: **schema** — MySQL's word for a database, the container of
    tables. `create database testdb` makes one; Workbench lists them
    in the Schemas panel.
[^insert]: **insert** — the SQL that adds a row: `INSERT INTO table
    (columns) VALUES (values)`. Workbench writes one for you when you
    type in the grid.
