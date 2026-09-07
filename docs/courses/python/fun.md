# 💡 Fun with functions

A cup of hot chocolate, too hot to drink. Each drop of milk cools it a
little. **Guess the final temperature before you press Cool** — then meet
the two functions behind the two buttons, and the same program as plain
Python.

```python
@component(icon="☕")
class Choco(Object):
    """For Alex, a freshman in a hurry, who loves hot chocolate
    Who wants to adjust the right temperature without burning themselves
    Our app is a learning tool like his favorite cup of hot chocolate
    With simple steps that comfort, not confuse"""
    temperature      = Attr(int, 140, min=0, max=212, unit="°F", hint="How hot the cup is right now")
    drops            = Attr(int, 2, min=0, max=20, hint="Milk drops you are about to add")
    degrees_per_drop = Attr(int, 5, min=1, max=20, unit="°F", hint="Each drop cools the cup this much")
    expected_result  = Attr(int, 0, min=0, max=212, unit="°F", hint="Your guess — BEFORE you cool it")
    verdict          = Attr(str, "…", ro=True, hint="Only guess() and cool() write here")

    def guess(self):
        """Reads your expected result. Writes the verdict: what you are betting on."""
        self.verdict = f"You expect {self.expected_result} °F after {self.drops} drops. Now cool it."

    def cool(self):
        """Reads temperature, drops and degrees per drop. Writes the new temperature and the verdict."""
        self.temperature = max(0, self.temperature - self.drops * self.degrees_per_drop)
        if self.temperature == self.expected_result:
            self.verdict = f"🎉 Congrats! {self.temperature} °F, exactly as you said."
            self.confetti()
        else:
            self.verdict = f"Nice try. Almost there — it is {self.temperature} °F. Try again."


choco = Choco()
```
{: .model #choco_model }

```
### 🎤 The Pitch

Every app starts as a **sentence** — for whom, and what it changes.

> **For** Alex, a freshman in a hurry, who loves hot chocolate  
> **Who wants** to adjust the right temperature without burning themselves  
> **Our app is a** *learning tool* like his favorite *cup of hot chocolate*  
> **With** simple steps that comfort, not confuse

```
{: .accordion }

`````
### !☕ A Web App

Play first. Set the cup, type your **expected result**, press **Guess**,
then **Cool** — and read the verdict. Guess right, and the cup celebrates. Each button is a **function**: a
named piece of behaviour the app can run on demand.

````
```python
```
{: .inspector #choco bind="choco" source="choco_model" }
````
{: .block title="☕ Choco" }
`````
{: .accordion }

````
### 🐍 The Code Backstage

The same program, as you will write it: **read**, **compute**, **write
back**. Press ▶ Run and answer the two questions in the console.

```python
"""
For Alex, a freshman in a hurry, who loves hot chocolate
Who wants to adjust the right temperature without burning themselves
Our app is a learning tool like his favorite cup of hot chocolate
With simple steps that comfort, not confuse
"""

# constants (not enforced by Python)
DEGREES_PER_DROP: int = 5  # (°F)

# read console
temperature: int = int(input("Initial temperature: "))
milk_drops: int = int(input("Milk drops: "))

# computations
temperature = temperature - milk_drops * DEGREES_PER_DROP
# alternative: temperature -= milk_drops * DEGREES_PER_DROP

# print result back to console
print(f"Final temperature = {temperature}")
```
{: .run rows="20" }

````
{: .accordion }

````
### 🦄 Does it work?

The page checks itself: it sets the cup, guesses, cools, and reads the
verdict back.

```gherkin
Feature: Two buttons, two functions
  As a beginner
  I want to guess before the app computes
  So that I feel the arithmetic before I read it

  Scenario: A right guess is rewarded
    Given a cup at 140 °F and two drops of five degrees
    :::python
    choco.temperature = 140
    choco.drops = 2
    choco.degrees_per_drop = 5
    :::
    When Alex guesses 130 and cools the cup
    :::python
    choco.expected_result = 130
    choco.guess()
    assert "expect 130" in choco.verdict, choco.verdict
    choco.cool()
    :::
    Then the cup is at 130 and the verdict says so
    :::python
    assert choco.temperature == 130, choco.temperature
    assert "Congrats" in choco.verdict, choco.verdict
    :::

  Scenario: A wrong guess is named, never punished
    Given the same cup, hot again
    :::python
    choco.temperature = 140
    choco.drops = 2
    choco.degrees_per_drop = 5
    :::
    When Alex guesses 120 and cools the cup
    :::python
    choco.expected_result = 120
    choco.cool()
    :::
    Then the verdict invites another try
    :::python
    assert choco.temperature == 130, choco.temperature
    assert "Try again" in choco.verdict, choco.verdict
    :::
```
{: .feature tags="ui,code,functions" status="pending" visible="true" celebration="true" }
````
{: .accordion }
