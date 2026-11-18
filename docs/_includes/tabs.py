@component(attrs=[{"n": "active", "t": "int"}], methods=["select"])
class Tabs(Block):
    """📑 Sections as tabs — one shown at a time, its title a tab."""
    path = Attr(str)                        # a file whose sections become the tabs, instead of a fence

    @property
    def active(self):
        if self._el is None:
            return 0
        tabs = self._el.querySelectorAll(".lc-tab-btn")
        for i in range(int(tabs.length)):
            if tabs.item(i).classList.contains("active"):
                return i
        return 0

    def select(self, n):
        if self._el is not None:
            tabs = self._el.querySelectorAll(".lc-tab-btn")
            if tabs is not None and int(tabs.length) > n:
                tabs.item(n).click()
        return self
