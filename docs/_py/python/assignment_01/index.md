# 📍 Assignment 01

**Draft — the brief is not written yet.** The page is the shape every
assignment will have: the tutor, your program, the proof.

## 🎓 Your tutor

Ask it anything about this week's work. It knows the lesson and how Michel
explains things; it will point you to the right place and ask you the next
question. It never writes your program — that is yours.

```yaml
provider: groq
model: openai/gpt-oss-120b
intro: "Stuck? Tell me where. I point, you write."
placeholder: "What are you trying to do, and what happens instead?"
system: |
  You are the tutor of Michel's Python class, assignment 01.
  You give DIRECTIONS, never the answer: name the lesson, the idiom, the
  next thing to try, the question to ask oneself. Never write the student's
  program or a line that solves the assignment. Short answers, one step at
  a time. (Placeholder — the sealed brief replaces this.)
```
{: .agent #tutor bound="program" rows="3" }

## 🐍 Your program

Write here, run with ▶. The tutor sees what you wrote and what it printed
when you ask — not before.

```python
# Assignment 01 — your program starts here
print("hello, Python")
```
{: .run #program }

When it does what the assignment asks, copy your program into Canvas as
the assignment says. Nothing is saved on this page: keep your work in Canvas
or in a file of your own.

## 🧪 Proof

```gherkin
Feature: The assignment page has a tutor and a place to run
  As a student of the Python class
  I want a tutor beside my program on every assignment page
  So that I can get a direction without leaving the page

  Scenario: The tutor is there, bound to the program
    Given the assignment page
    :::python
    self.tutor: Agent = self.page.tutor
    runners = Object._all("#lc-pyrun-program")
    self.program = runners[0] if runners else Object(None)
    :::
    When a student opens it from Canvas
    Then the tutor and the program are on the page
    :::python
    assert self.tutor.exists, "no tutor on the page"
    assert self.program._el is not None, "no program block on the page — the run block must be #program"
    :::
    And the tutor reads the program when asked
    :::python
    link = self.tutor._q(".lc-agent-bound")
    assert link._el is not None and "program" in str(link._el.textContent), \
        "the tutor is not bound to the program block — bound=\"program\" on its decoration"
    :::
```
{: .feature #assignment_proof visible="true" status="pending" tags="python,tutor" }

[in this course](#)
{: .folder parent="true" }
