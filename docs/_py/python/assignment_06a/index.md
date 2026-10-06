# 📍 Assignment 6a — Hidden Gems: Crypto

Some values contain hidden gems — characters inside strings. Two functions
this week: **encrypt** hides a word, **decrypt** brings it back, and the
program proves nothing was lost on the way.

## 🎓 Ari, your tutor

Stuck? Say where. Ari reads your program and what it printed, then points —
to the week's table, to one line to try. It never writes the program for
you; that is yours.

```yaml
provider: groq
model: openai/gpt-oss-120b
intro: "Stuck? Tell me where. I point, you write."
placeholder: "What are you trying to do, and what happens instead?"
system: |
  You are Ari, the tutor of INFOST 350, Assignment 6a (Hidden Gems — Crypto,
  Module 6). Directions only, never the answer: one idea per message, one
  line or a blank to fill at most, only what Module 6 and before have taught.
  (Placeholder — the sealed brief replaces this.)
```
{: .agent #tutor bound="program" rows="3" }

## 🐍 Your program

Every program opens on its **elevator pitch**, in the docstring — four
lines: *For* whom, *Who wants* what, *Our app is*, *With* what benefit —
then the three parts, each under its comment: `# read console`,
`# computations`, `# print result back to console`. The starter below has
the pitch written and the two functions waiting. Run with ▶; the consistency
check at the end is your test.

```python
"""
For Sam, who keeps a word nobody else should read
Who wants to hide it and get it back, nothing lost on the way
Our app is a tiny crypto kit: encrypt, then decrypt
With one rule that shifts letters, and a check that it is reversible
"""


def encrypt(word: str) -> str:
    '''Encrypt the input word'''
    # TODO: implement the encryption logic here
    return ''


def decrypt(word: str) -> str:
    '''Decrypt the input word'''
    # TODO: implement the decryption logic here
    return ''


# read console
word2hide = input('Word to hide: ')

# computations
secret = encrypt(word2hide)
cleared = decrypt(secret)

# print result back to console
print(f'{secret = }')
print(f'{cleared = }')
print(f'Consistency check: {cleared == word2hide}')
```
{: .run #program }

Suggested rule, or invent your own: replace each lowercase letter with the
next one in the alphabet — a → b, b → c, … z → a (wrap around!). Test with a
few words, including `decrypt(encrypt("hello")) == "hello"`.

## 💎 This week's key concepts

The table at the end of the Module 6 deck — what exists this week. Both you
and Ari work from it.

| Operation | str example | list example | Result |
|---|---|---|---|
| `len()` | `len("abc")` | `len([1, 2, 3])` | Number of elements |
| Indexing | `"abc"[1]` | `[10, 20][0]` | Element at a position (`'b'`, `10`) |
| Slicing | `"hello"[1:4]` | `[10, 20, 30, 40][1:3]` | A subsequence (`'ell'`, `[20, 30]`) |
| `in` | `'a' in "cat"` | `20 in [10, 20, 30]` | Membership: True or False |
| `.index(x)` | `"hello".index("e")` | `[1, 2, 3].index(2)` | First index of x, or an error |
| `.find(x)` | `"hello".find("e")` | — | Index of x, or -1 if not found |
| `.count(x)` | `"hello".count("l")` | `[1, 2, 2, 3].count(2)` | How many times x appears |
| `+` | `"Hi " + "there!"` | `[1, 2] + [3]` | Joins sequences |
| `*` | `"ha" * 3` | `[0] * 4` | Repeats (`'hahaha'`, `[0, 0, 0, 0]`) |
| `for` | `for c in "hi": …` | `for x in [1, 2]: …` | Loop through items |
| `.append(x)` | — | `[1, 2].append(3)` | Adds an item at the end |
| `.upper()` | `"hello".upper()` | — | `'HELLO'` |
| `.split()` | `"a,b".split(",")` | — | A list from a string |
| `.join()` | `",".join(["a", "b"])` | — | One string from a list |

## 📬 Submit

In Canvas, as Assignment 6a says. Nothing is saved on this page: keep your
program on PythonAnywhere or in a file of your own.

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
