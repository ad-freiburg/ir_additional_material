"""
Copyright 2023, University of Freiburg
Chair of Algorithms and Data Structures.
Sebastian Walter <swalter@cs.uni-freiburg.de>
"""

import operator
from typing import Optional

import numpy as np

_OPS = {
    "+": operator.add,
    "*": operator.mul,
    "/": operator.truediv,
    "-": operator.sub,
}


def _sep(text: str):
    print(f"{text}\n{'-' * len(text)}")


def _arr(name: str, arr: np.ndarray, print_values: bool):
    s = f"{name}: {' x '.join(str(d) for d in arr.shape)}"
    if print_values:
        s += f"\n{arr}"
    print(s)


def _expand(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    assert a.ndim <= b.ndim
    while a.ndim < b.ndim:
        a = a[np.newaxis, ...]
    return a


def broadcast(
    a: np.ndarray,
    b: np.ndarray,
    op_name: str,
    print_values: bool = False
) -> Optional[np.ndarray]:
    assert op_name in _OPS, \
        f"operator {op_name} not supported, must be one of {list(_OPS.keys())}"
    _sep("inputs")
    _arr("a", a, print_values)
    _arr("b", b, print_values)
    print()

    if not a.ndim == b.ndim:
        _sep("1. expansion")

        if a.ndim < b.ndim:
            a = _expand(a, b)
        else:
            b = _expand(b, a)

        _arr("a", a, print_values)
        _arr("b", b, print_values)
        print()

    if a.shape != b.shape:
        _sep("2. repetition")
        result_shape = []
        for i in range(a.ndim):
            if a.shape[i] == b.shape[i]:
                result_shape.append(a.shape[i])
            elif a.shape[i] == 1:
                a = a.repeat(b.shape[i], axis=i)
                result_shape.append(max(a.shape[i], b.shape[i]))
            elif b.shape[i] == 1:
                b = b.repeat(a.shape[i], axis=i)
                result_shape.append(max(a.shape[i], b.shape[i]))
            else:
                print(f"dimension {i} is incompatible")
                return None

        _arr("a", a, print_values)
        _arr("b", b, print_values)
        print()

    try:
        op = _OPS[op_name]
        result: np.ndarray = op(a, b)
        _sep("3. operation")
        _arr(f"a {str(op_name)} b", result, print_values)
        return result
    except Exception as e:
        print(f"broadcasting failed:\n{e}")
        return None
