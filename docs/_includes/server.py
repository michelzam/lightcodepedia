@component(attrs=[{"n": "exports", "t": "str", "data": True, "attr": "exports"}])
class Server(Block):
    """📡 A server, from the page — it serves a model at lc://<name>, and the pages a dataset lists."""
    model = Attr("Model")                   # the classes it serves
    pages = Attr("Dataset")                 # the pages it serves — rows of path and file

