@component(icon="📄")
class Code(Block):
    """📄 Code shown with its colours, a title bar and 📋 Copy — bound to a pad, ⬇ Add puts its lines there."""
    title       = Attr(str)                 # its title bar — a leading emoji is its icon
    lang        = Attr(str, "text")         # the language painted, when the fence names none
    placeholder = Attr(str)                 # what an empty card says, until a page event writes its lines
    bound       = Attr("Mdpad")             # the pad its ⬇ Add puts the lines in

    @property
    def text(self):
        """The card's lines."""
        v = self._attr("data-lc-value")
        if not v:
            return ""
        return str(js.JSON.parse(v).text or "")

    @text.setter
    def text(self, v):
        """Write the card's lines — an event's way to show code (an agent's
        on_response: code.text = agent.response.example). The card repaints;
        its ⬇ Add, if bound, offers the new lines."""
        f = getattr(self._el, "_lcSetText", None) if self._el is not None else None
        if f is not None:
            f(str(v))
