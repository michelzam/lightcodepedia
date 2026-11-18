@component()
class Cards(Block):
    """🃏 Sections as cards, side by side — a heading each, wrapping as the page narrows."""
    cols = Attr(str, "auto")                # how many side by side — a number, or auto to fill the width
    gap  = Attr(int, 18)                    # the space between cards, in pixels
