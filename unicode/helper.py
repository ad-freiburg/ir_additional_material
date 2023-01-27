"""
Copyright 2019, University of Freiburg
Chair of Algorithms and Data Structures.
Patrick Brosi <brosi@cs.uni-freiburg.de>
Sebastian Walter <swalter@cs.uni-freiburg.de>
"""

from array import array


def edit_distance(x: str, y: str) -> int:
    '''
    Computes the edit distance ED(x,y) for the two given strings x and
    y.

    >>> edit_distance("frei", "frei")
    0
    >>> edit_distance("frei", "freiburg")
    4
    >>> edit_distance("frei", "breifurg")
    5
    >>> edit_distance("freiburg", "stuttgart")
    8
    >>> edit_distance("", "freiburg")
    8
    >>> edit_distance("", "")
    0
    '''

    # Compute the dimensions of the matrix.
    n = len(x) + 1
    m = len(y) + 1

    matrix = array("I", [0] * m * n)

    # Initialize the first column.
    for row in range(n):
        matrix[m * row] = row
    # Initialize the first row.
    for i in range(m):
        matrix[i] = i

    # Compute the rest of the matrix.
    for row in range(1, n):
        for col in range(1, m):
            s = 1
            if x[row - 1] == y[col - 1]:
                s = 0

            rep_costs = matrix[m * (row - 1) + (col - 1)] + s
            add_costs = matrix[m * row + (col - 1)] + 1
            del_costs = matrix[m * (row - 1) + col] + 1

            matrix[m * row + col] = min(rep_costs, add_costs, del_costs)

    return matrix[-1]
