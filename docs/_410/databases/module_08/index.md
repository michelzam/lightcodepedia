# 👀 08 · From Designer to Auditor

🔍 You built UWM's database. This week you learn to judge one — yours first.

Ask Doc for a tour!
{: .avatar_trigger target="guide" }

Welcome back! Your uwm database stands: eight tables, keys, data, a view.
This week has two sides. First, **security**: a database worth building is
a database worth protecting, and one tiny query shows why. Then you
**switch roles**: from designer to **auditor**. An auditor reads a model
with a checklist in hand and counts what breaks the rules — kindly,
precisely, one table at a time.

The checklist you meet today is the one we recommend for **your project**:
audit your own model with it before anyone else does.

Every step ends with a little quiz, just for you. Take your time. 🙂

> An auditor walks into a database. "Nice tables," says the auditor. "Now show me
> your keys." 🔑

````
### 🔐 Step 1 · Security, in one query

[Common security threats](_slides/m08_03.jpg)
{: .embed image="true" width="100%" }

This week's lesson on security names the three goals — **confidentiality,
integrity, availability** — and the usual threats. One of them you can
try right here, harmlessly: **SQL injection**.

A login page asks for your user ID and glues it into a query:

~~~text
txtUserId = getRequestString("UserId");
txtSQL = "SELECT * FROM Users WHERE UserId = " + txtUserId;
~~~

Type `105`, and the query reads `... WHERE UserId = 105`: one user.
Type `105 OR 1=1`, and it reads `... WHERE UserId = 105 OR 1=1`. Since
`1=1` is always true, **every user** comes back. The input was meant to
be a *value*; it became *code*.

👉 Run **①** and **②** in the practice block and compare.

The cure is to never glue input into SQL: a **parameterized query**
(a prepared statement) sends the input as a value, so `105 OR 1=1` is
just an odd ID that matches nobody. Add **least privilege** — each user
gets only the rights their job needs — and the damage of any mistake
shrinks.

**Q:** Why does `105 OR 1=1` return every user?

- [ ] Because the database feels generous on Fridays and shares everything

  > Databases have no moods — only conditions. Look at the WHERE.

- [x] The OR makes the WHERE true for every row, since 1=1 always holds

  > Each row passes if its ID is 105 OR if 1 equals 1 — and 1 always
  > equals 1. The filter has been switched off.

- [ ] User 105 is an administrator, so the database shows all users

  > The ID does not matter. Try `999 OR 1=1`: still every user.

- [ ] The query crashes, and a crashing query shows the whole table

  > No crash at all — that is what makes it dangerous. The query runs
  > exactly as written.
{: .quiz }
````
{: .accordion #security }

````
### 🎯 Step 2 · From designer to auditor

[Auditing a DB model](_slides/m08_06.jpg)
{: .embed image="true" width="100%" }

You designed UWM's database. Now look at a design the way a reviewer
does: from the **outside in**. An auditor does not ask "does it work on
my laptop?" but "does it follow the rules, and does it answer the
questions?"

**No AI, only NI — Natural Intelligence.** An audit is a judgment you
make with your own eyes, rule by rule. That is the skill.

The audit sheet has two halves:

- **Design quality — doing the thing RIGHT.** Five sections: naming,
  relationships, primary keys, foreign keys, normalization. For each
  table and each criterion, you write the **number of violations**.
  **0 is the best score.**
- **Coverage and usefulness — doing the RIGHT thing.** For each table:
  does it serve the pitch, how many of the expected queries use it, how
  many tables point to it? Here you count **uses**. **The higher, the
  better.**

One column per table, **T1 to T10**, top of the map first: T1 is a table
with no foreign key, like Departments.

**Q:** On the design-quality half, a table scores 0 everywhere. What
does that mean?

- [ ] Nobody looked at it yet — a zero is an empty box

  > An empty box is empty. A 0 is written on purpose, after checking.

- [ ] The table is useless: zero points, zero value

  > That reading belongs to the other half, where uses are counted. Here
  > the count is of violations.

- [x] No rule is broken: 0 violations is the best possible score

  > On this half you count what is wrong. Zero wrong is perfect.

- [ ] The table forgot to bring its homework

  > Tables never bring homework. A zero here is good news.
{: .quiz }
````
{: .accordion #auditor }

````
### 🗂️ Step 3 · The audit sheet

[ER Model Design Audit — the outside-in evaluation sheet](_slides/m08_08.jpg)
{: .embed image="true" width="100%" }

The sheet, row by row. Each row names **what to check**; the next steps
show it on examples.

| Section | Criterion | What to check |
|---|---|---|
| 1 · Naming & style | Table & column naming | Tables plural and capitalized (`Students`); columns singular, CamelCase (`FirstName`, `StudentID`); no underscores |
| | Clarity & consistency | Names short, meaningful, the same in the diagram and in the SQL |
| 2 · Relationships & cardinality | Relationship integrity | Every line is 1 : N; a many-to-many goes through a table in the middle |
| | Diagram layout & hierarchy | The N side (with the FK) below its 1 side; the layout reads top-down |
| 3 · Primary keys | PK naming & type | Singular + ID (`StudentID`); INT, AUTO_INCREMENT, NOT NULL |
| | PK existence & uniqueness | Exactly one PK per table; unique and stable values |
| 4 · Foreign keys | FK naming & type | INT, same name as the PK it points to (`CustomerID` → `CustomerID`) |
| | Relationship direction | The FK points up to its parent, matching the 1 : N of the diagram |
| 5 · Normalization | 1NF — atomic values | One value per cell: no lists, no groups |
| | 2NF — whole-key dependency | Every non-key column depends on the entire key |
| | 3NF — no redundancy | No repeated facts, no derived data; non-key columns independent of each other |
| Coverage | Covers requirements | The table serves at least one need stated in the pitch |
| | Helps queries | How many of the expected queries use the table |
| | Referenced by other tables | How many tables point to it (it is their parent) |

You know most of these rules already: you used them in modules 06 and
07. The sheet only puts them **in one place**, so nothing is forgotten.

**Q:** In which half does "how many tables point to it" belong?

- [ ] Design quality — a table pointed to by many tables breaks a rule

  > Being pointed to is not a fault: Departments is pointed to by three
  > tables, and that is good design.

- [x] Coverage and usefulness — the higher the count, the better

  > A table many others rely on is a useful parent. Counted as uses, the
  > higher the better.

- [ ] Neither — the sheet ignores who points to whom

  > The last row of the sheet counts exactly that.

- [ ] Both halves, so the table gets punished and rewarded at once

  > One fact, one row — like in a good database.
{: .quiz }
````
{: .accordion #sheet }

````
### 🔤 Step 4 · Audit by example: names and keys

Sections 1, 3 and 4 are about **names and keys**. Here is a table from
an imaginary first draft, the way a classmate might hand it in:

~~~sql
CREATE TABLE instructor (
  id              INT AUTO_INCREMENT NOT NULL,
  First_Name      VARCHAR(45),
  LastName        VARCHAR(45),
  Department      VARCHAR(100),
  PRIMARY KEY (id)
);
~~~

Read it with the sheet:

| What you see | Criterion | Violations |
|---|---|---|
| `instructor` — singular, lowercase | Table & column naming | 1 |
| `First_Name` — an underscore | Table & column naming | 1 |
| `id` — not the table's name in singular + ID | PK naming & type | 1 |
| `Department` holds the department's **name**, as text | FK naming & type | 1 |

The fix: `Instructors`, `FirstName`, `InstructorID`, and a
`DepartmentID INT` that points to `Departments.DepartmentID`. The audit
does not rewrite the table — it **counts** and **notes**; the designer
fixes.

**Q:** In a draft, `Sections.Course` holds the course title as text.
Which criterion does it break?

- [ ] Diagram layout — the column sits too far right in the table

  > Columns have no seats. The problem is what the column holds.

- [ ] PK existence — Sections has no primary key

  > Nothing says Sections lacks its SectionID. The problem is the link
  > to Courses.

- [x] FK naming & type — the link should be `CourseID`, an INT

  > A link to another table is a foreign key: an INT named exactly like
  > the key it points to.

- [ ] 1NF — a course title is not atomic

  > A title is one value in one cell: atomic enough. The trouble is that
  > it replaces a key.
{: .quiz }
````
{: .accordion #names_keys }

````
### 🔗 Step 5 · Audit by example: lines and layout

Section 2 checks the **lines** of the diagram and how it **reads**.

- **Relationship integrity.** A draft draws a line straight from
  Students to Sections, "many to many". Violation: a many-to-many must
  go through a table in the middle — Enrollments. ❌
- **Diagram layout.** A draft puts Enrollments at the top and Departments
  at the bottom. The keys are right, but the eye reads it upside down.
  Violation: the N side goes **below** its 1 side. ❌
- **Relationship direction** (section 4). A draft stores a `CourseID` in
  Departments. One department, many courses — so the key belongs in
  Courses, pointing **up**. ❌

Your module 07 map passes all three: every line is 1 : N, Enrollments
sits at the bottom, every key points up. ✅

**Q:** A draft lays Students out **below** Enrollments, with the
StudentID in Enrollments. How many layout violations?

- [ ] Zero — any picture is fine as long as the SQL runs

  > The SQL may run, but the sheet audits the diagram too: it must read
  > top-down.

- [x] One — Enrollments (the N side) should sit below Students

  > The keys are right; the drawing is upside down. One layout
  > violation, easy to fix by dragging.

- [ ] Two — one for Students and one for Enrollments

  > One misplaced line, one violation. Count the fault, not the tables
  > it touches.

- [ ] Ten — and a stern email to the designer

  > Stern emails are not on the sheet. Kind, precise counts are.
{: .quiz }
````
{: .accordion #lines_layout }

````
### 🧼 Step 6 · Audit by example: normalization

Section 5 asks whether each fact lives in **one place**. Three levels,
three examples:

**1NF — atomic values.** One value per cell.

| StudentID | FirstName | Courses |
|---|---|---|
| 1 | Jay | INFOST 410, MATH 231 |

❌ A list in one cell. Who takes MATH 231? You would have to search
inside text. The fix you know: Enrollments, one row per pairing.

**2NF — the whole key.** It matters when a key has **two parts**.
Imagine Enrollments keyed by (StudentID, SectionID), with a column
`StudentLastName`:

| StudentID | SectionID | StudentLastName | Grade |
|---|---|---|---|
| 1 | 1 | Rivera | A |
| 1 | 3 | Rivera | C |

❌ The last name depends on StudentID alone — **part** of the key — so
it repeats on every enrollment of that student. It belongs in Students.
The grade depends on **both** parts: it stays. ✅

**3NF — no redundancy.** No repeated facts, no derived data.

| CourseID | CourseNumber | DepartmentID | DepartmentName |
|---|---|---|---|
| 5 | INFOST 410 | 1 | Information Studies |

❌ The name depends on DepartmentID, not on the course: module 06's
spreadsheet problem, back in disguise. Same for **derived data**: a
`StudentCount` column in Sections can be computed with COUNT, so storing
it invites the day it disagrees with the real count.

**Q:** Sections carries a `CourseCredits` column, copied from Courses.
Which level does it break?

- [ ] 1NF — the number of credits is not atomic

  > 3 is about as atomic as it gets. The trouble is where it lives.

- [ ] None — copying data makes queries faster, so it is encouraged

  > Faster to read, slower to keep right: change the credits of a course
  > and every copy must follow.

- [ ] 2NF — the key of Sections has two parts

  > SectionID is a single key. The problem is a fact stored twice.

- [x] 3NF — the credits describe the course, already stored in Courses

  > A repeated fact. The credits live in Courses; a section reaches them
  > through its CourseID.
{: .quiz }
````
{: .accordion #normalization }

````
### 📈 Step 7 · Coverage and usefulness — and your project

The second half of the sheet counts **uses**, the higher the better.
Take UWM's model from module 07 and its expected questions:

1. Which students are enrolled in a given section this term?
2. What courses belong to each department?
3. What grades has a student earned across all terms?
4. Which instructors are teaching the most credits this semester?

| Table | Helps queries (out of 4) | Referenced by |
|---|---|---|
| Departments | 1 (question 2) | 3 — Courses, Majors, Instructors |
| Courses | 4 | 1 — Sections |
| Sections | 3 (questions 1, 3, 4) | 1 — Enrollments |
| Majors | 0 | 1 — Students |

Majors helps none of the four questions — yet it covers a need stated
in the pitch (UWM tracks majors), and Students points to it. A low count
is a **question**, not a verdict: is a fifth query missing, one that
needs majors? That is exactly the "Q5: your suggestion" of the pitch.

**For your project — the audit we recommend.** Before you hand in your
model, audit it yourself with this sheet:

1. One column per table, top of the map first (T1 has no foreign key).
2. Every design-quality row: the number of violations. Aim for 0.
3. Every coverage row: the number of uses. A table at 0 everywhere
   needs a reason to exist.
4. Then fix, and audit again. Your final model should score 0 on the
   whole first half.

**Q:** In your project audit, a table scores 0 on every coverage row.
What do you do?

- [ ] Celebrate: 0 is the best score on every row of the sheet

  > On the coverage half, 0 means nobody uses it. The best score there is
  > a high one.

- [ ] Rename it, so the auditor stops noticing it

  > A new name changes nothing about its uses — and breaks the
  > consistency rule on the way.

- [ ] Nothing: unused tables never cost anything

  > Every table must be created, filled, kept right. Unused, it costs
  > without serving.

- [x] Ask what need it serves: add the query that uses it, or drop it

  > A table must earn its place: by a requirement and the queries that
  > use it. Find its query, or let it go.
{: .quiz }
````
{: .accordion #coverage }

````
### 🔎 Practice block — try it here

A small Users table, for the injection in step 1. Fictional people,
harmless data:

```json
[
  {"UserID": 101, "UserName": "jay.rivera", "Role": "student"},
  {"UserID": 102, "UserName": "max.nguyen", "Role": "student"},
  {"UserID": 103, "UserName": "miranda.okafor", "Role": "student"},
  {"UserID": 104, "UserName": "bill.kowalski", "Role": "student"},
  {"UserID": 105, "UserName": "ana.lopez", "Role": "student"},
  {"UserID": 106, "UserName": "edgar.codd", "Role": "instructor"},
  {"UserID": 107, "UserName": "registrar", "Role": "admin"}
]
```
{: .dataset #Users }

**① The honest input** — `105`:

```sql
SELECT * FROM Users
WHERE Users.UserID = 105
```
{: .query source="Users" #q_honest editable="true" }

[one user](#)
{: .datagrid source="q_honest" rows="1" }

**② The injected input** — `105 OR 1=1`, glued into the same query:

```sql
SELECT * FROM Users
WHERE Users.UserID = 105 OR 1=1
```
{: .query source="Users" #q_injected editable="true" }

[every user](#)
{: .datagrid source="q_injected" rows="7" }

**✋ Your move** — be the prepared statement. This query still carries
the injected text. Make it return **only user 105** again, the way a
parameterized query would treat the input as a plain value. Press ▶ Run.

```sql
SELECT * FROM Users
WHERE Users.UserID = 105 OR 1=1
```
{: .query source="Users" #q_mine editable="true" }

[your answer](#)
{: .datagrid source="q_mine" rows="7" }

The second check at the very bottom stays **red until you do it**.
````
{: .block title="🔎 Practice block" #live }

Two words to keep from this week: an `sql_injection`[^sql_injection]
turns an input into code. And an audit counts violations rule by rule,
then counts uses. The proof below runs the practice
block's own queries:

```gherkin
Feature: One input, two queries
  Scenario: The honest input finds one user
    Given the users and the honest query
    :::python
    self.users: Dataset = Dataset("Users")
    self.honest: Query = self.page.q_honest
    :::
    When the input is 105
    Then exactly one user comes back
    :::python
    assert self.honest.count == 1, self.honest.count
    :::

  Scenario: The injected input switches the filter off
    Given the users and the injected query
    :::python
    self.users: Dataset = Dataset("Users")
    self.injected: Query = self.page.q_injected
    :::
    When the input is 105 OR 1=1
    Then every user comes back, the admin included
    :::python
    assert self.injected.count == self.users.count, self.injected.count
    assert "admin" in self.injected.values("Role"), self.injected.values("Role")
    :::
```
{: .feature #activity_proof tags="sql_injection" visible="true" status="passing" }

And one check that is **yours**. It reads your query in the practice
block and stays red while the injection is still in it:

```gherkin
Feature: Your move — the input is a value
  Scenario: Only user 105 comes back
    Given your query in the practice block
    :::python
    self.mine: Query = self.page.q_mine
    :::
    When you press Run on your query
    Then the injected OR is gone
    :::python
    flat: str = " ".join(self.mine.query.upper().split())
    assert " OR " not in flat, \
        "the OR 1=1 is still there — a value cannot carry code: keep WHERE Users.UserID = 105, then press Run"
    :::
    And one user comes back, number 105
    :::python
    assert self.mine.count == 1, self.mine.count
    assert str(self.mine.values("UserID")[0]) == "105", self.mine.values("UserID")
    :::
```
{: .feature #your_move_proof tags="sql_injection" visible="true" status="pending" celebration="true" }

[Browse](#)
{: .folder parent="true" }

```yaml
bot: doc
voice: en-US
face:
  zoom: 1.2
script:
  - say: "Welcome back! Your UWM database stands. This week, two sides: one query that shows why security matters, then a new role. From designer to auditor."
  - at: security
    do: open
    say: "Step one. A login page glues your input into a query. Type 105, you get one user. Type 105 OR 1 equals 1, you get them all. The input became code. Parameterized queries keep it a value."
  - at: auditor
    do: open
    say: "Step two. An auditor reads a model from the outside in, with a checklist and natural intelligence. On one half, count violations: zero is best. On the other, count uses: higher is better."
  - at: sheet
    do: open
    say: "Step three. The audit sheet, row by row: naming, relationships, primary keys, foreign keys, normalization, and coverage. Rules you already used, now in one place."
  - at: names_keys
    do: open
    say: "Step four. Names and keys, on a real draft. A singular lowercase table, an underscore, a key called id, a department typed as text. Four violations, counted, not rewritten."
  - at: lines_layout
    do: open
    say: "Step five. Lines and layout. Many to many goes through a table in the middle, the many side sits below, and every key points up."
  - at: normalization
    do: open
    say: "Step six. Normalization. One value per cell, every column depends on the whole key, and no fact stored twice, not even a derived one."
  - at: coverage
    do: open
    say: "Step seven. Coverage and usefulness: count the queries a table helps and the tables that point to it. Then the audit we recommend for your project: audit yourself, fix, audit again."
  - at: live
    do: open
    say: "Here is the practice block. Run the honest input and the injected one. Your move: be the prepared statement, and bring back user 105 alone. The last check stays red until you do."
stories:
  summarize the page:
    - 'You might wonder: summarize the page'
    - This week starts with security, with one query that shows SQL injection.
    - Then you switch roles, from designer to auditor.
    - The audit sheet counts violations of naming, relationship, key and normalization rules, where zero is best.
    - It also counts how much each table is used, where higher is better.
    - The same sheet is the audit we recommend for your project, on your own model first.
  why does 1=1 matter:
    - 'You might wonder: why does 1=1 matter'
    - When input is glued into a query, the input can carry SQL.
    - OR 1=1 makes the WHERE true for every row, so the filter is switched off.
    - A parameterized query sends the input as a value, so it can never become code.
  why count violations and not points:
    - 'You might wonder: why count violations and not points'
    - A count of violations says exactly what to fix, and where.
    - Zero on the whole design-quality half means the model follows every rule.
    - The coverage half counts uses instead, so there a higher number is better.
```
{: .avatar #guide dock="true" size="115" }

[^sql_injection]: **sql_injection** — an attack where input glued into
    a query becomes SQL, like `105 OR 1=1`. Parameterized queries send
    the input as a value, so it can never become code.
