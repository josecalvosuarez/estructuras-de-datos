from dataclasses import dataclass

# ---------- Pretty Printer ----------

def _build_ascii_tree(node, label=str):
    """
    Recursively builds an ASCII rendering for a binary tree.
    Returns (lines, width, height, root_x).

    - lines: list of strings (each a row)
    - width: total character width of the block
    - height: number of rows
    - root_x: horizontal index (0-based) of the root label start within the block
    """
    if node is None:
        return [""], 0, 0, 0

    s = str(label(node))
    sw = len(s)

    left_lines, lw, lh, lx = _build_ascii_tree(getattr(node, "left", None), label) if getattr(node, "left", None) else ([""], 0, 0, 0)
    right_lines, rw, rh, rx = _build_ascii_tree(getattr(node, "right", None), label) if getattr(node, "right", None) else ([""], 0, 0, 0)

    # No children
    if lw == 0 and rw == 0:
        return [s], sw, 1, sw // 2

    # Only left child
    if rw == 0:
        # position root so its left edge is just after left block
        root_x = lw + 1 + (sw // 2)
        first = " " * (lx + 1) + "_" * (lw - lx - 1) + s
        second = " " * lx + "/" + " " * (lw - lx - 1 + sw)
        # pad right side to same height
        pad = [""] * lh
        merged = [l.ljust(lw) + " " * sw for l in left_lines]  # right is empty
        return [first, second] + merged, lw + sw, 2 + lh, root_x

    # Only right child
    if lw == 0:
        root_x = (sw // 2)
        first = s + "_" * rx + " " * (rw - rx)
        second = " " * (sw + rx) + "\\" + " " * (rw - rx - 1)
        merged = [" " * sw + r.ljust(rw) for r in right_lines]
        return [first, second] + merged, sw + rw, 2 + rh, root_x

    # Two children
    gap = 2  # minimum gap between left and right blocks
    # position subroots relative to their blocks
    # left connector goes from (lx) up to just before root; right from after root to (sw+rx)
    # Build top two connector rows
    first = (
        " " * (lx + 1) + "_" * (lw - lx - 1) +
        s +
        "_" * rx + " " * (rw - rx)
    )
    second = (
        " " * lx + "/" + " " * (lw - lx - 1) +
        " " * sw +
        " " * rx + "\\" + " " * (rw - rx - 1)
    )

    # Balance heights
    h = max(lh, rh)
    left_lines += [""] * (h - lh)
    right_lines += [""] * (h - rh)

    merged = [l.ljust(lw) + " " * sw + r.ljust(rw) for l, r in zip(left_lines, right_lines)]
    root_x = lw + (sw // 2)
    return [first, second] + merged, lw + sw + rw, 2 + h, root_x


def pretty_print(root, label=str):
    """Prints a binary tree with aligned branches and multi-digit support."""
    lines, _, _, _ = _build_ascii_tree(root, label)
    for line in lines:
        print(line.rstrip())

# ---------- Red-Black Tree ----------

@dataclass
class RBNode:
    key: any
    color = "R"
    left = None
    right = None
    parent = None

class RBTree:
    """Red-Black Tree following CLRS-style balancing rules."""

    def __init__(self):
        """Initializes an empty Red-Black tree."""
        self.NIL = RBNode(key=None, color="B")
        self.root = self.NIL

    def _is_nil(self, x):
        """Checks if a node is the sentinel NIL."""
        return x is self.NIL

    def rotate_left(self, x):
        """Performs a left rotation around node x."""
        y = x.right
        x.right = y.left
        if not self._is_nil(y.left):
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None or x.parent is self.NIL:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rotate_right(self, x):
        """Performs a right rotation around node x."""
        y = x.left
        x.left = y.right
        if not self._is_nil(y.right):
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None or x.parent is self.NIL:
            self.root = y
        elif x is x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def search(self, key):
        """Searches for a key in the Red-Black tree."""
        cur = self.root
        while not self._is_nil(cur):
            if key == cur.key:
                return cur
            cur = cur.left if key < cur.key else cur.right
        return None

    def insert(self, key):
        """Inserts a key into the Red-Black tree."""
        node = RBNode(key=key, color="R", left=self.NIL, right=self.NIL, parent=None)
        y = self.NIL
        x = self.root
        while not self._is_nil(x):
            y = x
            x = x.left if node.key < x.key else x.right
        node.parent = y if y is not self.NIL else None
        if y is self.NIL:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node
        self._insert_fixup(node)

    def _insert_fixup(self, z):
        """Restores Red-Black properties after insertion."""
        while z.parent and z.parent.color == "R":
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.right
                if y and y.color == "R":
                    z.parent.color = "B"
                    y.color = "B"
                    z.parent.parent.color = "R"
                    z = z.parent.parent
                else:
                    if z is z.parent.right:
                        z = z.parent
                        self.rotate_left(z)
                    z.parent.color = "B"
                    z.parent.parent.color = "R"
                    self.rotate_right(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y and y.color == "R":
                    z.parent.color = "B"
                    y.color = "B"
                    z.parent.parent.color = "R"
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self.rotate_right(z)
                    z.parent.color = "B"
                    z.parent.parent.color = "R"
                    self.rotate_left(z.parent.parent)
        self.root.color = "B"

    def pretty_print(self):
        """Displays the Red-Black tree structure."""
        def label(n):
            if self._is_nil(n):
                return ""
            return f"{n.key}({n.color})"
        pretty_print(self.root if not self._is_nil(self.root) else None, label=label)
