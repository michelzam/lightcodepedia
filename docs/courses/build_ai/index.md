# 🤖 Build-AI

![AI is reshaping the world. Builders wanted. — UWM School of Information Studies](/courses/AI-Builders.png){: .lc-banner }

[▶️ Doc, show me around](#)
{: .avatar_trigger target="guide" label-stop="⏹ Stop the tour" }

**AI is reshaping the world — builders wanted.** Build-AI is a private cohort
course where you build a **real `AI`[^ai] app**, versioned in your own private
bench: graded challenges, answer keys, live sessions, and a teacher who sees
your progress at every step.

```
### 🎯 You want to…
- 👩🏻‍💻 Create your own apps?
- 🤔 Avoid tech hassle?
- 🏗️ Become a builder in the AI era?
- 🪪 Earn your badge?

### 🥇 This course offers
- A gentle, yet engaging and efficient introduction to:
- Building apps
- AI basics
- Best software practices

### 🗺️ Formats
- Cohort — onsite or online
- 4, 8 or 15 weeks
- Everything runs in your browser — nothing to install
- Cloud storage for your work, at no additional cost
```
{: .blocks cols="3" #want }


```
### 👀 What's inside
- Interactive playground 
- Videos and avatars
- Self-guided examples and graded challenges
- Step-by-step directions to do anything
- Building blocks ready to assemble
- Instant help and guidance, any time
- All this in your browser, nothing to install
- A place to grow your skills

### 🤹🏼‍♂️ Skills you'll learn to
- Create web apps for any screen
- Shape your interface from basic blocks
- Run `Python` scripts in your browser
- Collaborate using `GitHub` 
- Use `data` and facilitate decisions
- Ship faster and better with AI at your side
- Create your own interactive, animated demos
- Demonstrate your skills to your sponsors
```
{: .blocks cols="2" #inside }

`````
### 🔁 How BUILD-AI works

````
### 🐝 The build loop
```
Need: every build starts with someone's problem
Design: turn the need into something you can hold
Blocks: snap the working parts together
AI: bring in the partner that thinks with you
Ship: put it in someone's hands
Learn: what you shipped starts the next loop
```
{: .build_loop height="440" #loop_ring }

### 🪄 Growing your own skills
[Chad's Magics!](/courses/chad_10s2.mp4)
{: .video autoplay="true" loop="true" #chad }

> Human hands, hearts and minds work daily, 
in the background, along with AI, 
to deliver the magics of joyful learning.
````
{: .blocks cols="2" }
`````
{: .accordion #loop }

### 😀 Friendly foundations {#foundations}
Everything rides on friendly foundations — `Python`[^python], `Markdown`[^md]
and `git`[^git], tamed for beginners — so you can focus on what matters:
building things that work, and making the world a better place, *your style*.

## 🎮 Try it first — two minutes {#try}

No account, no install, nothing to download: a real app runs on the page,
you change one number, and the page proves itself out loud. Then you decide.

[🎮 Join the game →](/courses/build_ai/start)
{: .button #join_btn }

## 🚀 Ready? {#ready}

Enrolled (or enrolling)? Two doors get you working:
```
### 1️⃣ Enroll
Enroll in your class

[🎟️ Enroll →](https://uwm.edu/registrar/enrollment/)
{: .button }

### 2️⃣ Tutorial 101
Explore basic building blocks.

[📖 Tutorial →](/tutorial101)
{: .button }
```
{: .blocks cols="2" #doors }

[^ai]: `Artificial Intelligence` is a software domain assisting people to deliver value in a way similar to what humans would do.
[^python]: `Python` is the most popular and friendly programming language, made even more friendly in this class. Nothing to install, no tech prerequisites.
[^md]: `Markdown` is a lightweight text-based note convention, perfect for smart humans and AI.
[^git]: `git` is a software tool helping builders manage versions of their work, share and collaborate — you'll use it from afar, no command line needed.

```yaml
bot: doc
face:
  zoom: 1.2
script:
  - say: "Hi, I'm Doc. This page is the door to Build-AI. I will walk you through it. Press me to pause."
  - at: want
    say: "Four questions. If one of them is yours, this course was made for you."
  - at: inside
    say: "This is what you get, and what you will be able to do. Everything runs in your browser. Nothing to install."
  - at: loop
    do: open
    with: "🔁 How BUILD-AI works"
    say: "Let me open the loop."
  - at: loop_ring
    say: "Need. Design. Blocks. AI. Ship. Learn. Every build goes around this ring, then goes around again."
    pause: 1
  - at: chad
    do: play
    say: "This is Chad's magic. Watch a few seconds."
    pause: 5
  - at: chad
    do: pause
    say: "Human hands and minds make this, with AI beside them. You will too."
  - at: inside
    do: xray
    say: "Everything on this page is text. The gear opens it. You learn here by playing with the text, not by reading about it."
    pause: 2
  - do: read
    say: "You will experiment a lot, with AI at your side. And you will ask each page to prove it behaves. The proof is on the page, green or red, for anyone to see."
  - at: foundations
    say: "Humans, AI and code play and learn together here. That is the whole method."
  - at: try
    say: "Two minutes, no account. Press the button, change one number, and watch the page prove itself."
  - at: doors
    say: "Already enrolled? Two doors. Your class, or the tutorial. See you inside."
stories: {}
```
{: .avatar #guide dock="true" size="115" }
