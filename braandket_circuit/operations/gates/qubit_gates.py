import abc

import numpy as np

from braandket import ArrayLike, BackendValue
from braandket_circuit.basics import QComposed, QSystem
from braandket_circuit.operations.operator import Identity, MatrixOperation, QubitsConstantMatrixOperation


# simple single qubit gates

class _SingleQubitConstantGate(QubitsConstantMatrixOperation):
    def __call__(self, qubit: QSystem):
        super().__call__(qubit)


I = Identity
X = _SingleQubitConstantGate(np.asarray([[0, 1], [1, 0]]), name="X")
Y = _SingleQubitConstantGate(np.asarray([[0, -1j], [+1j, 0]]), name="Y")
Z = _SingleQubitConstantGate(np.asarray([[1, 0], [0, -1]]), name="Z")
S = _SingleQubitConstantGate(np.asarray([[1, 0], [0, 1j]]), name="S")
T = _SingleQubitConstantGate(np.asarray([[1, 0], [0, np.exp(1j * np.pi / 4)]]), name="T")
H = _SingleQubitConstantGate(np.asarray([[1, 1], [1, -1]]) / np.sqrt(2), name="H")
NOT = X


# parametrized single qubit gates

class _SingleQubitParameterizedGate(MatrixOperation, abc.ABC):
    def __call__(self, qubit: QSystem):
        super().__call__(qubit)


class Rx(_SingleQubitParameterizedGate):
    def __init__(self, theta: ArrayLike):
        super().__init__(name="Rx")
        self._theta = theta

    @property
    def theta(self) -> ArrayLike:
        return self._theta

    def make_matrix(self, *systems: QSystem) -> BackendValue:
        backend = QComposed(*systems).backend
        theta = backend.convert(self.theta)
        half_theta = backend.div(theta, 2.0)
        cos_half_theta = backend.cos(half_theta)
        sin_half_theta = backend.sin(half_theta)
        m1j_sin_half_theta = backend.mul(sin_half_theta, -1.0j)
        return backend.add(
            cos_half_theta * I.make_matrix(*systems),
            m1j_sin_half_theta * X.make_matrix(*systems))


class Ry(_SingleQubitParameterizedGate):
    def __init__(self, theta: ArrayLike):
        self._theta = theta
        super().__init__(name="Ry")

    @property
    def theta(self) -> ArrayLike:
        return self._theta

    def make_matrix(self, *systems: QSystem) -> BackendValue:
        backend = QComposed(*systems).backend
        theta = backend.convert(self.theta)
        half_theta = backend.div(theta, 2.0)
        cos_half_theta = backend.cos(half_theta)
        sin_half_theta = backend.sin(half_theta)
        m1j_sin_half_theta = backend.mul(sin_half_theta, -1.0j)
        return backend.add(
            cos_half_theta * I.make_matrix(*systems),
            m1j_sin_half_theta * Y.make_matrix(*systems))


class Rz(_SingleQubitParameterizedGate):
    def __init__(self, theta: ArrayLike):
        self._theta = theta
        super().__init__(name="Rz")

    @property
    def theta(self) -> ArrayLike:
        return self._theta

    def make_matrix(self, *systems: QSystem) -> BackendValue:
        backend = QComposed(*systems).backend
        theta = backend.convert(self.theta)
        half_theta = backend.div(theta, 2.0)
        cos_half_theta = backend.cos(half_theta)
        sin_half_theta = backend.sin(half_theta)
        m1j_sin_half_theta = backend.mul(sin_half_theta, -1.0j)
        return backend.add(
            cos_half_theta * I.make_matrix(*systems),
            m1j_sin_half_theta * Z.make_matrix(*systems))
