# 🔮 From the future

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
    say: "And here's where to go — Lake Park, Riverside Park, even UWM where you'll hunt your credits. Lucky's rescue, mapped on Milwaukee's East Side."
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
location: East Side, Milwaukee (by UWM)
has_car: false
budget_usd: 80
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
UWM School of Information Studies,credits,Kenwood Campus,0.2,5.0
Lake Park,park,East Side,1.1,4.8
Riverside Park,park,Riverwest,1.9,4.6
Estabrook Park,park,Shorewood,3.4,4.7
Lakeshore Veterinary Specialists,vet,Glendale,6.1,4.7
MADACC Lost-Pet Hotline,hotline,—,0.0,4.6
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
### 🗺️ Where to go [Zoom in — the parks and campus are real Milwaukee places]

```json
[
  { "lat": 43.0766, "lon": -87.8817, "label": "🎓 UWM — School of Information Studies (hunt your credits)" },
  { "lat": 43.0556, "lon": -87.8720, "label": "🌳 Lake Park" },
  { "lat": 43.0731, "lon": -87.8957, "label": "🌳 Riverside Park" },
  { "lat": 43.0958, "lon": -87.9036, "label": "🌳 Estabrook Park" }
]
```
{: .map height="320" zoom="13" }
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
faces of the same object. We'll open each face in later chapters.

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
your very first click — you just couldn't see them. We'll write our own a few chapters on.

---

## 📌 Key concepts

The five ideas that make everything else possible — in plain words:

- **You don't need to code to build software now** — low-code blocks + AI let you assemble working apps. (This page is the proof.)
- **Start from the user and the problem, not the technology** — a real person's situation is where every app begins.
- **Behavior before architecture** — use the thing first; understand the machinery later.
- **Every live widget has a structure you can inspect** — screen, model and code are views of one object.
- **A "specification" is just the promises an app keeps**, written in plain language and checked automatically.

## 🎲 Test yourself

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

## 📖 From the future, decoded — the real words

You just did real software engineering; we only dressed it in a story. Here's
the translation, so the official words click into place *after* you've felt what
they mean:

| In the story | What professionals call it |
|---|---|
| Using Lucky's finished app *before* building it | **Outside-in**[^outside-in] (behavior-first) design |
| "The card that listens" — change a field, it reacts | A **data-bound form**[^data-bound] / model |
| "The list that compares options for Lucky" | A **data grid**[^data-grid] (a table view of records) |
| "Find it on the map" | A **map / geospatial view**[^geospatial] of the same data |
| "Screen, model and code are three views of one thing" | **Model–View synchronization**[^mvc] |
| "The promises the app kept the whole time" | The **specification**[^specification] (acceptance criteria) |
| "Promises checked automatically on every change" | **Automated / acceptance tests**[^acceptance] |

> Tell the story first; reveal the vocabulary last. By the time a learner hears
> "acceptance test," they've already *felt* one keeping Lucky safe. Hover any
> term above to see its definition — they all collect into the **Definitions**
> glossary at the foot of the chapter.
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

## ➡️ Next — where the story goes

You used the app. What comes next isn't fixed — it's whatever Chapter 1's
*urgent need* pulls in next from the **catalog**. Browse it, or ask Ari where to
go from here.

```
### 📚 The catalog
[See what to pull in next →](/micro_build_ai/catalog)

### 🤖 Ask Ari
[Not sure what's next? Ask the guide](/micro_build_ai/ari)

### 🗺️ The spine
[Back to the journey](/micro_build_ai/)
```
{: .cards cols="3" }

[^outside-in]: **Outside-in design** — building from the user's behavior and the finished experience *inward* to the code, instead of bottom-up from the database. Also called behavior-first.
[^data-bound]: **Data-bound form** — an input whose fields are wired to a data model, so editing the screen changes the data and vice-versa, live.
[^data-grid]: **Data grid** — a table view of structured records you can sort, select and compare; selecting a row can drive other widgets.
[^geospatial]: **Geospatial view** — data placed on a map by latitude/longitude, so *where* something is becomes part of the information.
[^mvc]: **Model–View synchronization** — keeping the screen (view) and the underlying data (model) in lock-step, so a change in one is reflected in the other automatically.
[^specification]: **Specification** — the agreed promises an app must keep, written in plain language; when made checkable they become *acceptance criteria*.
[^acceptance]: **Acceptance test** — an automated check that the app keeps a specific promise; it runs on every change and fails loudly if the promise breaks.
