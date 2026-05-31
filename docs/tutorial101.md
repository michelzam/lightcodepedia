---
title: Tutorial 101
---
# 💡 Tutorial 101

````
### 👋 Welcome! [This is a tutorial block]

🎓 This tutorial is a *light-code* `module` that demonstrates basic **building blocks**, or just `blocks` :

- ✅ Formatted text
- ✅ Basic blocks (image / text / videos)
- ✅ Interactive maps / proxies
- ✅ Data components (forms / grids / charts)
- ✅ Objects encapsulating data / state / behavior / functions
- ✅ Quizzes

Go ahead, explore, play, learn and have fun! 🎉

### 📖 This block is a text [Blocks can display formatted text, hints and help]

A `text` block is a simple block that displays formatted text.

- ✅ Formatted text **bold** / *italic* / colors
- ✅ Item lists
- ✅ Bouquet 🌹🌸💐🌺🌼🌻
- ✅ Text blocks use hints/helps
- ✅ Actually all blocks use hints/helps

Lightcode relies on [streamlit](https://streamlit.io). Here, we used **markdown**.
Please feel free to explore the streamlit documentation.
````
{: .blocks cols="2" }

````
### 🐕 This text block has an image [Blocks can also show images]

**Man's best friend** 🐶

![Lucky — a black Labrador](https://picsum.photos/id/237/500/400)

Cute, huh — this local dog?

### 📖 Doc [This is documentation about dogs]

Docs about dogs can use **bold** and *italic* text
and also be quite long and boring …

> In the haze of a London fog,
> A riff emerges, cutting like a saw.
> Strumming strings and pounding drums,
> Led Zeppelin, their magic comes.
> 
> Amid the mist, a black dog roams,
> Guiding the band to rock and roll thrones.
> Not just a pet, but a symbol, a sign,
> Of music that transcends all time.

> Amid the crowd, the thunder roars,
> With every note, the spirit soars.
> From stairways high to oceans deep,
> Their legacy forever to keep.

Read more about [Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/).
````
{: .blocks cols="2" }

````
### 🎥 Video [Play Lucky's favourite song]

🎵 Man's best song. Go ahead. Play it!

[▶️ Led Zeppelin — Black Dog](https://youtu.be/6tlSx0jkuLM?si=OHbXv8Vp9NKidh9e)

{: .video height="380" }
````
{: .block }

````
### 🐕 Proxy [This is a proxy, including content from another module]

This is a `proxy`, including content from another module.

[Lucky](/_dog)

{: .embed }

### 🐕 Proxy too [Just another proxy to the same module]

Just another `proxy`, including content from the same other module.

[Lucky](/_dog)

{: .embed }
````
{: .blocks cols="2" }

````
### 🗺️ Map [This map is interactive — zoom in to spot parks in Paris]

This `map` is interactive. You can zoom in and out to spot parcs in Paris if you want to walk your dog.

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
{: .map height="340" zoom="12" }
````
{: .block }

````
### 🐕 Grid [Select a row to update the chart]

Select a row to update the chart →

```csv
breed,top_speed_kmh
Greyhound,72
Saluki,68
Vizsla,64
Jack Russell,56
Border Collie,48
German Shepherd,48
Labrador,40
Beagle,40
Corgi,35
Pug,15
Bulldog,14
```
{: .datagrid #dog-grid-tuto format="csv" title="Dog top speeds" height="280" }

### 📊 Chart [Updates when you select a row in the grid]

Updates when you select a row in the grid ←

```csv
breed,top_speed_kmh
Greyhound,72
Saluki,68
Vizsla,64
Jack Russell,56
Border Collie,48
German Shepherd,48
Labrador,40
Beagle,40
Corgi,35
Pug,15
Bulldog,14
```
{: .chart type="bar" bound-to="dog-grid-tuto" x="breed" y="top_speed_kmh" height="280" }
````
{: .blocks cols="2" }

````
### 🐕 Lucky [Lucky's profile]

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

### 🦋 Wanda [Wanda's profile]

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

````
### 🎲 Your first riddle: Lucky & Wanda

**Q:** What is Lucky's breed?

- [ ] Beagle
- [ ] German Shepherd
- [x] Labrador Retriever
- [ ] Golden Retriever

{: .quiz }

**Q:** According to the grid, which dog runs the fastest?

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
````
{: .block }

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
