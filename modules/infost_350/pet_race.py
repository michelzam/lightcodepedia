"""
For a curious student
Who wants to organize a pet race
Our app shows a way to manage it
While having fun
"""

import time
import os

from toys import Toy

class Pet:
    def __init__(self, name: str, distance: int = 20, speed: int = 1, icon: str = "🐶"):
        self.name = name
        self.distance = distance
        self.icon = icon
        self.speed = speed
        self.toys: list[Toy] = []

    def __str__(self):
        return f"{self.icon} {self.name} {[str(toy) for toy in self.toys]}"

    def display(self):
        print("-" * self.distance, self)

    def come(self) -> None:
        self.distance -= self.speed
        self.display()

class RoboPet(Pet):
    def display(self):
        print("-" * self.distance, "🤖", self.icon, self.name)

class Race:
    def __init__(self, pets: list[Pet] = []):
        self.pets: list[Pet] = pets

    def run(self) -> Pet:
        """ Run the race and return the winner pet """
        print("Race with various kinds of pets")
        winner: Pet | None = None

        while winner is None:
            # os.system("clear")
            for pet in self.pets:
                pet.come()
                if pet.distance <= 0:
                    print(f"{pet.name} won!")
                    winner = pet
                    break
            time.sleep(0.5)
        return winner

class Tournament:
    def __init__(self, races: dict):
        self.races = races

    def run(self):
        winners = {}
        budget = 10 * len(self.races)
        for name, race in self.races.items():
            print(f"\n🏁 Starting race: {name}")
            winner = race.run()
            if winner:
                winner.toys.append(Toy(price=budget))
                budget -= 10
                winners[winner.name] = winner

        print("🏆 Winners:", ", ".join(str(pet) for pet in winners.values()))

def main():
    race1 = Race(pets=[Pet("Lucky", distance=10), RoboPet("Muppets", speed=2)])
    race2 = Race(pets=[Pet("Flora", icon="🐩"), RoboPet("Lassie", speed=3)])
    race3 = Race(pets=[Pet("Oliver", icon="🦮", distance=3)])
    tournament1 = Tournament({"first": race1, "second": race2, "third": race3})
    tournament1.run()

if __name__ == "__main__":
    main()
