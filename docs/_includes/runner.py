@component()
class Runner(Block):
    """📺 Another page run inside this one, live — a learner's own, or a shipped app."""
    src   = Attr(str)                       # the page it runs — a path, or ship:<app>
    title = Attr(str)                       # its window's title; "" for none
    bench = Attr(bool)                      # read from the learner's own space
    bay   = Attr(str)                       # the bay a shipped app is read from
    quiet = Attr(bool)                      # no window around it
