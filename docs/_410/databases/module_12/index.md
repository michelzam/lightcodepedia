# 🐘 12 · Your Project, One Bite at a Time

🎯 Everything you learned, in one database of your own: what the project asks, and how to build it bite by bite.

Ask Doc for a tour!
{: .avatar_trigger target="guide" }

Welcome back! Eleven modules are behind you: reading a model, querying
it, designing one, building it in Workbench, auditing it, changing data
safely. The final project asks for **all of it at once**, on a scenario
of your choice.

This page walks the project with you, using the **worked example** you
cannot pick, Scenario 3, the Mobile Health Tracker: its question, its
diagram, its tables, its query, the way you will build yours. You can
run every query right here.

> How do you eat an elephant? One bite at a time. 🐘 And how do you build
> a database? One table at a time, parents first.

Every step ends with a little quiz, just for you. Take your time. 🙂

````
### 🧭 Step 1 · The brief: one scenario, five pieces

**Choose one scenario**, then design and build the database that answers
its **engaging query** — a real question someone in that business asks.

| # | Scenario | Who asks what |
|---|---|---|
| 1 | 🤝 Freelance Work Platform — SkillBridge | A client reviews the freelancers they hired in the past year |
| 2 | 🧑‍🏫 Multilingual Course Management | A director looks for the most demanded languages |
| 3 | 🩺 Mobile Health Tracker — **the worked example, not for you to pick** | A doctor checks medication adherence |
| 4 | 🚛 Smart Logistics System | A manager looks for the routes with the most delays |
| 5 | 🖼️ Cultural Events Archive | The board highlights events with multilingual feedback |

The full text of each scenario — its description, the entities it may
include, and its engaging query word for word — is in the project's
brief on Canvas, with **sample data** for every scenario.

What you hand in, five pieces:

| Piece | What it is |
|---|---|
| 🗺️ ER diagram | Your tables, their keys, their lines — 1 : N, parents above |
| 🏗️ Create script | A `.sql` file with your CREATE TABLE statements |
| 📥 Data script | A `.sql` file with your INSERT INTO statements |
| 🔍 Engaging query | A `.sql` file with the query, and a **screenshot of its results** |
| 📝 Final report | 800–1000 words: your diagram, your choices, screenshots, challenges |

The rubric on Canvas says how each piece counts.

**Q:** Why can't you pick Scenario 3?

- [ ] It is cursed: every database built on it loses its keys

  > Keys get lost by forgetting to declare them, never by curses.

- [x] Its full solution is the example handed out: diagram, data, query

  > A scenario whose answer is already on the table teaches nothing
  > new. It is there to show you what a finished project looks like.

- [ ] Health data is illegal to store in MySQL

  > Hospitals run on relational databases. The reason is simpler.

- [ ] It has fewer tables than the others, so it is too easy to grade
  
  > Six tables, like the others. It is the example, that is all.
{: .quiz }
````
{: .accordion #brief }

````
### 🎯 Step 2 · Start from the question

The engaging query is not the last piece — it is the **first one to
read**. It says what your database must be able to answer, so it tells
you which tables you need. Read it **backward**: from the answer to the
tables.

Scenario 3's question: *each patient's medications, together with the
appointments they had with the doctor of their most recent visit.*

| In the answer… | …you need |
|---|---|
| each **patient**, by name | a `Users` table (FirstName, LastName) |
| their **medications**, by name | a `Medications` table — and since a patient takes many medications and a medication is taken by many patients, a table in the middle: `UserMedications` |
| their **appointments** | an `Appointments` table, pointing to the patient… |
| …with **the doctor** | …and to a `Doctors` table |

Four of the six tables come straight out of one sentence. The sixth,
`MedicationLogs` (did the patient take the dose?), comes from the
scenario's description: *log medication adherence*.

Two habits for your own question:

- **Names, not IDs.** "Each patient" means a name in the result, never a
  bare `UserID`. A name means one more JOIN, to the table that holds it.
- **Count words.** "The number of", "top 3", "the most", "3 or more" ask
  for `COUNT`, `GROUP BY`, `ORDER BY … DESC`, `LIMIT`, `HAVING`. You met
  each of them in modules 05 and 11.

**Q:** Scenario 5 asks for events with feedback in **3 or more distinct
languages**. Which clause keeps only those events?

- [ ] `WHERE COUNT(LanguageID) >= 3`

  > WHERE runs row by row, before any group exists: it cannot count.

- [ ] `ORDER BY LanguageID DESC LIMIT 3`

  > That keeps three rows, whatever they hold. The question is about
  > groups.

- [x] `HAVING COUNT(DISTINCT LanguageID) >= 3`, after the GROUP BY

  > HAVING filters groups after they are counted, and DISTINCT counts
  > each language once, however many visitors wrote in it.

- [ ] Ask each event politely how many languages it speaks

  > Events are shy. The GROUP BY asks for you.
{: .quiz }
````
{: .accordion #question }

````
### 🗺️ Step 3 · The ER diagram: parents above

Scenario 3's diagram, as it was handed out:

[Scenario 3 — Mobile Health Tracker, the ER diagram](_slides/m12_scenario3_erd.jpg)
{: .embed image="true" width="100%" }

Read it the way the audit sheet of module 08 reads it:

- **Top row: the parents.** `Medications`, `Users`, `Doctors` carry no
  foreign key. Nothing has to exist before them.
- **Middle row: the children.** `UserMedications` points up to Users and
  Medications; `Appointments` points up to Users and Doctors. Every line
  is **1 : N**, the many side below.
- **Bottom: the grandchild.** `MedicationLogs` points up to
  `UserMedications` — one prescription, many logged doses.
- **Many-to-many goes through a table in the middle.** Users ↔
  Medications is many-to-many; `UserMedications` turns it into two
  one-to-many, like Enrollments in UWM's map.

The naming conventions your diagram is read with:

| What | The rule | Example |
|---|---|---|
| Tables | Plural, PascalCase | `Customers`, `OrderDetails` |
| Columns | CamelCase | `FirstName`, `AppointmentDate` |
| Primary key | Singular table name + ID | `DoctorID` in Doctors |
| Foreign key | The name of the key it points to | `DoctorID` in Appointments |
| Lines | A verb or noun on the line; the ONE above the MANY | Users *books* Appointments |
| Everywhere | No spaces, no special characters | `MedicationLogs`, not `medication logs!` |

A tip from the audit: if you reverse-engineer your diagram from your SQL,
Workbench drops the tables in creation order, lines crossing. **Drag
them** until the parents sit on top and every line flows down.

**Q:** Why does `UserMedications` exist, since it holds no name at all?

- [ ] Workbench adds it automatically to keep diagrams symmetrical

  > Workbench draws what you create. Someone decided it was needed.

- [ ] To store the medications a second time, as a backup

  > A second copy would be a repeated fact, the 3NF trouble of module
  > 08. It holds only keys and the prescription's own facts.

- [x] It turns Users ↔ Medications, a many-to-many, into two 1 : N lines

  > One row per prescription: which user, which medication, since when.
  > Exactly the job of Enrollments between Students and Sections.

- [ ] Doctors refused to sit next to Medications
  
  > Doctors sit where their lines go: above Appointments.
{: .quiz }
````
{: .accordion #diagram }

````
### 🏗️ Step 4 · Create, then populate — parents first

Build in **two scripts**, so either can be run again on its own:

1. **Create** — every CREATE TABLE, parents first, each child with its
   `FOREIGN KEY … REFERENCES`.
2. **Populate** — every INSERT INTO, in the **same order**.

The order is your diagram read top-down. For Scenario 3:

| Round | Tables | Why now |
|---|---|---|
| 1 | Users, Doctors, Medications | no foreign key: nothing to wait for |
| 2 | UserMedications, Appointments | their parents now exist |
| 3 | MedicationLogs | its parent, UserMedications, now exists |

**If** you insert a child before its parents, **then** MySQL refuses with **error 1452**:
the foreign key points to a row that is not there yet. You met it in
module 09. Write this order in your report: it is your **data-loading
workflow**.

A few rows per table are enough — three to five — as long as the
engaging query **finds something**. Check it early: a query on dates
like "the past 12 months" counts back from **today**, so sample data
from long ago returns nothing. Adjust your dates, or say in the report
what the query would return.

All the tables of the example are in the **🔎 Practice block** below,
filled with the handout's data.

**Q:** In your scenario, `Shipments` points to `Suppliers`, `Warehouses`
and `Products`. When can its INSERT run?

- [ ] First, so the most important table is ready early

  > Its three foreign keys would point to nothing: error 1452, three
  > times over.

- [x] After the rows of all three parents exist

  > A child waits for every parent it points to. Round 2, at the
  > earliest.

- [ ] Any time, MySQL sorts the inserts itself

  > MySQL runs your script top to bottom, exactly as written.

- [ ] Only on Fridays, when the trucks are in
  
  > Trucks keep their own schedule. Inserts follow the foreign keys.
{: .quiz }
````
{: .accordion #build }

````
### 🔍 Step 5 · The engaging query: answer the question, with names

Here is the example's query, as it was handed out with its screenshot:

~~~sql
SELECT
    u.FirstName AS PatientFirstName,
    u.LastName AS PatientLastName,
    d.FirstName AS DoctorFirstName,
    d.LastName AS DoctorLastName,
    m.MedicationName,
    um.PrescribedDate,
    a.AppointmentDate,
    a.AppointmentTime,
    a.Status
FROM UserMedications um
JOIN Users u
    ON um.UserID = u.UserID
JOIN Medications m
    ON um.MedicationID = m.MedicationID
JOIN Appointments a
    ON a.UserID = u.UserID
    AND a.DoctorID = (SELECT DoctorID
                      FROM Appointments
                      WHERE UserID = u.UserID
                      ORDER BY AppointmentDate DESC
                      LIMIT 1)
JOIN Doctors d
    ON a.DoctorID = d.DoctorID
ORDER BY
    u.LastName, m.MedicationName;
~~~

[Scenario 3 — the query and its results in Workbench](_slides/m12_scenario3_results.jpg)
{: .embed image="true" width="100%" }

Read it with the question in hand:

- **Four JOINs**, one per table the answer names: patient, medication,
  appointment, doctor.
- **Names in the result**: first and last names, the medication's name —
  never a bare ID.
- **The small subquery** in the last ON finds the doctor of the
  patient's most recent visit. Your scenario may need one trick of the
  kind, or none: the question decides.
- **The screenshot** shows the query **and** its results in one picture.

👉 Run **①** in the practice block: the same joins, without the subquery
(in this data every patient sees one doctor, so the rows are the same).
Then run **②**: a count per patient, with a LEFT JOIN.

**Your move** — query **③** answers "who takes what?" with bare IDs.
Make it answer with **names**: the patient's last name and the
medication's name. Press ▶ Run.

**Q:** Query ① shows Sarah and Michael, but no Emily Davis. Why?

- [ ] Emily asked to be removed from the example

  > Emily is in Users, row 3. The query decides who shows up.

- [ ] The database lost her row during the last JOIN, a known MySQL bug

  > No bug: the JOIN does exactly what it promises.

- [x] She has no medication, so the inner JOIN finds no row to pair her with

  > An inner JOIN keeps only the pairs that exist. Query ②'s LEFT JOIN
  > keeps her, with a count of 0.

- [ ] Her appointments are cancelled, so she is hidden
  
  > She has no appointment and no medication at all. The JOIN on
  > UserMedications already drops her.
{: .quiz }
````
{: .accordion #query }

````
### 📝 Step 6 · The report: tell the story of your database

800–1000 words, with your screenshots. The template on Canvas is a help,
not a must: any structure works as long as **seven ingredients** are
there.

| # | Ingredient | One question it answers |
|---|---|---|
| 1 | System overview | What is this database for, and for whom? |
| 2 | ER diagram + loading order | What are the tables, and in which order are they filled? |
| 3 | Schema overview | What does each table hold, and how are they linked? |
| 4 | Data population | What did you insert? (screenshots) |
| 5 | Engaging query | What does it answer? SQL, screenshot of the results, and what they say |
| 6 | Challenges | What went wrong, and how did you get past it? |
| 7 | Conclusion | What works, and what would you add next? |

And the files, beside the report: the create script, the data script,
the query, the diagram as a picture. A `.mwb` file alone cannot be opened
without Workbench: export the diagram as an image too.

**Before you hand in, audit yourself** with the sheet of module 08: one
column per table, the number of violations on every design row (aim for
0), the number of uses on every coverage row. Fix, then audit again.

**Your words, your voice.** Challenges are the most personal part of the
report: what really happened while you built it. Ari, the course's AI TA,
is welcome as a coach — say where it helped.

**Q:** Your report is excellent, but the query's result appears nowhere.
What is missing?

- [ ] Nothing: the SQL is there, the reader can imagine the result

  > A reader cannot run your query. The screenshot is the proof it
  > works.

- [ ] A paragraph explaining that the query surely works

  > Surely is not a proof. A picture of the result is.

- [ ] An apology to the database for not running it

  > The database forgives. The rubric reads screenshots.

- [x] A screenshot of the query and its results, explained in a line or two

  > Ingredient 5: the SQL, its results on screen, and what they answer.
{: .quiz }
````
{: .accordion #report }

````
### 🐘 Step 7 · One bite at a time — your plan, and Ari

Don't build the whole project at once. Bites, each one done when it
**runs**:

1. **Pick** your scenario, read its engaging query **backward** (step 2).
2. **Sketch** the tables on paper: parents on top, keys, lines.
3. **Create** the parents only. Run. Then the children. Run.
4. **Populate** in the same order, a few rows each. Run.
5. **Query**: run the engaging query, fix until it answers with names.
   Screenshot.
6. **Diagram**: the final one, laid out parents on top. Export it.
7. **Audit** yourself with the module 08 sheet. Fix.
8. **Write** the report around your screenshots.

Fill your **plan card** with your own scenario, then press **Ask**: Ari,
the course's AI TA, reads it and asks the one question that moves your
plan forward. Ari never writes your SQL or your tables — the design is
yours. Optional: Ari needs a free AI key (🔑 on its panel).

```yaml
scenario: {value: "-", options: ["-", "1 · SkillBridge", "2 · Multilingual Course Management", "4 · Smart Logistics", "5 · Cultural Events Archive", "My own, approved by the instructor"]}
question: "the engaging query, in your own words"
tables: "the tables you plan, parents first"
labels: "the names your result will show (not IDs)"
stuck: "where you are stuck, if anywhere"
```
{: .form editable="true" #plan title="🐘 My project plan" }

```yaml
name: Ari
icon: 🤓
provider: groq
model: openai/gpt-oss-120b
intro: "Show me your plan. I only ask questions. 🐘"
max_tokens: 700
placeholder: "Ask me to challenge your plan."
system: |
  You are Ari, the AI TA of INFOST 410 (Databases, Michel Zam, UWM), module 12: the final
  project. The student picks one scenario (1 SkillBridge, 2 Multilingual Course Management,
  4 Smart Logistics, 5 Cultural Events Archive; 3 Mobile Health Tracker is the worked
  example and cannot be picked) and hands in an ER diagram, a create script, a data script,
  the engaging query with a screenshot of its results, and a report of 800-1000 words.
  You read the student's plan card: scenario, question, tables, labels, stuck.
  What was taught: read the engaging query backward, from the answer to the tables; every
  relationship 1:N, a many-to-many through a table in the middle; parents (no FK) above
  children in the diagram; tables plural PascalCase, columns CamelCase, PK = singular
  table name + ID, FK = the name of the key it points to; create and insert parents
  first (error 1452 otherwise); names in the result, never bare IDs; COUNT, GROUP BY,
  HAVING, ORDER BY DESC, LIMIT for count words; dates relative to today need recent data;
  audit with the module 08 sheet before handing in.
  How you help:
  - One question per reply, two sentences at most. Never two questions.
  - Never write SQL, a CREATE TABLE, an INSERT, the engaging query, or the list of tables.
    Never draw or list the model. Never write report text.
  - If a field is "-" or still holds its placeholder, ask about that field first.
  - Test the plan against the question: which table holds each name the answer shows,
    which table sits in the middle of a many-to-many, which table must be filled first.
  - If the student is stuck, ask what the error says or what the query returns now.
  - When the plan holds, say so in one line and point to the next bite.
  - Light humor, one emoji at most.
```
{: .agent #coach bound="{= dict(scenario=plan.scenario, question=plan.question, tables=plan.tables, labels=plan.labels, stuck=plan.stuck) }" rows="2" }

**Q:** You have three evenings left and nothing built. Which bite comes
first?

- [ ] The report, since it is worth the most words

  > A report about a database that does not exist yet is fiction.

- [ ] Ten tables at once, then run everything and hope

  > One error in table 2 hides behind eight others. Bites, and run each.

- [ ] A nap, so the elephant gets smaller on its own

  > Elephants do not shrink overnight. Projects neither.

- [x] Read the engaging query backward, then create the parent tables
  
  > The question tells you the tables; the parents can be created and
  > run tonight. Everything else stands on them.
{: .quiz }
````
{: .accordion #plan_step }

````
### 🔎 Practice block — Scenario 3, ready to run

The example's six tables, with the handout's data. Parents first:

```json
[
  {"UserID": 1, "FirstName": "Sarah", "LastName": "Thompson", "Email": "sarah@email.com", "DateOfBirth": "1985-06-15", "JoinDate": "2024-01-10"},
  {"UserID": 2, "FirstName": "Michael", "LastName": "Brown", "Email": "michael@email.com", "DateOfBirth": "1978-09-22", "JoinDate": "2024-02-15"},
  {"UserID": 3, "FirstName": "Emily", "LastName": "Davis", "Email": "emily@email.com", "DateOfBirth": "1992-03-30", "JoinDate": "2024-03-20"}
]
```
{: .dataset #Users }

[Users](#)
{: .datagrid source="Users" rows="3" }

```json
[
  {"DoctorID": 1, "FirstName": "Dr. James", "LastName": "Wilson", "Specialty": "Cardiology", "Phone": "555-0101"},
  {"DoctorID": 2, "FirstName": "Dr. Lisa", "LastName": "Anderson", "Specialty": "General Practice", "Phone": "555-0102"},
  {"DoctorID": 3, "FirstName": "Dr. Robert", "LastName": "Lee", "Specialty": "Endocrinology", "Phone": "555-0103"}
]
```
{: .dataset #Doctors }

[Doctors](#)
{: .datagrid source="Doctors" rows="3" }

```json
[
  {"MedicationID": 1, "MedicationName": "Lisinopril", "Dosage": "10mg", "Frequency": "Once daily", "Instructions": "Take in morning"},
  {"MedicationID": 2, "MedicationName": "Metformin", "Dosage": "500mg", "Frequency": "Twice daily", "Instructions": "Take with meals"},
  {"MedicationID": 3, "MedicationName": "Aspirin", "Dosage": "81mg", "Frequency": "Once daily", "Instructions": "Take with food"}
]
```
{: .dataset #Medications }

[Medications](#)
{: .datagrid source="Medications" rows="3" }

```json
[
  {"UserMedicationID": 1, "UserID": 1, "MedicationID": 1, "PrescribedDate": "2024-01-15", "Active": 1},
  {"UserMedicationID": 2, "UserID": 2, "MedicationID": 2, "PrescribedDate": "2024-02-20", "Active": 1},
  {"UserMedicationID": 3, "UserID": 1, "MedicationID": 3, "PrescribedDate": "2024-01-15", "Active": 1}
]
```
{: .dataset #UserMedications }

[UserMedications](#)
{: .datagrid source="UserMedications" rows="3" }

```json
[
  {"AppointmentID": 1, "UserID": 1, "DoctorID": 1, "AppointmentDate": "2024-11-20", "AppointmentTime": "10:00:00", "Status": "Scheduled", "Notes": "Regular checkup"},
  {"AppointmentID": 2, "UserID": 2, "DoctorID": 2, "AppointmentDate": "2024-11-15", "AppointmentTime": "14:30:00", "Status": "Scheduled", "Notes": "Follow-up"},
  {"AppointmentID": 3, "UserID": 1, "DoctorID": 1, "AppointmentDate": "2024-10-15", "AppointmentTime": "11:00:00", "Status": "Completed", "Notes": "Blood pressure check"}
]
```
{: .dataset #Appointments }

[Appointments](#)
{: .datagrid source="Appointments" rows="3" }

```json
[
  {"LogID": 1, "UserMedicationID": 1, "ScheduledDate": "2024-11-01", "Taken": "Yes", "TimeLogged": "08:30:00"},
  {"LogID": 2, "UserMedicationID": 1, "ScheduledDate": "2024-11-02", "Taken": "Yes", "TimeLogged": "08:45:00"},
  {"LogID": 3, "UserMedicationID": 1, "ScheduledDate": "2024-11-03", "Taken": "No", "Notes": "Forgot to take"},
  {"LogID": 4, "UserMedicationID": 2, "ScheduledDate": "2024-11-01", "Taken": "Yes", "TimeLogged": "09:00:00"},
  {"LogID": 5, "UserMedicationID": 2, "ScheduledDate": "2024-11-02", "Taken": "Yes", "TimeLogged": "09:15:00"}
]
```
{: .dataset #MedicationLogs }

[MedicationLogs](#)
{: .datagrid source="MedicationLogs" rows="5" }

**① The engaging query**, four JOINs, names in the result:

```sql
SELECT Users.FirstName, Users.LastName,
       Medications.MedicationName,
       Doctors.LastName AS DoctorLastName,
       Appointments.AppointmentDate, Appointments.Status
FROM UserMedications
JOIN Users ON UserMedications.UserID = Users.UserID
JOIN Medications ON UserMedications.MedicationID = Medications.MedicationID
JOIN Appointments ON Appointments.UserID = Users.UserID
JOIN Doctors ON Appointments.DoctorID = Doctors.DoctorID
ORDER BY Users.LastName, Medications.MedicationName
```
{: .query source="UserMedications,Users,Medications,Appointments,Doctors" #q_engaging editable="true" }

[patients, medications, appointments](#)
{: .datagrid source="q_engaging" rows="5" }

**② A count per patient**, the LEFT JOIN keeps everyone:

```sql
SELECT Users.UserID, Users.FirstName, Users.LastName,
       COUNT(UserMedications.UserMedicationID) AS Medications
FROM Users
LEFT JOIN UserMedications ON UserMedications.UserID = Users.UserID
GROUP BY Users.UserID, Users.FirstName, Users.LastName
```
{: .query source="Users,UserMedications" #q_count editable="true" }

[medications per patient](#)
{: .datagrid source="q_count" rows="3" }

**③ ✋ Your move** — names, not IDs. This query answers "who takes
what?" with bare numbers. Make it show the patient's `LastName` and the
`MedicationName` instead of `UserID` and `MedicationID`. Press ▶ Run.

```sql
SELECT UserMedications.UserID, UserMedications.MedicationID,
       UserMedications.PrescribedDate
FROM UserMedications
```
{: .query source="UserMedications,Users,Medications" #q_mine editable="true" }

[your answer](#)
{: .datagrid source="q_mine" rows="3" }

The second check at the very bottom stays **red until you do it**.
````
{: .block title="🔎 Practice block" #live }

Two words to keep from this week: the `engaging_query`[^engaging_query]
is the requirement you read first, and the `loading_order`[^loading_order]
is your diagram read top-down. The proof below runs the practice block's
own queries:

```gherkin
Feature: The worked example answers its question
  Scenario: The engaging query names patients and medications
    Given the example's tables and its engaging query
    :::python
    self.engaging: Query = self.page.q_engaging
    :::
    When the query runs
    Then five rows come back, with names and no patient without medication
    :::python
    assert self.engaging.count == 5, self.engaging.count
    assert sorted(set(self.engaging.values("LastName"))) == ["Brown", "Thompson"], self.engaging.values("LastName")
    assert "Lisinopril" in self.engaging.values("MedicationName"), self.engaging.values("MedicationName")
    :::

  Scenario: The LEFT JOIN keeps the patient with no medication
    Given the count per patient
    :::python
    self.per_patient: Query = self.page.q_count
    :::
    When the query runs
    Then three patients come back, Emily Davis with 0
    :::python
    assert self.per_patient.count == 3, self.per_patient.count
    counts: dict = dict(zip(self.per_patient.values("LastName"), self.per_patient.values("Medications")))
    assert counts.get("Davis") == "0", counts
    :::
```
{: .feature #activity_proof tags="engaging_query" visible="true" status="passing" }

And one check that is **yours**. It reads your query in the practice
block and stays red while it shows bare IDs:

```gherkin
Feature: Your move — names, not IDs
  Scenario: Who takes what, by name
    Given your query in the practice block
    :::python
    self.mine: Query = self.page.q_mine
    :::
    When you press Run on your query
    Then the result shows the patients' last names and the medications' names
    :::python
    names: list = sorted(self.mine.values("MedicationName"))
    assert names == ["Aspirin", "Lisinopril", "Metformin"], \
        "show Medications.MedicationName: JOIN Medications ON UserMedications.MedicationID = Medications.MedicationID"
    assert "Thompson" in self.mine.values("LastName"), \
        "show Users.LastName: JOIN Users ON UserMedications.UserID = Users.UserID"
    :::
    And no bare ID is left in the result
    :::python
    assert set(self.mine.values("UserID")) == {""}, "the UserID column is still in the result: replace it with the name"
    assert set(self.mine.values("MedicationID")) == {""}, "the MedicationID column is still in the result: replace it with the name"
    :::
```
{: .feature #your_move_proof tags="engaging_query" visible="true" status="pending" celebration="true" }

[Browse](#)
{: .folder parent="true" }

```yaml
bot: doc
voice: en-US
face:
  zoom: 1.2
script:
  - say: "Welcome back! This week is all about your final project. Everything you learned, in one database of your own, built one bite at a time. Scenario 3 shows the way."
  - at: brief
    do: open
    say: "Step one. The brief. Pick one scenario, not number three, which is the worked example. Hand in five pieces: the diagram, the create script, the data script, the engaging query with its results, and the report."
  - at: question
    do: open
    say: "Step two. Start from the question. Read the engaging query backward, from the answer to the tables. Names, not IDs. And count words call for count, group by, and having."
  - at: diagram
    do: open
    say: "Step three. The diagram. Parents on top, children below, every line one to many. A many to many goes through a table in the middle."
  - at: build
    do: open
    say: "Step four. Create, then populate, parents first. If you insert a child before its parents, then MySQL says error fourteen fifty two. That order is your data loading workflow."
  - at: query
    do: open
    say: "Step five. The engaging query. One join per table the answer names, names in the result, and a screenshot with the query and its results."
  - at: report
    do: open
    say: "Step six. The report. Seven ingredients, your own words, your screenshots. And audit yourself with the module eight sheet before you hand in."
  - at: plan_step
    do: open
    say: "Step seven. One bite at a time. Fill your plan card, and Ari asks the question that moves you forward. Ari never writes your design. It is yours."
  - at: live
    do: open
    say: "Here is the practice block, Scenario 3 ready to run. Your move: names, not IDs. The last check stays red until you do."
stories:
  summarize the page:
    - 'You might wonder: summarize the page'
    - This week is about the final project, walked through the worked example, Scenario 3.
    - You pick one scenario and hand in a diagram, two scripts, the engaging query with its results, and a report.
    - Read the engaging query backward to find your tables.
    - Draw parents on top, create and fill them first.
    - Answer with names, not IDs, and audit yourself before you hand in.
  where do I start:
    - 'You might wonder: where do I start'
    - Pick your scenario and read its engaging query backward, from the answer to the tables.
    - Then create the parent tables only, the ones with no foreign key, and run them.
    - One bite at a time, each bite done when it runs.
  why names and not ids:
    - 'You might wonder: why names and not IDs'
    - The person asking the question reads names, not numbers.
    - A name lives in its own table, so showing it takes one more join.
    - A result full of IDs answers the database, not the person.
```
{: .avatar #guide dock="true" size="115" }

[^engaging_query]: **engaging_query** — the real question a scenario asks
    of its database. Read it first, backward: the answer it wants names
    the tables you need.

[^loading_order]: **loading_order** — the order tables are created and
    filled: parents (no foreign key) first, then their children, so no
    foreign key ever points to a row that is not there yet.
