# 🛠️ 07 · Finish the Map, Build It in Workbench

🧱 Last week you drew the top of UWM's map. This week you finish it — and build it, table by table, in MySQL Workbench.

Ask Doc for a tour!
{: .avatar_trigger target="guide" }

Welcome back! Last week UWM's messy spreadsheet became the **top of a
new map**: Departments above Courses, Majors and Instructors, with Terms
on the top row. This week we finish the **bottom** of that map —
students, sections and enrollments — and meet a new kind of
relationship on the way: **many-to-many**.

Then the pencil goes down and the mouse comes out. You build UWM's
database **in MySQL Workbench, one iteration at a time**: draw a table,
let Workbench create it, put data in, query it — then draw more, and
watch your data survive every change.

Every step ends with a little quiz, just for you. Take your time. 🙂

> Why did the student and the section start dating? They had a lot in
> common — an Enrollment. 💞

```python
@component(icon="🏛️")
class Department(Object):
    DepartmentID   = Attr(int, hint="primary key")
    DepartmentName = Attr(str)
    DepartmentCode = Attr(str)

@component(icon="🗓️")
class Term(Object):
    TermID   = Attr(int, hint="primary key")
    TermName = Attr(str)

@component(icon="📘")
class Course(Object):
    CourseID     = Attr(int, hint="primary key")
    CourseNumber = Attr(str)
    CourseTitle  = Attr(str)
    Credits      = Attr(int)
    DepartmentID = Attr("Department", hint="foreign key → Departments")

@component(icon="🎓")
class Major(Object):
    MajorID      = Attr(int, hint="primary key")
    MajorName    = Attr(str)
    DepartmentID = Attr("Department", hint="foreign key → Departments")

@component(icon="🧑‍🏫")
class Instructor(Object):
    InstructorID = Attr(int, hint="primary key")
    FirstName    = Attr(str)
    LastName     = Attr(str)
    DepartmentID = Attr("Department", hint="foreign key → Departments")

@component(icon="🧑‍🎓")
class Student(Object):
    StudentID = Attr(int, hint="primary key")
    FirstName = Attr(str)
    LastName  = Attr(str)
    MajorID   = Attr("Major", hint="foreign key → Majors")

@component(icon="🚪")
class Section(Object):
    SectionID     = Attr(int, hint="primary key")
    SectionNumber = Attr(str)
    CourseID      = Attr("Course", hint="foreign key → Courses")
    TermID        = Attr("Term", hint="foreign key → Terms")
    InstructorID  = Attr("Instructor", hint="foreign key → Instructors")

@component(icon="📝")
class Enrollment(Object):
    EnrollmentID = Attr(int, hint="primary key")
    StudentID    = Attr("Student", hint="foreign key → Students")
    SectionID    = Attr("Section", hint="foreign key → Sections")
    Grade        = Attr(str)
```
{: .model #uwm_model }

````
### 🔁 Step 1 · From week 3: ER, SQL, data — both ways

[From week 3: ER, SQL, data](_slides/m07_03.jpg)
{: .embed image="true" width="100%" }

Remember the shop in module 03? Two sentences, one diagram, two tables:

> *A Customer may place zero, one, or many Orders, and each Order is
> placed by exactly one Customer.*

The diagram, the CREATE TABLE statements and the data are **three views
of the same design**. You can travel between them in two directions:

- **Forward** — from the diagram to the database: the diagram writes
  its own CREATE TABLE statements, and the database runs them.
- **Reverse** — from an existing database back to a diagram: Workbench
  reads the tables and draws the map.

In module 03 you typed the CREATE TABLE statements by hand. This week
Workbench types them for you: you draw, it **forward engineers**.

**Q:** You drew a diagram in Workbench and want the real tables in your
database. Which direction is that?

- [ ] Sideways — the diagram slides gently into the database while nobody watches

  > Workbench has no sideways button. Diagram to database is one named
  > direction.

- [ ] Reverse — the database reads the diagram back

  > Reverse goes the other way: from a database that already exists to a
  > new diagram.

- [x] Forward — the diagram writes the CREATE TABLE statements

  > From the drawing to the database: forward engineering. Workbench
  > writes the SQL, and you can read it before it runs.
{: .quiz }
````
{: .accordion #week3 }

````
### 🗺️ Step 2 · Where we stopped: the top of the map

Last week's sketch, the top half of UWM's map:

| Row | Tables | One department… |
|---|---|---|
| 1 | Departments, Terms | — |
| 2 | Courses, Majors, Instructors | …offers many courses, hosts many majors, employs many instructors |

Every line on it is **one-to-many**: the ONE side above, the MANY side
below, the foreign key on the MANY side. Terms points to nothing, so it
sits on the top row, waiting for a table that will need it.

[The top of the map](#)
{: .diagram scope="Course,Major,Instructor,Term" states="false" }

The design guidelines still hold, word for word:

1. **Names.** Tables plural and capitalized (`Students`), columns
   singular in CamelCase (`LastName`). No underscores.
2. **Primary key.** The table's name in singular, plus ID
   (`StudentID`): INT, AUTO_INCREMENT, NOT NULL. Exactly one per table.
3. **Foreign key.** Same name as the primary key it points to.
4. **Layout.** The MANY side below the ONE side it points to.

**Q:** Why does Terms sit on the top row, with no line yet?

- [ ] Because Terms is shy and prefers to watch the other tables from a distance

  > A shy table is still a table. Its row on the map follows a rule.

- [x] It holds no foreign key — it points to no other table

  > A table that points to nothing sits on the top row. Something below
  > will point to it this week.

- [ ] It is a column of Courses that got lost on the way

  > A term has its own facts (its name, like Fall 2026), so it is a
  > table of its own.

- [ ] Because a term is longer than a department, so it goes first

  > The map's rows follow the keys, not the calendar.
{: .quiz }
````
{: .accordion #top_recap }

````
### 🔀 Step 3 · Many-to-many? Two one-to-many

Now the bottom of the map. Three new things UWM tracks:

- **Students** — each student has one major; a major has many students.
  One-to-many, the pattern you know: `MajorID` in Students.
- **Sections** — INFOST 410 is a course; *INFOST 410, section 202, Fall
  2026, taught by Codd* is a **section** of it. A course has many
  sections; a term has many sections; an instructor teaches many
  sections. Three one-to-many lines: `CourseID`, `TermID` and
  `InstructorID` in Sections.
- And the students **in** the sections…

Try the sentences:

> *A student takes many sections. A section holds many students.*

Many on **both** sides. Where does the foreign key go? A `SectionID` in
Students allows one section per student. A `StudentID` in Sections
allows one student per section. Neither works. 🤔

**The trick: a table in the middle.** Each time a student takes a
section, that is one fact — an **enrollment** — and it gets its own row:

> *A student has many enrollments; each enrollment is for one student.*
> *A section has many enrollments; each enrollment is in one section.*

One many-to-many became **two one-to-many**. Enrollments sits **below**
both Students and Sections and carries **both** foreign keys:
`StudentID` and `SectionID`. And the grade? A grade belongs to one
student in one section — neither to the student alone nor to the
section alone. It lives in the enrollment. 🎯

Have you met this before? Yes: on the dataquest map, an order holds
many products and a product appears in many orders. In the middle,
**OrderDetails**, with an `OrderID` and a `ProductID` — and the
Quantity, which belongs to neither alone. Same pattern, new topic.

The whole map, as entities:

[UWM's whole map — Enrollments at the bottom](#)
{: .diagram scope="Enrollment,Student,Section,Course,Major,Instructor,Term" states="false" }

Four rows, every key pointing up:

| Row | Tables |
|---|---|
| 1 | Departments, Terms |
| 2 | Courses, Majors, Instructors |
| 3 | Students (MajorID), Sections (CourseID, TermID, InstructorID) |
| 4 | Enrollments (StudentID, SectionID, Grade) |

**Q:** "A student takes many sections; a section holds many students."
How does the design store it?

- [ ] With a very long sticky note listing everyone, taped to the classroom door

  > It works until someone adds a class. The database needs rows, not
  > tape.

- [ ] A `SectionID` column in Students

  > Then a student could take only one section. Many-to-many needs room
  > on both sides.

- [x] A table in the middle, Enrollments, with StudentID and SectionID

  > Two one-to-many lines: one enrollment per student per section, each
  > holding both keys — like OrderDetails between Orders and Products.

- [ ] A list of StudentIDs in one cell of Sections

  > A list in one cell breaks the first rule of tables: one value per
  > cell.
{: .quiz }
````
{: .accordion #many_to_many }

````
### 🛠️ Step 4 · Workbench, iteration #1: the topmost table

Time to build. Open **MySQL Workbench**. We build UWM's database in
**iterations**: a small piece first, working end to end, then the next
piece. Iteration #1 is a single table — the **topmost** one,
Departments, because it points to nothing.

[Forward engineering, the scenario](_slides/m07_04.jpg)
{: .embed image="true" width="100%" }

**In the model:**

1. **File › New Model.** Double-click the schema `mydb` and rename it
   **uwm**.
2. **Add Diagram** (double-click it). You get an empty canvas.
3. **Add a table** (the table tool, then click the canvas). Double-click
   it, name it **Departments**.
4. **Add the columns**, following the guidelines:

| Column | Datatype | PK | NN | AI |
|---|---|---|---|---|
| DepartmentID | INT | ✓ | ✓ | ✓ |
| DepartmentName | VARCHAR(100) | | | |
| DepartmentCode | VARCHAR(10) | | | |

5. **File › Save Model** (name it `uwm.mwb`, keep it: you will open it
   again every iteration).

[Forward, in pictures](_slides/m07_08.jpg)
{: .embed image="true" width="100%" }

**Into the database:**

6. **Database › Forward Engineer…** Connect to your local instance,
   keep the defaults, and **read the SQL** Workbench shows you before
   it runs: a CREATE SCHEMA and a CREATE TABLE — the very statement you
   typed by hand in module 03.

[Forward, the schema appears](_slides/m07_09.jpg)
{: .embed image="true" width="100%" }

**Check, then fill:**

7. Open the **Local instance** tab. In the Navigator, refresh SCHEMAS:
   **uwm** is there, with its table. Run `SELECT * FROM uwm.Departments;`
   — an empty grid, with the right columns.
8. Put UWM's first rows in. Run this — the first piece of the **UWM
   sample data**:

```sql
USE uwm;

INSERT INTO Departments (DepartmentID, DepartmentName, DepartmentCode) VALUES
  (1, 'Information Studies', 'INFOST'),
  (2, 'Computer Science', 'COMPSCI'),
  (3, 'Mathematical Sciences', 'MATH');

SELECT * FROM Departments;
```

Three departments in the grid? Iteration #1 is done. 🎉 Small, but
**working end to end**: diagram, table, data, query.

**Q:** Why start with Departments, and only Departments?

- [ ] Alphabetical order — D comes early, and Workbench likes tidy lists

  > Workbench does not care about the alphabet, and neither do keys.

- [ ] Because Departments has the most columns, so it is the hardest

  > It has three columns — the opposite of hard. That is the point.

- [x] It points to nothing, so it works alone — one small piece, end to end

  > The topmost table needs no other table. One iteration, from diagram
  > to data, before anything else is added.

- [ ] A database can only hold one table per model

  > A model holds as many tables as you like. We add them one iteration
  > at a time, on purpose.
{: .quiz }
````
{: .accordion #iteration_1 }

````
### 🔄 Step 5 · Iteration #2: one more table — synchronize, nothing lost

Back to the **diagram** (the `uwm.mwb` tab). Add the next table down the
map: **Courses**.

| Column | Datatype | PK | NN | AI |
|---|---|---|---|---|
| CourseID | INT | ✓ | ✓ | ✓ |
| CourseNumber | VARCHAR(20) | | | |
| CourseTitle | VARCHAR(150) | | | |
| Credits | INT | | | |

Then the line: pick the **1:n relationship tool**, click **Courses**
first (the MANY side), then **Departments**. Workbench adds a foreign key
column to Courses — rename it **DepartmentID**, the same name as the key
it points to (Workbench proposes `Departments_DepartmentID`, which
breaks guideline 3). Save the model.

Now the database already **has** a Departments table, **with data in
it**. Forward engineering again would try to create everything from
scratch. Instead:

[Synchronize the model with the database](_slides/m07_10.jpg)
{: .embed image="true" width="100%" }

**Database › Synchronize Model…** Workbench compares the diagram with
the database, lists the differences (one new table, Courses), and shows
the SQL that brings the database up to date — and only that.

Then check both things the slide numbers:

- **#1 — the old data is still there.** `SELECT * FROM Departments;`
  still shows three rows.
- **#2 — the new table is there too.** Fill it with the next piece of
  the sample data:

```sql
USE uwm;

INSERT INTO Courses (CourseID, CourseNumber, CourseTitle, Credits, DepartmentID) VALUES
  (1, 'INFOST 110', 'Introduction to Information Science and Technology', 3, 1),
  (2, 'INFOST 120', 'Information Technology Ethics', 3, 1),
  (3, 'INFOST 240', 'Web Design I', 3, 1),
  (4, 'INFOST 270', 'Generative AI Literacy', 3, 1),
  (5, 'INFOST 410', 'Database Information Retrieval Systems', 3, 1),
  (6, 'COMPSCI 250', 'Introductory Computer Programming', 3, 2),
  (7, 'MATH 231', 'Calculus and Analytic Geometry I', 4, 3);

SELECT * FROM Courses;
```

Notice the order: departments first, courses second. A course points to
its department, so the department must exist before the course does —
the database refuses a `DepartmentID` that points nowhere. **Insert from
the top of the map down.**

**Q:** You added Courses to the diagram, and the database already holds
three departments. What do you run?

- [ ] Nothing — the database reads the diagram on its own, every night at midnight

  > Databases do not dream about diagrams. You tell them to catch up.

- [ ] Forward Engineer again, from scratch

  > That rebuilds the schema from the diagram. Synchronize changes only
  > what differs, and the rows stay.

- [ ] Reverse Engineer, so the diagram learns about Courses

  > The diagram already knows about Courses — you drew it. The database
  > is the one behind.

- [x] Synchronize Model — only the difference goes to the database

  > Workbench compares both sides and sends only what changed: here, a
  > new table. The three departments stay where they are.
{: .quiz }
````
{: .accordion #iteration_2 }

````
### 🧱 Step 6 · Iterations #3 and #4: the whole map

Same loop, twice more: **draw · save · synchronize · check · insert**.

**Iteration #3 — the rest of the top.** Add **Terms**, **Majors** and
**Instructors**, then the two 1:n lines from Departments.

| Table | Columns (the ID is always INT, PK, NN, AI) |
|---|---|
| Terms | TermID, TermName VARCHAR(20) |
| Majors | MajorID, MajorName VARCHAR(100), DepartmentID |
| Instructors | InstructorID, FirstName VARCHAR(45), LastName VARCHAR(45), DepartmentID |

Synchronize, check the departments and courses are still there, then:

```sql
USE uwm;

INSERT INTO Terms (TermID, TermName) VALUES
  (1, 'Spring 2026'),
  (2, 'Fall 2026');

INSERT INTO Majors (MajorID, MajorName, DepartmentID) VALUES
  (1, 'Information Science and Technology', 1),
  (2, 'Computer Science', 2),
  (3, 'Mathematics', 3),
  (4, 'Actuarial Science', 3);

INSERT INTO Instructors (InstructorID, FirstName, LastName, DepartmentID) VALUES
  (1, 'Edgar', 'Codd', 1),
  (2, 'Grace', 'Hopper', 2),
  (3, 'Emmy', 'Noether', 3),
  (4, 'Alan', 'Turing', 2);

```

**Iteration #4 — the bottom.** Add **Students**, **Sections** and
**Enrollments**, and their five 1:n lines: Majors → Students; Courses,
Terms and Instructors → Sections; Students and Sections → Enrollments.

| Table | Columns (the ID is always INT, PK, NN, AI) |
|---|---|
| Students | StudentID, FirstName VARCHAR(45), LastName VARCHAR(45), MajorID |
| Sections | SectionID, SectionNumber VARCHAR(10), CourseID, TermID, InstructorID |
| Enrollments | EnrollmentID, StudentID, SectionID, Grade VARCHAR(2) |

Synchronize, check, then the last piece of the sample data — top of the
map down, so Enrollments goes last:

```sql
USE uwm;

INSERT INTO Students (StudentID, FirstName, LastName, MajorID) VALUES
  (1, 'Jay', 'Rivera', 1),
  (2, 'Max', 'Nguyen', 1),
  (3, 'Miranda', 'Okafor', 2),
  (4, 'Bill', 'Kowalski', 3),
  (5, 'Ana', 'Lopez', 4),
  (6, 'Lee', 'Park', 1);

INSERT INTO Sections (SectionID, SectionNumber, CourseID, TermID, InstructorID) VALUES
  (1, '202', 5, 1, 1),
  (2, '201', 6, 1, 4),
  (3, '401', 7, 1, 3),
  (4, '202', 5, 2, 1),
  (5, '201', 3, 2, 1),
  (6, '201', 6, 2, 2),
  (7, '401', 7, 2, 3);

INSERT INTO Enrollments (EnrollmentID, StudentID, SectionID, Grade) VALUES
  (1, 1, 1, 'A'),
  (2, 2, 1, 'B'),
  (3, 3, 2, 'A'),
  (4, 4, 3, 'B'),
  (5, 1, 3, 'C'),
  (6, 1, 4, NULL),
  (7, 2, 4, NULL),
  (8, 6, 4, NULL),
  (9, 5, 7, NULL),
  (10, 3, 6, NULL),
  (11, 4, 7, NULL),
  (12, 2, 5, NULL),
  (13, 6, 5, NULL);

```

The Fall 2026 grades are `NULL`: the term is not over yet. NULL means
*no value yet* — not zero, not an F. 😅

Your diagram now shows **eight tables in four rows**, every line
pointing up. Lay it out that way in Workbench: drag the tables so the
ONE side sits above the MANY side, like the map in step 3.

**Q:** Enrollments goes in last. Why?

- [ ] Because the grades are not ready yet, and the professor needs a coffee first

  > The coffee is real, but the database has a stricter reason.

- [x] Its rows point to students and sections, which must exist first

  > Every foreign key must point to a row that is already there. The
  > bottom of the map goes in last.

- [ ] Enrollments is the biggest table, and big tables always go last

  > Size has nothing to do with it — a two-row Enrollments would still
  > go last.

- [ ] Workbench sorts the inserts by the number of columns

  > Workbench runs what you give it, in your order. The keys decide the
  > order.
{: .quiz }
````
{: .accordion #whole_map }

````
### 🔭 Step 7 · Views — and the questions UWM wants answered

A design is good when it answers the expected questions. UWM's:

1. Which students are enrolled in a given section this term?
2. What courses belong to each department?
3. What grades has a student earned across all terms?
4. Which instructors are teaching the most credits this semester?

Questions 1 and 3 both need the same long road: Enrollments → Students,
Enrollments → Sections → Courses and Terms. Typing four joins every time
is tiring — and a typo away from a wrong answer. Enter the **view**.

[Views](_slides/m07_06.jpg)
{: .embed image="true" width="100%" }

A **view** is a SELECT saved under a name. You query it like a table;
the database runs the SELECT behind it every time, so it is never out of
date. Create it once, in your uwm database:

```sql
CREATE VIEW ClassLists AS
SELECT Enrollments.EnrollmentID, Terms.TermName,
       Courses.CourseNumber, Sections.SectionNumber,
       Students.StudentID, Students.FirstName, Students.LastName,
       Enrollments.Grade
FROM Enrollments
JOIN Students ON Enrollments.StudentID = Students.StudentID
JOIN Sections ON Enrollments.SectionID = Sections.SectionID
JOIN Courses  ON Sections.CourseID = Courses.CourseID
JOIN Terms    ON Sections.TermID = Terms.TermID;
```

One row per enrollment, so the EnrollmentID comes first — our habit. In
the Navigator, it appears under **Views**, not Tables. Now the questions
get short:

```sql
-- 1. Who is in INFOST 410, section 202, this term?
SELECT * FROM ClassLists
WHERE CourseNumber = 'INFOST 410' AND SectionNumber = '202'
  AND TermName = 'Fall 2026';

-- 3. Every grade Jay has earned, all terms
SELECT * FROM ClassLists
WHERE StudentID = 1;
```

Question 2 is last week's report. Question 4 travels Sections →
Courses (for the credits) and Instructors, for one term, one row per
instructor:

```sql
SELECT Instructors.InstructorID, Instructors.LastName,
       SUM(Courses.Credits) AS TotalCredits
FROM Sections
JOIN Instructors ON Sections.InstructorID = Instructors.InstructorID
JOIN Courses     ON Sections.CourseID = Courses.CourseID
JOIN Terms       ON Sections.TermID = Terms.TermID
WHERE Terms.TermName = 'Fall 2026'
GROUP BY Instructors.InstructorID, Instructors.LastName
ORDER BY TotalCredits DESC;
```

Run them in Workbench, on your own uwm database. Then run them here, in
the practice block: same data, same answers. ✅

**Q:** What does a view store?

- [ ] A screenshot of the result, taken the day you created it

  > A screenshot would go stale the first time a student enrolls. A view
  > never does.

- [ ] A copy of every row it shows, in a hidden table

  > No copy at all — that would bring back the spreadsheet's problem of
  > facts stored twice.

- [x] A saved SELECT, run again each time you query the view

  > Only the query is saved. Every SELECT on the view reads today's rows
  > from the real tables.

- [ ] Nothing: a view is a table with a different icon in Workbench

  > It looks like a table in a query, but it holds no rows of its own.
{: .quiz }
````
{: .accordion #views }

````
### 🔎 Practice block — try every step here

The **UWM sample data** — the same rows you inserted in Workbench, all
eight tables. Small on purpose: you can check every answer with your own
eyes.

```json
[
  {"DepartmentID": 1, "DepartmentName": "Information Studies", "DepartmentCode": "INFOST"},
  {"DepartmentID": 2, "DepartmentName": "Computer Science", "DepartmentCode": "COMPSCI"},
  {"DepartmentID": 3, "DepartmentName": "Mathematical Sciences", "DepartmentCode": "MATH"}
]
```
{: .dataset #Departments }

```json
[
  {"TermID": 1, "TermName": "Spring 2026"},
  {"TermID": 2, "TermName": "Fall 2026"}
]
```
{: .dataset #Terms }

```json
[
  {"CourseID": 1, "CourseNumber": "INFOST 110", "CourseTitle": "Introduction to Information Science and Technology", "Credits": 3, "DepartmentID": 1},
  {"CourseID": 2, "CourseNumber": "INFOST 120", "CourseTitle": "Information Technology Ethics", "Credits": 3, "DepartmentID": 1},
  {"CourseID": 3, "CourseNumber": "INFOST 240", "CourseTitle": "Web Design I", "Credits": 3, "DepartmentID": 1},
  {"CourseID": 4, "CourseNumber": "INFOST 270", "CourseTitle": "Generative AI Literacy", "Credits": 3, "DepartmentID": 1},
  {"CourseID": 5, "CourseNumber": "INFOST 410", "CourseTitle": "Database Information Retrieval Systems", "Credits": 3, "DepartmentID": 1},
  {"CourseID": 6, "CourseNumber": "COMPSCI 250", "CourseTitle": "Introductory Computer Programming", "Credits": 3, "DepartmentID": 2},
  {"CourseID": 7, "CourseNumber": "MATH 231", "CourseTitle": "Calculus and Analytic Geometry I", "Credits": 4, "DepartmentID": 3}
]
```
{: .dataset #Courses }

```json
[
  {"MajorID": 1, "MajorName": "Information Science and Technology", "DepartmentID": 1},
  {"MajorID": 2, "MajorName": "Computer Science", "DepartmentID": 2},
  {"MajorID": 3, "MajorName": "Mathematics", "DepartmentID": 3},
  {"MajorID": 4, "MajorName": "Actuarial Science", "DepartmentID": 3}
]
```
{: .dataset #Majors }

```json
[
  {"InstructorID": 1, "FirstName": "Edgar", "LastName": "Codd", "DepartmentID": 1},
  {"InstructorID": 2, "FirstName": "Grace", "LastName": "Hopper", "DepartmentID": 2},
  {"InstructorID": 3, "FirstName": "Emmy", "LastName": "Noether", "DepartmentID": 3},
  {"InstructorID": 4, "FirstName": "Alan", "LastName": "Turing", "DepartmentID": 2}
]
```
{: .dataset #Instructors }

```json
[
  {"StudentID": 1, "FirstName": "Jay", "LastName": "Rivera", "MajorID": 1},
  {"StudentID": 2, "FirstName": "Max", "LastName": "Nguyen", "MajorID": 1},
  {"StudentID": 3, "FirstName": "Miranda", "LastName": "Okafor", "MajorID": 2},
  {"StudentID": 4, "FirstName": "Bill", "LastName": "Kowalski", "MajorID": 3},
  {"StudentID": 5, "FirstName": "Ana", "LastName": "Lopez", "MajorID": 4},
  {"StudentID": 6, "FirstName": "Lee", "LastName": "Park", "MajorID": 1}
]
```
{: .dataset #Students }

```json
[
  {"SectionID": 1, "SectionNumber": "202", "CourseID": 5, "TermID": 1, "InstructorID": 1},
  {"SectionID": 2, "SectionNumber": "201", "CourseID": 6, "TermID": 1, "InstructorID": 4},
  {"SectionID": 3, "SectionNumber": "401", "CourseID": 7, "TermID": 1, "InstructorID": 3},
  {"SectionID": 4, "SectionNumber": "202", "CourseID": 5, "TermID": 2, "InstructorID": 1},
  {"SectionID": 5, "SectionNumber": "201", "CourseID": 3, "TermID": 2, "InstructorID": 1},
  {"SectionID": 6, "SectionNumber": "201", "CourseID": 6, "TermID": 2, "InstructorID": 2},
  {"SectionID": 7, "SectionNumber": "401", "CourseID": 7, "TermID": 2, "InstructorID": 3}
]
```
{: .dataset #Sections }

```json
[
  {"EnrollmentID": 1, "StudentID": 1, "SectionID": 1, "Grade": "A"},
  {"EnrollmentID": 2, "StudentID": 2, "SectionID": 1, "Grade": "B"},
  {"EnrollmentID": 3, "StudentID": 3, "SectionID": 2, "Grade": "A"},
  {"EnrollmentID": 4, "StudentID": 4, "SectionID": 3, "Grade": "B"},
  {"EnrollmentID": 5, "StudentID": 1, "SectionID": 3, "Grade": "C"},
  {"EnrollmentID": 6, "StudentID": 1, "SectionID": 4, "Grade": null},
  {"EnrollmentID": 7, "StudentID": 2, "SectionID": 4, "Grade": null},
  {"EnrollmentID": 8, "StudentID": 6, "SectionID": 4, "Grade": null},
  {"EnrollmentID": 9, "StudentID": 5, "SectionID": 7, "Grade": null},
  {"EnrollmentID": 10, "StudentID": 3, "SectionID": 6, "Grade": null},
  {"EnrollmentID": 11, "StudentID": 4, "SectionID": 7, "Grade": null},
  {"EnrollmentID": 12, "StudentID": 2, "SectionID": 5, "Grade": null},
  {"EnrollmentID": 13, "StudentID": 6, "SectionID": 5, "Grade": null}
]
```
{: .dataset #Enrollments }


**① Jay's sections** — many-to-many, through the table in the middle:

```sql
SELECT Enrollments.EnrollmentID, Students.FirstName,
       Enrollments.SectionID, Enrollments.Grade
FROM Enrollments
JOIN Students ON Enrollments.StudentID = Students.StudentID
WHERE Students.FirstName = 'Jay'
```
{: .query source="Enrollments,Students" #q_jay editable="true" }

[Jay's enrollments](#)
{: .datagrid source="q_jay" rows="3" }

**② The class list** — question 1, the long road the view saves you:

```sql
SELECT Enrollments.EnrollmentID, Terms.TermName,
       Courses.CourseNumber, Sections.SectionNumber,
       Students.StudentID, Students.FirstName, Students.LastName,
       Enrollments.Grade
FROM Enrollments
JOIN Students ON Enrollments.StudentID = Students.StudentID
JOIN Sections ON Enrollments.SectionID = Sections.SectionID
JOIN Courses  ON Sections.CourseID = Courses.CourseID
JOIN Terms    ON Sections.TermID = Terms.TermID
WHERE Courses.CourseNumber = 'INFOST 410'
  AND Terms.TermName = 'Fall 2026'
```
{: .query source="Enrollments,Students,Sections,Courses,Terms" #q_class editable="true" }

[INFOST 410, Fall 2026](#)
{: .datagrid source="q_class" rows="3" }

**③ Credits per instructor** — question 4, this term:

```sql
SELECT Instructors.InstructorID, Instructors.LastName,
       SUM(Courses.Credits) AS TotalCredits
FROM Sections
JOIN Instructors ON Sections.InstructorID = Instructors.InstructorID
JOIN Courses     ON Sections.CourseID = Courses.CourseID
JOIN Terms       ON Sections.TermID = Terms.TermID
WHERE Terms.TermName = 'Fall 2026'
GROUP BY Instructors.InstructorID, Instructors.LastName
ORDER BY TotalCredits DESC
```
{: .query source="Sections,Instructors,Courses,Terms" #q_credits editable="true" }

[credits taught, Fall 2026](#)
{: .datagrid source="q_credits" rows="3" }

**✋ Your move** — the class list of **MATH 231** this term. This query
is ② again. Change the course number, keep the term, press ▶ Run.
Two students should come back.

```sql
SELECT Enrollments.EnrollmentID, Terms.TermName,
       Courses.CourseNumber, Sections.SectionNumber,
       Students.StudentID, Students.FirstName, Students.LastName,
       Enrollments.Grade
FROM Enrollments
JOIN Students ON Enrollments.StudentID = Students.StudentID
JOIN Sections ON Enrollments.SectionID = Sections.SectionID
JOIN Courses  ON Sections.CourseID = Courses.CourseID
JOIN Terms    ON Sections.TermID = Terms.TermID
WHERE Courses.CourseNumber = 'INFOST 410'
  AND Terms.TermName = 'Fall 2026'
```
{: .query source="Enrollments,Students,Sections,Courses,Terms" #q_mine editable="true" }

[your answer](#)
{: .datagrid source="q_mine" rows="3" }

The second check at the very bottom stays **red until you do it**.
````
{: .block title="🔎 Practice block" #live }

Two words to keep from this week: a `many_to_many`[^many_to_many] line
becomes two one-to-many lines through a table in the middle, and a
`view`[^view] is a SELECT saved under a name. The proof below runs the
practice block's own queries:

```gherkin
Feature: Many-to-many, through the table in the middle
  Scenario: Each enrollment is one student in one section
    Given the students, the sections and the enrollments between them
    :::python
    self.students: Dataset = Dataset("Students")
    self.sections: Dataset = Dataset("Sections")
    self.enrollments: Dataset = Dataset("Enrollments")
    self.jay: Query = self.page.q_jay
    :::
    When Jay's enrollments are joined to the student's name
    Then Jay holds three enrollments, in three different sections
    :::python
    assert self.jay.count == 3, self.jay.count
    assert len(set(self.jay.values("SectionID"))) == 3, self.jay.values("SectionID")
    assert self.enrollments.count > self.students.count, self.enrollments.count
    :::

  Scenario: The class list — INFOST 410 this term
    Given the long road from Enrollments to Terms
    :::python
    self.class_list: Query = self.page.q_class
    :::
    When the class list is filtered on INFOST 410 and Fall 2026
    Then three students come back, none graded yet
    :::python
    assert self.class_list.count == 3, self.class_list.count
    grades: list = self.class_list.values("Grade")
    assert not any(grades), grades
    :::

  Scenario: Credits per instructor — one row per instructor
    Given the sections of Fall 2026 with their courses' credits
    :::python
    self.credits: Query = self.page.q_credits
    :::
    When the credits are summed per instructor
    Then Codd comes first, with 6 credits
    :::python
    names: list[str] = self.credits.values("LastName")
    totals: list = self.credits.values("TotalCredits")
    assert names[0] == "Codd", names
    assert str(totals[0]) == "6", totals
    :::
```
{: .feature #activity_proof tags="many_to_many, view" visible="true" status="passing" }

And one check that is **yours**. It reads your query in the practice
block and stays red while it still lists INFOST 410:

```gherkin
Feature: Your move — the MATH 231 class list
  Scenario: The class list of MATH 231, this term
    Given your query in the practice block
    :::python
    self.mine: Query = self.page.q_mine
    :::
    When you press Run on your query
    Then it lists MATH 231, Fall 2026
    :::python
    flat: str = " ".join(self.mine.query.upper().split())
    assert "MATH 231" in flat, \
        "still the INFOST 410 list — change the course number to 'MATH 231', then press Run"
    assert "FALL 2026" in flat, "keep the term: Terms.TermName = 'Fall 2026'"
    :::
    And two students come back
    :::python
    assert self.mine.count == 2, self.mine.count
    :::
```
{: .feature #your_move_proof tags="many_to_many" visible="true" status="pending" celebration="true" }

[Browse](#)
{: .folder parent="true" }

```yaml
bot: doc
voice: en-US
face:
  zoom: 1.2
script:
  - say: "Welcome back! Last week you drew the top of UWM's map. This week you finish the bottom, meet many-to-many, and build the whole thing in MySQL Workbench, one iteration at a time."
  - at: week3
    do: open
    say: "Step one. A reminder from week three: a diagram, its CREATE TABLE statements and its data are three views of one design. Forward goes from diagram to database. Reverse goes back."
  - at: top_recap
    do: open
    say: "Step two. Where we stopped: Departments and Terms on the top row, Courses, Majors and Instructors below. Every line one-to-many, every key pointing up."
  - at: many_to_many
    do: open
    say: "Step three. A student takes many sections, and a section holds many students. Many on both sides. The trick is a table in the middle, Enrollments, holding both keys and the grade. It is OrderDetails all over again."
  - at: iteration_1
    do: open
    say: "Step four. Open Workbench. Iteration one is a single table, Departments, from diagram to database to data to query. Small, but working end to end."
  - at: iteration_2
    do: open
    say: "Step five. Add Courses to the diagram, then synchronize instead of starting over. Check that the departments are still there, then insert the courses. Top of the map first."
  - at: whole_map
    do: open
    say: "Step six. The same loop twice more: the rest of the top, then the bottom. Eight tables, four rows, every line pointing up. Enrollments goes in last."
  - at: views
    do: open
    say: "Step seven. A view is a SELECT saved under a name. Create the class lists view once, and the long road through five tables becomes one short query."
  - at: live
    do: open
    say: "Here is the practice block, with the same sample data as your Workbench database. Run Jay's sections, the class list and the credits per instructor. Your move: the class list of MATH 231. The last check stays red until you do."
stories:
  summarize the page:
    - 'You might wonder: summarize the page'
    - This week we finish the bottom of UWM's map and build the whole design in MySQL Workbench.
    - A many-to-many line, like students and sections, becomes two one-to-many lines through Enrollments.
    - In Workbench we build in iterations, from the topmost table down, and synchronize the model each time.
    - Synchronizing changes only what differs, so the data already in the database stays.
    - A view saves a long SELECT under a name, like the class lists.
    - The practice block holds the same sample data, and your move lists the MATH 231 class.
  why a table in the middle:
    - 'You might wonder: why a table in the middle'
    - A foreign key holds one value, so it can only draw a one-to-many line.
    - When both sides say many, neither side can hold the key.
    - A table in the middle gives each pairing its own row, with both keys.
    - Facts about the pairing, like a grade, live in that row too.
  why synchronize instead of forward engineer:
    - 'You might wonder: why synchronize instead of forward engineer'
    - Forward engineering creates the database from the diagram, from scratch.
    - Once the database holds data, you only want to send what changed.
    - Synchronize compares the diagram and the database and sends just the difference, so the rows stay.
```
{: .avatar #guide dock="true" size="115" }

[^many_to_many]: **many_to_many** — a relationship with many on both
    sides, like students and sections. It is stored as two one-to-many
    lines through a table in the middle, like `Enrollments`, which holds
    both foreign keys.
[^view]: **view** — a SELECT saved under a name, like `ClassLists`. It
    is queried like a table, and runs its SELECT again each time, so it
    never goes out of date.
