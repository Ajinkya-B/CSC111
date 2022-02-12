"""
This file goes over some of the functions we used to work with binary search trees.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Ajinkya Bhosale.
"""

from __future__ import annotations
from typing import Any, Optional


class BinarySearchTree:
    """Binary Search Tree class.

    Representation Invariants:
      - (self._root is None) == (self._left is None)
      - (self._root is None) == (self._right is None)
      - (BST Property) if self._root is not None, then
          all items in self._left are <= self._root, and
          all items in self._right are >= self._root

    Note that duplicates of the root can appear in *either* the left or right subtrees.
    """
    # Private Instance Attributes:
    #   - _root:
    #       The item stored at the root of this tree, or None if this tree is empty.
    #   - _left:
    #       The left subtree, or None if this tree is empty.
    #   - _right:
    #       The right subtree, or None if this tree is empty.
    _root: Optional[Any]
    _left: Optional[BinarySearchTree]
    _right: Optional[BinarySearchTree]

    def __init__(self, root: Optional[Any]) -> None:
        """Initialize a new BST containing only the given root value.

        If <root> is None, initialize an empty tree.
        """
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)

    def __contains__(self, item) -> bool:
        """Returns whether <item> is in this BST.
        """
        if self.is_empty():
            return False
        elif item == self._root:
            return True
        elif item > self._root:
            return self._right.__contains__(item)
        else:
            return self._left.__contains__(item)

    def is_empty(self) -> bool:
        """Returns whether BST is empty.
        """
        return self._root is None

    def insert(self, item: Any) -> None:
        """Insert <item> into this tree.

        Do not change positions of any other values.
        """
        if self.is_empty():
            self._root = item
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)
        elif item >= self._root:
            self._right.insert(item)
        else:
            self._left.insert(item)

    def remove(self, item: Any) -> None:
        """Remove *one* occurrence of <item> from this BST.

        Do nothing if <item> is not in the BST.
        """
        if self.is_empty():
            return None
        elif item == self._root:
            self._delete_root()
        elif item > self._root:
            self._right.remove(item)
        else:
            self._left.remove(item)

    def _delete_root(self):
        """Remove the root of this BST.

        Preconditions:
            - not self.is_empty()
        """
        if self._left.is_empty() and self._right.is_empty():
            self._root = None
            self._left = None
            self._right = None
        elif self._left.is_empty():
            self._root, self._left, self._right = self._right._root, self._right._left, self._right._right
        elif self._right.is_empty():
            self._root, self._left, self._right = self._left._root, self._left._left, self._left._right
        else:
            # TODO: Complete case when deleting a middle root
            pass
    