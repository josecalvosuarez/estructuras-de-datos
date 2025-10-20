
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


# ---------- Binary Search Tree (BST) ----------

@dataclass
class BSTNode:
    key: any
    left = None
    right = None

class BST:
    """Binary Search Tree implementation with insert, search, delete."""

    def __init__(self):
        """Initializes an empty BST."""
        self.root = None

    def search(self, key):
        """Searches for a key in the tree."""
        cur = self.root
        while cur:
            if key == cur.key:
                return cur
            cur = cur.left if key < cur.key else cur.right
        return None

    def insert(self, key):
        """Inserts a key into the BST."""
        if not self.root:
            self.root = BSTNode(key)
            return
        parent, cur = None, self.root
        while cur:
            parent = cur
            cur = cur.left if key < cur.key else cur.right
        if key < parent.key:
            parent.left = BSTNode(key)
        else:
            parent.right = BSTNode(key)

    def _min_node(self, x):
        """Returns the node with the minimum key in a subtree."""
        while x.left:
            x = x.left
        return x

    def delete(self, key):
        """Deletes a key from the BST."""
        self.root = self._delete_rec(self.root, key)

    def _delete_rec(self, node, key):
        """Recursive deletion helper."""
        if not node:
            return None
        if key < node.key:
            node.left = self._delete_rec(node.left, key)
        elif key > node.key:
            node.right = self._delete_rec(node.right, key)
        else:
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            succ = self._min_node(node.right)
            node.key = succ.key
            node.right = self._delete_rec(node.right, succ.key)
        return node

    def pretty_print(self):
        """Displays the tree structure."""
        pretty_print(self.root, label=lambda n: str(n.key))


if __name__ == "__main__":
    print("=== BST ===")
    bst = BST()
    for k in [7, 3, 10, 1, 5, 9, 12, 4, 6, 11]:
        bst.insert(k)
    bst.pretty_print()
    print("\nDelete 7 (root):")
    bst.delete(7)
    bst.pretty_print()
    print("\nSearch 6:", bst.search(6) is not None)