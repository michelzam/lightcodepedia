"""
For playful students
Who can't find their toys
Our app shows a way to organize them
While having fun
"""


class Toy:
    def __init__(self, name: str = "", icon: str = "🧸", price: float = 1):
        self.name = name
        self.icon = icon
        self.price = price

    def __str__(self):  # called by python when converting to str
        return f"{self.icon} {self.name}, {self.price}$"

def play():
    toys = [Toy(name="Balloon", icon="🪀"), Toy(name="Teddy", price = 2)]

    for toy in toys:
        if toy.price < 2:
            print(toy)
        else:
            print()

    for toy in toys:
        print(toy if toy.price < 2 else "")  # if encapsulated in expression

    [print(toy) for toy in toys if toy.price < 2]

if __name__ == "__main__":
    play()

