@component()
class Blocks(Block):
    """🧱 Cards side by side — a fence's ### sections, one card each (Why · How · What · Done when)."""
    cols  = Attr(str)                       # cards per row
    title = Attr(str)                       # its title
    pass
