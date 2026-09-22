# 🎮 Join the game

⏱️ Two minutes. No account, no install, nothing to download.

[▶️ Doc, walk me through it](#)
{: .avatar_trigger target="guide" label-stop="⏹ Stop the walk" }

Below is an app. Not a picture of one — the thing itself, running on this
page, on your phone if that is what you are holding. Everything you touch
here was written as **text**, and you are about to change some.

## 🐕 The shelter's dogs

[Shelter Desk](#)
{: .runner src="app_shelter.md" title="🐕 Shelter Desk" #shelter }

**Nova has no fee yet.** Double-click her fee cell — double-tap on a phone —
type any number, and watch the chart answer. That is the whole trick: one
source of truth, every view follows. Nobody wired those two together; they
read the same three lines of text.

And that window is not a picture of an app. It **is** one: its own file,
running inside this page.

## 🧪 Now make the page prove it

A page can carry its own promises and check them out loud. Press ▶.

```gherkin
Feature: Every dog can go home
  Scenario: No dog is missing its fee
    Given the shelter's list
    :::python
    self.dogs: Dataset = self.page.dogs
    :::
    Then every dog has a fee
    :::python
    names: list = self.dogs.values("name")
    fees: list = self.dogs.values("fee")
    missing: list = [n for n, f in zip(names, fees) if not f.strip()]
    assert not missing, "no fee yet for: " + ", ".join(missing)
    :::
```
{: .feature #fee_proof visible="true" status="passing" celebration="true" }

Red until you fill Nova's fee, green the moment you do. Not a screenshot of
a test — the test, on the page, forever, for anyone who opens it.

## 🧠 One question

**Q:** You just typed a number and a chart moved. What did you change?

- [ ] The chart — its bars were redrawn by hand.
- [ ] Nothing; the page reloaded from a server.
- [x] The data. The chart reads it, so it followed.
- [ ] A setting saved in your browser.

  > One source, many views. That is the first idea of the whole course,
  > and you just used it before anyone explained it.
{: .quiz #start_quiz }

## 🚪 So — want one of your own?

What you just did was ours. The course is about pages that are **yours**:
your data, your app, your proof, kept in your own space and graded from it.

That is what a **bench** is, and it takes one invitation.

You are on the class roster, so your GitHub invitation is on its way to your
**@uwm.edu** address. Two things, once: sign up for GitHub **with that same
address** — the invitation is waiting for it — then accept, and your bench
opens. Nothing else to install, ever.
{: .in_class }

**No mail?** Check spam, but you do not need it: sign in to GitHub and open
[github.com/orgs/uwm-build-ai/invitation](https://github.com/orgs/uwm-build-ai/invitation)
— a waiting invitation shows up there. Still nothing after a week? Invitations
expire; write to [build-ai@uwm.edu](mailto:build-ai@uwm.edu) and we send a new one.
{: .in_class }

BUILD-AI runs as a cohort at the University of Wisconsin–Milwaukee. If you
want in, contact us at **[build-ai@uwm.edu](mailto:build-ai@uwm.edu)**.
{: .on_your_own }

```yaml
bot: doc
face:
  zoom: 1.2
script:
  - say: "Two minutes. No account. You will build something, and make the page prove it. Press me to pause."
  - at: shelter
    do: xray
    say: "This window is an app. The gear opens its text. Everything you see here is text you can change."
    pause: 2
  - at: dog_list
    do: read
    say: "Nova has no fee. Double-click her fee cell. Type any number. Press Enter."
  - at: fee_chart
    say: "The chart moved. You changed the data, not the picture. One source, many views."
  - at: fee_proof
    say: "Now press the play button. The page checks its own promise, out loud. Green means it kept its word."
  - at: start_quiz
    say: "One question. Answer it. The page tells you, nobody else."
  - say: "That is the method. Play. Experiment, with AI at your side. Then make the page bring the proof that it behaves."
  - at: fee_proof
    say: "Humans, AI and code play and learn together here. Want a page of your own? Read on below."
stories: {}
```
{: .avatar #guide dock="true" size="115" }
