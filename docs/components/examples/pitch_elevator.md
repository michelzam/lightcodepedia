# 🛗 Pitch elevator

Every app starts as a **sentence**. Say who it is for, say what it changes —
then watch that sentence become code, and run the code.

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

## 🎮 The app, and its Python
{: .accordion open="true" }

Same program, twice. On the **left**, the app a user sees. On the **right**,
the eleven lines that make it happen — yours to run and to break.

````
### 🖥 The app

Click a value and type over it — the app answers as you type.

```
name: your name
passion: hot chocolate
print_message: false
```
{: .form editable="true" #pitch title="Say hello" }

**1 · read** — the app put what you typed in a box called `name`, and it holds
**{= pitch.name }**.

**2 · compute** — it builds one sentence out of your two boxes:
**Hi {= pitch.name }, welcome to coding. Take it slow, like {= pitch.passion }.**

**3 · write back** — tick **Print Message** above, and the app says it out loud:

```
Hi {= pitch.name }, welcome to coding. Take it slow, like {= pitch.passion }.
```
{: .block tone="tool" visible="= pitch.print_message" }

### 🐍 The code

The app types for you. Here, you type in the code itself — change a string,
press ▶ Run.

```python
"""
For <students> who want to <taste programming without being burned>
Who need <a gentle, warming first experience>
Our app is a <learning tool> like <a cup of hot chocolate>
With <simple code that comforts, not intimidates>
"""

# read (in PythonAnywhere this line asks the console: input("name: "))
name: str = "your name"
passion: str = "hot chocolate"

# computation
message: str = f"Hi {name}, welcome to coding. Take it slow, like {passion}."

# write back
print(message)
```
{: .run rows="18" }
````
{: .block cols="1;1" title="🛗 Pitch elevator" }

## 🦄 Does it work?
{: .accordion }

The page checks itself — the same three steps, asserted.

```gherkin
Feature: The app and the code tell the same story
  As a student
  I want the app to answer to my own words
  So that I can see what a program does before I write one

  Scenario: The app greets whoever fills it in
    Given the pitch app
    :::python
    self.app: object = self.page.pitch
    :::
    When a student types their name and their passion
    :::python
    self.app.set("name", "Ada")
    self.app.set("passion", "long walks")
    :::
    Then the app collected both
    :::python
    assert str(self.app.data.name) == "Ada", self.app.data.name
    assert str(self.app.data.passion) == "long walks", self.app.data.passion
    :::

  Scenario: The printed line is the message, not a picture of one
    Given the pitch app filled in
    :::python
    self.app: object = self.page.pitch
    self.app.set("name", "Ada")
    self.app.set("passion", "long walks")
    self.app.set("print_message", True)
    :::
    Then the console shows the welcome, in the student's own words
    :::python
    out = Object._all(".lc-tone-tool")[0]._el.textContent
    assert "Hi Ada" in out, out
    assert "long walks" in out, out
    :::
```
{: .feature tags="ui,data" status="passing" }

## 🔗 Where this goes next

```
/components/form
/components/run
/components/accordion
```
{: .related }
