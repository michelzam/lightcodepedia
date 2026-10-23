# 🤑 09 · TILT — Transactions, Integrity, Logic, and Trust

🛢️ Until now you mostly read data. This week you change it — safely.

Ask Doc for a tour!
{: .avatar_trigger target="guide" }

Welcome back! Databases tell living stories — not just what data **is**,
but how it **changes**. Reading (SELECT) shows the present. Changing
(INSERT, UPDATE, DELETE) shapes the future. **TILT** names the four
habits that keep those changes meaningful and safe: **Transactions,
Integrity, Logic, and Trust**.

This week happens mostly in **MySQL Workbench**, on your **uwm**
database from module 07. Every step says what to run and **what you
should see**, so you can check yourself at each line. Work in order,
one step at a time.

Every step ends with a little quiz, just for you. Take your time. 🙂

> Why did the transaction break up with the database? It needed more
> commitment. 💍

````
### 🧰 Step 0 · Before you start: the same rows for everyone

Open MySQL Workbench and your **Local instance**. This week's numbers
assume your uwm database holds exactly **the UWM sample data** of module
07. If you added or changed rows since, no problem: this script puts the
sample data back. It empties the eight tables and refills them — your
tables, keys and the ClassLists view stay.

```sql
USE uwm;
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE Enrollments;
TRUNCATE TABLE Sections;
TRUNCATE TABLE Students;
TRUNCATE TABLE Instructors;
TRUNCATE TABLE Majors;
TRUNCATE TABLE Courses;
TRUNCATE TABLE Terms;
TRUNCATE TABLE Departments;
SET FOREIGN_KEY_CHECKS = 1;
INSERT INTO Departments (DepartmentID, DepartmentName, DepartmentCode) VALUES
  (1, 'Information Studies', 'INFOST'),
  (2, 'Computer Science', 'COMPSCI'),
  (3, 'Mathematical Sciences', 'MATH');
INSERT INTO Terms (TermID, TermName) VALUES
  (1, 'Spring 2026'),
  (2, 'Fall 2026');
INSERT INTO Courses (CourseID, CourseNumber, CourseTitle, Credits, DepartmentID) VALUES
  (1, 'INFOST 110', 'Introduction to Information Science and Technology', 3, 1),
  (2, 'INFOST 120', 'Information Technology Ethics', 3, 1),
  (3, 'INFOST 240', 'Web Design I', 3, 1),
  (4, 'INFOST 270', 'Generative AI Literacy', 3, 1),
  (5, 'INFOST 410', 'Database Information Retrieval Systems', 3, 1),
  (6, 'COMPSCI 250', 'Introductory Computer Programming', 3, 2),
  (7, 'MATH 231', 'Calculus and Analytic Geometry I', 4, 3);
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

SELECT COUNT(*) AS enrollments FROM Enrollments;
```

Run it all at once (⚡ the lightning bolt). **You should see:** a last
result of **13** enrollments.

**Q:** Why does the script switch FOREIGN_KEY_CHECKS off, then on again?

- [ ] To make the script run faster during the lunch break

  > Speed is not the point. Something in the script would be refused
  > otherwise.

- [x] To empty tables that other tables point to, then restore the guard

  > Emptying Departments while Courses points to it is refused. Off for
  > the cleanup, on again before any real work.

- [ ] Because foreign keys are optional in MySQL, so checking is wasted effort

  > The keys are the guard of your data — that is why the script turns
  > them back on.

- [ ] To delete the foreign keys from the model for good

  > The keys stay in the tables. Only the checking pauses, for a few
  > lines.
{: .quiz }
````
{: .accordion #setup }

````
### 🤑 Step 1 · Reading and changing — what Workbench already did for you

[INSERT, as Workbench writes it](_slides/m09_04.jpg)
{: .embed image="true" width="100%" }

You have been changing data for weeks. Each time you typed a row in the
**Result Grid** and clicked **Apply**, Workbench showed you a script —
an INSERT or an UPDATE — and ran it for you. The grid is a friendly
face; underneath, it is always SQL.

This week we write the changes ourselves, and we learn to make them
**safe**:

- 🔄 **Transactions** make change reversible.
- ⚖️ **Integrity** makes relationships reliable.
- 🧩 **Logic** makes decisions deliberate.
- 💡 Together, they build **Trust**.

**Q:** You add a row in the Result Grid and click Apply. What reaches
the database?

- [ ] A picture of the grid, which the database copies cell by cell

  > Databases do not read pictures. They read statements.

- [x] An INSERT statement that Workbench wrote and showed you first

  > The Apply dialog shows the exact INSERT before it runs. The grid is
  > a way of writing SQL.

- [ ] Nothing until the next morning, when the database syncs on its own

  > Apply runs right away. Nothing waits for the morning.

- [ ] A SELECT, since the grid is only for reading

  > The grid reads AND writes: an edit becomes an UPDATE, a new row an
  > INSERT.
{: .quiz }
````
{: .accordion #changing }

````
### 🔄 Step 2 · Transactions — all or nothing

[Transactions — making change safely](_slides/m09_05.jpg)
{: .embed image="true" width="100%" }

Imagine Ana switches her major to Mathematics **and** enrolls in Web
Design I this fall. Two changes that belong together: you want **both**
to happen — or **neither**. Half of it would leave UWM's records
telling a story that never happened.

A **transaction** groups several changes into one unit of work:

~~~sql
START TRANSACTION;   -- 🟩 begin: nothing is final from here
UPDATE ...;          -- 🟦 a change
INSERT ...;          -- 🟨 another change
COMMIT;              -- 🟩 make them all final, together
~~~

If something goes wrong before COMMIT, **ROLLBACK** cancels every change
since START TRANSACTION — as if nothing ever happened. That is
**atomicity**: all or nothing.

[ACID — the chemistry of reliability](_slides/m09_06.jpg)
{: .embed image="true" width="100%" }

Four letters, four promises, on UWM:

| | Promise | On UWM |
|---|---|---|
| **A** | Atomicity — all or nothing | Ana's new major and her new enrollment land together, or not at all |
| **C** | Consistency — from one valid state to another | No enrollment for a section that does not exist |
| **I** | Isolation — your unfinished work is invisible to others | Until you commit, a classmate's connection still sees the old rows |
| **D** | Durability — committed means kept | After COMMIT, Ana's change survives a crash or a restart |

**Q:** Between START TRANSACTION and COMMIT, the second of three changes
fails. With ROLLBACK, what stays in the database?

- [ ] The first change only, since it ran before the failure

  > That is "half of it" — exactly what a transaction prevents.
  > ROLLBACK cancels the first change too.

- [ ] The first and the third, skipping the one that failed

  > A transaction does not cherry-pick. One unit: all or nothing.

- [x] None of the three — the data is as it was before START TRANSACTION

  > Atomicity: ROLLBACK cancels everything since the transaction began.

- [ ] A note to the database administrator, apologizing for the trouble

  > Very polite, but the database keeps no apology notes.
{: .quiz }
````
{: .accordion #transactions }

````
### 🧪 Step 3 · Run it: a transaction that fails on purpose

Time to see atomicity with your own eyes, on your uwm database.

**First, the two Workbench toggles.** In the SQL editor's toolbar, switch
**off** both of these:

[The two toggles — OFF × 2](_slides/m09_toggles.jpg)
{: .embed image="true" width="100%" }

- **Continue after failed statements** — off, so a script **stops** at
  its first error instead of running on blindly.
- **Autocommit** — off, so nothing is final until you say COMMIT.
  (START TRANSACTION also pauses autocommit — the toggle makes it the
  rule for the whole tab.)

**Then run the blocks below one at a time**: select the lines of one
block with the mouse, click ⚡ (it runs only the selection), read the
result, then go to the next block. Compare each result with **You should
see**.

**① Before** — look at the rows the transaction will touch:

```sql
SELECT COUNT(*) FROM Enrollments;
SELECT StudentID, FirstName, MajorID FROM Students WHERE StudentID = 5;
```

You should see: **13** enrollments, and Ana with MajorID **4**
(Actuarial Science).

**② The transaction** — Ana switches to Mathematics (MajorID 3) and
enrolls in Web Design I this fall (section 5). The last line is the
mistake: section 99 does not exist.

```sql
START TRANSACTION;
UPDATE Students SET MajorID = 3 WHERE StudentID = 5;
INSERT INTO Enrollments (StudentID, SectionID) VALUES (5, 5);
INSERT INTO Enrollments (StudentID, SectionID) VALUES (5, 99);
```

You should see: three green checks, then a red **Error Code: 1452.
Cannot add or update a child row: a foreign key constraint fails** in
the Output panel. Integrity said no.

**③ Inside, before deciding** — the error did **not** undo anything by
itself. Look:

```sql
SELECT COUNT(*) FROM Enrollments;
SELECT StudentID, FirstName, MajorID FROM Students WHERE StudentID = 5;
```

You should see: **14** enrollments and Ana with MajorID **3**. Your
session sees its own unfinished work. Nobody else does yet — that is
isolation.

**④ Roll back** — the plan failed halfway, so cancel all of it:

```sql
ROLLBACK;
SELECT COUNT(*) FROM Enrollments;
SELECT StudentID, FirstName, MajorID FROM Students WHERE StudentID = 5;
```

You should see: **13** enrollments and Ana back at MajorID **4**. All
or nothing — here, nothing. 🎉

Leave autocommit **off** for the rest of the week, and remember what it
means: from now on, a change you want to keep needs its **COMMIT**.

**If ④ shows 14 and 3**, the changes were already committed: autocommit
was on, or START TRANSACTION was skipped. Each statement became final as
it ran, and ROLLBACK had nothing left to cancel. Run the step 0 script to
get the sample data back, switch autocommit off, and try again.

**Q:** In block ③, why does your session already see 14 enrollments?

- [ ] Because the error rolled back the bad insert and committed the rest

  > An error inside a transaction cancels only the failing statement.
  > Nothing was committed: you decide, with COMMIT or ROLLBACK.

- [x] Your session sees its own changes before they are committed

  > Until COMMIT, the new row is yours alone. Others still count 13.
  > ROLLBACK makes it vanish for you too.

- [ ] Because Workbench caches the count and shows yesterday's number

  > Workbench counts fresh every time. The 14 is real — and not final.

- [ ] Because section 99 was created automatically to save the day

  > No section appears by magic. The failed insert left no row.
{: .quiz }
````
{: .accordion #run_it }

````
### ⚖️ Step 4 · Integrity — the database says no

[Integrity — keeping data honest](_slides/m09_07.jpg)
{: .embed image="true" width="100%" }

In step 3, the database refused an enrollment for a section that does
not exist. That is **referential integrity**: the primary and foreign
keys you drew in module 07 are guards, and the database checks them on
every change.

Try three more refusals, one block at a time (each one fails, and
changes nothing):

```sql
-- a) delete a major that a student still points to
DELETE FROM Majors WHERE MajorID = 4;
```

You should see: **Error Code: 1451. Cannot delete or update a parent
row**. Ana still points to major 4.

```sql
-- b) a second student with an existing StudentID
INSERT INTO Students (StudentID, FirstName, LastName, MajorID)
VALUES (1, 'Jo', 'Doe', 1);
```

You should see: **Error Code: 1062. Duplicate entry '1' for key …PRIMARY**.
A primary key never repeats.

```sql
-- c) a student in a major that does not exist
INSERT INTO Students (FirstName, LastName, MajorID)
VALUES ('Jo', 'Doe', 42);
```

You should see: **Error Code: 1452** again — a child row pointing to a
missing parent.

A student can exist without an enrollment, but an enrollment cannot
exist without its student. A major can lose its last student, but not
the other way around.

**Q:** Why is `DELETE FROM Majors WHERE MajorID = 4` refused?

- [ ] Actuarial Science is a protected major, by order of the dean

  > No dean was consulted. The keys decide.

- [x] A student row still points to major 4 through its MajorID

  > Deleting the parent would leave Ana pointing to nothing. Integrity
  > refuses.

- [ ] DELETE is forbidden in MySQL unless autocommit is on

  > DELETE works in both modes. This one breaks a key.

- [ ] Majors has no primary key, so no row can be found

  > MajorID is its primary key. The row is found — and protected.
{: .quiz }
````
{: .accordion #integrity }

````
### 🧩 Step 5 · Logic — look first, act second

[Logic — thinking before changing](_slides/m09_08.jpg)
{: .embed image="true" width="100%" }

Before a risky UPDATE or DELETE, run a **SELECT with the same WHERE**.
It shows exactly the rows the change will touch. Look first, act second.

~~~sql
-- the change you plan:
UPDATE Students SET MajorID = 1 WHERE MajorID = 2;
-- look first, with the same WHERE:
SELECT * FROM Students WHERE MajorID = 2;
~~~

One row — Miranda. Now you know what the UPDATE will do, before it does
it.

And the classic accident: an UPDATE or DELETE **without a WHERE** touches
**every row**. `SELECT * FROM Students` shows what
`UPDATE Students SET MajorID = 1` would change: all six students. 😱

You can practice the look-first habit right here, in the practice block
below: these are SELECTs, so nothing can break.

**Q:** You plan `DELETE FROM Enrollments WHERE SectionID = 5`. What do
you run first?

- [ ] The DELETE twice, just to be sure it really worked

  > The second run would find nothing to delete — and the first may
  > already have deleted too much.

- [ ] `SELECT * FROM Enrollments` — all of them, to be safe

  > That shows every row, not the ones the DELETE will hit. Use the same
  > WHERE.

- [x] `SELECT * FROM Enrollments WHERE SectionID = 5`

  > The same WHERE, as a SELECT: exactly the rows the DELETE will
  > remove.

- [ ] `ROLLBACK`, in case the DELETE goes wrong later

  > ROLLBACK cancels what already happened in a transaction. Looking
  > first prevents the mistake.
{: .quiz }
````
{: .accordion #logic }

````
### 💡 Step 6 · Trust — what it all builds toward

Each layer of TILT reinforces the next:

- 🔄 **Transactions** make change reversible.
- ⚖️ **Integrity** makes relationships reliable.
- 🧩 **Logic** makes decisions deliberate.
- 💡 Together, they build **Trust** — in your data, and in yourself as
  its caretaker.

Your database becomes more than storage: a system that honors what is
true, even while it changes.

**Your routine for any change**, from now on, in your project too:

1. **Look** — SELECT with the WHERE you plan to use.
2. **Begin** — START TRANSACTION.
3. **Change** — the INSERTs, UPDATEs, DELETEs.
4. **Check** — SELECT again: is it what you meant?
5. **Decide** — COMMIT if yes, ROLLBACK if not.

**Q:** In that routine, when is the change final?

- [ ] As soon as the UPDATE line shows a green check

  > Green means it ran — inside the transaction, not yet for good.

- [ ] When you close Workbench for the day

  > Closing an open transaction does the opposite: unfinished work is
  > rolled back.

- [x] At COMMIT, after you checked the result

  > COMMIT is the decision. Before it, ROLLBACK can still cancel
  > everything.

- [ ] Never — a transaction can always be undone later

  > After COMMIT, durability takes over: the change is kept.
{: .quiz }
````
{: .accordion #trust }

````
### 🔎 Practice block — look first, here

The UWM sample data you just reset — students, majors, enrollments.
These are SELECTs: look as much as you like, nothing changes.

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
  {"MajorID": 1, "MajorName": "Information Science and Technology", "DepartmentID": 1},
  {"MajorID": 2, "MajorName": "Computer Science", "DepartmentID": 2},
  {"MajorID": 3, "MajorName": "Mathematics", "DepartmentID": 3},
  {"MajorID": 4, "MajorName": "Actuarial Science", "DepartmentID": 3}
]
```
{: .dataset #Majors }

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


**① Look first** — the rows `UPDATE Students SET MajorID = 1 WHERE
MajorID = 2` would change:

```sql
SELECT * FROM Students
WHERE Students.MajorID = 2
```
{: .query source="Students" #q_look editable="true" }

[the rows the UPDATE would touch](#)
{: .datagrid source="q_look" rows="1" }

**② The forgotten WHERE** — the rows `UPDATE Students SET MajorID = 1`
would change, without a WHERE:

```sql
SELECT * FROM Students
```
{: .query source="Students" #q_all editable="true" }

[every student](#)
{: .datagrid source="q_all" rows="6" }

**✋ Your move** — you plan
`UPDATE Enrollments SET Grade = 'B' WHERE SectionID = 5`. Change this
query so it shows **exactly the rows that UPDATE would touch**, then
press ▶ Run. Two enrollments should come back.

```sql
SELECT * FROM Enrollments
```
{: .query source="Enrollments" #q_mine editable="true" }

[your answer](#)
{: .datagrid source="q_mine" rows="3" }

The second check at the very bottom stays **red until you do it**.
````
{: .block title="🔎 Practice block" #live }

Three ideas to keep from this week: a transaction is all or nothing,
integrity lets the keys refuse what makes no sense, and
`look_first`[^look_first] runs the WHERE as a SELECT before any change. The proof below runs the practice block's own
queries:

```gherkin
Feature: Look first, act second
  Scenario: The same WHERE shows the rows a change will touch
    Given the students and the look-first query
    :::python
    self.students: Dataset = Dataset("Students")
    self.look: Query = self.page.q_look
    :::
    When the WHERE of the planned UPDATE runs as a SELECT
    Then one student comes back, Miranda
    :::python
    assert self.look.count == 1, self.look.count
    assert self.look.values("FirstName") == ["Miranda"], self.look.values("FirstName")
    :::

  Scenario: Without a WHERE, every row is touched
    Given the students and the query with no WHERE
    :::python
    self.students: Dataset = Dataset("Students")
    self.all: Query = self.page.q_all
    :::
    When the planned UPDATE forgets its WHERE
    Then all six students would change
    :::python
    assert self.all.count == self.students.count == 6, self.all.count
    :::
```
{: .feature #activity_proof tags="look_first" visible="true" status="passing" }

And one check that is **yours**. It reads your query in the practice
block and stays red while it still shows every enrollment:

```gherkin
Feature: Your move — look before the UPDATE
  Scenario: The rows of section 5, and only those
    Given your query in the practice block
    :::python
    self.mine: Query = self.page.q_mine
    :::
    When you press Run on your query
    Then it uses the UPDATE's own WHERE
    :::python
    flat: str = " ".join(self.mine.query.upper().split())
    assert "WHERE" in flat and "SECTIONID" in flat.split("WHERE")[-1], \
        "add the UPDATE's WHERE: WHERE Enrollments.SectionID = 5, then press Run"
    :::
    And two enrollments come back, both in section 5
    :::python
    assert self.mine.count == 2, self.mine.count
    assert {str(s) for s in self.mine.values("SectionID")} == {"5"}, self.mine.values("SectionID")
    :::
```
{: .feature #your_move_proof tags="look_first" visible="true" status="pending" celebration="true" }

[Browse](#)
{: .folder parent="true" }

```yaml
bot: doc
voice: en-US
face:
  zoom: 1.2
script:
  - say: "Welcome back! Until now you mostly read data. This week you change it, safely. TILT: transactions, integrity, logic, and trust. Most of it happens in Workbench, and every step tells you what you should see."
  - at: setup
    do: open
    say: "Step zero. One script puts the UWM sample data back, so your numbers match the page. Run it all at once. You should see thirteen enrollments."
  - at: changing
    do: open
    say: "Step one. Every time you clicked Apply in the grid, Workbench wrote an INSERT or an UPDATE for you. This week you write the changes yourself, and make them safe."
  - at: transactions
    do: open
    say: "Step two. A transaction groups changes into one unit: all or nothing. COMMIT makes them final together. ROLLBACK cancels them all."
  - at: run_it
    do: open
    say: "Step three. Switch off the two toggles, then run the blocks one at a time. The last insert fails on purpose. Look inside, then roll back. Thirteen enrollments, and Ana back on her old major."
  - at: integrity
    do: open
    say: "Step four. The keys you drew are guards. A missing parent, a parent still in use, a repeated key: three refusals, three error codes."
  - at: logic
    do: open
    say: "Step five. Look first, act second. Run the WHERE of your change as a SELECT, and see exactly what it will touch. And never forget the WHERE."
  - at: trust
    do: open
    say: "Step six. Trust is what the other three build. Your routine from now on: look, begin, change, check, decide."
  - at: live
    do: open
    say: "Here is the practice block. Look first, then see what a forgotten WHERE would touch. Your move: show exactly the rows of section five. The last check stays red until you do."
stories:
  summarize the page:
    - 'You might wonder: summarize the page'
    - This week is about changing data safely, with four habits called TILT.
    - Transactions group changes so they happen all together or not at all.
    - Integrity lets the keys refuse changes that make no sense.
    - Logic means running the WHERE as a SELECT before any change.
    - Trust is what the three build, in your data and in yourself.
  why did the error not undo everything:
    - 'You might wonder: why did the error not undo everything'
    - Inside a transaction, an error cancels only the statement that failed.
    - The earlier changes wait, unfinished, until you decide.
    - COMMIT keeps them, ROLLBACK cancels them all.
  why does rollback do nothing:
    - 'You might wonder: why does rollback do nothing'
    - ROLLBACK only cancels changes that are not committed yet.
    - With autocommit on and no START TRANSACTION, each statement is final as it runs.
    - Run the step zero script, switch autocommit off, and try again.
```
{: .avatar #guide dock="true" size="115" }

[^look_first]: **look_first** — running the WHERE of a planned UPDATE or
    DELETE as a SELECT, to see exactly which rows it will touch.
