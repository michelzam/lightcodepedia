@component(methods=["open", "close"])
class Dropdown(Block):
    """🔽 A button that opens a list of links."""
    label = Attr(str, "Menu")               # the button's words

    def _menu(self):
        return self._el.querySelector(".lc-dd-menu") if self._el else None

    @property
    def opened(self):
        m = self._menu()
        return bool(m and m.classList.contains("open"))

    def open(self):
        m = self._menu()
        if m is not None:
            m.classList.add("open")
        return self

    def close(self):
        m = self._menu()
        if m is not None:
            m.classList.remove("open")
        return self
