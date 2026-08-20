# 🎮 Join the game

⏱️ Two minutes. No account, no install, nothing to download.

Below is an app. Not a picture of one — the thing itself, running on this
page, on your phone if that is what you are holding. Everything you touch
here was written as **text**, and you are about to change some.

## 🐕 The shelter's dogs

[Shelter Desk](#)
{: .runner src="app_shelter.md" title="🐕 Shelter Desk" }

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
  - say: "Two minutes, and you build something. No account needed."
  - at: dog_list
    say: "Nova has no adoption fee. Type any number in her row."
  - at: fee_chart
    say: "The chart followed. You changed the data, not the picture."
  - at: fee_proof
    say: "Now press play. The page checks its own promise, out loud."
  - say: "That is the deal. Pages that run, and prove themselves."
stories: {}
```
{: .avatar #guide dock="true" size="115" }
