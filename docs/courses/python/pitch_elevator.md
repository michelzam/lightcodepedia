# 🛗 Pitch elevator

Every app starts as a **sentence**. Say who it is for, say what it changes —
then meet the three steps that turn that sentence into a program: **read**,
**compute**, **write back**.

## Start

```
### 🎤 The pitch
Fill the blanks out loud, in one breath. That is the whole ride: **an
elevator pitch** is a promise short enough to say between two floors.

> **For** students curious to *taste programming* without being burned  
> **Who need** a gentle, warming first experience  
> **Our app is a** *learning tool* like *a cup of hot chocolate*  
> **With** simple code that comforts, not intimidates

```
{: .accordion }

````
### 🖥 The app

Here is the finished thing, the way a user meets it: a box to fill, a button
to press, an answer that was not there before.

```
name:  
```
{: .form editable="true" #ask title="Say hello" }

[▶ input, compute and print](#)
{: .button #say }
```python
name = button.page.ask.data.name
message = f"Hi {name}, welcome to coding. Take it slow, like hot chocolate."
```
{: .onclick }

{=message}

````
{: .accordion }


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

# read  (the box above plays this part)
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

  Scenario: The button reads, computes, and writes back
    Given a student who typed their name
    :::python
    self.page.ask.name = "Ada"
    :::
    When they press the button
    :::python
    self.page.say.click()
    :::
    Then the message is theirs
    :::python
    assert "Hi Ada" in message, message
    assert "welcome to coding" in message, message
    :::

  Scenario: A second name gets a second welcome
    The message follows the box — it is computed, never canned.

    Given another student at the same page
    :::python
    self.page.ask.name = "Bo"
    :::
    When they press the button
    :::python
    self.page.say.click()
    :::
    Then the welcome greets them, not the one before
    :::python
    assert "Hi Bo" in message, message
    :::
```
{: .feature tags="ui,code" status="passing" visible="true" celebration="true" }
