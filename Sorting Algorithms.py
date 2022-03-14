"""
This file contains all the sorting algorithms we covered in the last unit.
"""

from typing import Any

# Binary Sort
# Compare the item ot the middle of a sorted list. If the item we are searchoiing for is
# greater than the middle, the item is in the right.
# If the item we are looking for is less than the middle, the item is to the left.
# Otherwise, we have found the item.


def binary_search(lst: list, item: Any) -> bool:
    """Return whether item is in lst using the binary search algorithm.

    Preconditions:
        - is_sorted(lst)
    """
    b = 0
    e = len(lst)

    while b < e:
        # Loop invariants
        assert all(lst[i] < item for i in range(0, b))
        assert all(lst[i] > item for i in range(e, len(lst)))

        m = (e - b) // 2
        if item == lst[m]:
            return True
        elif item < lst[m]:
            e = m
            ...
        else:
            b = m + 1
            ...

    # If the loop ends without finding the item, the item is not in the list.
    return False
