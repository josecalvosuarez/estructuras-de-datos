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

# ---------- AVL Tree ----------

@dataclass
class AVLNode:
    key: any
    left = None
    right = None
    height = 1

def _height(n):
    """Returns node height (0 if None)."""
    return n.height if n else 0

def _update(n):
    """Updates the height of a node."""
    n.height = 1 + max(_height(n.left), _height(n.right))

def _balance(n):
    """Returns balance factor of a node."""
    return (_height(n.left) - _height(n.right)) if n else 0

class AVLTree:
    """AVL Tree with self-balancing insert and delete."""

    def __init__(self):
        """Initializes an empty AVL tree."""
        self.root = None

    def rotate_left(self, z):
        """Performs a left rotation."""
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        _update(z)
        _update(y)
        return y

    def rotate_right(self, z):
        """Performs a right rotation."""
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        _update(z)
        _update(y)
        return y

    def search(self, key):
        """Searches for a key in the AVL tree."""
        cur = self.root
        while cur:
            if key == cur.key:
                return cur
            cur = cur.left if key < cur.key else cur.right
        return None

    def insert(self, key):
        """Inserts a key into the AVL tree."""
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return AVLNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        _update(node)
        bf = _balance(node)
        if bf > 1 and key < node.left.key:
            return self.rotate_right(node)
        if bf < -1 and key > node.right.key:
            return self.rotate_left(node)
        if bf > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if bf < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    def _min_node(self, n):
        while n.left:
            n = n.left
        return n

    def delete(self, key):
        """Deletes a key from the AVL tree."""
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            succ = self._min_node(node.right)
            node.key = succ.key
            node.right = self._delete(node.right, succ.key)
        _update(node)
        bf = _balance(node)
        if bf > 1 and _balance(node.left) >= 0:
            return self.rotate_right(node)
        if bf > 1 and _balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if bf < -1 and _balance(node.right) <= 0:
            return self.rotate_left(node)
        if bf < -1 and _balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    def pretty_print(self):
        """Displays the AVL tree structure."""
        pretty_print(self.root, label=lambda n: str(n.key))
