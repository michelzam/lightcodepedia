@component(attrs=[{"n": "samples", "t": "int"}, {"n": "heap_mb", "t": "float"}, {"n": "dom_nodes", "t": "int"}])
class Vitals(Block):
    """📊 The page's own health, sampled — memory, parts, time."""
    interval = Attr(float, 2)               # seconds between samples
    max      = Attr(int, 120)               # how many samples it keeps

    @property
    def samples(self):
        return int(self._attr("data-samples") or 0)

    @property
    def heap_mb(self):
        v = self._attr("data-heap")
        return float(v) if v else None

    @property
    def dom_nodes(self):
        return int(self._attr("data-dom") or 0)
