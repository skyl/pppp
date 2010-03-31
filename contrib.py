"""
Just throwing some ideas and algorithms in here that I'm not currently using.
"""

# This is released with the #python license, not sure if I will add it in
import collections

def count_shared_elements(*iterables):
    """
    >>> count_shared_elements((1,2,1), (1,1,3))
    2
    >>> count_shared_elements((1,2,3), (3,2,1))
    3
    >>> count_shared_elements((1,1,1), (1,0,0))
    1
    """
    n = 0
    counts = map(count, iterables)
    for item in min(counts, key=len):
        n += min(count[item] for count in counts)
    return n

def count(iterable):
    counts = collections.defaultdict(int)
    for item in iterable:
        counts[item] += 1
    return counts

