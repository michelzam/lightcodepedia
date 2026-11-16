@component()
class Folder(Block):
    """📁 A folder's pages as cards — this one's, the parent's, or a path's — with the reader's progress."""
    view         = Attr(str)                        # cards unless said; recap — one line per page: earned, missed, left
    parent       = Attr(bool)                       # list the folder this page sits in
    path         = Attr(str)                        # the folder it lists, when not this page's own
    source       = Attr(str)                        # a server's pages it lists instead — db.table
    cols         = Attr(str, "auto")                # cards per row
    sort         = Attr(str)                        # name unless said; recent — the last touched first
    open         = Attr(str)                        # runner — a card opens its page in the runner
    title        = Attr(str)                        # its title bar
    tools        = Attr(str)                        # the 🧰 metrics tools under it, comma-separated
    show_private = Attr(bool, column="show-private")  # the author's pages (named _…) show too
