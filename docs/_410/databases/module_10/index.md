# 🧙 10 · Advanced SQL — Procedures, Cursors, and Triggers

⚡ Until now you told the database what to do, line by line. This week the database learns to act on its own.

Ask Doc for a tour!
{: .avatar_trigger target="guide" }

Welcome back! So far, every change in your database happened because
**you** typed it. This week the logic moves **inside** the database:

- a **stored procedure** — a routine you save once and **call** by name;
- a **cursor** — a way to walk through rows **one at a time**;
- a **trigger** — logic the database runs **by itself** when data changes.

Procedures and cursors you meet **on paper** this week: read them,
understand them, no need to run them. The **trigger** is the one you
build — in **MySQL Workbench**, on a small database of its own,
**coursedb**: two tables, made for experiments. Your **uwm** and
**shopdb** stay untouched. Every hands-on step says what to run and
**what you should see**, so you can check yourself at each line.

Every step ends with a little quiz, just for you. Take your time. 🙂

> Why did the trigger never get invited to parties? Every time something
> changed, it reacted. ⚡

````
### 🧰 Step 0 · Before you start: coursedb and two settings

Open MySQL Workbench and your **Local instance**. First, the **Query**
menu — two checkmarks, like last week, but one has changed:

- **Stop Script Execution on Errors** — **checked** ✓.
- **Auto-Commit Transactions** — **checked** ✓ this week. We are not
  rolling anything back today: each change should be kept as soon as it
  runs.

Then build **coursedb**: two courses, and three course **resources**
(guidelines, cheat sheets…) that will soon track their own versions.

```sql
CREATE DATABASE IF NOT EXISTS coursedb;
USE coursedb;
DROP TABLE IF EXISTS Resources;
DROP TABLE IF EXISTS Courses;

CREATE TABLE Courses (
  CourseID     INT NOT NULL AUTO_INCREMENT,
  CourseNumber VARCHAR(20),
  CourseTitle  VARCHAR(100),
  PRIMARY KEY (CourseID)
);

CREATE TABLE Resources (
  ResourceID  INT NOT NULL AUTO_INCREMENT,
  CourseID    INT NOT NULL,
  Title       VARCHAR(100),
  Description TEXT,
  Version     INT DEFAULT 1,
  LastUpdated DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (ResourceID),
  FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
);

INSERT INTO Courses (CourseNumber, CourseTitle) VALUES
  ('INFOST 350', 'Intro to Application Development'),
  ('INFOST 410', 'Database Information Retrieval Systems');

INSERT INTO Resources (CourseID, Title, Description) VALUES
  (2, 'Project Guidelines', 'Initial draft for Module 6'),
  (2, 'Query Cheat Sheet', 'SELECT, JOIN, GROUP BY'),
  (1, 'Python Setup', 'Install and first run');

SELECT ResourceID, CourseID, Title, Version FROM Resources;
```

Run it all at once (⚡). **You should see:** **3** resources, each at
**Version 1**, and **coursedb** in the Navigator's SCHEMAS (🔄 to
refresh). Lost at any point this week? Run this script again, then redo
the steps from step 3: it rebuilds coursedb from scratch — and only
coursedb.

**Q:** Why does this script start with `DROP TABLE IF EXISTS Resources`?

- [ ] To make the database lighter, since empty databases run faster

  > Speed is not the point — the tables are tiny either way.

- [x] So the script can run again and again, always from the same start

  > Drop, then create: run it twice, and you get the same two clean
  > tables. That is what makes the numbers on this page yours too.

- [ ] Because MySQL forbids two tables with the same name in two databases

  > Two databases may both have a Resources table. The DROP is about
  > running the script again in this one.

- [ ] To delete the Resources table of your uwm database

  > `USE coursedb;` comes first: only coursedb is touched.
{: .quiz }
````
{: .accordion #setup }

````
### 🧙 Step 1 · Three tools, one idea: logic inside the database

[Putting it all together](_slides/m10_05.jpg)
{: .embed image="true" width="100%" }

| Tool | Who runs it | Type of logic |
|---|---|---|
| 🧩 Stored procedure | **You** call it, with CALL | Explicit, reusable |
| 🔁 Cursor | Lives **inside** a procedure | Procedural, row by row |
| ⚡ Trigger | **The database** calls it, on a change | Automatic, event-driven |

Seen together, they turn a static database into an **active** system —
one that can act, decide, and react.

**Q:** Which tool runs without anyone calling it?

- [ ] A stored procedure, once it has been saved

  > Saved is not running: a procedure waits for its CALL.

- [ ] A cursor, as soon as it is declared

  > A cursor lives inside a procedure, and only moves when the procedure
  > runs and FETCHes.

- [x] A trigger, when the change it watches happens

  > The database itself runs the trigger, every time the event occurs.

- [ ] None of them — the database never acts by itself

  > That was true until this week. A trigger is exactly the exception.
{: .quiz }
````
{: .accordion #three_tools }

````
### 🧩 Step 2 · Stored procedures — on paper

[Stored procedures](_slides/m10_02.jpg)
{: .embed image="true" width="100%" }

When the same SQL keeps coming back — adding a resource, cleaning a
log — you can wrap it into a **stored procedure**: a routine saved in
the database, run by name with **CALL**, like a reusable function.

**To read, not to run** — the INSERT of step 0, wrapped once:

~~~sql
CREATE PROCEDURE AddResource(IN NewCourseID INT,
                             IN NewTitle VARCHAR(100),
                             IN NewDescription TEXT)
BEGIN
  INSERT INTO Resources (CourseID, Title, Description)
  VALUES (NewCourseID, NewTitle, NewDescription);
END;

-- then, any time:
CALL AddResource(2, 'Project Guidelines', 'Initial draft for Module 6');
~~~

Read it like a sentence: *AddResource takes a course, a title and a
description, and inserts them as a new resource.* Three CALLs would give
the three rows step 0 inserted by hand.

Why bother? ♻ **Reusability** — written once, used often. 🧱
**Consistency** — fix the logic in one place. 🔒 **Security and
performance** — the SQL stays on the server.

**Q:** Once AddResource is saved, what does a fourth resource cost?

- [ ] A new procedure, since each procedure works only once

  > A procedure is saved for good: call it as often as you like.

- [x] One CALL line with three values

  > That is the point of a procedure: the INSERT is written once, inside
  > it. Each new resource is just a CALL.

- [ ] Nothing — the procedure adds resources by itself every night

  > A procedure never runs on its own. It waits for a CALL.

- [ ] A copy of the whole procedure, pasted again

  > The procedure lives in the database: you only CALL it.
{: .quiz }
````
{: .accordion #procedure }

````
### ⚡ Step 3 · A trigger: the database reacts on its own

[Triggers](_slides/m10_04.jpg)
{: .embed image="true" width="100%" }

The resources change over time. Each time a **Description** changes, we
want the **Version** to go up by one and **LastUpdated** to take the
current time — without anyone remembering to do it. That is a trigger's
job:

```sql
USE coursedb;
DROP TRIGGER IF EXISTS TrgResourcesVersion;

DELIMITER //
CREATE TRIGGER TrgResourcesVersion
BEFORE UPDATE ON Resources
FOR EACH ROW
BEGIN
  IF NEW.Description <> OLD.Description THEN
    SET NEW.Version = OLD.Version + 1;
    SET NEW.LastUpdated = NOW();
  END IF;
END //
DELIMITER ;

SHOW TRIGGERS LIKE 'Resources';
```

Select the whole block — the DELIMITER lines included — and run it.

**Why DELIMITER?** The trigger's body contains semicolons. `DELIMITER //`
tells Workbench: "until I say otherwise, a statement ends with //" — so
the whole trigger travels to the server as **one** statement. Then
`DELIMITER ;` puts the usual ending back.

Read it like a sentence: *before any row of Resources is updated, if its
new Description differs from the old one, raise its Version by one and
stamp the time.*

- **OLD** is the row **as it was**; **NEW** is the row **as it is about
  to be**.
- **BEFORE** UPDATE lets the trigger still change NEW — the row is not
  saved yet.

You should see: the last line lists **one** trigger, TrgResourcesVersion,
event **UPDATE**, timing **BEFORE**.

**Q:** In this trigger, what is `OLD.Version`?

- [ ] The version number of MySQL running the trigger

  > A fine guess, but OLD is about the row, not the server.

- [x] The row's Version before the update — the value being replaced

  > OLD is the row as it was; NEW is the row as it is about to be saved.

- [ ] The oldest version of the resource ever saved, version 1

  > OLD holds the current value just before this update — 3, say, not
  > always 1.

- [ ] A copy of the whole Resources table, kept for safety

  > Only one row at a time: FOR EACH ROW.
{: .quiz }
````
{: .accordion #trigger }

````
### 🧪 Step 4 · Test the trigger, one update at a time

Now watch the database react. Run each block on its own, then compare
with **You should see**.

**① Change the description** of resource 1:

```sql
UPDATE Resources SET Description = 'Added section about triggers'
WHERE ResourceID = 1;
SELECT ResourceID, Title, Version, LastUpdated FROM Resources
WHERE ResourceID = 1;
```

You should see: **Version 2**, and a **LastUpdated** that moved to
right now. Nobody typed `Version = 2` — the trigger did.

**② Change only the title:**

```sql
UPDATE Resources SET Title = 'Project Guidelines v2'
WHERE ResourceID = 1;
SELECT ResourceID, Title, Version, LastUpdated FROM Resources
WHERE ResourceID = 1;
```

You should see: the new title, but **Version still 2**, and LastUpdated
unchanged. The trigger fired — but its IF said no.

**③ Write the same description again:**

```sql
UPDATE Resources SET Description = 'Added section about triggers'
WHERE ResourceID = 1;
SELECT ResourceID, Version FROM Resources WHERE ResourceID = 1;
```

You should see: **Version still 2**. NEW and OLD are equal, so nothing
changed that matters.

**④ A real change, then a change to several rows at once:**

```sql
UPDATE Resources SET Description = 'Final version'
WHERE ResourceID = 1;
UPDATE Resources SET Description = CONCAT(Description, ' (reviewed)')
WHERE CourseID = 2;
SELECT ResourceID, CourseID, Title, Version FROM Resources;
```

You should see: resource 1 at **Version 4**, resource 2 at **Version 2**,
resource 3 still at **Version 1**. The second UPDATE touched two rows,
and the trigger ran **once for each** — FOR EACH ROW.

**Q:** In ②, the trigger fired but Version stayed at 2. Why?

- [ ] The trigger was asleep, since titles do not wake it up

  > It did wake up — every UPDATE on Resources fires it. Then its IF
  > decided.

- [ ] A trigger fires only once per resource, then never again

  > It fires on every update, as ③ and ④ show.

- [ ] The UPDATE failed, so the title did not change either

  > The title did change. Only the Version did not.

- [x] Its IF compares the descriptions — they were equal, so it did nothing

  > NEW.Description equals OLD.Description when only the title changes,
  > so the two SET lines are skipped.
{: .quiz }
````
{: .accordion #test_trigger }

````
### 🔁 Step 5 · Cursors — on paper

[Cursors](_slides/m10_03.jpg)
{: .embed image="true" width="100%" }

Sometimes one big query is not enough: each row needs its own
decision. A **cursor** lets a stored procedure walk through a query's
rows **one at a time**.

**To read, not to run** — a procedure that adds up every Version, row
by row:

~~~sql
CREATE PROCEDURE SumVersions(OUT Total INT)
BEGIN
  DECLARE Done INT DEFAULT 0;
  DECLARE OneVersion INT;
  DECLARE VersionCursor CURSOR FOR SELECT Version FROM Resources;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET Done = 1;
  SET Total = 0;
  OPEN VersionCursor;
  ReadLoop: LOOP
    FETCH VersionCursor INTO OneVersion;
    IF Done = 1 THEN LEAVE ReadLoop; END IF;
    SET Total = Total + OneVersion;
  END LOOP;
  CLOSE VersionCursor;
END;
~~~

The four moves of every cursor: **DECLARE** it for a query, **OPEN** it,
**FETCH** row after row, **CLOSE** it. The **handler** sets `Done` when
there are no more rows, so the loop knows when to stop.

After step 4, this cursor would answer **7**: 4 + 2 + 1. And one line of
set logic gives the same answer — this one you can run:

```sql
SELECT SUM(Version) AS TotalVersions FROM Resources;
```

You should see: **7**. Same answer, two ways of thinking: the cursor
walks **step by step**; SUM answers for the **whole set** at once. For a
sum, SUM is simpler and faster — a cursor earns its place when each row
needs its own decision.

**Q:** What tells the cursor's loop that the rows are finished?

- [ ] The cursor counts the rows first, then stops at the last one

  > A cursor does not count ahead. It fetches until there is nothing
  > left to fetch.

- [x] The NOT FOUND handler sets Done to 1, and the loop leaves

  > When FETCH finds no more rows, the handler fires; the IF then leaves
  > ReadLoop.

- [ ] CLOSE, which runs after every FETCH

  > CLOSE runs once, after the loop, to release the cursor.

- [ ] Nothing — the loop runs forever, so a cursor must never be used

  > Without the handler it would. With it, the loop ends cleanly.
{: .quiz }
````
{: .accordion #cursor }

````
### 🔎 Practice block — read what the trigger wrote

The resources as they stand after step 4 — the versions the trigger
counted. These are SELECTs on a copy: look as much as you like.

```json
[
  {"CourseID": 1, "CourseNumber": "INFOST 350", "CourseTitle": "Intro to Application Development"},
  {"CourseID": 2, "CourseNumber": "INFOST 410", "CourseTitle": "Database Information Retrieval Systems"}
]
```
{: .dataset #Courses }

```json
[
  {"ResourceID": 1, "CourseID": 2, "Title": "Project Guidelines v2", "Description": "Final version (reviewed)", "Version": 4},
  {"ResourceID": 2, "CourseID": 2, "Title": "Query Cheat Sheet", "Description": "SELECT, JOIN, GROUP BY (reviewed)", "Version": 2},
  {"ResourceID": 3, "CourseID": 1, "Title": "Python Setup", "Description": "Install and first run", "Version": 1}
]
```
{: .dataset #Resources }

**① Resources the trigger has touched** — Version above 1:

```sql
SELECT Resources.ResourceID, Resources.Title, Resources.Version
FROM Resources
WHERE Resources.Version > 1
```
{: .query source="Resources" #q_touched editable="true" }

[changed at least once](#)
{: .datagrid source="q_touched" rows="2" }

**② The set answer** — what the cursor of step 5 would add up, row by row:

```sql
SELECT SUM(Resources.Version) AS TotalVersions
FROM Resources
```
{: .query source="Resources" #q_total editable="true" }

[all versions, at once](#)
{: .datagrid source="q_total" rows="1" }

**✋ Your move** — the total of versions **per course**, one row per
course, the CourseID first. Change ② so it groups by the course, then
press ▶ Run. INFOST 410 (course 2) should total 6.

```sql
SELECT SUM(Resources.Version) AS TotalVersions
FROM Resources
```
{: .query source="Resources" #q_mine editable="true" }

[your answer](#)
{: .datagrid source="q_mine" rows="2" }

The second check at the very bottom stays **red until you do it**.
````
{: .block title="🔎 Practice block" #live }

One word to keep from this week: a `trigger`[^trigger] is logic the
database runs by itself, before or after a change, once for each row.
The proof below runs the practice block's own queries:

```gherkin
Feature: What the trigger wrote
  Scenario: Two resources changed, one never did
    Given the resources after step 4
    :::python
    self.resources: Dataset = Dataset("Resources")
    self.touched: Query = self.page.q_touched
    :::
    When the resources with a Version above 1 are selected
    Then two come back, resource 3 is not among them
    :::python
    assert self.touched.count == 2, self.touched.count
    assert 3 not in [int(x) for x in self.touched.values("ResourceID")], self.touched.values("ResourceID")
    :::

  Scenario: The set answer equals the cursor's
    Given the resources after step 4
    :::python
    self.total: Query = self.page.q_total
    :::
    When the versions are summed as a set
    Then the total is 7, like the cursor's
    :::python
    assert str(self.total.values("TotalVersions")[0]) == "7", self.total.values("TotalVersions")
    :::
```
{: .feature #activity_proof tags="trigger" visible="true" status="passing" }

And one check that is **yours**. It reads your query in the practice
block and stays red while it still sums everything at once:

```gherkin
Feature: Your move — versions per course
  Scenario: One row per course, course 2 with 6
    Given your query in the practice block
    :::python
    self.mine: Query = self.page.q_mine
    :::
    When you press Run on your query
    Then it groups by the course
    :::python
    flat: str = " ".join(self.mine.query.upper().split())
    assert "GROUP BY" in flat and "COURSEID" in flat.split("GROUP BY")[-1], \
        "group by the course: GROUP BY Resources.CourseID, with Resources.CourseID first in the SELECT"
    :::
    And course 2 totals 6
    :::python
    assert self.mine.count == 2, self.mine.count
    ids: list = [str(x) for x in self.mine.values("CourseID")]
    totals: list = [str(x) for x in self.mine.values("TotalVersions")]
    assert "2" in ids, "put Resources.CourseID in the SELECT, first"
    assert totals[ids.index("2")] == "6", totals
    :::
```
{: .feature #your_move_proof tags="trigger" visible="true" status="pending" celebration="true" }

[Browse](#)
{: .folder parent="true" }

```yaml
bot: doc
voice: en-US
face:
  zoom: 1.2
script:
  - say: "Welcome back! This week the logic moves inside the database. Procedures and cursors on paper, and one trigger you build yourself, in Workbench, on a small database called coursedb."
  - at: setup
    do: open
    say: "Step zero. In the Query menu, check Stop Script Execution on Errors, and this week check Auto-Commit Transactions too. Then build coursedb. You should see three resources, each at version one."
  - at: three_tools
    do: open
    say: "Step one. Three tools, one idea. You call a procedure. A cursor lives inside a procedure. And the database calls a trigger, by itself, when data changes."
  - at: procedure
    do: open
    say: "Step two, on paper. A stored procedure is a routine saved once in the database and run by name with CALL. Read it like a sentence. No need to run it."
  - at: trigger
    do: open
    say: "Step three. Now you build. A trigger that watches every update: if the description changes, the version goes up by one and the time is stamped. DELIMITER lets it travel as one statement. OLD is the row as it was, NEW the row about to be saved."
  - at: test_trigger
    do: open
    say: "Step four. Test it, one update at a time. A new description: version two. A new title only: still two. The same description: still two. Then several rows at once: the trigger runs for each row."
  - at: cursor
    do: open
    say: "Step five, on paper. A cursor walks rows one at a time: declare, open, fetch, close. This one would add up the versions to seven. Run SUM, and you get seven too, for the whole set at once."
  - at: live
    do: open
    say: "Here is the practice block, with the resources the trigger changed. Your move: total the versions per course. Course two should total six. The last check stays red until you do."
stories:
  summarize the page:
    - 'You might wonder: summarize the page'
    - This week the logic moves inside the database, in three tools.
    - A stored procedure is a routine you save once and call by name, read here on paper.
    - A cursor walks through rows one at a time inside a procedure, also on paper.
    - The trigger is the one you build, in Workbench, on a small database called coursedb.
    - It raises a version every time a description changes, all by itself.
  why delimiter:
    - 'You might wonder: why delimiter'
    - A trigger body holds several statements, each ending with a semicolon.
    - DELIMITER double slash tells Workbench that a statement now ends with double slash.
    - So the whole trigger reaches the server as one statement, and DELIMITER semicolon puts things back.
  trigger or procedure:
    - 'You might wonder: trigger or procedure'
    - You run a procedure yourself, with CALL, when you decide.
    - The database runs a trigger, every time the change it watches happens.
    - Use a trigger for what must never be forgotten, like a version number.
```
{: .avatar #guide dock="true" size="115" }

[^trigger]: **trigger** — logic the database runs by itself, BEFORE or
    AFTER an INSERT, UPDATE or DELETE, once FOR EACH ROW; OLD is the row
    as it was, NEW the row as it will be.
