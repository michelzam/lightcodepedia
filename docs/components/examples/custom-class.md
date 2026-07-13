---
---

# 🐍 Your own class

You've met **Lucky** and **Wanda** as objects. Every object is built from a **class** — a blueprint that says what an object *has* (attributes) and what it can *do* (methods). Here you write your own, live in the browser. Edit the code, press **▶ Run**.

## 🧱 The smallest class

A class with an `__init__` that stores some **attributes**, then one **instance** made from it:

```python
class Dog:
    def __init__(self, name, breed, top_speed_kmh):
        self.name = name              # attributes — what the object HAS
        self.breed = breed
        self.top_speed_kmh = top_speed_kmh

lucky = Dog("Lucky", "Beagle", 40)    # an instance — a real dog
print(lucky.name, "is a", lucky.breed)
print("Top speed:", lucky.top_speed_kmh, "km/h")
```
{: .run rows="11" }

`self` is the object talking about itself. `Dog(...)` runs `__init__` and hands you a new dog.

## 🐾 Add behaviour — methods

A **method** is a function that belongs to the object and can use its own state:

```python
class Dog:
    def __init__(self, name, top_speed_kmh):
        self.name = name
        self.top_speed_kmh = top_speed_kmh

    def bark(self):                       # behaviour — what the object can DO
        return f"{self.name} says woof!"

    def run(self):
        return f"{self.name} runs at {self.top_speed_kmh} km/h"

lucky = Dog("Lucky", 40)
wanda = Dog("Wanda", 6)                   # same blueprint, different object
print(lucky.bark())
print(wanda.run())
```
{: .run rows="15" }

One class, two objects — each carries its own attributes, each behaves on its own state. That's the whole idea of object-oriented programming.

## 🔗 Objects that know each other

Objects communicate by holding a **reference to another object**. Declare the link as a typed attribute — `friend: Pet` — then follow it from one object to the next:

```python
class Pet:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.friend = None              # friend: Pet — a typed link to another object

lucky = Pet("Lucky", "dog")
wanda = Pet("Wanda", "fish")
lucky.friend = wanda                    # now Lucky knows Wanda
print(lucky.name, "→", lucky.friend.name, "the", lucky.friend.species)
```
{: .run rows="13" }

`lucky.friend.species` *hops* from one object to another through an attribute you declared. That declared link is how a graph of objects is navigated.

The platform's own components get this for free: each one inherits a base class `Block`, which hands it `self.page` — a live directory that resolves any other component by id (`self.page.dog_grid`). Your own classes aren't components, so you simply declare the exact links you need — `friend: Pet` — and nothing more. Same idea; explicit instead of built in.

## 🎯 Your turn

Add a `fetch()` method that returns `"<name> fetches the ball!"`, then call it. The Run button checks nothing — just see your class come alive:

```python
class Dog:
    def __init__(self, name):
        self.name = name

    # add your fetch(self) method here

rex = Dog("Rex")
# print(rex.fetch())
```
{: .run rows="11" }

> Lovely first lesson after the 3D playground: students *used* Lucky and Wanda as
> objects; now they build the blueprint those objects came from. The penny drops:
> "so a class is just the recipe, and each object is a cake."
{: .speaker-note }

**Q:** In `lucky = Dog("Lucky", 40)`, what is `Dog`?

- [ ] The object — a specific dog named Lucky.
- [x] The class — the blueprint every Dog object is built from.
- [ ] A method that prints the dog's name.
- [ ] An attribute of `lucky`.
{: .quiz }

**Q:** What does `self` refer to inside a method?

- [x] The specific object the method was called on.
- [ ] The class itself, shared by all objects.
- [ ] The previous object created.
- [ ] A required keyword with no real meaning.
{: .quiz }

See these same dogs as live 3D objects in the [Lucky & Wanda playground](/components/examples/lucky3d).
