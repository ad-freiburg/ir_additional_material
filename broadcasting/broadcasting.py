"""
Copyright 2023, University of Freiburg
Chair of Algorithms and Data Structures.
Sebastian Walter <swalter@cs.uni-freiburg.de>
"""

import argparse

import numpy as np
from helper import broadcast


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--values",
        action="store_true",
        help="not only print shapes, but also values of the arrays"
    )
    return parser.parse_args()


# General information:
#
# The broadcasting rules apply to arithmetic element-wise operations
# (*, /, +, -, ...) between two (multi-dimensional) vectors.
#
# The rules are:
# 1. if the two vectors do not have the same number of dimensions,
#    expand the one with fewer dimensions with ones to the left
#    until they have the same number of dimensions
#
# 2. if shapes are not compatible, for each dimension do the following:
#    check for compatibility of the dimensions:
#       - they are equal --> do nothing
#       - one of them is 1 -->
#           repeat it to match the other dimension
#           (this is only conceptually true, in the actual implementation
#           the values are simply reused to save memory)
#       - else -->  fail
#
# 3. now that the shapes match exactly, perform the element-wise
#    operation on the two vectors


def run(args: argparse.Namespace):
    # matching example
    print("Example: matching shapes")
    a = np.array([1, 2, 3, 4])
    b = np.array([4, 3, 2, 1])
    res = broadcast(a, b, "*", args.values)
    assert res is not None
    assert np.array_equal(res, a * b)
    print()

    # non-matching example
    print("Example: non-matching shapes")
    a = np.array([
        [1, 2, 3, 4],
        [5, 6, 7, 8]
    ])
    b = np.array([4, 3, 2, 1])
    res = broadcast(a, b, "+", args.values)
    assert res is not None
    assert np.array_equal(res, a + b)
    print()

    # scalar example
    print("Example: scalar")
    a = np.array([1, 2, 3, 4])
    b = np.array(2)
    res = broadcast(a, b, "*", args.values)
    assert res is not None
    assert np.array_equal(res, a * b)
    print()

    # advanced example
    # use broadcasting to create grids of values,
    # e.g. scale a with every value in b
    print("Example: grid")
    a = np.array([[1, 2, 3, 4]])  # 1 x 4
    b = np.array([[4], [3], [2], [1]])  # 4 x 1
    res = broadcast(a, b, "*", args.values)
    assert res is not None
    assert np.array_equal(res, a * b)
    print()

    # real world example: shifting image
    # we have a 10 x 10 image with rgb values (range [0..255]),
    # and mean rgb values, e.g. estimated from a training set
    print("Example: image")
    image = np.random.randint(0, 256, (10, 10, 3))
    mean = np.array([127, 125, 130])
    res = broadcast(image, mean, "-", args.values)
    assert res is not None
    assert np.array_equal(res, image - mean)


if __name__ == "__main__":
    run(parse_args())
