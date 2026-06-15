# 🔮 Chapter 1 · From the future

## 🎯 The goal

Imagine it's already done. **Lucky built an app** — the **Paws Support
Navigator** — and it works: a worried dog-owner types *"my dog swallowed
something and I have no car"*, and seconds later they have a calm, ranked list
of what to do and where to go. No code on screen. No manual. It just helps.

That finished app is where we begin. Today you don't build it — **you use it**,
like any visitor would. Everything after this module is us walking *backwards*
to uncover how a dog (and you) could possibly make such a thing.

> From-the-future rule: we meet the result first. The "how" is the reward for
> being curious, not the price of admission.
{: .speaker-note }

## 🚗 Short on time? Let me drive

Ari's little roadster can take the wheel and **drive you through this whole
chapter** — it rolls to each part of Lucky's app, spotlights it, and explains it
out loud. Press play and ride along, or read on and explore at your own pace.

```yaml
voice: en-US
rate: 1.0
rive:
  url: https://cdn.rive.app/animations/vehicles.riv
script:
  - say: "Buckle up — I'll drive you through Lucky's app in under a minute. Here we go!"
  - at: "#m1-situation"
    input: bump
    say: "First stop: Lucky's situation. This card is the app listening — who needs help, and how badly. Change a field and everything reacts."
  - at: "#lc-datagrid-paws_grid"
    input: bump
    say: "Now the services nearby. Click a row and the chart follows it — the app is comparing options to get Lucky rescued."
  - at: "#m1-map"
    input: bump
    say: "And here's where to go. Real vets, real parks — Lucky's rescue, mapped."
  - at: "#m1-design"
    say: "Pop the hood: the screen, the model, and the code are three views of one thing."
  - at: "#m1-specs"
    say: "The app kept promises the whole time you used it. Those promises are its spec — you'll write your own soon."
  - say: "That's the chapter! Now take the wheel yourself. See you in the next one."
```
{: .avatar #m1_drive size="150" }

[🚗 Let me drive you faster](#)
{: .avatar-trigger target="m1_drive" label-stop="⏹ Stop the car" }

## 🧱 Before you start

Nothing. Bring curiosity and a browser. This is the first stop on the map.

---

## 🐾 Discover — use the app as a user

This is the real thing. Poke it. Notice that **you already know how to use it**,
even though nobody has explained anything yet.

### 1️⃣ Tell it your situation {#m1-situation}

This card is a live object — change any field and it updates instantly. It's how
the Navigator understands *who needs help*.

````
### 🐕 Lucky's situation [Edit any field — it's live]

```yaml
who: Lucky (and me)
need: Find a vet — Lucky swallowed something
urgency: high
location: 5th arrondissement
has_car: false
budget_eur: 80
```
{: .form editable="true" }
````
{: .block }

### 2️⃣ See what's nearby

The Navigator keeps a list of community services. Here it is as a table you can
sort and a chart that follows your selection — **select a row** to compare.

````
### 🗂️ Services [Click a row — the chart follows it]

```csv
service,kind,neighbourhood,distance_km,rating
Dr. Patel Veterinary,vet,5th,1.4,4.8
City Lost-Pet Hotline,hotline,—,0.0,4.7
Bois de Boulogne Dog Run,park,16th,2.1,4.6
Happy Tails Shelter,adoption,11th,3.2,4.5
Good Dog Training,training,10th,2.7,4.4
PawPrint Grooming,grooming,3rd,0.9,4.2
```
{: .dataset #paws_services }

```csv
```
{: .datagrid bind="paws_services" #paws_grid title="Community services near you" height="260" }

### ⭐ Ratings [Updates when you pick a service]

[Selected service](#)
{: .chart type="bar" bound-to="paws_grid" x="service" height="260" }
````
{: .blocks cols="2" }

### 3️⃣ Find it on the map {#m1-map}

````
### 🗺️ Where to go [Zoom in — the vet and the parks are real places]

```json
[
  { "lat": 48.8462, "lon": 2.3372, "label": "🏥 Dr. Patel Veterinary" },
  { "lat": 48.8620, "lon": 2.2474, "label": "🌳 Bois de Boulogne Dog Run" },
  { "lat": 48.8795, "lon": 2.3090, "label": "🐾 PawPrint Grooming" }
]
```
{: .map height="320" zoom="12" }
````
{: .block }

You just **operated a working app** — chose a situation, compared options, found
a place — without a single line of code. That's the whole point: *behavior comes
first.*

---

## 🔧 Design — peek under the hood (just a peek) {#m1-design}

Here's the first secret: the form, the table, the chart and the map aren't four
separate things. They're **views of one underlying model**. Try it:

- Hold **⌥ Option / Alt** and hover the round lens over the table or the form.
  Through the lens, the widget is stripped to its **inside** — its type, and the
  live value of every setting. That inspector is the *model* talking.

You don't design anything yet. You just learn that **every live thing on the
page has a structure you can look into** — screen, model and code are three
faces of the same object. We'll open each face in later modules.

## 📜 Specs — the promises were there all along {#m1-specs}

Why did the app feel trustworthy? Because it was quietly **keeping promises** the
whole time you used it — for example:

- *"Show the closest suitable service first."*
- *"Never recommend a service that's closed or irrelevant to the need."*
- *"If urgency is high, surface a hotline."*

Those sentences are the app's **specification** — written *before* you arrived,
and checked **automatically** every time the app changes. On Lightcodepedia you
can see this exact idea running live: the
[evidence page](/nodes) shows the site testing **itself** after every update,
and turning the results into living documentation. The features were there from
your very first click — you just couldn't see them. We'll write our own in M7.

---

## 📌 Key concepts

The five ideas that make everything else possible — in plain words:

- **You don't need to code to build software now** — low-code blocks + AI let you assemble working apps. (This page is the proof.)
- **Start from the user and the problem, not the technology** — a real person's situation is where every app begins.
- **Behavior before architecture** — use the thing first; understand the machinery later.
- **Every live widget has a structure you can inspect** — screen, model and code are views of one object.
- **A "specification" is just the promises an app keeps**, written in plain language and checked automatically.

## 🎲 Test yourself

````
**Q:** In BUILD-AI, what do you need before you can build a working app?

- [ ] Several years of programming experience
- [ ] To install software on your computer
- [x] Curiosity and a web browser
- [ ] A maths degree
{: .quiz }

**Q:** "Start outside-in" means you begin from…

- [x] the user and their problem
- [ ] the database schema
- [ ] the programming language
- [ ] the server configuration
{: .quiz }

**Q:** "Behavior before architecture" means…

- [ ] you must read all the code before touching the app
- [x] you use and observe the working app first, then learn how it's built
- [ ] architecture doesn't matter
- [ ] you should never look under the hood
{: .quiz }

**Q:** In plain words, a software *specification* is…

- [ ] a list of bugs
- [ ] the brand of computer you use
- [x] the promises the app keeps, written down and checked automatically
- [ ] a marketing brochure
{: .quiz }
````

## 📖 Chapter 1, decoded — the real words

You just did real software engineering; we only dressed it in a story. Here's
the translation, so the official words click into place *after* you've felt what
they mean:

| In the story | What professionals call it |
|---|---|
| Using Lucky's finished app *before* building it | **Outside-in** (behavior-first) design |
| "The card that listens" — change a field, it reacts | A **data-bound form / model** |
| "The list that compares options for Lucky" | A **data grid** (a table view of records) |
| "Find it on the map" | A **map / geospatial view** of the same data |
| "Screen, model and code are three views of one thing" | **Model–View synchronization** |
| "The promises the app kept the whole time" | The **specification** (acceptance criteria) |
| "Promises checked automatically on every change" | **Automated / acceptance tests** |

> Tell the story first; reveal the vocabulary last. By the time a learner hears
> "acceptance test," they've already *felt* one keeping Lucky safe.
{: .speaker-note }

## 🤖 Ask Ari

**"Why are we using the finished app before learning anything?"**
Because behavior is easier to grasp than architecture. You build intuition by
*doing*, then each later module earns you one layer of "how." That's the
from-the-future way.

**"I didn't write any code — did I really 'build' something?"**
Not yet — you *operated* it. But notice you already understood it. That
understanding is the foundation we'll build on. In the capstone you'll frame
your own app.

**"What's the difference between Lucky and Ari?"**
**Lucky** 🐕 is the pet you're teaching — the thing in the app. **Ari** is me,
your guide. Different jobs.

Those are the questions everyone asks — but you can ask your own. With your key
in place, Ari is live right here:

```yaml
title: Ari
icon: 🐾
system: |
  You are Ari, an Aristotelian pair-lightcoder and guide for the BUILD-AI
  course on Lightcodepedia. You help complete beginners build real, useful
  apps with low-code blocks and AI — no prior coding needed.
  Style: warm, brief, practical, Socratic. Start from the goal and the user's
  situation (behavior before architecture). Prefer one small next step over a
  long explanation. Use plain language; define any term in a few words.
  The learner just operated the finished "Paws Support Navigator" without
  writing code (the "from the future" reveal). Lucky 🐕 is the pet; Wanda 🐠 is
  the friendly skeptic. Keep answers under ~120 words unless asked for more.
intro: "Just used the app without coding? Ask me why that works — or what's next."
placeholder: "Why did we use the app before learning how it works?"
```
{: .agent id="ari_m1" }

No key yet? [Grab one in a minute →](/micro_build_ai/onboarding) and Ari wakes up.

## ⭐ Your karma

Every quiz you just passed added **karma**, saved right here in your browser. It
follows you across all eight modules and counts toward your **BUILD-AI
credential** — no sign-up, nothing stored on a server.

## ➡️ Next — what the iteration needs

You used the app. What comes next isn't a fixed chapter — it's whatever
Iteration 1's *urgent need* pulls in next from the **catalog**. Browse it, or
ask Ari where to go from here.

```
### 📚 The catalog
[See what to pull in next →](/micro_build_ai/catalog)

### 🤖 Ask Ari
[Not sure what's next? Ask the guide](/micro_build_ai/ari)

### 🗺️ The spine
[Back to the journey](/micro_build_ai/)
```
{: .cards cols="3" }
