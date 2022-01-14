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

        if curr is None:
            raise IndexError
        else:
            return curr.item

    def __contains__(self, item: Any) -> bool:
        """Return whether item is in this linked list.

        >>> linky = LinkedList()
        >>> linky.__contains__(10)
        False
        >>> node2 = _Node(20)
        >>> node1 = _Node(10, node2)
        >>> linky._first = node1
        >>> linky.__contains__(20)
        True
        """
        curr = self._first

        while curr is not None:
            if curr.item == item:
                return True
            curr = curr.next
        return False

    def __len__(self) -> int:
        """Return the number of elements in this list. """
        len_so_far = 1
        curr = self._first

        if curr is None:
            return 0
        else:
            while curr.next is not None:
                len_so_far += 1
                curr = curr.next

            return len_so_far

    def __setitem__(self, i: int, item: Any) -> None:
        """Store item at index i in this list.

        Raise IndexError if i >= len(self).

        Preconditions:
            - i >= 0
        """
        curr = self._first
        count = 0
        if curr is None:
            raise IndexError
        elif i == 0:
            curr.item = item
        else:
            while curr.next is not None and count != i:
                curr = curr.next
                count += 1

            if curr.next is None:
                raise IndexError
            elif count == i:
                curr.item = item

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

    def sum(self) -> float:
        """Return the sum of the elements in this linked list.

        Preconditions:
            - all elements in this linked list are floats
        """
        curr = self._first
        sum_so_far = 0

        while curr is not None:
            sum_so_far += curr.item
            curr = curr.next

        return sum_so_far

    def count(self, item: Any) -> int:
        """Return the number of times the given item occurs in this list."""
        count = 0
        curr = self._first

        if curr is None:
            return 0
        elif curr.next is None:
            if curr.item == item:
                return 1
            else:
                return 0
        else:
            while curr.next is not None:
                if curr.item == item:
                    count += 1

            return count

    def index(self, item: Any) -> int:
        """Return the index of the first occurrence of the given item in this list.

        Raise ValueError if the given item is not present.
        """
        curr = self._first
        count = 0

        if curr is None:
            raise ValueError
        elif curr.next is None:
            if curr.item == item:
                return 0
            else:
                raise ValueError
        else:
            while curr.next is not None:
                if curr.item == item:
                    return count
                curr = curr.next
                count += 1

            raise ValueError

    def append(self, item: Any) -> None:
        """Add the given item to the end of this linked list.

        >>> linky = LinkedList()  # LinkedLists start empty
        >>> linky.append(111)
        >>> linky.append(-5)
        >>> linky.append(9000)
        >>> linky.to_list()
        [111, -5, 9000]
        """
        new_node = _Node(item)
        curr = self._first

        if curr is None:
            self._first = new_node
        else:
            while curr.next is not None:
                curr = curr.next

            curr.next = new_node

    def remove_first(self) -> Any:
        """Remove and return the first element of this list.

        Raise an IndexError if this list is empty.

        >>> lst = LinkedList([1, 2, 3])
        >>> lst.remove_first()
        1
        >>> lst.to_list()
        [2, 3]
        >>> lst.remove_first()
        2
        >>> lst.remove_first()
        3
        """
        curr = self._first
        if curr is None:
            raise IndexError
        else:
            self._first = curr.next
            return curr.item

    def remove_last(self) -> Any:
        """Remove and return the last element of this list.

        Raise an IndexError if this list is empty.

        >>> lst = LinkedList([1, 2, 3])
        >>> lst.remove_last()
        3
        >>> lst.to_list()
        [1, 2]
        >>> lst.remove_last()
        2
        >>> lst.remove_last()
        1
        """
        curr = self._first

        if curr is None:  # Case where linked list is empty
            raise IndexError
        elif curr.next is None:  # Case where the liked list only contains one element
            temp = curr.item
            self._first = None
            return temp
        else:  # Case where the linked list has more than 1 element
            while curr.next.next is not None:
                curr = curr.next
            temp = curr.next.item
            curr.next = None
            return temp
