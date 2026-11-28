@component(attrs=[{"n": "sent", "t": "int"}])
class Visits(Block):
    """👣 Anonymous usage of a public page, counted — the sentence a visitor reads is the switch."""
    @property
    def sent(self):
        return int(self._attr("data-lc-sent") or 0)
