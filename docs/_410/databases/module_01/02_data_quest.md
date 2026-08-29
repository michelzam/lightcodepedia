# 🏆 The Data Quest

🎤 Do you like cranberry sauce? Made in Wisconsin. So does **Tom** —
he just doesn't know yet that he is about to win something.

The shop needs to pick the **best customer of the year**: the first
one to order cranberry sauce after Labor Day. To deliver the award we
need his contact info. And here starts our quest 🏴‍☠️ — because the
answer lives in a **database**, the place where data lives.

- [🗽 Welcome to 410](01_welcome.md)
{: .prerequisite }

Ask Doc for a tour!
{: .avatar_trigger target="guide" }

````
### 🔎 The data, live

This is a real table — touch it. Every fact about our customers,
one row per person, one column per kind of fact:

```json
[
  {"CustomerID": 1, "ContactName": "Maria Anders", "City": "Berlin", "Country": "Germany"},
  {"CustomerID": 2, "ContactName": "Ana Trujillo", "City": "Mexico D.F.", "Country": "Mexico"},
  {"CustomerID": 3, "ContactName": "Antonio Moreno", "City": "Mexico D.F.", "Country": "Mexico"},
  {"CustomerID": 4, "ContactName": "Thomas Hardy", "City": "London", "Country": "UK"},
  {"CustomerID": 5, "ContactName": "Christina Berglund", "City": "Lulea", "Country": "Sweden"}
]
```
{: .dataset #customers }

[the customers](#)
{: .datagrid #customers_grid bind="customers" rows="5" }
````
{: .block title="🛢️ Customers — a table" #quest_app }

```
### 🗣️ The words for what you see

- The whole rectangle is a **table** — and tables have names.
- One horizontal line is a **row**, also called a **tuple**: all the
  facts that belong to one customer.
- One vertical slice is a **column**, like `ContactName` — columns
  have names and types: text 🔤, numbers 🔢, dates 📆…
- The winner is **one row**: Thomas Hardy, London. Selecting him out
  of the table — that is the whole game.
```
{: .accordion #vocabulary }

```
### 🪜 From noise to wisdom — DIKIW

Raw marks on a disk are **noise** until they are organized. Then:

- **Data** — the given facts: `Thomas Hardy`, `London`.
- **Information** — facts with shape: a list of customers by city.
- **Knowledge** — a good sentence over the data: *"Thomas lives in
  London."*
- **Wisdom** — what you decide because of it: *he wins; deliver the
  award to London.*

That sentence — "Thomas lives in London" — is a good **one-table
sentence**. Can you find more? How about a **multi-table** one?
```
{: .accordion #dikiw }

```
### 🗨️ Say it in English, then in SQL

First in English: *"From the customers, show me the contact names
and cities."* Every query you will ever write starts as an English
sentence — keep that habit.

Then in **SQL** — Structured Query Language:

~~~sql
SELECT ContactName, City
FROM Customers;
~~~

And the winner, one row only:

~~~sql
SELECT * FROM Customers
WHERE ContactName = 'Thomas Hardy';
~~~

🔗 Try it on a full-size database:
[w3schools SQL TryIt](https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all)
```
{: .accordion #speak_sql }

````
### 🖇️ Two tables, one sentence

Orders live in their own table — with a column that points back:

```json
[
  {"OrderID": 101, "CustomerID": 4, "Product": "Cranberry sauce", "OrderedOn": "Sept 2"},
  {"OrderID": 102, "CustomerID": 1, "Product": "Chai", "OrderedOn": "Sept 4"},
  {"OrderID": 103, "CustomerID": 4, "Product": "Chai", "OrderedOn": "Sept 9"}
]
```
{: .dataset #orders }

[the orders](#)
{: .datagrid #orders_grid bind="orders" rows="3" }

`CustomerID` in **Orders** is a **foreign key** 🔑 — it relates each
order back to exactly one row of **Customers**, whose `CustomerID`
is the **primary key**. Link by key equality: P🔑 = F🔑.

That buys the multi-table sentence: *"Thomas lives in London **and**
ordered cranberry sauce on Sept 2."* Two tables, one truth.
````
{: .accordion #two_tables }

**Q:** "Thomas Hardy, London" sits in one horizontal line of the
customers table. What is that line called?

- [ ] A column of the table

  > Columns run the other way — vertical slices like `ContactName`,
  > one *kind* of fact across everyone.

- [x] A row, or tuple

  > One row = all the facts that belong together about one customer.
  > Finding the right row was the whole quest.

- [ ] One of the strategic key columns

  > Keys are special *columns*, not lines — the strategic ones that
  > identify and link. They get their moment two cards down.
{: .quiz }

**Q:** How does an order know which customer placed it?

- [ ] The two tables are stored side by side on the same disk

  > Where tables live on disk is the DBMS's private business — and
  > neighborhood is not a relationship.

- [ ] The customer's full name is copied into every order

  > Copying invites drift: Thomas moves, and half his orders still
  > say London. One fact should live in one place.

- [x] It carries a CustomerID equal to a customer's key

  > Link by key equality: the foreign key in orders points at the
  > primary key in customers. One shared identifier, zero copies.
{: .quiz }

```
### 🔬 Observations — what we just played

- 🎸 Tables are powerful instruments: named, typed, touchable.
- 🏷️ Columns have names and types; some are **strategic**: keys.
- ⚖️ We compared column values with fixed values — constants.
- 🖇️ Tables link by key equality: primary key = foreign key.
- 🏋️‍♂️ We asked in English first, then in SQL — same question.
- 🔭 With this we can explore the *whole* database, to solve
  problems. Wahoo 🎉

⚙️ **The module check** waits in Canvas, Module 01 — the quest
continues there, on a bigger table.
```
{: .accordion #observations }

[Browse](#)
{: .folder parent="true" }

```yaml
bot: doc
voice: en-US
face:
  zoom: 1.2
script:
  - say: "A shop, an award, and one question: who was first to order cranberry sauce after Labor Day? Watch where the answer lives."
  - at: quest_app
    do: open
    say: "This is not a picture of a table — it is a table. The facts about every customer, in rows and columns."
  - at: quest_app
    do: select
    with: "Thomas Hardy"
    say: "There is our winner: one row. Selecting exactly the rows you mean — that is the whole game, and soon you will say it in SQL."
  - at: vocabulary
    do: open
    say: "Table, row, column. Three words, but they are load-bearing — every conversation about databases stands on them."
  - at: dikiw
    do: open
    say: "Data becomes information, information becomes knowledge, knowledge becomes a decision. The award gets delivered because a row was found."
  - at: speak_sql
    do: open
    say: "English first, always. SQL is just the English sentence with its tie on."
  - at: two_tables
    do: open
    say: "Here is the trick the whole relational world runs on: two tables, linked by key equality. Primary key meets foreign key, and one sentence spans both."
  - at: observations
    do: open
    say: "You started with a problem, found Tom with your bare hands, then with SQL. The module check in Canvas lets you play it again on a bigger board."
stories:
  summarize the page:
    - 'You might wonder: summarize the page'
    - A shop must find its best customer — the first to order cranberry sauce after Labor Day.
    - The answer lives in a database, in a customers table with rows and columns.
    - You learn the words table, row, column, and the DIKIW ladder from data to wisdom.
    - Queries start in English and become SQL, selecting exactly the rows you mean.
    - Two tables link by key equality, letting one sentence span customers and orders.
  who is Thomas Hardy:
    - 'You might wonder: who is Thomas Hardy'
    - Thomas Hardy is a customer in London — row four of the customers table.
    - He was the first to order cranberry sauce after Labor Day, so he wins the award.
    - Finding his row, then his contact info, is your first data quest.
```
{: .avatar #guide dock="true" size="115" }
