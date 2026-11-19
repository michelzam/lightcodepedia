@component()
class Diagram(Block):
    """🗺 The model, drawn — classes, their links and their states, read live from the page's islands."""
    scope  = Attr(str)                      # a class, or several: A,B — each with what it links to; the whole model unless said
    states = Attr(bool, True)               # the state machines drawn too; false hides them
