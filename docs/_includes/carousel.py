@component(attrs=[{"n": "current", "t": "int"}], methods=["next", "prev", "goto"])
class Carousel(Block):
    """🎠 Slides that turn by themselves — a list, one item at a time, dots to jump."""
    delay = Attr(int, 4000)                 # ms each item stays

    @property
    def current(self):
        items = self._qq(".lc-carousel-item")
        for i in range(len(items)):
            if items[i]._el.classList.contains("active"):
                return i
        return 0

    def _dots(self):
        return self._el.querySelectorAll(".lc-carousel-dots span") if self._el else None

    def goto(self, n):
        d = self._dots()
        if d is not None and int(d.length) > n:
            d.item(n).click()
        return self

    def next(self):
        items = self._qq(".lc-carousel-item")
        return self.goto((self.current + 1) % len(items)) if items else self

    def prev(self):
        items = self._qq(".lc-carousel-item")
        return self.goto((self.current - 1) % len(items)) if items else self
