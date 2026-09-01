# 🛗 Pitch elevator

Every app starts as a **sentence**. Say who it is for, say what it changes —
then meet the three steps that turn that sentence into a program: **read**,
**compute**, **write back**.

## 🎤 The pitch
{: .accordion open="true" }

Fill the blanks out loud, in one breath. That is the whole ride: **an
elevator pitch** is a promise short enough to say between two floors.

> For **&lt;students&gt;** who want to **&lt;taste programming without being burned&gt;**  
> Who need **&lt;a gentle, warming first experience&gt;**  
> Our app is a **&lt;learning tool&gt;** like **&lt;a cup of hot chocolate&gt;**  
> With **&lt;simple code that comforts, not intimidates&gt;**

The bold parts are the only ones that matter — the rest is scaffolding. Your
turn:

> For **&lt;who&gt;** who want to **&lt;what they wish for&gt;**  
> Who need **&lt;what is missing today&gt;**  
> Our app is a **&lt;kind of thing&gt;** like **&lt;something familiar&gt;**  
> With **&lt;what makes it yours&gt;**

That last comparison is where your passion goes. Hot chocolate is one
answer. Yours will be another.

## 🖥 The app
{: .accordion open="true" }

Here is the finished thing, the way a user meets it: a box to fill, a button
to press, an answer that was not there before.

```
name: your name
```
{: .form editable="true" #ask title="Say hello" }

[▶ Say hello](#)
{: .button #say }

```python
name = button.page.ask.data.name
message = f"Hi {name}, welcome to coding. Take it slow, like hot chocolate."
button.page.out.set("message", message)
```
{: .onclick }

```
message: ""
```
{: .form #out title="What the program says" }

Three lines behind that button, and they are the three steps of every
program ever written: it **read** what you typed, it **computed** a
sentence, it **wrote** the answer back.

## 🐍 The code
{: .accordion open="true" }

The same program, written the way you will write it for real. Change a
string, press ▶ Run.

```python
"""
For <students> who want to <taste programming without being burned>
Who need <a gentle, warming first experience>
Our app is a <learning tool> like <a cup of hot chocolate>
With <simple code that comforts, not intimidates>
"""

# read
name: str = "your name"

# computation
message: str = f"Hi {name}, welcome to coding. Take it slow, like hot chocolate."

# write back
print(message)
```
{: .run rows="16" }

**Why not `input()` here?** A web page has no console to type into. `input()`
would sit there waiting for one and freeze the tab, so this runner refuses it
and says so. In a real terminal — PythonAnywhere, or Python on your machine —
`input("name: ")` is exactly the right first line, and it plays the part the
box above plays here.

## 🦄 Does it work?
{: .accordion }

The page checks itself: it fills the box, presses the button, and reads the
answer back.

```gherkin
Feature: The button turns a name into a welcome
  As a beginner
  I want to press one button and see my own words come back
  So that I can watch a program work before I write one

  Scenario: An empty message waits for the button
    Given a fresh page
    :::python
    self.out: Form = self.page.out
    :::
    Then the program has said nothing yet
    :::python
    assert not str(self.out.data.message or ""), self.out.data.message
    :::

  Scenario: The button reads, computes, and writes back
    Given a student who typed their name
    :::python
    self.page.ask.set("name", "Ada")
    :::
    When they press the button
    :::python
    self.page.say.click()
    :::
    Then the message is theirs
    :::python
    said = str(self.page.out.data.message or "")
    assert "Hi Ada" in said, said
    assert "welcome to coding" in said, said
    :::
```
{: .feature tags="ui,code" status="passing" }

## 🔗 Where this goes next

```
/courses/python
/components/form
/components/run
```
{: .related }
