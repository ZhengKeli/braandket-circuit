from typing import Optional

import numpy as np

from braandket import ArrayLike
from braandket_circuit.basics import QOperation


class MatrixOperation(QOperation[None]):
    """ MatrixOperation that has a constant matrix. """

    def __init__(self, matrix: ArrayLike, *, name: Optional[str] = None):
        super().__init__(name=name)
        self._matrix = matrix

        shape = _get_shape(matrix)
        if len(shape) != 2 or shape[0] != shape[1]:
            raise ValueError(f"expected matrix shape (N, N), got {shape}")
        self._N = shape[0]

    @property
    def N(self) -> int:
        return self._N

    @property
    def matrix(self) -> ArrayLike:
        return self._matrix


class QubitsMatrixOperation(MatrixOperation):
    """ MatrixOperation that acts on qubit systems. """

    def __init__(self, matrix: ArrayLike, *, name: Optional[str] = None):
        super().__init__(matrix, name=name)
        n = _log2int(self.N, strict=True)
        if n is None:
            raise ValueError(f"expected matrix shape (2**n, 2**n), got ({self.N},{self.N})")
        self._n = n

    @property
    def n(self) -> int:
        return self._n


# utils

def _get_shape(matrix: ArrayLike):
    try:
        shape = matrix.shape
    except AttributeError:
        shape = np.shape(matrix)
    return shape


def _log2int(x: int, *, strict: bool = False) -> Optional[int]:
    if strict and x & (x - 1) != 0:
        return None
    return x.bit_length() - 1
