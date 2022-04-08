"""
This file contains all the sorting algorithms we covered in the last unit.
"""

from typing import Any


"""
============================================
Binary Search
============================================
"""
# In this case we already start with a sorted list.
# Then we compare the item we are searching for to the middle of the list.
# i.e. If we have a sorted list of length 100, we would be searching for the 50th index item

# How Binary Search Works?
# IF the center item is equal to the item we are searching for then we return True.
# IF the center item is greater, then we only have to search for the right half.
# IF the center item is lower, then we only need to search the left half.
# Finally, IF there are no more elements to search for then we can return False.


# Iterative implementation of Binary Search

def binary_search(lst: list, item: Any) -> bool:
    """Return whether item is in lst using the binary search algorithm.

    Preconditions:
        - is_sorted(lst)
    """
    # b and e are the endpoints of the current search range: lst[b:e]
    b = 0
    e = len(lst)

    while b < e:
        c = (e + b) // 2  # center point of the list
        if item == lst[c]:
            return True
        elif item < lst[c]:
            e = c
        else:  # item > lst[c]
            b = c + 1

    return False

# Running-Time :)

# the assignment statement and the return statement all count as 1 step.
# Initially the length of the current search range is n.
# The while loop stops once b >= e.
# On each iteration of hte while loop, hte length of the current search range is halved.
# -> i.e. the size decreases by a factor of 2

# In total, the binary search function requires log_2(n) + 1 steps.
# which is Theta of log(n).


"""
============================================
Selection Sort
============================================
"""
# Given an unsorted list, we repeatedly extract the lowest element and put it in a sorted stack
#     [1, 2, 7, 3, 4]
#     |____| |______|
#      |          |
#    sorted    unsorted
# So in this case, we would find min([7, 3, 4]), which is 3.
# Now we place this 3 in the 2nd index and the current state becomes...
#     [1, 2, 3, 7, 4]
#     |_______| |___|
#       |          |
#     sorted    unsorted
# We repeat this process n times, where n is the length of the list.


# In-place/mutating implementation of selection sort

def selection_sort(lst: list) -> None:
    """Sort the given list using the selection sort algorithm.
    >>> lst = [3, 7, 2, 5]
    >>> selection_sort(lst)
    >>> lst
    [2, 3, 5, 7]
    """

    for i in range(len(lst)):
        smallest_index = _min_index(lst, i)
        lst[i], lst[smallest_index] = lst[smallest_index], lst[i]

    # While loop implementation
    # b = 0
    # e = len(lst)
    #
    # while b < e:
    #     smallest_index = _min_index(lst, b)
    #     lst[b], lst[smallest_index] = lst[smallest_index], lst[b]
    #     b += 1


def _min_index(lst: list, i: int) -> int:
    min_index = i
    for k in range(i, len(lst)):
        if lst[k] < lst[min_index]:
            min_index = k
    return min_index


# Running-Time :)
# Let n be hte size of the input list, lst

# First I will calculate the RT of the helper function

# The assignment and the return statement count as 1 step
# The for loop iterates n - i times
# For a fixed iteration of the for loop, the loop body takes at most 1 step per iteration
# So the for loop takes a combines 1*(n-i) = n-i steps

# The total steps this function takes is n-i+1 steps which is
# Big-O of n-i


# Now I will calculate the RT of the main function

# The for loop iterates n times
# For a fixed iteration of the for loop...
#   - The call to _min_index function takes n-i steps
#   - The mutating statements after take 1 step
# So this gives a total of n^2 - n(n-1)/2 + n steps, which is a Theta bound of n^2


"""
============================================
Insertion Sort
============================================
"""
# Uses the same idea as Selection Sort, to create a boundary between sorted and unsorted parts.
# It checks the current item to the ones previous in order to insert it into the correct location.

# For example,
#     [1, 7, 8, 2, 4]
#     |_______||____|
#      |          |
#    sorted    unsorted
# In this current state we are on index 3(item: 2)
# First we check 2 with the index before it, in this case 8.
# Since 8 is greater than 2, we swap their places.
#      [1, 7, 2, 8, 4]
# Now we compare 2 with 7, so we make a swap again.
#      [1, 2, 7, 8, 4]
# Now we compare 2 to 1, and since 1 is less than 2 we stop.
#     [1, 2, 7, 8, 4]
#     |__________||_|
#       |          |
#     sorted    unsorted
# We continue this till we have no item left to sort


# In-place/mutating implementation of selection sort
def insertion_sort(lst: list) -> None:
    """Sort the given list using the insertion sort algorithm.
    >>> lst = [3, 7, 2, 5]
    >>> insertion_sort(lst)
    >>> lst
    [2, 3, 5, 7]
    """
    for i in range(len(lst)):
        _insert(lst, i)


def _insert(lst: list, i: int) -> None:
    """Move lst[i] so that lst[:i + 1] is sorted.

    Preconditions:
        - 0 <= i < len(lst)
        - is_sorted(lst[:i])

    >>> lst = [7, 3, 5, 2]
    >>> _insert(lst, 1)
    >>> lst  # lst[:2] is not sorted
    [3, 7, 5, 2]
    """
    for i in range(i, 0, -1):
        if lst[i] >= lst[i-1]:
            return
        else:
            # Swap lst[i] with lst[i-1]
            lst[i], lst[i-1] = lst[i-1], lst[i]
    return


# Running-Time(Worst-case) :)

# Let n be the size of the input list, lst

# Fist I will calculate the Worst Case RT of the helper function

# The for loop iterates at most i times for a fixed iteration of the for loop,
# assuming the else branch run every time...
#    - the loop body takes 1 step each time
# So the for loop will take a t most 1*i = i steps
# Therefore, the Big-O bound of the helper function is i

# Now I will calculate the Worst Case RT of the main function

# The loop iterates n times
# For a fixed iteration of the loop...
#    - the function call to the helper function takes at most i steps
# Note that the steps required for each iteration depends on the value of i
# Since the value of i increments by 1, going from 0 to n-1, the for loop will take n(n-1)/2 steps.
# Therefore, the Big-O bound of this function is n^2.


"""
===============================================
Selection Sort vs Insertion Sort: Running Times
===============================================
"""

# Although the worst case RT of insertion sort matches the RT of selection sort, normally the list wouldn't be at the
# worst case state. The best case RT of insertion sort is n, which is much faster than any RT of selection sort.


"""
===============================================
Divide-and-Conquer Algorithms
===============================================
"""

# This way of sorting refers to:
# 1. Given a list to sort, split it up into two or more smaller lists.
# 2. Recursively run the sorting algorithm on each smaller list separately.
# 3. Combine the sorted results of each recursive call into a single sorted list.


"""
============================================
Mergesort
============================================
"""

# 1. Divide the input list into right and left half.
# 2. Recursively sort each half
# 3. Merge each sorted half together


# Non-mutating implementation of mergesort
def mergesort(lst: list) -> list:
    """Return a new sorted list with the same elements as lst.
    >>> lst = [3, 7, 2, 5]
    >>> mergesort(lst)
    [2, 3, 5, 7]
    """
    if len(lst) < 2:  # base case: cannot divide the input list any further.
        return lst.copy()  # to return a NEW list object
    else:
        # Divide the input list into two pieces
        c = len(lst) // 2
        left = lst[:c]
        right = lst[c:]

        # Sort each part recursively
        left_sorted = mergesort(left)
        right_sorted = mergesort(right)

        # Combine the two sorted parts
        return _merge(left_sorted, right_sorted)


def _merge(lst1: list, lst2: list) -> list:
    """Return a sorted list with the elements in lst1 and lst2.

    Preconditions:
        - is_sorted(lst1)
        - is_sorted(lst2)
    """
    sorted_list = []
    i1 = 0
    i2 = 0
    while i1 < len(lst1) and i2 < len(lst2):
        if lst1[i1] <= lst2[i2]:
            sorted_list.append(lst1[i1])
            i1 += 1
        else:
            sorted_list.append(lst2[i2])
            i2 += 1

    assert i1 == len(lst1) or i2 == len(lst2)

    if i1 == len(lst1):
        return sorted_list + lst2[i2:]
    else:  # i2 == len(lst2)
        return sorted_list + lst1[i1:]


"""
============================================
Quicksort
============================================
"""

# 1. First we pick one element from the input list, this is called the pivot
#    - Using the pivot, we divide the list into two pieces:
#         - elements less than or equal to the pivot
#         - elements greater than the pivot
# 2. Now, we recursively sort each part.
# 3. Finally, we concatenate the two sorted parts


# Non-mutating implementation of quicksort
def quicksort(lst: list) -> list:
    """Return a sorted list with the same elements as lst.
    >>> lst = [3, 7, 2, 5]
    >>> quicksort(lst)
    [2, 3, 5, 7]
    """
    if len(lst) < 2:  # Base Case
        return lst.copy()
    else:
        # Divide the input list into 2 pieces while always using the first element as a pivot.
        pivot = lst[0]
        smaller, bigger = _partition(lst[1:], pivot)

        # Sort each part recursively
        smaller_sorted = quicksort(smaller)
        bigger_sorted = quicksort(bigger)

        # Combine the two sorted parts
        return smaller_sorted + [pivot] + bigger_sorted


def _partition(lst: list, pivot: Any) -> tuple[list, list]:
    """Return a partition of lst with the chosen pivot.

    Return two lists, where the first contains the items in lst
    that are <= pivot, and the second contains the items in lst that are > pivot.
    """
    smaller = []
    bigger = []

    for item in lst:
        if item <= pivot:
            smaller.append(item)
        else:
            bigger.append(item)

    return smaller, bigger
