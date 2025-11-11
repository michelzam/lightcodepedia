import sys
print(f"I am a file from server disk")
modules = [m for m in sys.modules if not m.startswith("_")]
# print(f"{modules = }")

def dummy(name: str = "noname") -> str:
    return f"Return from {name}!"