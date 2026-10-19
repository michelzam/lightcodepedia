# 🗄 Database

🏢 **Advanced, enterprise-grade.** A class on a page becomes a table in a
real database, shared by a whole class, a team, a company — rows that
outlive the page, the browser and the day. This page lists what the door
can do. It shows no key, names no provider and runs no example: the
setup is done with you, for your own database. **Get in touch** — a
contact line will appear here soon.

## 🚪 One line, one door

A database is **one line** on the page, a link whose scheme says the
kind of service and whose decoration gives it a name:

````markdown
[the shelter](…://shelter)
{: .database #shelter unlisted="…" }
````
{: .code title="🗄 The database line — scheme and key arrive with the setup" }

The page holds **no key**: the address and the public key live in a
course-level file the page reads once, never in the material, never in a
learner's copy. What the page does hold is the database's **unlisted
name**, the way a document is shared "anyone with the link": whoever has
the page reads and adds; nobody else even sees the tables.

Then any class declares that it lives there, and each class is a table:

````markdown
```python
class Walk(Object):
    dog = Attr(Dog)
    walker = Attr(str)
    hour = Attr(datetime, datetime.now, ro=True)
```
{: .model source="shelter" }

[the walks](#)
{: .datagrid source="Walk" #walks }
````
{: .code title="🧥 A class that lives in the database — its table has the same name" }

No SQL, no address, no connection code: the [class](dataset#a-class-as-source--the-list-dressed)
is the whole contract.

## 🧰 What the door does

- **A table per class.** The class makes its table on the author's device
  the first time; the columns follow the attributes — typed, defaulted,
  read-only where the class says so. A reference (`dog = Attr(Dog)`) is a
  column of ids shown as names, picked from the other table.
- **Saves by itself.** ➕ New, an edit in a cell or a card, a verb's
  effect — each change goes to the table as soon as it has a value, and
  once. The grid says so: **●** waiting, **⟳** on its way, **✓** saved,
  **⚠** refused (tap to try again). No Save button to forget.
- **Reads the others'.** **↻** fetches what classmates saved since; a
  refresh of the page comes back to the same rows.
- **The table keeps its own notes.** When a row last changed, how, and
  from where, in `_`-prefixed columns the page never shows and never
  sends — an audit trail for free.
- **Inheritance travels.** A subclass (`class Sprint(Walk)`) saves in its
  parent's table with its own columns and its kind in a `_sub` column;
  one list holds both, each row knowing what it is.
- **The structure evolves under control.** Rename an attribute
  (`was="old"`), add one, remove one, add a subclass: the page **freezes
  the rows**, lists the steps, and the database's **owner** reviews and
  applies them from the app's title — 🔄 *n changes*. A learner's edit
  never alters a table's shape; a column no class answers to is offered to
  🧹, never dropped silently.
- **An unlisted name instead of an account.** Students need no sign-up:
  the name on the line is the key to the class's tables, and only to
  those.
- **A SQL door, too.** For a warehouse, the same line names it and a SQL
  fence runs on it through a proxy you host — the fence holds the
  statement, the line says where it runs.
- **Honest when it cannot.** An unreachable database says so under the
  grid, as a line, never as a fake row; a wrong name on the author's
  device says which one to put.

## 🧭 What it is for

A class register that the whole room writes in. A shared log on a shop
floor. A small operational app — reservations, visits, walks — built in
a lesson's afternoon and kept for a season. Anything where *everyone
adds rows and only the owner changes what a row is.*

## 🔐 What it is not

Not a place for secrets: the page's key is a **public** one, scoped by
the provider's rules and by the unlisted name. Not a replacement for
your system of record: it is the fastest honest door between a page and
a table. Row-level identity (who wrote this row, "my rows only") is the
next step, and part of the conversation.

## 🤝 Talk to us

This feature is set up with you: the service, the tables' home, the
owner's device, the course file that carries the key. **No contact
information yet** — it will be on this page when the door opens.

## 🔗 Related components & examples

```
/components/dataset
/components/model
/components/form
```
{: .related }
