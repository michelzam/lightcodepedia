@component(attrs=[{"n": "value", "t": "str"}])
class Stat(Block):
    """🏷️ One headline number from a dataset — a small chip, and the section's title while it is folded."""
    bind        = Attr(str)                 # the dataset it reads
    format      = Attr(str)                 # its words: {col} from the picked row, {count} the rows
    pick        = Attr(str, "last")         # which row feeds it: last or first
    ok_when     = Attr(str, column="ok-when")       # when the number is good — otherwise it shows red
    requires    = Attr(str)                 # a column that must be there before it says anything
    stale_after = Attr(int, column="stale-after")   # seconds: older data than this says ⚠️ stale
    stale_field = Attr(str, "run", column="stale-field")  # the column holding the row's time
    source      = Attr("Dataset")           # the other name of bind

    @property
    def value(self):
        return self.text
