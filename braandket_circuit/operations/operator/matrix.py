import abc
from typing import Optional

import numpy as np

from braandket import ArrayLike, BackendValue, OperatorTensor
from braandket_circuit.basics import QSystem, QSystemStruct
from .operator import OperatorOperation


class MatrixOperation(OperatorOperation):
    """ Operation that can be fully described by a matrix. """

    @abc.abstractmethod
    def make_matrix(self, *args: QSystemStruct) -> BackendValue:
        pass

    def make_operator_tensor(self, *args: QSystemStruct) -> OperatorTensor:
        matrix = self.make_matrix(*args)
        system = QSystem.of(args)
        return OperatorTensor.from_matrix(matrix, system.spaces, backend=system.backend)

    def __call__(self, *args: QSystemStruct):
        return super().__call__(*args)


class ConstantMatrixOperation(MatrixOperation):
    """ MatrixOperation that has a constant matrix. """

    def __init__(self, matrix: ArrayLike, *, name: Optional[str] = None):
        super().__init__(name=name)
        shape = _get_shape(matrix)
        if len(shape) != 2 or shape[0] != shape[1]:
            raise ValueError(f"expected matrix shape (N, N), got {shape}")
        self._N = shape[0]
        self._matrix = matrix

    @property
    def N(self) -> int:
        return self._N

    @property
    def matrix(self) -> ArrayLike:
        return self._matrix

    def make_matrix(self, *args: QSystemStruct) -> ArrayLike:
        # TODO check systems shape compatible with matrix shape
        return self.matrix


class QubitsConstantMatrixOperation(ConstantMatrixOperation):
    """ MatrixOperation that acts on qubit systems. """

    def __init__(self, matrix: BackendValue, *, name: Optional[str] = None):
        super().__init__(matrix, name=name)
        n = log2int(self.N, strict=True)
        if n is None:
            raise ValueError(f"expected matrix shape (2**n, 2**n), got ({self.N},{self.N})")
        self._n = n

    @property
    def n(self) -> int:
        return self._n


# utils

def _get_shape(matrix: BackendValue):
    try:
        shape = matrix.shape
    except AttributeError:
        shape = np.shape(matrix)
    return shape


def log2int(x: int, *, strict: bool = False) -> Optional[int]:
    if strict and x & (x - 1) != 0:
        return None
    return x.bit_length() - 1
