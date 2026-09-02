# 🛗 Elevator pitch

Every app starts as a **sentence**. Say who it is for, say what it changes —
then meet the three steps that turn that sentence into a program: **read**,
**compute**, **write back**.

```
### 🎤 The Pitch

An **elevator pitch** is a promise short enough to say between two floors.

> **For** students curious to *taste programming* without being burned  
> **Who need** a gentle, warming first experience  
> **Our app is a** *learning tool* like *a cup of hot chocolate*  
> **With** simple code that comforts, not intimidates

```
{: .accordion }

`````
### !🖥 A Web App

Here is a living running app, as user meets it: a box to fill, a button
to press, an answer that was not there before.

````
```
name:  
```
{: .form editable="true" #ask }

[▶ input, compute and print](#)
{: .button #say }
```python
name = button.page.ask.data.name
message = f"Hi {name}, welcome to coding. Take it slow, like hot chocolate."
```
{: .onclick }

{=message}

````
{: .block title="Say hello" }
`````
{: .accordion }

````
### 🐍 The Code Backstage

The same program, written the way you will write it for real. Just press ▶ Run and interract.

```python
"""
For <students> who want to <taste programming without being burned>
Who need <a gentle, warming first experience>
Our app is a <learning tool> like <a cup of hot chocolate>
With <simple code that comforts, not intimidates>
"""

# read  (the box above plays this part)
name: str = input("Your name: ")

# computation
message: str = f"Hi {name}, welcome to coding. Take it slow, like hot chocolate."

# write back
print(message)
```
{: .run rows="16" }

````
{: .accordion}


````
### 🦄 Does it work?

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
````
{: .accordion }
