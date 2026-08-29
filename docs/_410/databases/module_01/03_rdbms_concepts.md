# 📋 Databases & RDBMS Concepts

The Data Quest gave you the moves. This page gives you the words —
the five concepts the whole semester stands on.

- [🏆 The Data Quest](02_data_quest.md)
{: .prerequisite }

Ask Doc for a tour!
{: .avatar_trigger target="guide" }

```
### 🏆 1 · From story to structure

Thomas Hardy, a customer in London, places the first order for
cranberry sauce after Labor Day — six hours ahead of Milwaukee.
To serve him well we must 📝 record his contact details, 📦 note
what he ordered, 🚚 ensure reliable delivery.

These facts are **data**. From data we build **information**
(summaries of sales, customer lists), then **knowledge** (patterns,
loyal customers), and eventually **wisdom** (strategic decisions).

To select the best customer of the year, we need a place where the
data is **stored, organized, and accessible**: the database.
```
{: .accordion #story_to_structure }

```
### 🛢️ 2 · What is a database?

> "A database is a collection of data, organized to reflect the
> essential aspects of a given problem space, or domain."

💡 The database mirrors the real world — but **only in the
dimensions that matter**. For our shop, the relevant domain is
customers, orders, products.

🪄 Organizing tables is a **design choice**, not a law of nature:
analyzing the problem, shaping tables with columns, and choosing
efficient ways to connect them. That craft is where this course is
headed.
```
{: .accordion #what_database }

```
### 🖥️ 3 · What is a DBMS?

> "A database management system (DBMS) is the software that defines,
> creates, maintains, and controls access to the database." [Rigaux]

👮‍♀️ The DBMS is the **only official way in**. No app, script, or
intern reaches the data around it.

⚙️ It is our survival toolset: it keeps the data **consistent,
retrievable, and secure** — through crashes, concurrent users, and
Mondays. MySQL, which you will install soon, is one.
```
{: .accordion #what_dbms }

```
### 📋 4 · Why "relational"?

Because the data are stored as **relations** — and a relation is
just a way of tying pieces of information together, at two levels:

**Within a row** — `CustomerID = 4`, `ContactName = Thomas Hardy`,
`City = London` are related because they describe the *same person*.
The columns define what kinds of facts we can store.

**Across tables** — Orders carries a `CustomerID`; that ID relates
each order back to the right row in Customers. Shared identifiers —
**keys** — connect the tables.

One word, two levels of connection. That is the relational model.
```
{: .accordion #relational }

```
### 🌍 5 · Why it matters

Databases are behind almost every modern information system:

- 💳 banking systems,
- 💬 social media platforms,
- 🔬 scientific archives,
- 🛒 retail and logistics networks.

Understanding databases means understanding how information is
**stored, retrieved, and kept reliable at scale** — from your bank
account to the scientific archive for berries.
```
{: .accordion #why_matters }

**Q:** Your app wants to read customer data. What is the official way in?

- [ ] Open the database files directly — it is faster

  > Faster until the first crash or the second user. Going around
  > the guard is how data stops being consistent and secure.

- [x] Ask the DBMS — the one official way in

  > The DBMS defines, creates, maintains, and controls access — the
  > lid, the label, and the guard on the jar.

- [ ] Email the query to the database administrator and wait

  > The admin runs it through… the DBMS. Charming, but you added a
  > human to the pipeline, not a way in.
{: .quiz }

**Q:** "Relational" means the data are related — at how many levels?

- [ ] One: rows are related to their table

  > Belonging to a table is just residence. The model's power is in
  > *what* relates: values to each other, rows to rows.

- [x] Two — within a row, and across tables through keys

  > Within a row, values describe the same entity. Across tables,
  > shared keys connect rows. Hold both and the model fits in your
  > hand.

- [ ] It refers to the friendly relations among database admins

  > Admins are lovely people, but the term is math: a relation is a
  > way of tying pieces of information together.
{: .quiz }

```
### 📖 Formal definitions — for reference

**ISO/IEC 2382** (adapted): "A database is a collection of data
organized according to a schema, to serve one or more applications."

**Oxford English Dictionary**: "A structured set of data held in a
computer, especially one that is accessible in various ways."

**Rigaux et al. (2000)**: "A database is a collection of data,
organized to reflect the essential aspects of a given domain."

Three definitions, one spine: **organized data, in service of a
purpose**.
```
{: .accordion #definitions }

```
### ✅ Your move

Everything graded lives in **Canvas 410, Module 01**: the Welcome
and Syllabus quizzes if you have not taken them, the module check,
and your video introduction in the discussion.
```
{: .accordion #your_move }

[Browse](#)
{: .folder parent="true" }

```yaml
bot: doc
voice: en-US
face:
  zoom: 1.2
script:
  - at: story_to_structure
    do: open
    say: "Everything starts as a story. The concepts exist because a real shop needed a real answer about a real Thomas."
  - at: what_database
    do: open
    say: "The key word is organized — a database mirrors the world, but only in the dimensions that matter. Choosing those dimensions is design, and design is a choice you will learn to make."
  - at: what_dbms
    do: open
    say: "The database is the jar; the DBMS is the lid, the label, and the guard. One official way in — that is what keeps the data trustworthy."
  - at: relational
    do: open
    say: "Relational means related twice: values in a row belong to one entity, and rows across tables meet through keys. Hold both levels and the whole model fits in your hand."
  - at: why_matters
    do: open
    say: "Your bank balance is a row. Your transcript is a row. Reliability at scale is not an abstraction — it is your life, stored carefully."
  - at: your_move
    do: open
    say: "Words done, moves next: Canvas, Module 01. And keep your one-table sentences coming."
stories:
  summarize the page:
    - 'You might wonder: summarize the page'
    - This page names the five concepts behind the Data Quest.
    - A database is data organized to mirror the aspects of a domain that matter.
    - The DBMS is the only official way to reach the data, keeping it consistent and secure.
    - Relational means related at two levels — within a row, and across tables through keys.
    - It closes with formal definitions and your next moves in Canvas, Module 01.
  what is the difference between a database and a DBMS:
    - 'You might wonder: what is the difference between a database and a DBMS'
    - The database is the organized collection of data itself — the jar with the tables.
    - The DBMS is the software around it, the only official way to define, create, and reach the data.
    - MySQL is a DBMS; the shop's customers and orders are a database it manages.
```
{: .avatar #guide dock="true" size="115" }
