# 📚 The BUILD-AI catalog

The lifecycle isn't a track you march down — it's an **atlas you route through**.
Each entry below is a **chapter**: a self-contained turn of the moonwalk
you pull in when a chapter's *urgent need* calls for it. Some are live now;
others get built when a chapter first demands them — which is exactly how a
real backlog grows.

## 🧬 Every chapter is the same shape

A chapter is modelled as a `KnowledgeNode` — a real class in the
[component model](/components/model). Its **state machine is the path you walk**
through the page:

[KnowledgeNode](#)
{: .diagram scope="KnowledgeNode" }

`locked → discovering` *(place)* `→ designing` *(action)* `→ specifying`
*(time)* `→ mastered`. Chapters link to each other through `prerequisites` and
`next`, so the catalog is a **graph**, not a list — a chapter is just a path
through it. Hold **⌥ Option / Alt** and hover a chapter's widgets to x-ray them
against this model.

---

## 📖 Chapter 1 · Make it exist

*Constraint: turn an idea into a running thing, fast.*

```
### 🔑 Get your key · live
**Need:** "I want to ask Ari and ship my own work."
Account + token, staged for least privilege.

[Open chapter →](/micro_build_ai/onboarding)

### 🔮 From the future · live
**Need:** "Show me it's even possible."
Operate the finished Paws Support Navigator as a user — no code.

[Open chapter →](/micro_build_ai/m1-from-the-future)

### 🤖 Ask Ari · live
**Need:** "I'm stuck and want to ask, right now."
Your live Aristotelian guide, powered by your own key.

[Open chapter →](/micro_build_ai/ari)
```
{: .cards cols="3" }

---

## 📖 Chapter 2 · Make it right for someone

*Constraint: a real user shows up with a real requirement.*

```
### 🤖 The AI inside · planned
**Need:** "Make it actually *do* something smart."
Summarise · classify · recommend · explain.

[Pulled in when needed]

### 🗣️ Directing AI · planned
**Need:** "Make the AI do what I meant, reliably."
Prompt · disclose · check · stay in control.

[Pulled in when needed]

### ✅ Can we trust it? · planned
**Need:** "Prove it does what the user asked."
The examples it must pass — acceptance tests as living promises.

[Pulled in when needed]
```
{: .cards cols="3" }

---

## 📖 Chapter 3 · Make it last

*Constraint: it has to survive change and be deployed for real.*

```
### ⚙️ Rules & data · planned
**Need:** "Handle the messy real world."
Eligibility rules and the services behind the app.

[Pulled in when needed]

### 🧱 Building blocks · planned
**Need:** "Stop rebuilding the same thing."
Forms, grids and maps, snapped together and reused.

[Pulled in when needed]

### 📜 The spec · planned
**Need:** "Write down the promises and check them automatically."
Plain-language behavior → an automated suite → living docs.

[Pulled in when needed]
```
{: .cards cols="3" }

---

## 🏆 The last chapter · yours

*Constraint: your world to save, your scaffold-free build. The story doesn't end
here — it hands you the pen. You pull from the whole atlas on demand.*

```
### 💡 Your world to save · live
**Need:** "One person, one problem — now I build, for real."
Frame your own app from a single real user and ship it. The never-ending story's
final chapter is the one you write.

[Open chapter →](/micro_build_ai/capstone)
```
{: .cards cols="1" }

---

## 🧭 For authors

Building a new chapter? Start from the
[node template](/micro_build_ai/node-template) — it's the author's skeleton and
a reading aid in one. Every chapter follows the same three-unity shape, so
learners always know where they are.

```
### 🗺️ Back to the spine
[The 3-chapter journey](/micro_build_ai/)

### 🧭 Node template
[The author's skeleton](/micro_build_ai/node-template)
```
{: .cards cols="2" }
