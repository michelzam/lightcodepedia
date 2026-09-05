# 🔎 02 · Data Quest 2

🗺️ Eight tables, one order, and a claim to check.

Module 01 found Thomas Hardy with your bare hands, in a five-row table.
The real database has **eight tables and a thousand rows** — too many
to scroll. This module hands you the tool that makes scrolling
unnecessary: the **query**. You say what you want in English, then in
SQL, and the database does the walking.

**The promise:** by the end of this module you can turn an English
sentence into a SQL query that answers it — on one table, then across
two — and you can tell a *related* pair of tables from a *crossed* one.

**Two walks, in order:**

1. [🗺️ The Treasure Hunt](01_hunt.md) — the eight tables of the shop,
   live on the page. Run your first queries here, then on the full-size
   database. A claim about Thomas waits to be checked.
2. [📋 Query Concepts](02_concepts.md) — the words for what you just
   did: selection, projection, join, cross product, nested query.

Each page has a guide — press play and Doc walks you through, or read at
your own pace.

- [🏆 The Data Quest](../module_01/02_data_quest.md)
- [📋 Databases & RDBMS Concepts](../module_01/03_rdbms_concepts.md)
{: .prerequisite }

[Browse](#)
{: .folder parent="true"}

```
### 🗺️ Module map

Where each key word is taught — open a page, then the section:

| Word | Where |
|---|---|
| table, row, column | [The Treasure Hunt](01_hunt.md) · *Eight tables — the map* |
| select (columns, `*`) | [The Treasure Hunt](01_hunt.md) · *Say it in English, then run it* · [Query Concepts](02_concepts.md) · *Select columns* |
| where (rows) | [The Treasure Hunt](01_hunt.md) · *Say it in English* · [Query Concepts](02_concepts.md) · *Select rows* |
| key, join, crossed tables | [The Treasure Hunt](01_hunt.md) · *Two tables* and *Crossed tables* · [Query Concepts](02_concepts.md) · *Cross product and join* |
| a result is a table | [The Treasure Hunt](01_hunt.md) · *A result is a table* · [Query Concepts](02_concepts.md) · section 5 |

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
  - say: "Module one was a five-row table. The real shop has eight tables and about a thousand rows — nobody scrolls that. This module gives you the query: say what you want, and the database walks for you."
  - say: "Two walks. First the Treasure Hunt, where the eight tables are live on the page and you run real SQL on them. Then the concepts page, which names every move you made. The module map below shows where each key word lives."
stories:
  summarize the page:
    - 'You might wonder: summarize the page'
    - Module 02 moves from scrolling a table to querying a database.
    - It has two walks — the Treasure Hunt over the shop's eight tables, and the query concepts page.
    - You will write queries in English first, then in SQL, on one table and then across two.
    - The module map shows where each key word — table, select, where, key — is taught.
  what should I do first:
    - 'You might wonder: what should I do first'
    - Open the Treasure Hunt and play the tour — the eight tables are live, and Doc runs the first query for you.
    - Then read the concepts page, which names what you did.
    - Finish with the ladder on the hunt page — one sentence over two tables, then more, then all eight.
```
{: .avatar #guide dock="true" size="115" }
