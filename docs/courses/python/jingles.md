# 🎮 Arcade jingles

Every arcade game has three sounds: the coin, the level up, the game over.
Each one is a **list of notes**, and a **loop** plays them. Press ▶ Run.
Turn your sound on.

## 🪙 The coin

A note is a name and a length in beats. Two notes, and you have a coin.

```python
play.tempo = 180
play.wave = "square"

coin = [("B5", 1), ("E6", 3)]

for note, beats in coin:
    play(note, beats)

print("ping!")
```
{: .run #coin }

`play("B5", 1)` queues one note; the next call queues the next one after
it. The song plays once the program is done.

## 🆙 Level up, game over

Same loop, other lists. Run both: the first climbs, the second falls.

```python
play.tempo = 200

level_up  = [("C5", 1), ("E5", 1), ("G5", 1), ("C6", 1), ("E6", 1), ("G6", 3)]
game_over = [("C5", 2), ("G4", 2), ("E4", 2), ("A4", 1), ("B4", 1), ("A4", 1), ("G#4", 1), ("A#4", 1), ("G#4", 1), ("G4", 4)]

for note, beats in level_up:
    play(note, beats)

play("R", 2)              # a rest: silence, two beats

for note, beats in game_over:
    play(note, beats)
```
{: .run #level }

## 🧱 Notes as objects

A tuple is fine. A class says what a note *is*: a name and a duration.
`play` reads both.

```python
class Note:
    def __init__(self, note, duration=1):
        self.note = note
        self.duration = duration

power_up = [Note("G4"), Note("B4"), Note("D5"), Note("G5"), Note("B5"), Note("D6"), Note("G6", 2)]

play.tempo = 220
for n in power_up:
    play(n.note, n.duration)

show(power_up[0])
```
{: .run #power }

## 🎹 A scale from a loop

Nobody typed these notes: `range` did. Change the `4` to a `5`. Reverse the
list with `[::-1]`.

```python
names = ["C", "D", "E", "F", "G", "A", "B"]
scale = [names[i] + "4" for i in range(7)] + ["C5"]

play.tempo = 240
play.wave = "triangle"
play(scale)                 # a whole list at once, one beat each
play(scale[::-1])           # and back down

print(scale)
```
{: .run #scale }

## 🎼 Your jingle

Write your own: a list, a loop. Three to eight notes. Make it yours.

```python
play.tempo = 180
play.wave = "square"

mine = [("E5", 1), ("E5", 1), ("R", 1), ("E5", 1)]

for note, beats in mine:
    play(note, beats)
```
{: .run #mine }

```gherkin
Feature: The arcade plays
  As someone learning lists and loops
  I want my loops to make a sound
  So that I can hear what the program did

  Scenario: The coin rang
    Given the coin runner
    :::python
    self.coin: Object = Object._all("#lc-pyrun-coin")[0]
    :::
    Then it played two notes, the last one E6
    :::python
    played: int = int(self.coin._attr("data-lc-played") or 0)
    assert played >= 2, "press ▶ Run on the coin block first"
    assert self.coin._attr("data-lc-last-note") == "E6", "the coin ends on E6"
    :::

  Scenario: Your jingle played
    Given your runner
    :::python
    self.mine: Object = Object._all("#lc-pyrun-mine")[0]
    :::
    Then at least three notes played
    :::python
    played: int = int(self.mine._attr("data-lc-played") or 0)
    assert played >= 3, "write three notes or more in mine, then ▶ Run"
    :::
```
{: .feature #jingles_proof visible="true" status="pending" tags="run,play" celebration="true" }

[^play]: **play** — every runner's note player: `play("C5", 1)`, or a whole
    list; `play.tempo`, `play.wave`, `play.stop()`.
