@component(attrs=[{"n": "text", "t": "str"}, {"n": "color", "t": "str"}],
           events=["on_click"], methods=["click"])
class Button(Block):
    """🖱️ A button — its Python runs on a click, the page's values in hand."""
    kind = Attr(str)                        # secondary, success, danger or outline — its look

    @property
    def text(self):
        return str(self._el.textContent or "").strip() if self._el else ""

    @text.setter
    def text(self, v):
        if self._el:
            self._el.textContent = str(v)

    @property
    def color(self):
        return self._attr("data-color") or ""

    @color.setter
    def color(self, v):
        if self._el:
            if v:
                self._el.setAttribute("data-color", v)
            else:
                self._el.removeAttribute("data-color")

    def _event_src(self, name):
        # on_click carries its Python body in data-lc-py (see click()).
        return self._attr("data-lc-py") or "" if name == "on_click" else ""

    def click(self):
        code = self._attr("data-lc-py") or ""
        if not code:
            if self._el:
                self._el.click()
            return self
        # A BARE BODY RUNS AT MODULE SCOPE, `button` in hand — the same
        # contract the JS side runs on a real click, so a proof cannot pass
        # on semantics no reader ever gets. What the lines set, the page
        # reads: `message = …` in a button feeds `{= message }` beside it.
        g = globals()
        g["button"] = self
        try:
            if "def on_click" in code:
                exec(code + "\non_click(button)\n", g)
            else:
                exec(code, g)
        except Exception as _e:
            if self._el:
                self._el.setAttribute("data-lc-err", str(_e))
        try:
            js.window.document.dispatchEvent(js.CustomEvent.new("lc-model-changed"))
        except Exception:
            pass
        return self


# ════════════════════════ gallery component wrappers ═════════════════════════
# Knobs are typed properties (data-* backed); behaviours are methods.
