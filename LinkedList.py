"""
This file goes over some of the methods we implemented for a Linked List as a List ADT.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Ajinkya Bhosale.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

import math


class EmptyListError(Exception):
    """A custom error for Empty List Errors"""
    def __str__(self) -> str:
        return "The operation doesn't work on an empty list"


@dataclass
class _Node:
    """
    A node in a linked list.

    Instance Attributes:
      - item: The data stored in the node
      - next: The next node in the list, if any
    """
    item: Any
    next: Optional[_Node] = None


class LinkedList:
    """
    A linked list implementation of the List ADT
     """
    # Private Instance Attributes:
    #  - _first: stores the first node of the list, or by default None to represent an empty list
    _first: Optional[_Node]

    def __init__(self) -> None:
        self._first = None

    def __getitem__(self, item: int) -> Any:
        """Return the item stored at index i in this linked list.
        Raise an IndexError if index i is out of bounds.

        Preconditions:
            - i >= 0
        """

        curr = self._first
        curr_index = 0

        while curr is not None and curr_index != item:
            curr = curr.next
            curr_index += 1

        assert curr is None or curr_index == item
        if curr is None:
            raise IndexError
        else:
            return curr.item

    def maximum(self) -> float:
        """Return the maximum element in this linked list.

        Preconditions:
            - every element in this linked list is a float
            - this linked list is not empty

        >>> linky = LinkedList()
        >>> node3 = _Node(30.0)
        >>> node2 = _Node(-20.5, node3)
        >>> node1 = _Node(10.1, node2)
        >>> linky._first = node1
        >>> linky.maximum()
        30.0
        """
        max_so_far = -math.inf
        curr = self._first

        if curr is None:
            raise EmptyListError

        while curr is not None:
            max_so_far = max(max_so_far, curr.item)

        return max_so_far

    def is_empty(self) -> bool:
        """Returns if a list is empty."""
        return self._first is None

    def to_list(self) -> list:
        """Returns the linked list as an array based implementation of List ADT"""
        list_so_far = []
        curr = self._first

        while curr is not None:
            list_so_far.append(curr.item)
            curr = curr.next

        return list_so_far
