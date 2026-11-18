@component()
class Qr(Block):
    """🔳 A square a phone scans — a link, a shipped app, or this page."""
    size  = Attr(int, 180)                  # pixels, a side
    ship  = Attr(str)                       # the shipped app it opens — its latest version
    here  = Attr(bool)                      # opens this very page
    align = Attr(str)                       # left, center or right
