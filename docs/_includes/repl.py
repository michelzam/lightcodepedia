@component()
class Repl(Block):
    """⌨️ A Python prompt in the page — type, run, see; what ran before is kept."""
    init = Attr(str)                        # the lines it runs first

