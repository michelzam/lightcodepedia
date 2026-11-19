@component()
class Grid(Block):
    """▤ Sections laid out in a grid of cells — a layout, not data (for rows, a datagrid)."""
    cols     = Attr(str, "auto")            # how many side by side — a number, or auto to fill the width
    gap      = Attr(int, 18)                # the space between cells, in pixels
    headings = Attr(str, "show")            # show or hide each cell's heading
