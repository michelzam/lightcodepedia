@component(icon="🍔", methods=["items"])
class Menu(Block):
    """🍔 A page's menu — its links, folded behind ☰ on a phone."""

    def items(self):
        return [o.text for o in self._qq("a, li")]
