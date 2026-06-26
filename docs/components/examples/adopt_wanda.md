# 1️⃣ The Platform 🚁

<!--
## (Nice animated gif here)
While the avatar starts

**Learners _build_ — they don't just read.**  ·  explore → challenge → KARMA


```yaml
name: "Prof. LC"
voice: en-US
rate: 0.96
script:
  - say: "Adopt Wanda — a learning scenario in three acts: explore, then a challenge, then KARMA."
  - at: "#platform"
    say: "Lightcodepedia is an open, low-code platform: learners build interactive content from plain markdown. And it's peer-recognised at ACM SIGCSE."
  - at: "#features"
    say: "Everything is live. Here are Lucky and Wanda as editable objects — and there are maps, grids, charts and quizzes too."
  - at: "#explore"
    say: "Act one: meet the objects. Edit attributes, call methods, watch the pets react. Free play — no goal yet."
  - at: "#understanding"
    say: "We check understanding as we go — a quick quiz, with feedback on every choice."
  - at: "#gap"
    say: "Act two: the challenge. Adopt Wanda — but the checkbox is locked and only Lucky can reach her. Each pet is a little state machine: feed Lucky, he grows, Wanda gets curious, she blows a bubble, then Lucky barks her home. The learner discovers that order — exploring in the dark, with no traces."
  - at: "#finish"
    say: "All we receive is the finish photo: the final state, the quiz passed. From that alone — was it the learner's own reasoning, or an AI-assisted paste? You can't tell."
  - at: "#karma"
    say: "Act three: with traces. Every step is written back as code — that's what we can capture today."
  - at: "#analyse_btn"
    say: "Instead of the only finish photo, what if we can see the movie of the learning journey? That's where KARMA's meaningful, auditable process will live."
  - at: "#value"
    say: "KARMA brings generic, transparent, scalable instrumentation. Goal-matched traces. Hesitations and misconceptions as positive signals. Assess and guide, in real time."
```
{: .avatar #guide size="150" step="true" }

[▶ Start](#)
{: .avatar-trigger target="guide" label-stop="⏹ Stop" }

**🎬**{: title="Record in one pass: press 📽️, then ▶ Start and Next → to advance one beat at a time — the guide waits between lines. Do your interactions between clicks: feed Lucky / blow a bubble on the quest; open the editor → 📝 Log on the Log step." }

--> 
## ① The platform today {#platform}


```
### 💡Lightcodepedia
📖 Open, low-code, scalable **learning** platform  
👷🏻‍♂️ Learners learn to **build** interactive content  
❣️ From plain **markdown**{: .red }, no ~~HTML, JS, server.~~  
🤖 AI empowered, yet, yet **free** to use  
🖼️ Text, **images** & videos, Iiteractive maps & embeds  
![Lucky — a black Labrador](/assets/lab.jpg)


### 🎥 Interactive
🎵 Play and 📽️ Record **videos** (like this one)  
📊 **Data** — forms, grids, charts  

[▶️ Led Zeppelin — Black Dog](https://youtu.be/mX4OPdzcIaI)

{: .video height="380" }

```
{: .blocks cols="2" }


## 📊 Living Components — Progressive disclosure


````
### 🐕 Data [Editable — click a cell to change a value, then watch the chart]

Select a dog to update the chart.

```csv
breed,top_speed_kmh,cute
Greyhound,72,70
Saluki,68,72
Vizsla,64,78
Jack Russell,56,85
Border Collie,48,82
German Shepherd,48,80
Labrador,40,92
Beagle,40,88
Corgi,35,95
Pug,15,98
Bulldog,14,90
```
{: .dataset #dog_data }

```csv
```
{: .datagrid bind="dog_data" #dog_grid_tuto title="Dog top speeds & cuteness" height="280" editable="true" }

### 📊 Chart [Updates live when you select or edit a row]

Updates when you select a dog.

[Selected dog](#)
{: .chart type="bar" bound-to="dog_grid_tuto" x="breed" height="280" }
````
{: .blocks cols="2" }


```
### Interactive familiar widgets 
- ✅ Text, images & video
- ✅ Interactive maps & embeds

### Interactive familiar widgets 
- Data — forms, grids, charts
- with progressive disclosure x-ray!

```
{: .blocks cols="2" }

````
### 🐍 Code — write & run Python
```python
class Dog:
    def __init__(self, name):
        self.name = name
    def bark(self):
        return self.name + " says Woof!"

print(Dog("Lucky").bark())
```
{: .run }

### 🎲 Quiz — instant feedback
**Q:** What makes something an *object*?

- [ ] Just the data it stores.
- [x] State **and** behaviour, together.
- [ ] A file you `import`.
{: .quiz }
````
{: .blocks cols="2" }

## ✨ Momentum
🏅 **Peer-reviewed at ACM SIGCSE** — Demo & Poster *(2026)* · Tutorial *(2025)* · Jury *(2024)* · Exhibitor *(2023)*
```
### 🎓 ACM SIGCSE TS 2026_ — Anonymous Peer Review
- 💬 _A rare fusion of low-code technology and computing pedagogy — innovative and grounded._
- 💬 _The progression from visual exploration to executable models supports authentic learning while staying accessible for diverse learners._
{: .carousel delay="10000"}
### 👨‍🎓 UWM Student Feedback
- 💬 _Working on this assignment has shown me how visual and interactive elements make learning and coding clearer. Seeing how pets (Lucky and Wanda) react in real time made methods, states, and relationships more concrete. It also improved my ability to think from a user's perspective and design engaging, user-friendly features. Overall, it enhanced my coding skills and problem-solving approach._
- 💬 _More quotes here_
{: .carousel delay="10000"}
###
```
{: .blocks cols="2"}

### Workshops and summer schools
![Summer Schools](/assets/SummerSchoolZoom.jpg){: height="320" }


# 2️⃣ Adopt Wanda 🐕🐠 

Thomas, an undocumented neurodivergent learner has a challenge: 

**🎬**{: title="Run the code (▶), then answer the quiz — both are live widgets from plain markdown." }

## 🐾 Act 1 — Meet the objects {#explore}

```yaml
lucky:
  colour: Golden
  weight_kg: 30
  top_speed_kmh: 45
  adopted: true
wanda:
  colour: Orange
  weight_kg: 0.03
  top_speed_kmh: 6
  adopted: false
```
{: .scene3d #explore_scene height="420" console="false" }

**🎬**{: title="Free play: click attributes & methods, watch the pets react. No goal yet — and no code shown." }

## ✅ Check understanding {#understanding}

**Q:** You click `wanda.blow_bubble()`. What is that?

- [ ] An **attribute** — a value stored on Wanda.

  > Attributes are *state* you read or set — like `colour` or `adopted`. `blow_bubble()` *does* something instead.

- [x] A **method** — behaviour Wanda can perform.

  > Exactly — behaviour an object invokes, usually using its own state.

- [ ] A separate program you `import`.

  > No — it belongs to the object itself. That co-location of state **and** behaviour is what makes it an object.

- [ ] Nothing — fish can't blow bubbles.

  > They can here! An object's behaviour is whatever it's defined to do — Wanda's bubble even nudges Lucky.
{: .quiz #check_objects }

**🎬**{: title="Let them answer — feedback appears on every option, right and wrong. The platform checks understanding inline." }

## 🎯 Act 2 — The challenge {#gap}

```yaml
lucky:
  colour: Golden
  weight_kg: 30
  top_speed_kmh: 45
  adopted: true
wanda:
  colour: Orange
  weight_kg: 0.03
  top_speed_kmh: 6
  adopted: false
```
{: .scene3d #challenge_scene height="420" goal="adopt_wanda" }

**🎬**{: title="Locked checkbox; each method only fires in the right state (chips show it). Discover the order: eat → Wanda curious → blow_bubble → bark → adopted. Try off-path moves too — solved in the dark, no trace." }

## 🕵️ The finish photo {#finish}

**Q:** A learner submits the "finish photo" — Wanda adopted, the quiz passed. From that result alone, can you tell whether it was their own reasoning or an AI-assisted paste?

- [x] No — the finish looks identical either way. You'd need the *process*.

  > That's the gap: same outcome, very different journeys.

- [ ] Yes — reaching the goal proves understanding.

  > Not on its own — a paste reaches the same goal with no understanding.

- [ ] Yes — AI answers are always wrong.

  > They're often right — which is exactly why the result can't tell you.

- [ ] Only if you watched them the whole time.

  > You can't watch everyone — which is why the *trace* matters.
{: .quiz #finish_photo }

**🎬**{: title="Same submitted state + quiz, whether reasoned or pasted. That's the gap KARMA fills." }

## 🧭 Act 3 — With traces: KARMA {#karma}

```yaml
lucky:
  colour: Golden
  weight_kg: 30
  top_speed_kmh: 45
  adopted: true
wanda:
  colour: Orange
  weight_kg: 0.03
  top_speed_kmh: 6
  adopted: false
```
{: .scene3d #karma_quest height="420" goal="adopt_wanda" trail="true" }

**🎬**{: title="Replay and solve — the code trail fills with every click, wrong turns included. That's what we can capture today." }

### 🔬 KARMA analysis

````
### !🔗 Source URL — *set off-camera*
```yaml
url: ""
```
{: .form #analysis_src editable="true" title="Analysis source" }

### !🖼️ Analysis
[Analyse](#)
{: .button #analyse_btn }

```python
def on_click(button):
    u = (button.page.analysis_src.data.url or "").strip()
    # a Google Drive share link → its direct-image CDN form (needs "Anyone with the link")
    if "drive.google.com" in u:
        fid = ""
        if "/d/" in u:
            fid = u.split("/d/")[1].split("/")[0].split("?")[0]
        elif "id=" in u:
            fid = u.split("id=")[1].split("&")[0]
        if fid:
            u = "https://lh3.googleusercontent.com/d/" + fid
    if u:
        button.page.analysis_frame.image(u)
```
{: .onclick }

[blank](about:blank)
{: .embed-page #analysis_frame height="360" }
````
{: .accordion }

**🎬**{: title="Two-section accordion (eager): off-camera, open 🔗 Source URL → paste the image URL into the form → collapse it. On camera, open 🖼️ Analysis → Analyse → the image loads auto-fitted. Never committed; URL only in the form." }

## 📝 The empty Log {#log_beat}

# 📝 Switch to the editor → the **Log** tab

**🎬**{: title="Open the page editor (✏️ / ⌥⇧E) → 📝 Log. Empty by design — Process Log · coming with KARMA. The trail shows WHAT was clicked; the Log is HOW they got there." }

## 💡 What KARMA brings {#value}

- 🧩 **Generic & native** — all authoring content, nothing to wire.
- 🔍 **Transparent & auditable** — a reproducible record of the process.
- 📈 **Scalable** — the same instrumentation, everywhere.
- 🎯 **Goal-matched** — measured against the **assignment's goal**.
- 🤔 **Struggle as signal** — choices, hesitations, misconceptions used **positively**.
- ⏱️ **Real-time** — assess and **guide** as the learner works.
- 🎨 Mass customisation!

**The activity is live on the open platform today. KARMA fills the Log — so students get the feedback they need.**

**🎬**{: title="End here. Value only — no engine, no schema, no internals." }
