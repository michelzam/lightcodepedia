## 1️⃣ The Platform 🚁

🤹🏼‍♂️ Learning Playground: 1️⃣ Discover, 2️⃣ Challenge / Gap, and 3️⃣ The Future -> Karma.
{: .block #welcome }

[▶ Play](#)
{: .avatar-trigger target="secret_avatar" label-stop="⏹ Stop" }


```
### 💡Lightcodepedia 
📖 Open, low-code, scalable **learning** platform  
👷🏻‍♂️ Learners learn to **build** interactive content  
❣️ From plain **markdown**{: .red }, no ~~HTML, JS, server.~~  
🤖 AI empowered, yet **free** to use  
🖼️ Text, **images** & videos, Iiteractive maps & embeds  
![Lucky — a black Labrador](/assets/lab.jpg)


### 🕹️ Interactive 
🎵 Play and 📽️ Record **videos** (like this one)  
📊 **Data** — forms, grids, charts  

[▶️ Led Zeppelin — Black Dog](https://youtu.be/mX4OPdzcIaI)

{: .video height="380"}

```
{: .blocks cols="2" #interactive }


## 📊 Living Components — Progressive disclosure
{: .block #living_components}

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
{: .blocks cols="2" #chart1 }

### 🐍 Code — write & run Python & AI
````

###  Code
```python
class Dog:
    def __init__(self, name):
        self.name = name
    def bark(self):
        return self.name + " says Woof!"

print(Dog("Lucky").bark()
```
{: .run #buggy }

### 🎲 Quiz — instant feedback
**Q:** What makes something an *object*?

- [ ] Just the data it stores.
- [x] State **and** behaviour, together.
- [ ] A file you `import`.
{: .quiz }
````
{: .blocks cols="2" #quiz1}


### Agent
```yaml
system: |
  You are a Python tutor. When asked to fix code, reply with the
  COMPLETE fixed code in a single python fenced block. Keep prose short.
```
{: .agent bound="buggy" #tutor }


## ✨ Momentum
🏅 **Peer-reviewed at ACM SIGCSE** — Demo & Poster *(2026)* · Tutorial *(2025)* · Jury *(2024)* · Exhibitor *(2023)*
```
### 🎓 ACM SIGCSE TS 2026 — Peer Review
💬 _A rare fusion of low-code technology and computing pedagogy — innovative and grounded._  
💬 _The progression from visual exploration to executable models supports authentic learning while staying accessible for diverse learners._  
💬 A deeply thoughtful and forward-thinking contribution that bridges professional software practices with approachable computing education.

### 👨‍🎓 UWM Student Feedback
💬 _Working on this assignment has shown me how visual and interactive elements make learning and coding clearer. Seeing how pets (Lucky and Wanda) react in real time made methods, states, and relationships more concrete. It also improved my ability to think from a user's perspective and design engaging, user-friendly features. Overall, it enhanced my coding skills and problem-solving approach._
{: .block #momentum}
###
```
{: .blocks cols="2"}

```
### 🧑🏻‍🎓 Workshops and Summer Schools
👍 Thumbs up at scale!
![Summer School](/assets/SummerSchoolZoom.jpg)
```
{: .blocks }



## 2️⃣ Adopt Wanda 🐕 + 🐠 = 🏰
🐠 Challenge: Adopt Wanda, a fish. 
🐕 Yet only the brave dog Lucky can do communicate with.   
🎯 __Actualy, it's all about problem solving with object states and behavior.__

## 🥎 Play with pets

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

## 🕵️ The finish photo {#finish}

## Yet, Does this reflect the learning?
However, the gap is that, whatever the learning environment is, only the final photo 
is not reliable enough to confirm learrnerss’ skill match CLO, including in the AI era 
where a copy/paste gives a shortcut, jeopardising both academic cunduct and student’s 
later biger problems.

If you're an educator you can ask yourself
**Q:** A learner submits the "finish photo" — Wanda adopted, the quiz passed. 
From that result alone, can you tell whether it was their own reasoning or an AI-assisted paste?

- [x] No — the finish looks identical either way. You'd need the *process*.

  > That's the gap: same outcome, very different journeys.

- [ ] Yes — reaching the goal proves understanding.

  > Not on its own — a paste reaches the same goal with no understanding.

- [ ] Yes — AI answers are always wrong.

  > They're often right — which is exactly why the result can't tell you.

- [ ] Only if you watched them the whole time.

  > You can't watch everyone — which is why the *trace* matters.
{: .quiz #finish_photo }


## 3️⃣ Play with Traces: KARMA {#karma}

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

### 🔬 KARMA analysis{#analysis}


````
### !🔗 Source URL — *set off-camera*
```yaml
url: ""
```
{: .form #analysis_src editable="true" title="Analysis source" }

#### !🔗 Video source — *set off-camera, then fold*
```yaml
video_url: ""
```
{: .form #secret_src editable="true" title="Private video URL" }

[📼 Load video](#)
{: .button #load_secret_video }

```python
def on_click(button):
    u = (button.page.secret_src.data.video_url or "").strip()
    if u:
        button.page.secret_avatar.video(u)
```
{: .onclick }

[📁 Choose a local video…](#)
{: .avatar-trigger target="secret_avatar" pick="video" }

```yaml
name: "Aristotle"
transparent: true
script:
  - say: "Welcome to Karma,  the next big feature."
    video: true
    cues:
      - t: 0
        at: "#welcome"
        say: "Welcome"
      - t: 21
        at: "#interactive"
        say: "Users can play, learn, and earn credits 🏆"
      - t: 30
        at: "#living_components"
        say: "Select your breed."
      - t: 34
        at: "#buggy"
        say: "Code"
      - t: 38
        at: "#tutor"
        say: "Ask for help."
      - t: 38
        at: "#quiz1"
        say: "Answer quiz."
      - t: 47
        at: "#momentum"
        say: "Momentum"
      - t: 60
        at: "#challenge_scene"
        say: "Challenge"
      - t: 90
        at: "#finish"
        say: "Finish photo"
      - t: 115        
        at: "#karma"
        say: "Beyond the platform: Karma"
      - t: 138
        at: "#finish"
        say: "Finish photo"
      - t: 140
        at: "#analysis"
        say: "Analysis"
      - t: 160
        at: "#value"
        say: "Thanks for watching"


```
{: .avatar #secret_avatar size="180" step="true" }


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
