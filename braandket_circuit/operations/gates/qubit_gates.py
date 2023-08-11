from typing import Union

import numpy as np

from braandket import QSystem
from braandket_circuit.operations.operator import Identity, QubitsMatrixOperation


# simple single qubit gates

class SingleQubitGateFromMatrix(QubitsMatrixOperation):
    def __call__(self, qubit: QSystem):
        super().__call__(qubit)


I = Identity
X = SingleQubitGateFromMatrix(np.asarray([[0, 1], [1, 0]]), name="X")
Y = SingleQubitGateFromMatrix(np.asarray([[0, -1j], [+1j, 0]]), name="Y")
Z = SingleQubitGateFromMatrix(np.asarray([[1, 0], [0, -1]]), name="Z")
S = SingleQubitGateFromMatrix(np.asarray([[1, 0], [0, 1j]]), name="S")
T = SingleQubitGateFromMatrix(np.asarray([[1, 0], [0, np.exp(1j * np.pi / 4)]]), name="T")
H = SingleQubitGateFromMatrix(np.asarray([[1, 1], [1, -1]]) / np.sqrt(2), name="H")
NOT = X


# parametrized single qubit gates

class Rx(SingleQubitGateFromMatrix):
    def __init__(self, theta: Union[np.ndarray, float]):
        self._theta = theta
        half_theta = self.theta / 2
        cos_half_theta = np.cos(half_theta)
        sin_half_theta = np.sin(half_theta)
        super().__init__(np.asarray([
            [cos_half_theta * +1, sin_half_theta * -1j],
            [sin_half_theta * -1j, cos_half_theta * +1]
        ]), name="Rx")

    @property
    def theta(self) -> Union[np.ndarray, float]:
        return self._theta


class Ry(SingleQubitGateFromMatrix):
    def __init__(self, theta: Union[np.ndarray, float]):
        self._theta = theta
        half_theta = self.theta / 2
        cos_half_theta = np.cos(half_theta)
        sin_half_theta = np.sin(half_theta)
        super().__init__(np.asarray([
            [cos_half_theta * +1, sin_half_theta * -1],
            [sin_half_theta * +1, cos_half_theta * +1]
        ]), name="Ry")

    @property
    def theta(self) -> Union[np.ndarray, float]:
        return self._theta


class Rz(SingleQubitGateFromMatrix):
    def __init__(self, theta: Union[np.ndarray, float]):
        self._theta = theta
        half_theta_j = self.theta / 2 * 1j
        super().__init__(np.asarray([
            [np.exp(-half_theta_j), 0],
            [0, np.exp(+half_theta_j)]
        ]), name="Rz")

    @property
    def theta(self) -> Union[np.ndarray, float]:
        return self._theta
