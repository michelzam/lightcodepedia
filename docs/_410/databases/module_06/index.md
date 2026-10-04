# 🏗️ 06 · From Reading to Designing

✏️ Last week you read the map. This week you start drawing one.

Ask Doc for a tour!
{: .avatar_trigger target="guide" }

Welcome back! Last week you learned to **read** a database design — the
dataquest map — and turn it into queries. This week we **turn around**:
instead of receiving a map, you start **drawing** one.

The plan, in small steps: first we replay one query, frame by frame.
Then we flip the direction, from using a design to making one. And then
UWM asks for your help: its course information lives in a messy
spreadsheet, and you will design the **top of a brand-new map** for it.
Next week we finish the bottom of that map.

Every step ends with a little quiz, just for you. Take your time. 🙂

> A spreadsheet walks into a bar and orders a drink. Then it orders the
> same drink again. And again. The bartender says: "You need
> normalization." 🍹

````
### 🔁 Step 1 · Replay: one query, built frame by frame

Remember last week's question: *which category has the most products?*
Here is how one student built the answer — **one small change at a
time**, running the query after every change:

[Frames 2 to 9 — one query, built step by step](_slides/m06_04.jpg)
{: .embed image="true" width="100%" }

Now do it yourself: each frame has its own editor, over the real 77
products. Press ▶ Run on each one, in order, and watch the answer grow.

**Frame 2** — start tiny, with one table. 8 rows. Good.

```sql
SELECT Categories.CategoryID
FROM Categories
```
{: .query source="Categories,Products" #frame_2 editable="true" }

[frame 2](#)
{: .datagrid source="frame_2" rows="3" }

**Frame 3** — add `Products.ProductID`… but Products is not in the FROM. **Error** — the database does not know where to find it.

```sql
SELECT Categories.CategoryID, Products.ProductID
FROM Categories
```
{: .query source="Categories,Products" #frame_3 editable="true" }

[frame 3](#)
{: .datagrid source="frame_3" rows="3" }

**Frame 4** — join Products to Categories on their key. 77 rows: one per product.

```sql
SELECT Categories.CategoryID, Products.ProductID AS ProductCount
FROM Products
LEFT JOIN Categories ON Products.CategoryID = Categories.CategoryID
```
{: .query source="Categories,Products" #frame_4 editable="true" }

[frame 4](#)
{: .datagrid source="frame_4" rows="3" }

**Frame 5** — try to COUNT the products. w3schools says **error**: one row per product cannot also be one count per category. Our editor is more forgiving — it answers one row, 77. A number, but not an answer to the question!

```sql
SELECT Categories.CategoryID, COUNT(Products.ProductID) AS ProductCount
FROM Products
LEFT JOIN Categories ON Products.CategoryID = Categories.CategoryID
```
{: .query source="Categories,Products" #frame_5 editable="true" }

[frame 5](#)
{: .datagrid source="frame_5" rows="3" }

**Frame 6** — add `GROUP BY Categories.CategoryID`. 8 rows, each with its count. 🎉

```sql
SELECT Categories.CategoryID, COUNT(Products.ProductID) AS ProductCount
FROM Products
LEFT JOIN Categories ON Products.CategoryID = Categories.CategoryID
GROUP BY Categories.CategoryID
```
{: .query source="Categories,Products" #frame_6 editable="true" }

[frame 6](#)
{: .datagrid source="frame_6" rows="3" }

**Frame 7** — sort by the count, biggest first.

```sql
SELECT Categories.CategoryID, COUNT(Products.ProductID) AS ProductCount
FROM Products
LEFT JOIN Categories ON Products.CategoryID = Categories.CategoryID
GROUP BY Categories.CategoryID
ORDER BY COUNT(Products.ProductID) DESC
```
{: .query source="Categories,Products" #frame_7 editable="true" }

[frame 7](#)
{: .datagrid source="frame_7" rows="3" }

**Frame 8** — keep only the top row, and ask for the CategoryName too. On w3schools the name does **not** show up — it is not on the GROUP BY guest list. (Our editor forgives and shows it anyway; w3schools and MySQL are stricter.)

```sql
SELECT TOP 1 Categories.CategoryID, Categories.CategoryName,
       COUNT(Products.ProductID) AS ProductCount
FROM Products
LEFT JOIN Categories ON Products.CategoryID = Categories.CategoryID
GROUP BY Categories.CategoryID
ORDER BY COUNT(Products.ProductID) DESC
```
{: .query source="Categories,Products" #frame_8 editable="true" }

[frame 8](#)
{: .datagrid source="frame_8" rows="3" }

**Frame 9** — add CategoryName to the GROUP BY too. Confections, 13 products. Done!

```sql
SELECT TOP 1 Categories.CategoryID, Categories.CategoryName,
       COUNT(Products.ProductID) AS ProductCount
FROM Products
LEFT JOIN Categories ON Products.CategoryID = Categories.CategoryID
GROUP BY Categories.CategoryID, Categories.CategoryName
ORDER BY COUNT(Products.ProductID) DESC
```
{: .query source="Categories,Products" #frame_9 editable="true" }

[frame 9](#)
{: .datagrid source="frame_9" rows="3" }

Two errors on the way — and that is perfectly fine. **Each error is a
message, not a failure.** Run, read the result, change one thing, run
again: that is System 2 at work.

**Q:** Frame 5 shows an error. What is the database telling you?

- [ ] It is tired, and would like a short nap before it starts counting anything

  > Databases never sleep. The message is about the groups: COUNT needs
  > to know what to count *per*.

- [ ] Products and Categories cannot be joined together

  > They can — frame 4 joined them and got 77 rows.

- [x] It cannot count per category until you say GROUP BY

  > Exactly what frame 6 does. One row per product cannot also be one
  > count per category — GROUP BY makes the groups.

- [ ] COUNT only works on a single table, never with a JOIN

  > COUNT works fine after a JOIN. It just needs a GROUP BY to know what
  > each count is for.
{: .quiz }

**Q:** In frame 8, the query asks for CategoryName, but the result does
not show it. Why?

- [ ] CategoryName was hiding behind the 13 products, out of pure shyness

  > Shy columns do not exist. It is the GROUP BY guest list at work.

- [x] It is not in the GROUP BY, so it is not on the guest list

  > The rule from last week: with GROUP BY, only group fields and
  > aggregates. Frame 9 adds CategoryName to the GROUP BY — and there it
  > is.

- [ ] TOP 1 removes every column except the first two

  > TOP 1 keeps one row, with all its columns. The missing column is the
  > GROUP BY's doing.
{: .quiz }
````
{: .accordion #replay }

````
### 🛟 Step 2 · UWM needs help

[UWM needs help](_slides/m06_07.jpg)
{: .embed image="true" width="100%" }

**The story.** UWM keeps track of students, majors, courses, instructors
and enrollments in **spreadsheets**. The same information — like a
department's name — is typed again and again, on many rows. That makes
updates error-prone: change it in one row, forget another, and the
spreadsheet now disagrees with itself.

UWM needs a proper database, where each fact is stored **once**. That is
your job — this week the top of the map, next week the rest.

**🔎 Explore first.** Before designing anything, look at the real data.
Open UWM's course catalog in a new tab:

👉 [catalog.uwm.edu/course-search](https://catalog.uwm.edu/course-search/)

Search for a few courses from **Information Studies** (the subject code
is INFOST), then a few from another department you know — Computer
Science, Mathematics… For each course, jot down on paper:

- the **department** it belongs to (and its code, like INFOST);
- the course **number** (like 410);
- its **title**;
- its number of **credits**.

Five or six courses are plenty. Look at your notes: which values come
back again and again? Which describe the *department*, and which
describe the *course*?

**The trap.** Notes like yours often end up in one big table — one row
per course, every column side by side. Here is a small piece of what
UWM's spreadsheet looks like:

[UWM's old spreadsheet](#)
{: .datagrid source="CourseSheet" rows="7" }

It looks tidy. It is a trap: the department's name is typed again on
every course row. Nothing is wrong *today* — the trouble starts the day
something changes. 😬 Count for yourself, or let **①** in the practice
block count for you.

**Q:** If the Information Studies department got a new name, how many
rows of this spreadsheet would you have to fix?

- [ ] Zero — spreadsheets would update themselves overnight while everyone sleeps

  > If only! Every copy of the name must be fixed by hand — and every
  > copy you miss becomes a mistake.

- [ ] One — the name appears only once in the spreadsheet

  > It appears on every one of its course rows. Run ① and count.

- [x] Five — one for every Information Studies course

  > Five copies of the same fact, five chances to forget one. In a good
  > design the name is stored once, so the fix touches one row.

- [ ] Seven — every row of the spreadsheet

  > Only the Information Studies rows carry that name. The Computer
  > Science and Mathematics rows stay as they are.
{: .quiz }
````
{: .accordion #uwm }

````
### ✂️ Step 3 · Split it: Departments above Courses

The fix is to give each **thing** its own table:

- **Departments** — one row per department: its ID, its name, its code.
- **Courses** — one row per course: its ID, number, title, credits…
  and **which department it belongs to**.

How does a course say which department it belongs to? With a **foreign
key**: a `DepartmentID` column in Courses, holding the ID of its
department. One department offers many courses; each course belongs to
one department. So, by our layout rule, **Departments sits above
Courses**.

Does this look familiar? It is exactly **Categories → Products** from
the dataquest map: one category, many products, the CategoryID in
Products. Same pattern, new topic. 🎯

**First in English, then as a diagram.** A designer always starts with
plain sentences:

> *A department offers many courses. Each course belongs to exactly one
> department.*

The same two sentences, drawn as entities — the same kind of map you
read in module 02:

```python
@component(icon="🏛️")
class Department(Object):
    DepartmentID   = Attr(int, hint="primary key")
    DepartmentName = Attr(str)
    DepartmentCode = Attr(str)

@component(icon="📘")
class Course(Object):
    CourseID     = Attr(int, hint="primary key")
    CourseNumber = Attr(str)
    CourseTitle  = Attr(str)
    Credits      = Attr(int)
    DepartmentID = Attr("Department", hint="foreign key → Departments")
```
{: .model #uwm_model }

[Departments above Courses — one key between them](#)
{: .diagram scope="Course" states="false" }

Read it like the sentences: a **Course** names its Department through
`DepartmentID`; the Department sits **above**, because it is the ONE
side. Later, in MySQL Workbench, a diagram like this one can write its
own CREATE TABLE statements — but first, see the data it will hold.

**The data.** The same seven courses as the spreadsheet, now in two
tables:

[Departments — one row each](#)
{: .datagrid source="Departments" rows="3" }

[Courses — each pointing to its department](#)
{: .datagrid source="Courses" rows="7" }

**In SQL**, the same design becomes two CREATE TABLE statements:

~~~sql
CREATE TABLE Departments (
  DepartmentID   INT AUTO_INCREMENT NOT NULL,
  DepartmentName VARCHAR(100),
  DepartmentCode VARCHAR(10),
  PRIMARY KEY (DepartmentID)
);

CREATE TABLE Courses (
  CourseID     INT AUTO_INCREMENT NOT NULL,
  CourseNumber VARCHAR(20),
  CourseTitle  VARCHAR(150),
  Credits      INT,
  DepartmentID INT,
  PRIMARY KEY (CourseID),
  FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);
~~~

And the rename? Now it changes **one row** in Departments, and every
course follows. That is the whole point of a good design.

**Q:** Where does `DepartmentID` live as a foreign key?

- [ ] On a sticky note on the dean's fridge, next to the pizza menu and the parking tickets

  > A cozy place, but the database cannot read the fridge. The foreign
  > key goes in a table.

- [x] In Courses — each course points up to its one department

  > The MANY side carries the foreign key. Each course holds the ID of
  > the department it belongs to.

- [ ] In Departments — one column listing all of its course IDs

  > A list of IDs in one cell breaks the first rule of tables: one value
  > per cell. Turn it around: each course points to its department.

- [ ] In both tables at once, just to be on the safe side

  > Two copies of the same link can disagree — the very problem we are
  > fixing. One foreign key, on the MANY side.
{: .quiz }
````
{: .accordion #split }

````
### 📐 Step 4 · Design guidelines, part 1

[Design guidelines](_slides/m06_09.jpg)
{: .embed image="true" width="100%" }

Designers follow **conventions**, so that everyone can read everyone
else's database. This week, four of them:

1. **Names.** Tables are plural and capitalized: `Departments`,
   `Courses`. Columns are singular, in CamelCase: `CourseTitle`. No
   underscores.
2. **Primary key.** The table's name in singular, plus ID:
   `CourseID`. An INT, AUTO_INCREMENT, NOT NULL. Exactly one per table.
3. **Foreign key.** Same name as the primary key it points to:
   `Courses.DepartmentID` points to `Departments.DepartmentID`.
4. **Layout.** The table holding the foreign key (the MANY side) sits
   **below** the table it points to.

The last rows of the guidelines (normalization) come next week.

**Q:** Which names follow our guidelines? Check all that apply.

- [ ] `TheBigTableOfEverything.StuffAndThings`

  > Tempting — one table for everything is exactly the spreadsheet we
  > are escaping from.

- [x] `Courses.CourseID`

  > Plural table, singular name plus ID for the primary key. Textbook.

- [ ] `tbl_course.course_id`

  > Underscores and prefixes. Our convention: `Courses.CourseID`.

- [x] `Courses.DepartmentID`

  > A foreign key with the same name as the primary key it points to.

- [ ] `Course.departmentName`

  > Singular table, and a name where the key should be. The course
  > points to its department with `DepartmentID`.
{: .quiz }
````
{: .accordion #guidelines }

````
### 📊 Step 5 · The first report: courses per department

A design is good when it answers the expected questions. UWM's first
question: **which courses belong to each department?**

Two tables, one key — you know this:

~~~sql
SELECT Courses.CourseID, Courses.CourseNumber, Courses.CourseTitle,
       Departments.DepartmentName
FROM Courses
JOIN Departments ON Courses.DepartmentID = Departments.DepartmentID;
~~~

Notice the first column: `Courses.CourseID`. **A good habit: always
start a result with the ID of what one row stands for.** Here one row is
one course, so the CourseID comes first — a glance at the first column
tells you the nature of the result.

And **how many** courses per department? One row per department, so we
group by the department — and the DepartmentID comes first:

~~~sql
SELECT Departments.DepartmentID, Departments.DepartmentName,
       COUNT(Courses.CourseID) AS CourseCount
FROM Courses
JOIN Departments ON Courses.DepartmentID = Departments.DepartmentID
GROUP BY Departments.DepartmentID, Departments.DepartmentName;
~~~

Compare with last week: Categories and Products, Departments and
Courses. Same shape, same query. **The pattern travels.**

👉 Try it: **②** and **③** in the practice block.

**Q:** "How many courses per department?" — what does the GROUP BY
need?

- [ ] `Courses.Mood`, to group the happy courses apart from the grumpy ones

  > Courses have no mood column — though some Monday morning sections
  > might deserve one.

- [ ] `Courses.CourseID`, so each course gets counted

  > One group per course holds one course: every count comes back 1.

- [x] The department: `Departments.DepartmentID` and its name

  > "Per department" means one group per department. The name is in
  > the GROUP BY too, because it is in the SELECT.

- [ ] `Courses.Credits`, since credits are a number

  > That groups courses by how many credits they carry — a different
  > question.
{: .quiz }
````
{: .accordion #first_report }

````
### ↔️ Step 6 · Two directions, one map — the designer's checklist

You have just split one spreadsheet into two tables, named them well,
and checked them against a first report. Time to step back and see the
method. Remember the two pillars from last week:

- **Representation** — how data is stored: CREATE TABLE.
- **Usage** — how data is used: SELECT.

Until this week, someone else built the tables and you used them. **Now
you build them.** Every query anyone will ever write on your database
can only travel the roads *you* draw. So a designer always thinks of
the questions first.

[A designer's checklist](_slides/m06_10.jpg)
{: .embed image="true" width="100%" }

A designer's checklist, in order:

1. Start with the **entities** — the things the database is about
   (departments, courses…). Each one becomes a table.
2. Add useful **attributes** — each one becomes a column.
3. Add the **relationships** and their **cardinalities** (one, many).
4. Check the **layout**: the ONE side above, the MANY side below.
5. Check against the **expected queries**: can each one be answered?

Paper, pencil and sticky notes are perfect for this. Professionals do it
too.

**Q:** Why does a designer check the design against the expected
queries?

- [ ] To make sure the queries like the color of the sticky notes on the board

  > Queries have no taste in colors. They only care about the roads.

- [ ] Because the database refuses to create a table nobody queries

  > The database will happily create any table. Whether it is useful is
  > the designer's job.

- [x] Because a query can only travel the roads the design gives it

  > If no road leads from one table to another, no query can make the
  > trip. Checking the questions first catches a missing road early.
{: .quiz }
````
{: .accordion #two_ways }

````
### 🧩 Step 7 · The rest of the top of the map

Departments and Courses are the first two pieces. The top of UWM's map
has a few more, all with the **same pattern** — one department, many of
something:

- **Majors** — a department hosts many majors; each major belongs to one
  department.
- **Instructors** — a department employs many instructors; each
  instructor has one home department.
- **Terms** — Fall 2026, Spring 2027… a table of its own, on the top
  row, because it points to nothing.

Try it on paper with sticky notes: one sticky note per table, its
columns below, a line for each relationship, the ONE side above. Check
your names against the guidelines. That drawing is the top half of
UWM's new map.

Students, course sections and enrollments wait at the bottom of the
map — next week, together with a new kind of relationship. 👀

👉 And **your move**, at the bottom of the practice block: the same
report again, for Majors.

**Q:** "A department hosts many majors; each major belongs to one
department." Which line does this sentence draw?

- [ ] A heart shape, because the department truly loves all its majors equally

  > Sweet, but ER diagrams only know two shapes: one and many.

- [x] 1 : N — Departments above Majors, the foreign key in Majors

  > Same pattern as Departments and Courses. Majors carries
  > `DepartmentID` and sits below.

- [ ] 1 : N — Majors above Departments, the foreign key in Departments

  > Upside down. The MANY side — Majors — carries the key and sits
  > below.

- [ ] No line at all — a major's department is just a column of text

  > A department's name typed on each major is the spreadsheet problem
  > again. A key keeps one copy of the name.
{: .quiz }
````
{: .accordion #top_of_map }

````
### 🔎 Practice block — try every step here

A small sample, inspired by the UWM schedule of classes: three
departments, seven courses, four majors — plus the dataquest's 77
products for the replay. Small on purpose — you can
check every answer with your own eyes.

**The old spreadsheet** — everything in one table:

```json
[
  {"CourseNumber": "INFOST 110", "CourseTitle": "Introduction to Information Science and Technology", "Credits": 3, "DepartmentName": "Information Studies", "DepartmentCode": "INFOST"},
  {"CourseNumber": "INFOST 120", "CourseTitle": "Information Technology Ethics", "Credits": 3, "DepartmentName": "Information Studies", "DepartmentCode": "INFOST"},
  {"CourseNumber": "INFOST 240", "CourseTitle": "Web Design I", "Credits": 3, "DepartmentName": "Information Studies", "DepartmentCode": "INFOST"},
  {"CourseNumber": "INFOST 270", "CourseTitle": "Generative AI Literacy", "Credits": 3, "DepartmentName": "Information Studies", "DepartmentCode": "INFOST"},
  {"CourseNumber": "INFOST 410", "CourseTitle": "Database Information Retrieval Systems", "Credits": 3, "DepartmentName": "Information Studies", "DepartmentCode": "INFOST"},
  {"CourseNumber": "COMPSCI 250", "CourseTitle": "Introductory Computer Programming", "Credits": 3, "DepartmentName": "Computer Science", "DepartmentCode": "COMPSCI"},
  {"CourseNumber": "MATH 231", "CourseTitle": "Calculus and Analytic Geometry I", "Credits": 4, "DepartmentName": "Mathematical Sciences", "DepartmentCode": "MATH"}
]
```
{: .dataset #CourseSheet }

**The new design** — each thing in its own table:

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

The dataquest's categories and its 77 products, for the replay in step 1:

```json
[
  {"CategoryID": 1, "CategoryName": "Beverages"},
  {"CategoryID": 2, "CategoryName": "Condiments"},
  {"CategoryID": 3, "CategoryName": "Confections"},
  {"CategoryID": 4, "CategoryName": "Dairy Products"},
  {"CategoryID": 5, "CategoryName": "Grains/Cereals"},
  {"CategoryID": 6, "CategoryName": "Meat/Poultry"},
  {"CategoryID": 7, "CategoryName": "Produce"},
  {"CategoryID": 8, "CategoryName": "Seafood"}
]
```
{: .dataset #Categories }

```json
[
  {"ProductID": 1, "ProductName": "Chais", "CategoryID": 1},
  {"ProductID": 2, "ProductName": "Chang", "CategoryID": 1},
  {"ProductID": 3, "ProductName": "Aniseed Syrup", "CategoryID": 2},
  {"ProductID": 4, "ProductName": "Chef Anton's Cajun Seasoning", "CategoryID": 2},
  {"ProductID": 5, "ProductName": "Chef Anton's Gumbo Mix", "CategoryID": 2},
  {"ProductID": 6, "ProductName": "Grandma's Boysenberry Spread", "CategoryID": 2},
  {"ProductID": 7, "ProductName": "Uncle Bob's Organic Dried Pears", "CategoryID": 7},
  {"ProductID": 8, "ProductName": "Northwoods Cranberry Sauce", "CategoryID": 2},
  {"ProductID": 9, "ProductName": "Mishi Kobe Niku", "CategoryID": 6},
  {"ProductID": 10, "ProductName": "Ikura", "CategoryID": 8},
  {"ProductID": 11, "ProductName": "Queso Cabrales", "CategoryID": 4},
  {"ProductID": 12, "ProductName": "Queso Manchego La Pastora", "CategoryID": 4},
  {"ProductID": 13, "ProductName": "Konbu", "CategoryID": 8},
  {"ProductID": 14, "ProductName": "Tofu", "CategoryID": 7},
  {"ProductID": 15, "ProductName": "Genen Shouyu", "CategoryID": 2},
  {"ProductID": 16, "ProductName": "Pavlova", "CategoryID": 3},
  {"ProductID": 17, "ProductName": "Alice Mutton", "CategoryID": 6},
  {"ProductID": 18, "ProductName": "Carnarvon Tigers", "CategoryID": 8},
  {"ProductID": 19, "ProductName": "Teatime Chocolate Biscuits", "CategoryID": 3},
  {"ProductID": 20, "ProductName": "Sir Rodney's Marmalade", "CategoryID": 3},
  {"ProductID": 21, "ProductName": "Sir Rodney's Scones", "CategoryID": 3},
  {"ProductID": 22, "ProductName": "Gustaf's Knäckebröd", "CategoryID": 5},
  {"ProductID": 23, "ProductName": "Tunnbröd", "CategoryID": 5},
  {"ProductID": 24, "ProductName": "Guaraná Fantástica", "CategoryID": 1},
  {"ProductID": 25, "ProductName": "NuNuCa Nuß-Nougat-Creme", "CategoryID": 3},
  {"ProductID": 26, "ProductName": "Gumbär Gummibärchen", "CategoryID": 3},
  {"ProductID": 27, "ProductName": "Schoggi Schokolade", "CategoryID": 3},
  {"ProductID": 28, "ProductName": "Rössle Sauerkraut", "CategoryID": 7},
  {"ProductID": 29, "ProductName": "Thüringer Rostbratwurst", "CategoryID": 6},
  {"ProductID": 30, "ProductName": "Nord-Ost Matjeshering", "CategoryID": 8},
  {"ProductID": 31, "ProductName": "Gorgonzola Telino", "CategoryID": 4},
  {"ProductID": 32, "ProductName": "Mascarpone Fabioli", "CategoryID": 4},
  {"ProductID": 33, "ProductName": "Geitost", "CategoryID": 4},
  {"ProductID": 34, "ProductName": "Sasquatch Ale", "CategoryID": 1},
  {"ProductID": 35, "ProductName": "Steeleye Stout", "CategoryID": 1},
  {"ProductID": 36, "ProductName": "Inlagd Sill", "CategoryID": 8},
  {"ProductID": 37, "ProductName": "Gravad lax", "CategoryID": 8},
  {"ProductID": 38, "ProductName": "Côte de Blaye", "CategoryID": 1},
  {"ProductID": 39, "ProductName": "Chartreuse verte", "CategoryID": 1},
  {"ProductID": 40, "ProductName": "Boston Crab Meat", "CategoryID": 8},
  {"ProductID": 41, "ProductName": "Jack's New England Clam Chowder", "CategoryID": 8},
  {"ProductID": 42, "ProductName": "Singaporean Hokkien Fried Mee", "CategoryID": 5},
  {"ProductID": 43, "ProductName": "Ipoh Coffee", "CategoryID": 1},
  {"ProductID": 44, "ProductName": "Gula Malacca", "CategoryID": 2},
  {"ProductID": 45, "ProductName": "Rogede sild", "CategoryID": 8},
  {"ProductID": 46, "ProductName": "Spegesild", "CategoryID": 8},
  {"ProductID": 47, "ProductName": "Zaanse koeken", "CategoryID": 3},
  {"ProductID": 48, "ProductName": "Chocolade", "CategoryID": 3},
  {"ProductID": 49, "ProductName": "Maxilaku", "CategoryID": 3},
  {"ProductID": 50, "ProductName": "Valkoinen suklaa", "CategoryID": 3},
  {"ProductID": 51, "ProductName": "Manjimup Dried Apples", "CategoryID": 7},
  {"ProductID": 52, "ProductName": "Filo Mix", "CategoryID": 5},
  {"ProductID": 53, "ProductName": "Perth Pasties", "CategoryID": 6},
  {"ProductID": 54, "ProductName": "Tourtière", "CategoryID": 6},
  {"ProductID": 55, "ProductName": "Pâté chinois", "CategoryID": 6},
  {"ProductID": 56, "ProductName": "Gnocchi di nonna Alice", "CategoryID": 5},
  {"ProductID": 57, "ProductName": "Ravioli Angelo", "CategoryID": 5},
  {"ProductID": 58, "ProductName": "Escargots de Bourgogne", "CategoryID": 8},
  {"ProductID": 59, "ProductName": "Raclette Courdavault", "CategoryID": 4},
  {"ProductID": 60, "ProductName": "Camembert Pierrot", "CategoryID": 4},
  {"ProductID": 61, "ProductName": "Sirop d'érable", "CategoryID": 2},
  {"ProductID": 62, "ProductName": "Tarte au sucre", "CategoryID": 3},
  {"ProductID": 63, "ProductName": "Vegie-spread", "CategoryID": 2},
  {"ProductID": 64, "ProductName": "Wimmers gute Semmelknödel", "CategoryID": 5},
  {"ProductID": 65, "ProductName": "Louisiana Fiery Hot Pepper Sauce", "CategoryID": 2},
  {"ProductID": 66, "ProductName": "Louisiana Hot Spiced Okra", "CategoryID": 2},
  {"ProductID": 67, "ProductName": "Laughing Lumberjack Lager", "CategoryID": 1},
  {"ProductID": 68, "ProductName": "Scottish Longbreads", "CategoryID": 3},
  {"ProductID": 69, "ProductName": "Gudbrandsdalsost", "CategoryID": 4},
  {"ProductID": 70, "ProductName": "Outback Lager", "CategoryID": 1},
  {"ProductID": 71, "ProductName": "Flotemysost", "CategoryID": 4},
  {"ProductID": 72, "ProductName": "Mozzarella di Giovanni", "CategoryID": 4},
  {"ProductID": 73, "ProductName": "Röd Kaviar", "CategoryID": 8},
  {"ProductID": 74, "ProductName": "Longlife Tofu", "CategoryID": 7},
  {"ProductID": 75, "ProductName": "Rhönbräu Klosterbier", "CategoryID": 1},
  {"ProductID": 76, "ProductName": "Lakkalikööri", "CategoryID": 1},
  {"ProductID": 77, "ProductName": "Original Frankfurter grüne Soße", "CategoryID": 2}
]
```
{: .dataset #Products }

**① The spreadsheet's problem** — every row carrying the Information
Studies name. Count them:

```sql
SELECT * FROM CourseSheet
WHERE CourseSheet.DepartmentName = 'Information Studies'
```
{: .query source="CourseSheet" #q_sheet editable="true" }

[rows to fix after a rename](#)
{: .datagrid source="q_sheet" rows="5" }

**② Courses with their department** — two tables, one key:

```sql
SELECT Courses.CourseID, Courses.CourseNumber, Courses.CourseTitle,
       Departments.DepartmentName
FROM Courses
JOIN Departments ON Courses.DepartmentID = Departments.DepartmentID
```
{: .query source="Courses,Departments" #q_courses editable="true" }

[each course with its department](#)
{: .datagrid source="q_courses" rows="4" }

**③ Courses per department** — one row per department:

```sql
SELECT Departments.DepartmentID, Departments.DepartmentName,
       COUNT(Courses.CourseID) AS CourseCount
FROM Courses
JOIN Departments ON Courses.DepartmentID = Departments.DepartmentID
GROUP BY Departments.DepartmentID, Departments.DepartmentName
```
{: .query source="Courses,Departments" #q_per_dept editable="true" }

[courses per department](#)
{: .datagrid source="q_per_dept" rows="3" }

**✋ Your move** — the same report, for **majors**. This query still
counts courses. Change it so it counts **majors per department**, in a
column called `MajorCount`:

1. replace `Courses` with `Majors` everywhere (the table and its key:
   `Majors.MajorID`, `Majors.DepartmentID`);
2. rename the count: `COUNT(Majors.MajorID) AS MajorCount`;
3. keep the GROUP BY on the department — and keep
   `Departments.DepartmentID` as the first column: one row, one department.

Press ▶ Run. Mathematical Sciences should host 2 majors.

```sql
SELECT Departments.DepartmentID, Departments.DepartmentName,
       COUNT(Courses.CourseID) AS CourseCount
FROM Courses
JOIN Departments ON Courses.DepartmentID = Departments.DepartmentID
GROUP BY Departments.DepartmentID, Departments.DepartmentName
```
{: .query source="Majors,Courses,Departments" #q_mine editable="true" }

[your answer](#)
{: .datagrid source="q_mine" rows="3" }

The second check at the very bottom stays **red until you do it**.
````
{: .block title="🔎 Practice block" #live }

Two words to keep from this week: a `foreign_key`[^foreign_key] lives
on the MANY side and points up to the ONE side, and a
`group_by`[^group_by] lets only its own fields and aggregates into the
SELECT. The proof below runs the practice block's own queries:

```gherkin
Feature: One fact, one place
  Scenario: The spreadsheet repeats the department on every course
    Given the spreadsheet and the rows carrying Information Studies
    :::python
    self.sheet: Query = self.page.q_sheet
    self.departments: Dataset = Dataset("Departments")
    :::
    When the department gets a new name
    Then five rows carry the name, where the new design keeps one
    :::python
    assert self.sheet.count == 5, self.sheet.count
    names: list[str] = self.departments.values("DepartmentName")
    assert names.count("Information Studies") == 1, names
    :::

  Scenario: Two tables — one row per course
    Given the courses and the query joining their department
    :::python
    self.courses: Dataset = Dataset("Courses")
    self.joined: Query = self.page.q_courses
    :::
    When the courses are joined to their department
    Then there are as many rows as courses
    :::python
    assert self.joined.count == self.courses.count, self.joined.count
    :::

  Scenario: Per department — one row per department
    Given the departments and the courses counted per department
    :::python
    self.departments: Dataset = Dataset("Departments")
    self.per_dept: Query = self.page.q_per_dept
    :::
    When the courses are counted per department
    Then each department is one group, Information Studies with 5
    :::python
    assert self.per_dept.count == self.departments.count, self.per_dept.count
    names: list[str] = self.per_dept.values("DepartmentName")
    counts: list[str] = self.per_dept.values("CourseCount")
    assert str(counts[names.index("Information Studies")]) == "5", counts
    :::
```
{: .feature #activity_proof tags="foreign_key, group_by" visible="true" status="passing" }

And one check that is **yours**. It reads your query in the practice
block and stays red while it still counts courses:

```gherkin
Feature: Your move — majors per department
  Scenario: The majors are counted per department
    Given your query in the practice block
    :::python
    self.mine: Query = self.page.q_mine
    self.majors: Dataset = Dataset("Majors")
    :::
    When you press Run on your query
    Then it counts majors, grouped by the department
    :::python
    flat: str = " ".join(self.mine.query.upper().split())
    assert "FROM MAJORS" in flat, \
        "still counting courses — start from Majors: FROM Majors JOIN Departments …, then press Run"
    group: str = flat.split("GROUP BY")[-1] if "GROUP BY" in flat else ""
    assert "DEPARTMENTID" in group, \
        "keep the group on the department: GROUP BY Departments.DepartmentID, Departments.DepartmentName"
    :::
    And one row per department, Mathematical Sciences with 2 majors
    :::python
    depts: set = set(self.majors.values("DepartmentID"))
    assert self.mine.count == len(depts), self.mine.count
    names: list[str] = self.mine.values("DepartmentName")
    counts: list[str] = self.mine.values("MajorCount")
    assert counts, "name the count: COUNT(Majors.MajorID) AS MajorCount"
    assert str(counts[names.index("Mathematical Sciences")]) == "2", counts
    :::
```
{: .feature #your_move_proof tags="foreign_key" visible="true" status="pending" celebration="true" }

[Browse](#)
{: .folder parent="true" }

```yaml
bot: doc
voice: en-US
face:
  zoom: 1.2
script:
  - say: "Welcome back! Last week you read a database map. This week you start drawing one. Small steps, a little quiz after each, and a messy spreadsheet waiting for your help."
  - at: replay
    do: open
    say: "Step one. Here is last week's question, built one frame at a time, with an editor for every frame. Run them in order. Two errors on the way, and that is fine: each error is a message, not a failure."
  - at: uwm
    do: open
    say: "Step two. UWM needs help. First, explore the real course catalog and note a few courses: department, number, title, credits. Then look at the spreadsheet such notes become. It looks tidy. It is a trap."
  - at: split
    do: open
    say: "Step three. Split it. Two sentences in English first, then the same sentences as a diagram, then the data, then the SQL. Departments above, courses below, one key between them. It is Categories and Products all over again."
  - at: guidelines
    do: open
    say: "Step four. Designers follow conventions, so everyone can read everyone's database: plural table names, singular ID primary keys, foreign keys named like the key they point to, and the many side below."
  - at: first_report
    do: open
    say: "Step five. The first report: which courses belong to each department, and how many. Same shape as last week, same query. The pattern travels."
  - at: two_ways
    do: open
    say: "Step six. Time to step back and see the method: entities, attributes, relationships, layout, and a check against the questions. Every future query can only travel the roads you draw."
  - at: top_of_map
    do: open
    say: "Step seven. The rest of the top of the map: majors, instructors, terms. Grab sticky notes and sketch it. Students, sections and enrollments wait at the bottom, next week."
  - at: live
    do: open
    say: "Here is the practice block. Count the spreadsheet rows to fix, join the two new tables, count courses per department. And your move: the same report for majors. The last check stays red until you do."
stories:
  summarize the page:
    - 'You might wonder: summarize the page'
    - This week we move from reading a database design to drawing one.
    - We replay one query frame by frame, where each error is a message, not a failure.
    - UWM keeps its course information in a spreadsheet that repeats the department name on many rows.
    - The fix is to split it into Departments and Courses, with a DepartmentID foreign key in Courses.
    - Design guidelines keep names, primary keys, foreign keys and layout readable for everyone.
    - The practice block lets you run every step, and your move counts majors per department.
  why not keep everything in one spreadsheet:
    - 'You might wonder: why not keep everything in one spreadsheet'
    - A spreadsheet often types the same fact on many rows, like a department name on every course.
    - When that fact changes, every copy must be fixed, and a forgotten copy becomes a mistake.
    - A database stores each fact once, in its own table, and links to it with a key.
    - Then a change touches one row, and every linked row follows.
  where does the foreign key go:
    - 'You might wonder: where does the foreign key go'
    - The foreign key goes on the MANY side of the relationship.
    - One department offers many courses, so each course carries a DepartmentID.
    - On the map, the table with the foreign key sits below the table it points to.
```
{: .avatar #guide dock="true" size="115" }

[^foreign_key]: **foreign_key** — a column that holds the ID of a row
    in another table, like `Courses.DepartmentID`. It lives on the MANY
    side and points up to the ONE side.
[^group_by]: **group_by** — sorting rows into groups and making one row
    per group. The SELECT may hold only the GROUP BY fields and
    aggregates such as COUNT, SUM or MAX.
