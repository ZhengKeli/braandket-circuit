import abc

import numpy as np

from braandket import ArrayLike, BackendValue
from braandket_circuit.basics import QParticle
from braandket_circuit.operations.identity import Identity
from braandket_circuit.operations.matrix import MatrixOperation, QubitsMatrixOperation
from braandket_circuit.operations.structural import Controlled


# simple single qubit gates

class _SingleQubitConstantGate(QubitsMatrixOperation):
    def __call__(self, qubit: QParticle):
        return super().__call__(qubit)

    def __repr__(self):
        return f"{self.name}"


I = Identity
X = _SingleQubitConstantGate(np.asarray([[0, 1], [1, 0]]), name="X")
Y = _SingleQubitConstantGate(np.asarray([[0, -1j], [+1j, 0]]), name="Y")
Z = _SingleQubitConstantGate(np.asarray([[1, 0], [0, -1]]), name="Z")
S = _SingleQubitConstantGate(np.asarray([[1, 0], [0, 1j]]), name="S")
T = _SingleQubitConstantGate(np.asarray([[1, 0], [0, np.exp(1j * np.pi / 4)]]), name="T")
H = _SingleQubitConstantGate(np.asarray([[1, 1], [1, -1]]) / np.sqrt(2), name="H")
NOT = X


# parametrized single qubit gates

class _SingleQubitRotationGate(MatrixOperation, abc.ABC):
    def __init__(self, theta: ArrayLike, *, name: str):
        super().__init__(name=name)
        self._theta = theta

    @property
    def theta(self) -> ArrayLike:
        return self._theta

    def __call__(self, qubit: QParticle):
        return super().__call__(qubit)

    def __repr__(self) -> str:
        return f'{self.name}({self.theta})'


class Rx(_SingleQubitRotationGate):
    def __init__(self, theta: ArrayLike):
        super().__init__(theta, name="Rx")

    def make_matrix(self, qubit: QParticle) -> BackendValue:
        backend = qubit.backend
        theta = backend.convert(self.theta)
        half_theta = backend.div(theta, 2.0)
        cos_half_theta = backend.cos(half_theta)
        sin_half_theta = backend.sin(half_theta)
        m1j_sin_half_theta = backend.mul(sin_half_theta, -1.0j)
        return backend.add(
            cos_half_theta * I.make_matrix(qubit),
            m1j_sin_half_theta * X.make_matrix(qubit))


class Ry(_SingleQubitRotationGate):
    def __init__(self, theta: ArrayLike):
        super().__init__(theta, name="Ry")

    def make_matrix(self, qubit: QParticle) -> BackendValue:
        backend = qubit.backend
        theta = backend.convert(self.theta)
        half_theta = backend.div(theta, 2.0)
        cos_half_theta = backend.cos(half_theta)
        sin_half_theta = backend.sin(half_theta)
        m1j_sin_half_theta = backend.mul(sin_half_theta, -1.0j)
        return backend.add(
            cos_half_theta * I.make_matrix(qubit),
            m1j_sin_half_theta * Y.make_matrix(qubit))


class Rz(_SingleQubitRotationGate):
    def __init__(self, theta: ArrayLike):
        super().__init__(theta, name="Rz")

    def make_matrix(self, qubit: QParticle) -> BackendValue:
        backend = qubit.backend
        theta = backend.convert(self.theta)
        half_theta = backend.div(theta, 2.0)
        cos_half_theta = backend.cos(half_theta)
        sin_half_theta = backend.sin(half_theta)
        m1j_sin_half_theta = backend.mul(sin_half_theta, -1.0j)
        return backend.add(
            cos_half_theta * I.make_matrix(qubit),
            m1j_sin_half_theta * Z.make_matrix(qubit))


# controlled gates

CX = Controlled(X)
CY = Controlled(Y)
CZ = Controlled(Z)
CNOT = CX
