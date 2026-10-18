# 📒 The walk log

Every walk the class has made, kept in the shelter's database.

[the shelter](supabase://shelter)
{: .database #shelter unlisted="a4d8afb272f7" }

```python
class Dog(Object):
    """🐕 A dog of the shelter."""
    name = Attr(str)

class Walk(Object):
    """🦮 One walk of a shelter dog."""
    dog = Attr(Dog)
    walker = Attr(str)
    hour = Attr(str)

    @property
    def who(self):
        """👥 The dog and its walker."""
        return (self.dog.name if self.dog else "?") + " & " + self.walker
```
{: .model source="shelter" }

[the walks](#)
{: .datagrid source="Walk" #walks }

### 📝 TODO

- [ ] a form on the selected walk
- [ ] my walk in the log: ＋, the dog, the form

[Title](#)
{: .form master="walks" }