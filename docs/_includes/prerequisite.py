@component()
class Prerequisite(Block):
    """📋 A gate — the pages to finish first; what follows stays hidden until they are done."""
    pass_pct = Attr(int, 100, column="pass")    # the share of each page's points needed, in %
    escape   = Attr(str)                        # "true" offers a "show it anyway" button — or its own words
    features = Attr(bool)                       # the pages' proofs must be green too, not only their points
