---
title: Tutorial 101
---
# 💡 Tutorial 101

Meet **Lucky** 🐶 — a black Labrador Retriever. He'll walk you through every building block on this page.

```
### 👋 Welcome!

👩‍🎓 This tutorial introduces the **building blocks** of a Lightcodepedia page — by telling a story.

The story is about **Lucky** 🐶, a friendly black Labrador Retriever who loves parks, tennis balls, and long naps.

Along the way you'll see a **block**, a **video**, an interactive **map**, a **data table** linked live to a **chart**, two **forms** side by side, and a **quiz**.

Go ahead — explore, play, learn and have fun! 🎉

### 🐾 Lucky at a glance

- **Breed:** Labrador Retriever
- **Age:** 3 years
- **Colour:** Black
- **Top speed:** 40 km/h
- **Favourite toy:** tennis ball
- **Fear:** vacuum cleaners
- **Character:** friendly, playful, easily distracted by smells
```
{: .blocks cols="2" }

```
### 🐕 Lucky
![Lucky — a black Labrador](https://picsum.photos/id/237/500/400)

This is **Lucky** 🐶 — a three-year-old Labrador Retriever who loves parks, tennis balls, and long naps.

### 🐕 Lucky
![Lucky — a black Labrador](https://picsum.photos/id/237/500/400)

This is **Lucky** 🐶 — a three-year-old Labrador Retriever who loves parks, tennis balls, and long naps.
```
{: .blocks cols="2" }

```
### 🎵 Lucky's favourite song
🎵 Man's best song. Go ahead. Play it!

[▶️ Led Zeppelin — Black Dog](https://youtu.be/6tlSx0jkuLM?si=OHbXv8Vp9NKidh9e)
{: .video height="380" }
```
{: .block }

````
### 🗺️ Where to walk Lucky in Paris

Click a marker to see the park name. Scroll to zoom. Drag to pan.

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
````
{: .block }

## 🏃 How fast can dogs run?

````
### 🐕 Dog speeds — table

Select a row to update the chart.

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
{: .datagrid #dog-grid-tuto format="csv" title="Dog top speeds" height="260" }

### 📊 Dog speeds — chart

Click a row in the table to update this chart.

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
{: .chart type="bar" bound-to="dog-grid-tuto" x="breed" height="260" }
````
{: .blocks cols="2" }

Lucky is a Labrador — 40 km/h. He could outrun most humans (top speed: ~37 km/h). He will not outrun a Greyhound.

## 🐾 Meet Lucky & Wanda

````
### 🐕 Lucky
```yaml
name: Lucky
age: 3
breed: Labrador Retriever
colour: Black
weight_kg: 28
top_speed_kmh: 40
adopted: true
favorite_toys:
  - tennis ball
  - squeaky bone
  - old sock
vet:
  name: Dr. Patel
  phone: "555-0142"
notes: Afraid of vacuum cleaners. Excellent at looking innocent.
```
{: .form }

### 🦋 Wanda
```yaml
name: Wanda
age: 2
breed: Golden Retriever
colour: Golden
weight_kg: 25
top_speed_kmh: 40
adopted: false
favorite_toys:
  - frisbee
  - rope toy
  - plush bear
vet:
  name: Dr. Patel
  phone: "555-0142"
notes: Best friends with Lucky. Wakes him up every morning.
```
{: .form }
````
{: .blocks cols="2" }

## 🧩 Quick check — about Lucky

**Q:** What is Lucky's breed?

- [ ] Beagle
- [ ] German Shepherd
- [x] Labrador Retriever
- [ ] Golden Retriever
{: .quiz }

**Q:** According to the table, which dog runs the fastest?

- [x] Greyhound — 72 km/h
- [ ] Saluki — 68 km/h
- [ ] Border Collie — 48 km/h
- [ ] Labrador — 40 km/h
{: .quiz }

**Q:** Which Paris park is the largest?

- [ ] Parc Monceau
- [ ] Buttes-Chaumont
- [x] Bois de Boulogne — over 800 hectares
- [ ] Jardin du Luxembourg
{: .quiz }

**Q:** What is Wanda's breed?

- [ ] Labrador Retriever
- [ ] Poodle
- [ ] Husky
- [x] Golden Retriever
{: .quiz }

## 🚀 What's next?

```
### ⚙️ Build your own page
Fork the repo and start adding blocks in minutes.

[Start building →](/tutorial102)

### 🧩 Component library
Every block, with live examples and full documentation.

[Browse →](/components/)

### 🏠 Back to home
[Home →](/)
```
{: .cards cols="3" }

{% include backtotop.md %}
