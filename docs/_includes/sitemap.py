@component()
class Sitemap(Block):
    """🗺️ A folder drawn as a map — its pages, how they link, which are done."""
    path   = Attr(str, ".")                     # the folder it maps — the link's own target unless said
    height = Attr(int, 420)                     # pixels
