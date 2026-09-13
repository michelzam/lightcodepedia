# 🏗️ 03 · Build the Shop

🧱 The shop was theirs. Now it is yours.

Module 01 found Thomas Hardy in a table. Module 02 asked the database
about him with queries. Both times the tables were **someone else's**
— w3schools built them. This module hands you the trowel: MySQL is on
your machine, Workbench is open, a Customers table is already in it.
You will add the missing tables, tie them together with keys,
and watch the database draw a picture of what you built.

**The promise:** by the end of this module you can turn an English
sentence about the shop — *a customer places orders* — into a table
with a key, tie it to another table with a foreign key, and read the
model the database draws of itself. And you can smell a poor design
before it bites.

**Three walks, in order:**

1. [🔧 Setup — MySQL on your machine](00_setup.md) — install MySQL
   Server and Workbench, create your database and the Customers table,
   insert Thomas Hardy: fourteen pictured steps.
2. [🧱 The Moon Walk](01_moon_walk.md) — from data to structure and
   back: reverse engineer your Customers, build Orders with a foreign
   key, insert, join, and reverse engineer again to see the model grow.
3. [📐 Good Design](02_design.md) — the words: entity, key,
   relationship, cardinality — and three smell tests that tell a poor
   table from a good one.

Each page has a guide — press play and Doc walks you through, or read at
your own pace. Already have MySQL and a Customers table with Thomas in
it? Skim the Setup page, take its two quizzes, and go on.

- [🗺️ The Treasure Hunt](../module_02/01_hunt.md)
- [📋 Query Concepts](../module_02/02_concepts.md)
{: .prerequisite }

[Browse](#)
{: .folder parent="true"}

```
### 🗺️ Module map

Where each key word is taught — open a page, then the section:

| Word | Where |
|---|---|
| server, client, schema, insert | [Setup](00_setup.md) · steps 1, 5, 6, 10 |
| type (INT, VARCHAR, DATE) | [Setup](00_setup.md) · *The script* · [The Moon Walk](01_moon_walk.md) · *Reverse engineer* |
| primary key, foreign key | [The Moon Walk](01_moon_walk.md) · *Build Orders* · [Good Design](02_design.md) · *The building blocks* |
| relationship, 1:N | [The Moon Walk](01_moon_walk.md) · *Reverse engineer again* · [Good Design](02_design.md) · *English to ER* |
| entity, model | [Good Design](02_design.md) · *From table to entity* and *The picture* |
| normal forms, smell tests | [Good Design](02_design.md) · *Three smell tests* |

[Map](.)
{: .sitemap height="420" }
```
{: .accordion #module_map }

```yaml
bot: doc
voice: en-US
face:
  zoom: 1.2
script:
  - say: "Two modules on someone else's tables. This one is yours: MySQL on your machine, Workbench open, your Customers table waiting. We build the shop around it."
  - say: "Three walks. Setup first — MySQL on your machine, your database, your Customers table with Thomas in it. Then the Moon Walk — build Orders with a foreign key and watch the model grow. Then Good Design, the words and three smell tests. The module map below shows where each key word lives."
stories:
  summarize the page:
    - 'You might wonder: summarize the page'
    - Module 03 moves from reading the shop's tables to building your own, in MySQL Workbench.
    - It has three walks — Setup, where MySQL lands on your machine with a Customers table; the Moon Walk, where you build Orders tied to Customers and reverse engineer the model; and Good Design, the words and three smell tests.
    - The module map shows where each key word — type, key, relationship, entity, normal form — is taught.
  what should I do first:
    - 'You might wonder: what should I do first'
    - Open Setup and follow the fourteen pictured steps until Thomas Hardy is in your Customers table.
    - Then open the Moon Walk and play the tour — Doc walks the script step by step.
    - Finish with Good Design, which names what you built and shows what a poor table looks like.
```
{: .avatar #guide dock="true" size="115" }
