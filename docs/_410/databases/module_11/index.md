# 🌉 11 · From SQL Mastery to NoSQL Beginnings

🎯 A pivotal week: first you prove your SQL, then you open the door to a new family of databases.

Ask Doc for a tour!
{: .avatar_trigger target="guide" }

Welcome back! Ten modules of SQL are behind you: tables, keys, joins,
groups, views, transactions, triggers. This week has two halves:

- **SQL mastery** — a game, **SQuizL**, on the UWM data you know: predict
  an answer, then let the database settle it.
- **NoSQL beginnings** — the same data in other shapes (documents,
  graphs), and a second game: **pick the right database** for a real
  company.

Every game here can be played **three ways** — choose yours each time:

| | How |
|---|---|
| 🧍 **Alone** | Predict, then check with the query or the reveal. The 🏆 counts your points. |
| 👥 **With a person** | Each of you predicts silently on your own screen; count 3… 2… 1… and reveal; then check together. |
| 🤖 **With Ari** | Ari, our Socratic partner, plays against you or questions your choices. Optional: it needs a free AI key (🔑 on Ari's panel). |

The games are **opportunities, not obligations**: they carry the week's
content, and the graded assignment reads what they reveal. Take your time. 🙂

> Why did the SQL query break up with the NoSQL database? It needed more
> structure in the relationship. 💔

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

```json
[
  {"PersonID": 1, "Name": "Matt"},
  {"PersonID": 2, "Name": "Michel"},
  {"PersonID": 3, "Name": "Chris"},
  {"PersonID": 4, "Name": "Ben"}
]
```
{: .dataset #People }

```json
[
  {"ConnectionID": 1, "FromName": "Matt", "ToName": "Chris"},
  {"ConnectionID": 2, "FromName": "Michel", "ToName": "Ben"},
  {"ConnectionID": 3, "FromName": "Chris", "ToName": "Ben"}
]
```
{: .dataset #Connections }


````
### 📚 Step 0 · The data you play with

Every game this week runs on data you can see right here — open this
step whenever you need to look something up.

**The UWM sample data** (module 07) — eight tables, top of the map first:

[Departments](#)
{: .datagrid source="Departments" rows="4" }

[Terms](#)
{: .datagrid source="Terms" rows="4" }

[Courses](#)
{: .datagrid source="Courses" rows="4" }

[Majors](#)
{: .datagrid source="Majors" rows="4" }

[Instructors](#)
{: .datagrid source="Instructors" rows="4" }

[Students](#)
{: .datagrid source="Students" rows="4" }

[Sections](#)
{: .datagrid source="Sections" rows="4" }

[Enrollments](#)
{: .datagrid source="Enrollments" rows="6" }

**The little network** of step 3 — four people, three arrows:

[People](#)
{: .datagrid source="People" rows="4" }

[Connections](#)
{: .datagrid source="Connections" rows="3" }

Tip: in SQuizL, look **here** while you predict; run the query only to
check.
````
{: .accordion #data }

````
### 🏆 Step 1 · SQuizL — predict, then let the database decide

Eight challenges on the **UWM sample data** of module 07 — the tables
are in the **📚 Step 0** just above. For each one:

1. **Predict** — look at the tables of Step 0, then pick your answer in
   the quiz *before* running anything.
2. **Reveal** — the quiz tells you right away, and your 🏆 counts it.
3. **Check** — press ▶ Run on the challenge's query in the practice
   block, and see the database agree.

**No AI to answer for you here** — Ari can be your opponent, never your
helper (see the 🤖 box at the end of this step).

**① Join** — `Students JOIN Majors ON Students.MajorID = Majors.MajorID`.
How many rows?

- [ ] 4, one per major

  > Majors has 4 rows, but the join keeps one row per student.

- [x] 6, one per student

  > Each student has exactly one major, so each of the 6 students finds
  > one partner row. Check: query ① in the practice block.

- [ ] 24, every student with every major

  > That is a join without its ON — a cross product.

- [ ] 10, students plus majors

  > A join pairs rows; it never adds the two tables up.
{: .quiz }

**② LEFT JOIN** — which instructor teaches **no** section in Fall 2026?

- [ ] Codd, too busy with the trigger of module 10

  > Codd teaches two sections this fall: INFOST 410 and INFOST 240.

- [ ] Nobody — every instructor teaches each term

  > One instructor taught only in Spring 2026. The LEFT JOIN finds the
  > rows with no partner.

- [x] Turing

  > Turing's only section is COMPSCI 250 in Spring 2026. The LEFT JOIN
  > keeps him with an empty partner — `IS NULL` keeps only those.

- [ ] Hopper

  > Hopper teaches COMPSCI 250 this fall.
{: .quiz }

**③ GROUP BY** — enrollments per term?

- [ ] 13 and 13, since every term sees every enrollment

  > Each enrollment is in one section, and each section in one term.

- [x] Spring 2026: 5 · Fall 2026: 8

  > One group per term. 5 + 8 = 13, the whole table — nothing lost,
  > nothing doubled.

- [ ] Spring 2026: 8 · Fall 2026: 5

  > Reversed: this fall is the busier term.

- [ ] 2 and 2, one per term
  
  > That counts terms, not enrollments.
{: .quiz }

**④ HAVING** — courses with **more than 2** enrollments, over both terms.
How many courses?

- [ ] 0, since no course is that popular

  > Run it: two courses pass the bar.

- [ ] 1, INFOST 410 only

  > INFOST 410 has 5, but MATH 231 has 4 — also above 2.

- [x] 2 — INFOST 410 (5) and MATH 231 (4)

  > HAVING filters the groups after GROUP BY has counted them.

- [ ] 7, every course
  
  > HAVING keeps only the groups above the bar.
{: .quiz }

**⑤ Subquery** — students whose major belongs to department 1
(Information Studies), with `WHERE MajorID IN (SELECT …)`. How many?

- [ ] 1, since department 1 has one major

  > Right about the major (Information Science and Technology) — but
  > three students chose it.

- [ ] 6, every student

  > The subquery narrows the majors to department 1's.

- [x] 3 — Jay, Max and Lee

  > The inner SELECT returns MajorID 1; the outer one keeps the three
  > students who hold it.

- [ ] 0, since a subquery cannot read another table
  
  > It can — that is what makes it useful.
{: .quiz }

**⑥ ORDER BY … LIMIT 1** — "the student with the most enrollments".
What is wrong with the answer?

- [x] Nothing visible: one name comes back, but two students tie at 3

  > Jay and Max both hold 3 enrollments. LIMIT 1 keeps one of them — and
  > which one depends on the engine. Remove the LIMIT and look.

- [ ] It returns two rows, since LIMIT ignores ties

  > LIMIT 1 always returns at most one row.

- [ ] It returns the student with the fewest enrollments

  > DESC puts the largest first.

- [ ] An error, since LIMIT needs a WHERE
  
  > LIMIT works on its own.
{: .quiz }

**⑦ NULL** — `WHERE Grade = NULL`. How many rows?

- [ ] 8, the Fall 2026 enrollments

  > 8 is the right count for `IS NULL`. With `= NULL`, nothing matches.

- [x] 0

  > NULL is not a value, so nothing ever *equals* it. `IS NULL` finds
  > the 8 enrollments not graded yet.

- [ ] 13, since NULL matches anything

  > NULL matches nothing with `=`.

- [ ] An error, since NULL cannot be written in SQL
  
  > SQL accepts the line — and silently returns nothing. A trap, not an
  > error.
{: .quiz }

**⑧ Integrity** (no query to run here — think back to module 09) — an
INSERT into Enrollments with `SectionID = 99`, a section that does not
exist. In MySQL?

- [ ] It works, and section 99 is created automatically

  > Nothing is created behind your back.

- [ ] It works, with SectionID set to NULL

  > The value you wrote is kept — and refused.

- [x] Refused: Error 1452, a foreign key fails

  > The FK on SectionID points to Sections; a value with no parent row
  > is refused — integrity at work, the C of ACID.

- [ ] Refused: Error 1062, a duplicate key
  
  > 1062 is a repeated primary key. Here the parent is missing.
{: .quiz }

**🤖 Play SQuizL against Ari** (optional). Lock your round on the card —
the challenge number and **your** answer letter (A = first option) — then
press Ask. Ari picks its own answer with a one-line reason, never changes
yours, and sends you to the query to settle who wins.

```yaml
challenge: {value: 1, options: [1, 2, 3, 4, 5, 6, 7]}
my_answer: {value: "-", options: ["-", A, B, C, D]}
```
{: .form editable="true" #round title="🎴 My locked round" }

```yaml
name: Ari
icon: 🤓
provider: groq
model: openai/gpt-oss-120b
intro: "Lock your answer on the card, then challenge me. ✊"
max_tokens: 600
placeholder: "Ready? Ask me to reveal."
system: |
  You are Ari, a playful SQuizL opponent for INFOST 410 (Databases, Michel Zam, UWM).
  You read the student's locked round: the challenge number and their answer letter.
  Data: UWM sample data (module 07). Tables: Departments(3), Terms(Spring 2026, Fall 2026),
  Courses(7), Majors(4), Instructors(Codd, Hopper, Noether, Turing), Students(6: Jay, Max,
  Miranda, Bill, Ana, Lee), Sections(7), Enrollments(13; the 8 of Fall 2026 have Grade NULL).
  Challenges (options in order A, B, C, D):
  1. Students JOIN Majors: how many rows? A 4 · B 6 · C 24 · D 10
  2. LEFT JOIN: which instructor teaches no section in Fall 2026? A Codd · B Nobody · C Turing · D Hopper
  3. GROUP BY: enrollments per term? A 13 and 13 · B Spring 5, Fall 8 · C Spring 8, Fall 5 · D 2 and 2
  4. HAVING: courses with more than 2 enrollments? A 0 · B 1 · C 2 · D 7
  5. Subquery: students whose major is in department 1? A 1 · B 6 · C 3 · D 0
  6. ORDER BY ... LIMIT 1, most enrollments: what is wrong? A a tie is hidden · B two rows · C fewest · D error
  7. WHERE Grade = NULL: how many rows? A 8 · B 0 · C 13 · D error
  Rules:
  - If my_answer is "-", say only: lock your answer on the card first. Never reveal anything.
  - Otherwise: give YOUR pick (one letter) with one short reason, in two lines at most.
    You may disagree with the student. Never say who is right.
  - End every reply with: "Run query N in the practice block — the database decides. 🏁"
  - Never write the SQL, never explain the full solution. Light humor, one emoji at most.
```
{: .agent #rival bound="{= dict(challenge=round.challenge, my_answer=round.my_answer) }" rows="2" }
````
{: .accordion #squizl }

````
### 🗂️ Step 2 · SQL and NoSQL — two families

[SQL and NoSQL](_slides/m11_sql_vs_nosql.jpg)
{: .embed image="true" width="100%" }

Everything so far was **relational**: fixed tables, rows and columns, a
schema decided first, keys and joins to connect facts. **NoSQL** ("not
only SQL") names the families that store data differently:

| Family | Stores | Example |
|---|---|---|
| 📄 Document | JSON-like documents, nested | MongoDB, CouchDB |
| 🔑 Key-value | a value behind each key | Redis, DynamoDB |
| 🧱 Wide column | huge tables of columns, written fast | Cassandra, HBase |
| 🕸️ Graph | nodes and the relationships between them | Neo4j |

**Q:** Which sentence fits a **document** database?

- [ ] Every row must have exactly the same columns

  > That is the relational promise — a fixed schema.

- [x] One record can nest its own lists and sub-objects

  > A student document can carry its enrollments inside it. No join
  > needed to read them — but the same fact may be stored twice.

- [ ] Relationships are stored as edges between nodes

  > That is a graph database.

- [ ] Only one value is stored, behind a key
  
  > That is a key-value store.
{: .quiz }
````
{: .accordion #families }

````
### 🕸️ Step 3 · Same data, three shapes

A tiny network from the slides: four people, three connections —
**Matt → Chris**, **Michel → Ben**, **Chris → Ben**.

**As rows** (relational) — the two tables are in 📚 Step 0: `People` and
`Connections`, one row per arrow.

**As a document** (MongoDB style) — one person with their connections
nested inside:

~~~json
{ "name": "Matt",
  "connectedTo": [ { "name": "Chris",
                     "connectedTo": [ { "name": "Ben" } ] } ] }
~~~

**As a graph** (Neo4j, Cypher) — nodes and arrows, written as you would
draw them:

~~~text
CREATE (:Person {name:"Matt"}), (:Person {name:"Michel"}),
       (:Person {name:"Chris"}), (:Person {name:"Ben"});
MATCH (a:Person {name:"Matt"}),  (x:Person {name:"Chris"}) CREATE (a)-[:CONNECTED_TO]->(x);
MATCH (b:Person {name:"Michel"}), (y:Person {name:"Ben"})  CREATE (b)-[:CONNECTED_TO]->(y);
MATCH (x:Person {name:"Chris"}), (y:Person {name:"Ben"})   CREATE (x)-[:CONNECTED_TO]->(y);

MATCH (a:Person {name:"Matt"})-[:CONNECTED_TO*]->(c)
MATCH (b:Person {name:"Michel"})-[:CONNECTED_TO*]->(c)
RETURN DISTINCT c;
~~~

The last three lines ask: **who can both Matt and Michel reach, however
many hops away?** Cypher says it with `*` — any number of arrows.

In SQL, each hop is **one more join** of Connections with itself. Run
**⑨** and **⑩** in the practice block: Matt reaches Chris and Ben; the
person both reach is **Ben**. Two hops already take a self-join and a
subquery — imagine six.

**Q:** Why does the graph shape suit "who can reach whom"?

- [ ] Graphs store more data than tables

  > Same four people, same three arrows. The difference is how the
  > question is asked.

- [ ] SQL cannot store connections at all

  > It can — the Connections table does. Querying many hops is the hard
  > part.

- [x] Following arrows is the native move: `*` means any number of hops

  > In SQL every extra hop is another self-join; in Cypher, one star.

- [ ] Neo4j has no keys, so it is faster
  
  > Nodes still have identities. Speed comes from storing the arrows
  > themselves.
{: .quiz }
````
{: .accordion #shapes }

````
### ⚖️ Step 4 · Choosing a database — the criteria and CAP

[CAP theorem — a database for each pair](_slides/m11_cap.jpg)
{: .embed image="true" width="100%" }

The criteria, in a line each:

- **Scalability** — add servers (horizontal) rather than a bigger one.
- **Schema flexibility** — can the structure evolve without a migration?
- **Performance** — fast writes, or fast reads?
- **Consistency and availability** — the **CAP theorem** (Eric Brewer):
  a distributed database guarantees only **two** of **C**onsistency,
  **A**vailability, **P**artition tolerance.
- **Cost**, and **ease of use and integration**.

**Q:** A shopping cart must stay available during a network split, even
if two servers briefly disagree. Which CAP pair?

- [ ] CA — consistent and available, no partitions allowed

  > A cart spread over servers must survive a split: P is required.

- [ ] CP — consistent, even if the cart is unavailable for a while

  > A cart that refuses to load loses sales. Availability matters more.

- [x] AP — available and partition tolerant, eventually consistent

  > The DynamoDB pick in the slide: always answer, agree a moment later.

- [ ] All three, with a good enough server
  
  > Brewer's point: during a partition, you choose two.
{: .quiz }
````
{: .accordion #criteria }

````
### 🗳️ Step 5 · Pick the database — four real cases

[Case studies](_slides/m11_case_studies.jpg)
{: .embed image="true" width="100%" }

Four companies, four needs. **Your turn to decide** — for each case:
the data **shape**, the **CAP** pair that matters, the **database**, and
**why**.

| Case | The need |
|---|---|
| 🛒 E-commerce (Amazon) | huge transaction volumes, low latency, AWS integration |
| 🤝 Social media (LinkedIn) | complex relationships between users, posts, comments |
| 📰 Content management (Strapi) | flexible content structure, nested data |
| 📈 Real-time analytics (Instagram) | floods of time-series writes, always available |

Play it **your** way:

- 🧍 **Alone** — fill the card below for one case, then answer the
  reveal quiz: it tells you what the company chose.
- 👥 **With a person** — each fills a card silently; reveal; argue for
  one minute each; then the quiz settles it.
- 🤖 **With Ari** — fill the card and press Ask. Ari never names a
  database first: it asks questions until your **why** holds.

```yaml
case: {value: "E-commerce (Amazon)", options: ["E-commerce (Amazon)", "Social media (LinkedIn)", "Content management (Strapi)", "Real-time analytics (Instagram)", "My own app"]}
shape: {value: "-", options: ["-", "Rows and joins", "Documents", "Graph of relationships", "Key-value", "Wide columns / time series"]}
cap: {value: "-", options: ["-", "CA", "CP", "AP"]}
database: {value: "-", options: ["-", "MySQL", "MongoDB", "Cassandra", "Redis", "HBase", "CouchDB", "Neo4j", "DynamoDB"]}
why: "one sentence, your own words"
```
{: .form editable="true" #card title="🗳️ My decision card" }

```yaml
name: Ari
icon: 🤓
provider: groq
model: openai/gpt-oss-120b
intro: "Show me your card. I only ask questions. 🧭"
max_tokens: 700
placeholder: "Ask me to challenge your card."
system: |
  You are Ari, the Socratic partner of INFOST 410 (Databases, Michel Zam, UWM), module 11:
  choosing a NoSQL database. You read the student's decision card: case, data shape,
  CAP pair, database, why.
  The criteria taught: scalability (horizontal), schema flexibility, read/write
  performance, consistency and availability (CAP: a distributed database keeps two of
  Consistency, Availability, Partition tolerance), cost, ease of use and integration.
  The CAP table taught: MySQL CA (not distributed); MongoDB AP; Cassandra AP; Redis
  cluster CP; HBase CP; CouchDB AP; Neo4j CP; DynamoDB AP (eventually consistent).
  How you help:
  - One question per reply, two sentences at most. Never two questions.
  - Never name a database the student has not named. Never fill the card.
  - If a field is "-" or the why is the placeholder, ask about that field first.
  - Test the why against the case's need: ask what would break, what grows, what must
    never be wrong, what must always answer.
  - When card and need agree and the why names a criterion, say so in one line and
    suggest they check the reveal quiz. Do not say whether the company chose the same.
  - Light humor, one emoji at most.
```
{: .agent #advisor bound="{= dict(case=card.case, shape=card.shape, cap=card.cap, database=card.database, why=card.why) }" rows="2" }

**The reveal** — what each company chose (from the slides):

**Q:** 🛒 **E-commerce (Amazon)** chose…

- [ ] Neo4j, for the relationships between customers

  > Relationships matter less here than raw volume and latency.

- [ ] MySQL, for strong ACID transactions

  > A classic pick for a bank — but this platform needed to scale out.

- [x] DynamoDB — scalability, low latency, AWS integration

  > A massively scalable key-value store, AP, eventually consistent.

- [ ] Cassandra, for time-series writes
  
  > Cassandra is the analytics case's pick.
{: .quiz }

**Q:** 🤝 **Social media (LinkedIn)** chose…

- [ ] MongoDB, for flexible posts

  > Posts are flexible, but the hard part is the web of relationships.

- [x] Neo4j — relationships between users, posts and comments

  > A graph database: following connections is its native move.

- [ ] Redis, for fast caching

  > Redis caches sessions and counters, not a social graph.

- [ ] DynamoDB, for scale
  
  > Scale matters, but the queries are about connections.
{: .quiz }

**Q:** 📰 **Content management (Strapi)** chose…

- [x] MongoDB — flexible document model, nested content

  > Each piece of content is a document with its own nested structure.

- [ ] HBase, for analytics

  > HBase is a big-data column store.

- [ ] Neo4j, for links between pages

  > Links exist, but the need is flexible nested content.

- [ ] MySQL, for a fixed schema
  
  > A fixed schema is exactly what a CMS wanted to avoid.
{: .quiz }

**Q:** 📈 **Real-time analytics (Instagram)** chose…

- [ ] Neo4j, for the followers graph

  > The case is about machinery data, written fast, not followers.

- [ ] MongoDB, for documents

  > Documents fit content; this need is a flood of time-series writes.

- [ ] Redis, for counters
  
  > Counters are fast, but the data must also be stored at scale.

- [x] Apache Cassandra — fast writes, high availability, no single point of failure

  > A wide-column store, AP: it scales horizontally and keeps writing.
{: .quiz }
````
{: .accordion #pick }

````
### 🧪 Step 6 · Try them for real (optional)

Two free playgrounds, if you want to feel the difference:

- **Neo4j** — open the console at
  [console-preview.neo4j.io](https://console-preview.neo4j.io/onboarding)
  (free sign-up), paste the Cypher of step 3, and run it. **You should
  see:** one node, **Ben**. Want more? The free course
  [Neo4j Fundamentals](https://graphacademy.neo4j.com/courses/neo4j-fundamentals/?category=beginners).
- **MongoDB** — open [mycompiler.io](https://www.mycompiler.io/new/mongodb)
  (no sign-up), paste and run:

~~~text
db.students.insertMany([
  { id: 1, name: 'Ryan',   gender: 'M' },
  { id: 2, name: 'Joanna', gender: 'F' }
]);
db.students.find({ gender: 'F' });
~~~

[MongoDB on mycompiler](_slides/m11_mongodb.jpg)
{: .embed image="true" width="100%" }

**You should see:** two inserted ids, then one document — **Joanna**. The
`find` is a WHERE without SQL: a document that matches the pattern.

**Q:** `db.students.find({ gender: 'F' })` is closest to which SQL?

- [ ] `INSERT INTO students VALUES ('F')`

  > find reads; insertMany wrote.

- [x] `SELECT * FROM students WHERE gender = 'F'`

  > A filter written as a document: every field you give must match.

- [ ] `SELECT gender FROM students GROUP BY gender`

  > No grouping here — one filter, matching documents.

- [ ] `DELETE FROM students WHERE gender = 'F'`
  
  > find never changes anything.
{: .quiz }
````
{: .accordion #try_it }

````
### 🔎 Practice block — the queries that settle the games

The queries that settle the games — on the data of the 📚 step at the top.

**① Join**

```sql
SELECT Students.StudentID, Students.FirstName, Majors.MajorName
FROM Students
JOIN Majors ON Students.MajorID = Majors.MajorID
```
{: .query source="Students,Majors" #q1 editable="true" }

[①](#)
{: .datagrid source="q1" rows="3" }

**② LEFT JOIN** — instructors with no Fall 2026 section

```sql
SELECT Instructors.InstructorID, Instructors.LastName
FROM Instructors
LEFT JOIN (SELECT Sections.InstructorID AS TaughtBy
           FROM Sections JOIN Terms ON Sections.TermID = Terms.TermID
           WHERE Terms.TermName = 'Fall 2026') AS Fall
       ON Instructors.InstructorID = Fall.TaughtBy
WHERE Fall.TaughtBy IS NULL
```
{: .query source="Instructors,Sections,Terms" #q2 editable="true" }

[②](#)
{: .datagrid source="q2" rows="1" }

**③ GROUP BY** — enrollments per term

```sql
SELECT Terms.TermID, Terms.TermName, COUNT(Enrollments.EnrollmentID) AS Enrolled
FROM Enrollments
JOIN Sections ON Enrollments.SectionID = Sections.SectionID
JOIN Terms ON Sections.TermID = Terms.TermID
GROUP BY Terms.TermID, Terms.TermName
```
{: .query source="Enrollments,Sections,Terms" #q3 editable="true" }

[③](#)
{: .datagrid source="q3" rows="2" }

**④ HAVING** — courses with more than 2 enrollments

```sql
SELECT Courses.CourseID, Courses.CourseNumber, COUNT(Enrollments.EnrollmentID) AS Enrolled
FROM Enrollments
JOIN Sections ON Enrollments.SectionID = Sections.SectionID
JOIN Courses ON Sections.CourseID = Courses.CourseID
GROUP BY Courses.CourseID, Courses.CourseNumber
HAVING COUNT(Enrollments.EnrollmentID) > 2
```
{: .query source="Enrollments,Sections,Courses" #q4 editable="true" }

[④](#)
{: .datagrid source="q4" rows="2" }

**⑤ Subquery** — students whose major is in department 1

```sql
SELECT Students.StudentID, Students.FirstName
FROM Students
WHERE Students.MajorID IN (SELECT Majors.MajorID FROM Majors
                           WHERE Majors.DepartmentID = 1)
```
{: .query source="Students,Majors" #q5 editable="true" }

[⑤](#)
{: .datagrid source="q5" rows="3" }

**⑥ ORDER BY … LIMIT 1** — then delete the LIMIT line and run again

```sql
SELECT Students.StudentID, Students.FirstName,
       COUNT(Enrollments.EnrollmentID) AS Taken
FROM Students
JOIN Enrollments ON Students.StudentID = Enrollments.StudentID
GROUP BY Students.StudentID, Students.FirstName
ORDER BY Taken DESC
LIMIT 1
```
{: .query source="Students,Enrollments" #q6 editable="true" }

[⑥](#)
{: .datagrid source="q6" rows="3" }

**⑦ NULL** — then write `IS NULL` instead of `= NULL`

```sql
SELECT * FROM Enrollments
WHERE Enrollments.Grade = NULL
```
{: .query source="Enrollments" #q7 editable="true" }

[⑦](#)
{: .datagrid source="q7" rows="3" }

**⑨ Two hops** — every path of two arrows

```sql
SELECT HopOne.FromName AS StartName, HopOne.ToName AS ViaName,
       HopTwo.ToName AS ReachedName
FROM Connections AS HopOne
JOIN Connections AS HopTwo ON HopOne.ToName = HopTwo.FromName
```
{: .query source="Connections" #q9 editable="true" }

[⑨](#)
{: .datagrid source="q9" rows="1" }

**⑩ Who can both Matt and Michel reach?** — Matt in two hops, Michel in one

```sql
SELECT HopTwo.ToName AS ReachedName
FROM Connections AS HopOne
JOIN Connections AS HopTwo ON HopOne.ToName = HopTwo.FromName
WHERE HopOne.FromName = 'Matt'
  AND HopTwo.ToName IN (SELECT Connections.ToName FROM Connections
                        WHERE Connections.FromName = 'Michel')
```
{: .query source="Connections" #q10 editable="true" }

[⑩](#)
{: .datagrid source="q10" rows="1" }

**✋ Your move** — **everyone Matt can reach, in one hop or two.** This
query only finds one hop. Add the second hop with `UNION` and the
self-join of ⑨, keeping the column name `ReachedName`, then press ▶ Run.
Two people should come back.

```sql
SELECT Connections.ToName AS ReachedName
FROM Connections
WHERE Connections.FromName = 'Matt'
```
{: .query source="Connections" #q_mine editable="true" }

[your answer](#)
{: .datagrid source="q_mine" rows="2" }

The second check at the very bottom stays **red until you do it**.
````
{: .block title="🔎 Practice block" #live }

Two ideas to keep from this week: the same facts fit in rows, documents
or a graph, and the `cap`[^cap] theorem says which two guarantees a
distributed database keeps. The proof below runs the practice block's
own queries:

```gherkin
Feature: The database settles the games
  Scenario: SQuizL's challenges answer as the quiz says
    Given the UWM sample data and the challenge queries
    :::python
    self.q1: Query = self.page.q1
    self.q2: Query = self.page.q2
    self.q4: Query = self.page.q4
    self.q7: Query = self.page.q7
    :::
    When each challenge query runs
    Then the join keeps 6 rows, Turing teaches nothing this fall, two courses pass HAVING, = NULL finds nothing
    :::python
    assert self.q1.count == 6, self.q1.count
    assert self.q2.values("LastName") == ["Turing"], self.q2.values("LastName")
    assert self.q4.count == 2, self.q4.count
    assert self.q7.count == 0, self.q7.count
    :::

  Scenario: Two hops in SQL find Ben
    Given the network of step 3
    :::python
    self.both: Query = self.page.q10
    :::
    When the two reaches are crossed
    Then Ben is the one both Matt and Michel reach
    :::python
    assert self.both.values("ReachedName") == ["Ben"], self.both.values("ReachedName")
    :::
```
{: .feature #activity_proof tags="cap" visible="true" status="passing" }

And one check that is **yours**. It reads your query in the practice
block and stays red while it finds only one hop:

```gherkin
Feature: Your move — everyone Matt can reach
  Scenario: One hop or two
    Given your query in the practice block
    :::python
    self.mine: Query = self.page.q_mine
    :::
    When you press Run on your query
    Then it adds a second hop with UNION
    :::python
    flat: str = " ".join(self.mine.query.upper().split())
    assert "UNION" in flat, "add the second hop: UNION SELECT … the self-join of ⑨ … WHERE HopOne.FromName = 'Matt'"
    :::
    And Chris and Ben come back
    :::python
    names: list = sorted(str(n) for n in self.mine.values("ReachedName"))
    assert names == ["Ben", "Chris"], names
    :::
```
{: .feature #your_move_proof tags="cap" visible="true" status="pending" celebration="true" }

[Browse](#)
{: .folder parent="true" }

```yaml
bot: doc
voice: en-US
face:
  zoom: 1.2
script:
  - say: "Welcome back! A pivotal week. First you prove your SQL with a game, then you open the door to NoSQL. Every game plays three ways: alone, with a person, or with Ari. All optional, all worth it."
  - at: data
    do: open
    say: "Step zero. The data you play with: the eight UWM tables you know, and a little network of four people. Look here whenever you need to."
  - at: squizl
    do: open
    say: "Step one. SQuizL. Eight challenges on the UWM data. Predict first, the quiz reveals, then the query in the practice block settles it. Ari can be your opponent, never your helper."
  - at: families
    do: open
    say: "Step two. Relational is one family. NoSQL names the others: documents, key value, wide columns, and graphs."
  - at: shapes
    do: open
    say: "Step three. Four people, three arrows, three shapes: rows, a document, a graph. In SQL every hop is one more join. In Cypher, a single star."
  - at: criteria
    do: open
    say: "Step four. How to choose: scalability, flexibility, performance, cost, and the CAP theorem. A distributed database keeps only two of consistency, availability and partition tolerance."
  - at: pick
    do: open
    say: "Step five. Four real companies. Fill your decision card: the shape, the CAP pair, the database, and why. Then the reveal tells you what they chose."
  - at: try_it
    do: open
    say: "Step six, optional. Try Neo4j and MongoDB for real, in two free playgrounds. You should see Ben, then Joanna."
  - at: live
    do: open
    say: "Here is the practice block, the queries that settle the games. Your move: everyone Matt can reach, in one hop or two. The last check stays red until you do."
stories:
  summarize the page:
    - 'You might wonder: summarize the page'
    - This week you prove your SQL with a game, then meet NoSQL.
    - SQuizL asks eight questions on the UWM data, and the database settles each one.
    - NoSQL stores data as documents, key values, wide columns or graphs.
    - The CAP theorem says a distributed database keeps two of three guarantees.
    - Picking a database means matching its shape and its CAP pair to the need.
  how do I play with ari:
    - 'You might wonder: how do I play with Ari'
    - Ari is optional, and needs a free AI key, saved with the key button on its panel.
    - In SQuizL, lock your answer on the card first, then ask Ari to reveal its own.
    - In the decision game, Ari reads your card and only asks questions.
  sql or nosql:
    - 'You might wonder: SQL or NoSQL'
    - Choose SQL when the facts must stay consistent and the structure is stable.
    - Choose a NoSQL family when the shape, the scale, or the speed asks for it.
    - Many real systems use both, each for what it does best.
```
{: .avatar #guide dock="true" size="115" }

[^cap]: **cap** — the CAP theorem (Eric Brewer): a distributed database
    can guarantee only two of Consistency, Availability and Partition
    tolerance at the same time.
