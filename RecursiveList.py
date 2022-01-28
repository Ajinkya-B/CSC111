"""
This file goes over some of the functions we used to work with recursive list.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Ajinkya Bhosale.
"""

from __future__ import annotations
from typing import Any, Optional, Union


# Simple recursion function using Euclidean Algorithm
def euclidean_gcd(a: int, b: int) -> int:
    """Return the gcd of a and b.

    Preconditions:
        - a >= 0 and b >= 0
    """
    # base case
    if b == 0:
        return a
    else:
        return euclidean_gcd(b, a % b)


# Recursive Function Design Recipe for Nested Lists
#
# 1. Write a doctest example for the base case.
#    (What should the return value be for the base case?)
#
# 2. Write a doctest example to illustrate the induction step.
#    - Pick a nested list containing at least 3 sublist, where at least:
#         - one that's integer
#         - one that's nested list
#
#
# Code template for recursive list:
#
# def function(nested_list: Union[int, list]) -> ...:
#     if isinstance(nested_list, int):
#         ...
#     else:
#         accumulator = ...
#
#         for sublist in nested_list:
#             rec_value = function(sublist)
#             accumulator = ... accumulator ... rec_value ...
#
#         return accumulator


# Traversing through non-uniform nested lists
# [[1, [2]], [[[3]]], 4, [[5, 6], [[[7]]]]]
def flatten_list(nested_list: Union[int, list]) -> list:
    """
    Returns a simple non-nested list
    >>> flatten_list(1)
    [1]
    >>> flatten_list([[1, [2]], [[[3]]], 4, [[5, 6], [[[7]]]]])
    [1, 2, 3, 4, 5, 6, 7]
    """

    if isinstance(nested_list, int):
        return [nested_list]
    else:
        list_so_far = []
        for sublist in nested_list:
            list_so_far.extend(flatten_list(sublist))

        return list_so_far


def sum_nested(nested_list: Union[int, list]) -> int:
    """
    Return the sum of the given nested list.

    >>> sum_nested(1)
    1
    >>> sum_nested([1, [2, 3], [[4], 5]])
    15
    """

    if isinstance(nested_list, int):
        return nested_list
    else:
        sum_so_far = 0
        for sublist in nested_list:
            sum_so_far += sum_nested(sublist)

        return sum_so_far


def all_less_than(nested_list: Union[int, list], n: int) -> bool:
    """Return whether every integer in nested_list is less than n.

    >>> all_less_than(10, 3)
    False
    >>> all_less_than([1, 2, [1, 2], 4], 10)
    True
    >>> all_less_than([], 0)
    True
    """

    if isinstance(nested_list, int):
        return n > nested_list
    else:
        for sublist in nested_list:
            if not all_less_than(sublist, n):
                return False

        return True


def add_n(nested_list: Union[int, list], n: int) -> Union[int, list]:
    """Return a new nested list where n is added to every item in nested_list.

    >>> add_n(10, 3)
    13
    >>> add_n([1, 2, [1, 2], 4], 10)
    [11, 12, [11, 12], 14]
    """
    if isinstance(nested_list, int):
        return nested_list + n
    else:
        list_so_far = []
        for sublist in nested_list:
            list_so_far.append(add_n(sublist, n))

        return list_so_far