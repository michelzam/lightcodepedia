# 💡 Tutorial 101

## 👋 Welcome

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

Lightcode relies on **nothing** on the server side. It runs **markdown** files with tiny custom kramdown decorations to bring blocks alive.
````
{: .blocks cols="2" }

````
### 🐕 This text block has an image [Blocks can also show images]

**Man's best friend** 🐶

![Lucky — a black Labrador](/assets/lab.jpg)

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
>
> Amid the crowd, the thunder roars,
> With every note, the spirit soars.
> From stairways high to oceans deep,
> Their legacy forever to keep.

Read more about [markdown](https://www.markdownguide.org/cheat-sheet/).
````
{: .blocks cols="2" }

## 🎬 Video

````
### 🎥 Video [Play Lucky's favourite song]

🎵 Man's best song. Go ahead. Play it!

[▶️ Led Zeppelin — Black Dog](https://youtu.be/6tlSx0jkuLM?si=OHbXv8Vp9NKidh9e)

{: .video height="380" }
````
{: .block }

## 🔗 Proxies

````
### 🐕 Proxy [This is a proxy, including content from another module]

This is a `proxy`, including content from another module.

[Lucky](/_dog)

{: .embed }

### 🐕 Proxy too [Just another proxy to the same module]

Another `proxy`, including the same module.

[Lucky](/_dog)

{: .embed }
````
{: .blocks cols="2" }

## 🗺️ Map

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

## 📊 Dataset, Grid & Chart

One **dataset**, declared once — the grid is its editable list view, the chart
shows whichever row you select. Data flows `dataset → grid → chart`
(Shift + Alt-hover any of them to see the pipes).

````
### 🐕 Grid [Editable — click a cell to change a value, then watch the chart]

Select a row to update the chart → edit a number to refresh it.

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

Updates when you select a row in the grid ← edit a value and it refreshes.

[Selected dog](#)
{: .chart type="bar" bound-to="dog_grid_tuto" x="breed" height="280" }
````
{: .blocks cols="2" }

## 📋 Forms

````
### 🐕 Lucky [Editable — change any field, it's a live object]

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
{: .form editable="true" }

### 🐠 Wanda [Editable — Wanda is a fish, not a dog!]

```yaml
name: Wanda
age: 2
breed: Goldfish
colour: Orange
weight_kg: 0.03
top_speed_kmh: 6
adopted: false
favorite_toys:
  - plastic castle
  - bubble ring
  - flake food
vet:
  name: Dr. Patel
  phone: "555-0142"
notes: A fish, not a dog! Best friends with Lucky through the bowl glass.
```
{: .form editable="true" }
````
{: .blocks cols="2" }

## 🎲 Quiz

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

**Q:** Wanda is not a dog. What kind of animal is she?

- [ ] A dog, just like Lucky
- [ ] A cat
- [x] A fish 🐠
- [ ] A bird

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


