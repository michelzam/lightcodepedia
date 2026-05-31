# 👋 Welcome!

👩‍🎓 This tutorial introduces the **building blocks** of a Lightcodepedia page — by telling a story.

The story is about a dog called **Lucky** 🐶

Along the way you'll see:

- [x] A **text block** with an image — meet Lucky
- [x] A **video** — his favourite song
- [x] A **map** — where to walk him in Paris
- [x] A **data table** — how fast dogs can run
- [x] A **chart** — linked live to the table
- [x] A **form** — Lucky's full profile
- [x] A **code runner** — say hello to Lucky
- [x] A **quiz** — about the story, not the technology

Go ahead — explore, play, learn and have fun! 🎉

> Tell learners: "Don't just read — everything on this page is live. Click, select, run. That's the whole point."
{: .speaker-note }

---

## 🐕 Meet Lucky

This block is a **text block**. It can hold text, lists, images — and a dog.

![Lucky — a cheerful Beagle](https://lightcodepedia.jollybush-84a428fe.francecentral.azurecontainerapps.io/media/8fd1c9c5fa0e06f96b21dd9440b20d673e30499dda6a6ade356edb3c.jpg)

This is **Lucky** 🐶 — a three-year-old Beagle who loves parks, tennis balls, and long naps.

He's about to appear on every block of this page.

_Text blocks use standard markdown: **bold**, _italic_, lists, links, images. Everything you already know._

---

## 🎵 Lucky's favourite song

This block is a **video block**. Press play.

[▶️ Lucky's favourite song](https://youtu.be/6tlSx0jkuLM?si=OHbXv8Vp9NKidh9e)
{: .video height="320" }

This is Lucky's all-time favourite song — he wags his tail every time it comes on.

_A video block embeds any YouTube link. One line of markdown, one tag._

---

## 🗺️ Where to walk Lucky in Paris

This block is a **map**. Click and drag to explore. Scroll to zoom in.

```json
[
  { "lat": 48.8620, "lon": 2.2474, "label": "🌳 Bois de Boulogne" },
  { "lat": 48.8797, "lon": 2.3832, "label": "🌳 Buttes-Chaumont" },
  { "lat": 48.8795, "lon": 2.3090, "label": "🌳 Parc Monceau" },
  { "lat": 48.8462, "lon": 2.3372, "label": "🌳 Jardin du Luxembourg" },
  { "lat": 48.8360, "lon": 2.4414, "label": "🌳 Bois de Vincennes" },
  { "lat": 48.8937, "lon": 2.3938, "label": "🌳 Parc de la Villette" }
]
```
{: .map height="320" zoom="12" }

All six parks allow dogs on a leash. The Bois de Boulogne is the largest — over 800 hectares. Lucky could run for days.

_A map block shows any list of coordinates as clickable pins._

---

## 🏃 How fast can Lucky run?

This block is a **data table**. Click any row — the chart below updates.

```csv
breed,top_speed_kmh,size,temperament
Greyhound,72,Large,Calm
Saluki,68,Large,Independent
Vizsla,64,Medium,Energetic
Jack Russell,56,Small,Fearless
Border Collie,48,Medium,Focused
German Shepherd,48,Large,Loyal
Labrador,40,Large,Friendly
Beagle,40,Medium,Curious
Corgi,35,Small,Cheerful
Pug,15,Small,Relaxed
Bulldog,14,Medium,Stubborn
```
{: .datagrid #dog-grid format="csv" title="Dog top speeds" height="260" }

Lucky is a Beagle — 40 km/h. He could outrun most humans (top speed: ~37 km/h). He will not outrun a Greyhound.

---

## 📈 The same data — as a chart

This block is a **chart**, linked to the table above. Select a row — the chart redraws.

```csv
breed,top_speed_kmh,size,temperament
Greyhound,72,Large,Calm
Saluki,68,Large,Independent
Vizsla,64,Medium,Energetic
Jack Russell,56,Small,Fearless
Border Collie,48,Medium,Focused
German Shepherd,48,Large,Loyal
Labrador,40,Large,Friendly
Beagle,40,Medium,Curious
Corgi,35,Small,Cheerful
Pug,15,Small,Relaxed
Bulldog,14,Medium,Stubborn
```
{: .chart type="bar" bound-to="dog-grid" x="breed" height="260" }

> Ask: "Is Lucky the fastest dog? What about the most relaxed?" — let them click to compare breeds.
{: .speaker-note }

_Select a row in the table above to update this chart. Table and chart are linked — no page reload._

---

## 📋 Lucky's profile

This block is a **form**. It shows a full profile of one object — here, Lucky.

```yaml
name: Lucky
age: 3
breed: Beagle
weight_kg: 11.2
top_speed_kmh: 40
adopted: true
favorite_toys:
  - squeaky bone
  - tennis ball
  - old sock
vet:
  name: Dr. Patel
  phone: "555-0142"
notes: Afraid of vacuum cleaners. Excellent at looking innocent.
```
{: .form }

Notice how each type of value looks different: numbers in green, the checkbox for the boolean, pills for the list, a hover button for the nested vet object.

_A form turns a structured object into a readable profile card. Try hovering the Vet button._

---

## ▶️ Say hello to Lucky

This block is a **code runner**. Click ▶ **Run**.

```python
print("Hello, Lucky! 🐶")
```
{: .run }

That's it. Real code, running in your browser. No install. No account.

Change `Lucky` to your own name and run it again.

> This is the first time many learners realise they just wrote code. Let it land.
{: .speaker-note }

---

## 🧩 Quick check — about Lucky

**Q:** What is Lucky's breed?

- [ ] Labrador
- [ ] Greyhound
- [x] Beagle
- [ ] Pug
{: .quiz }

**Q:** According to the table, which dog runs the fastest?

- [x] Greyhound — 72 km/h
- [ ] Border Collie — 48 km/h
- [ ] Saluki — 68 km/h
- [ ] Labrador — 40 km/h
{: .quiz }

**Q:** Which park is the largest in the map?

- [ ] Parc Monceau
- [ ] Buttes-Chaumont
- [x] Bois de Boulogne — over 800 hectares
- [ ] Jardin du Luxembourg
{: .quiz }

**Q:** The Led Zeppelin song is named after a dog who…

- [ ] Belonged to Robert Plant since childhood.
- [ ] Was the drummer's pet.
- [x] Wandered into the recording studio and left without a name.
- [ ] Was painted on the album cover.
{: .quiz }

---

## 🚀 What's next?

You've seen every building block — through Lucky's eyes. Ready to add them to your own page?

```
### ⚙️ Step 2 — Build your own page
Make a copy of this site and start adding blocks in minutes.

[Start building →](/tutorial102)

### 🧩 Component library
Every block, with live examples and full documentation.

[Browse →](/components/)

### 🏠 Back to home
[Home →](/)
```
{: .cards cols="3" }

{% include backtotop.md %}
