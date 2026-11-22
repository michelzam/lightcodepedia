# 📤 13 · Second Iteration — The Report and the Export

🎯 No new material this week: a guide to catch up, finish your database, and package it for the hand-in.

Ask Doc for a tour!
{: .avatar_trigger target="guide" }

Welcome back! This week there is **nothing new to learn** — no new
database, no new quiz. It is a week to **catch up** and to move your
project to its second iteration: a database that runs, a report that
tells its story, and the files that prove it.

Two handouts guide the week, both on Canvas:

- 📜 **The Final Report Template** — seven sections, each with a
  Scenario 3 example of the detail expected.
- 📜 **ExportDB** — how to export your database from Workbench as one
  `.sql` file.

This page walks both, step by step. Open the step where you are; skip
what is already done.

> Why did the database bring a suitcase? It was getting **exported**. 🧳

````
### 🧭 Step 1 · Where are you? One card, one next bite

Before anything else, take stock. Tick where you are, honestly — nobody
grades this card, it only tells you (and Ari) where to start.

```yaml
scenario: {value: "-", options: ["-", "1 · SkillBridge", "2 · Multilingual Course Management", "4 · Smart Logistics", "5 · Cultural Events Archive", "My own, approved by the instructor"]}
diagram: {value: "not yet", options: ["not yet", "sketched on paper", "in Workbench", "laid out, parents on top"]}
create_script: {value: "not yet", options: ["not yet", "some tables", "all tables, they run"]}
data_script: {value: "not yet", options: ["not yet", "some tables", "every table, parents first"]}
engaging_query: {value: "not yet", options: ["not yet", "written", "runs, shows names"]}
report: {value: "not yet", options: ["not yet", "started from the template", "all seven sections"]}
stuck: "where you are stuck, if anywhere"
```
{: .form editable="true" #status title="🧭 My project, right now" }

**Your next bite** is the first piece still at *not yet*, in this order:
diagram → create script → data script → engaging query → report →
export. Module 12 walks each piece on the worked example:

| Piece | Where to look again |
|---|---|
| 🗺️ Diagram, parents on top | [Module 12 · Step 3](../module_12/index.md) |
| 🏗️ Create, then populate | [Module 12 · Step 4](../module_12/index.md) |
| 🔍 The engaging query | [Module 12 · Step 5](../module_12/index.md) |
| 🧾 Audit your own model | [Module 08 · Step 7](../module_08/index.md) |

Stuck? Fill the card, then press **Ask**: Ari reads it and asks the one
question that moves you forward. Ari never writes your SQL, your tables
or your report. Optional: Ari needs a free AI key (🔑 on its panel).

```yaml
name: Ari
icon: 🤓
provider: groq
model: openai/gpt-oss-120b
intro: "Show me your card. One bite at a time — which one is next? 🐘"
max_tokens: 700
placeholder: "Tell me where you are stuck."
system: |
  You are Ari, the AI TA of INFOST 410 (Databases, Michel Zam, UWM), module 13: the
  project's second iteration, a catch-up week with no new material. The student picks
  one scenario (1 SkillBridge, 2 Multilingual Course Management, 4 Smart Logistics,
  5 Cultural Events Archive; 3 Mobile Health Tracker is the worked example and cannot
  be picked) and hands in: an ER diagram, a create script, a data script, the engaging
  query with a screenshot of its results, a report of 800-1000 words, and the database
  exported from Workbench as .sql.
  You read the student's status card: scenario, diagram, create_script, data_script,
  engaging_query, report, stuck.
  The next bite is the first piece still at "not yet", in this order: diagram, create
  script, data script, engaging query, report, export.
  What was taught: read the engaging query backward to find the tables; every
  relationship 1:N, a many-to-many through a table in the middle; parents above children
  in the diagram; create and insert parents first (error 1452 otherwise); names in the
  result, never bare IDs; the report follows the template's seven sections (overview,
  ER diagram + data-loading order, schema overview, data population with SELECT
  screenshots, engaging query with SQL + screenshot + explanation, challenges,
  conclusion); the diagram is exported as a picture (File > Export > Export as PNG in
  the diagram view); the database is exported with Server > Data Export, the schema
  ticked, Dump Structure and Data, Export to Self-Contained File, Include Create Schema.
  How you help:
  - One question per reply, two sentences at most. Never two questions.
  - Start from the first piece at "not yet". If "stuck" is filled, ask about that first.
  - Never write SQL, a CREATE TABLE, an INSERT, the engaging query, the list of tables,
    or report text. Never draw the model.
  - If the student is behind, be encouraging and concrete: one bite for tonight.
  - When everything is done, point to the export and the final checklist (step 6).
  - Light humor, one emoji at most.
```
{: .agent #coach bound="{= dict(scenario=status.scenario, diagram=status.diagram, create_script=status.create_script, data_script=status.data_script, engaging_query=status.engaging_query, report=status.report, stuck=status.stuck) }" rows="2" }
````
{: .accordion #where }

````
### 📝 Step 2 · The report template, section by section

The template is a **guide to the detail expected**, not a form to copy:
every section shows what *you* write, then an example on Scenario 3.
The example is pedagogical — your report tells **your** scenario.

| # | Section | What you write | Size |
|---|---|---|---|
| 1 | System overview | What the database is for, and for whom | 3–5 sentences |
| 2.1 | ER diagram explanation | The entities, the key relationships, the cardinalities — and **one** screenshot of the diagram | a paragraph + the picture |
| 2.2 | Workflow and data-loading order | The story of your data, in the order it is inserted: parents first | a short list |
| 3 | Schema overview | How you structured the tables — names, keys, links. The full SQL stays in your `.sql` file | a paragraph |
| 4 | Data population | What sample data you inserted — with **SELECT screenshots** | a paragraph + pictures |
| 5 | Engaging query | 5.1 the SQL · 5.2 a screenshot of the query **and** its result · 5.3 what it returns, and why it answers the question | SQL + picture + 3–5 sentences |
| 6 | Challenges and notes | What went wrong, and how you got past it — your own story | 5–7 sentences |
| 7 | Conclusion | How the database meets the scenario's needs | 3–5 sentences |

Three sections deserve a closer look.

**2.2 · The workflow is the loading order.** The template tells
Scenario 3 as a story — *the admin adds doctors, users subscribe,
medications are recorded, doctors prescribe, users book appointments,
patients log their doses* — and each sentence is one table, filled in
that order. Tell yours the same way: who does what first, and which
table each step fills. If the story reads well, your INSERTs never meet
error 1452.

**4 · Data population: one SELECT per table.** One small screenshot per
table, the query and its rows in the same picture:

[A SELECT screenshot — Doctors](_slides/m13_select_doctors.jpg)
{: .embed image="true" width="60%" }

[A SELECT screenshot — Users](_slides/m13_select_users.jpg)
{: .embed image="true" width="80%" }

**5 · The engaging query: SQL, picture, explanation.** The picture shows
the query **and** its result together — the proof it runs:

[The engaging query and its result — Scenario 3](_slides/m13_query_results.jpg)
{: .embed image="true" width="100%" }

Then 3–5 sentences: what each row is, what the joins bring together,
why it answers the person who asked.

✅ **Done when** your document has the seven headings, each filled with
your scenario, and every *Insert screenshot here* replaced by a picture.
````
{: .accordion #template }

````
### 🗺️ Step 3 · Export the diagram as a picture

The report needs your diagram as an **image**: a `.mwb` file opens only
in Workbench, and nobody reading your report has it open.

1. Open your model's **EER diagram** in Workbench.
2. **Lay it out** before exporting: parents (no foreign key) on top,
   children below, every line flowing down. A diagram reverse-engineered
   from SQL drops the tables in creation order — drag them into place.
3. **File → Export → Export as PNG…** and save the picture.
4. Insert it in section 2.1 of your report, and keep the file for the
   hand-in.

This is what a laid-out diagram looks like — the template's own:

[Scenario 3 — the diagram, parents on top](_slides/m13_scenario3_erd.jpg)
{: .embed image="true" width="100%" }

✅ **Done when** your PNG reads top-down: Medications, Users, Doctors on
the first row in the example; in yours, every table with no foreign key.
````
{: .accordion #diagram_export }

````
### 📤 Step 4 · Export the database as a .sql file

The handout **ExportDB**, step by step: Workbench writes your whole
database — tables and rows — into one `.sql` file that rebuilds it
anywhere.

[ExportDB — Data Export in MySQL Workbench, six steps](_slides/m13_export_db.jpg)
{: .embed image="true" width="100%" }

| Step | Where | What to do |
|---|---|---|
| 1 | Menu **Server** | **Data Export** |
| 2 | *Tables to Export*, left | Tick **your** database (your project's schema, not a practice one); its tables appear ticked on the right |
| 3 | **Advanced Options…**, top right | Keep **complete-insert** (INSERTs name their columns) and **extended-insert** (several rows per INSERT); **quote-names** is on by default |
| 4 | *Export Options*, below | **Dump Structure and Data** · **Export to Self-Contained File** (one `.sql`) · **Include Create Schema** |
| 5 | *Objects to Export* | Tick *Dump Stored Procedures and Functions* or *Dump Triggers* only if your project has some |
| 6 | **Start Export** | *Export Completed*: the log names the file — that `.sql` is ready to upload in Canvas |

Two habits that save a bad surprise:

- **Name the file** after your project (`skillbridge.sql`, not
  Workbench's default `Dump…sql`), and note where Workbench saved it — the log's
  last line says it.
- **Test the file once**: create an empty schema, then **Server → Data
  Import → Import from Self-Contained File**, pick your `.sql`, and look:
  every table, every row, back. A dump that rebuilds your database is a
  dump that works.

The dropdown of step 4 also offers *Dump Structure Only* and *Dump Data
Only*: one way to get your create script and your data script as two
separate files, if you have not written them by hand.

✅ **Done when** your `.sql` file rebuilds your database in an empty
schema, tables and rows.
````
{: .accordion #db_export }

````
### 📸 Step 5 · Screenshots that prove

Every claim of the report rests on a picture. Good screenshots share
three habits:

| Habit | Why |
|---|---|
| The **query and its result** in one picture | The reader sees what ran *and* what came back |
| **Readable**: crop to the editor and the result grid | A full screen at the size of a stamp proves nothing |
| **Names, not IDs**, in the engaging query's result | The person who asked reads names |

The list, section by section:

| Section | Screenshot |
|---|---|
| 2.1 | The ER diagram, exported as PNG (step 3) |
| 4 | One `SELECT * FROM YourTable;` per table, with its rows |
| 5.2 | The engaging query and its result |
| 6 | Optional: an error you met and fixed — a good challenge story |

✅ **Done when** every *Insert screenshot here* of the template holds a
picture you made from your own database.
````
{: .accordion #screenshots }

````
### 📦 Step 6 · Before you hand in

The whole package, one last look:

| File | What it holds |
|---|---|
| 📝 Your report (Word document) | The seven sections, 800–1000 words, with the screenshots |
| 🗺️ The diagram (PNG) | Laid out, parents on top |
| 🏗️ The create script (`.sql`) | Every CREATE TABLE, parents first |
| 📥 The data script (`.sql`) | Every INSERT, in the same order |
| 🔍 The engaging query (`.sql`) | The query alone |
| 📤 The exported database (`.sql`) | From Data Export, tested once (step 4) |

And three checks of your own:

1. **Audit** your model with the sheet of [module 08](../module_08/index.md):
   0 violations on the design half.
2. **Run everything once more**, in order, on an empty schema: create,
   populate, query. What runs for you runs for the reader.
3. **Read your report aloud**: section 6 should sound like *you* — what
   really happened while you built it. Ari is welcome as a coach; say
   where it helped.

✅ **Done when** the six files are in one folder, the report reads well,
and you would be happy to show it to the person who asked the question.
````
{: .accordion #hand_in }

[Browse](#)
{: .folder parent="true" }

```yaml
bot: doc
voice: en-US
face:
  zoom: 1.2
script:
  - say: "Welcome back! No new material this week. It is a week to catch up, finish your database, and package it: the report, and the export."
  - at: where
    do: open
    say: "Step one. Where are you? Fill the card honestly. Your next bite is the first piece still at not yet. Ari can ask you the question that moves you forward."
  - at: template
    do: open
    say: "Step two. The report template. Seven sections, each with an example on Scenario 3. Tell your own scenario, and replace every insert screenshot here with your own picture."
  - at: diagram_export
    do: open
    say: "Step three. Export the diagram as a picture. Lay it out first, parents on top. Then file, export, export as PNG."
  - at: db_export
    do: open
    say: "Step four. Export the database. Server, Data Export, your schema, structure and data, one self contained file. Then test it once: import it into an empty schema."
  - at: screenshots
    do: open
    say: "Step five. Screenshots that prove. The query and its result in one picture, cropped, readable, with names and not IDs."
  - at: hand_in
    do: open
    say: "Step six. Before you hand in. Six files, an audit, one last run on an empty schema, and a report that sounds like you."
stories:
  summarize the page:
    - 'You might wonder: summarize the page'
    - This week brings no new material, only a guide to catch up on the project.
    - Take stock of where you are, and do the next piece still missing.
    - Follow the report template's seven sections, on your own scenario.
    - Export the diagram as a picture, and the database as one .sql file from Workbench.
    - Then check the whole package before you hand it in.
  how do I export:
    - 'You might wonder: how do I export my database'
    - In Workbench, open the Server menu, then Data Export.
    - Tick your schema, choose Dump Structure and Data, and Export to Self-Contained File.
    - Press Start Export, and keep the .sql file the log names.
  why test the export:
    - 'You might wonder: why test the export'
    - A dump that fails to rebuild your database proves nothing.
    - Import it once into an empty schema, and look for every table and every row.
```
{: .avatar #guide dock="true" size="115" }
