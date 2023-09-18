import abc

from braandket import ArrayLike
from braandket_circuit.basics import QOperation, QParticle
from braandket_circuit.operations.identity import Identity
from braandket_circuit.operations.measurement import DesiredMeasurement, ProjectiveMeasurement
from braandket_circuit.operations.structural import Controlled

# identity

I = Identity


# single qubit constant gates

class _SingleQubitConstantGate(QOperation):
    def __call__(self, qubit: QParticle):
        return super().__call__(qubit)

    def __repr__(self):
        return f"{self.name}"


X = _SingleQubitConstantGate(name="X")
Y = _SingleQubitConstantGate(name="Y")
Z = _SingleQubitConstantGate(name="Z")
S = _SingleQubitConstantGate(name="S")
T = _SingleQubitConstantGate(name="T")
H = _SingleQubitConstantGate(name="H")
NOT = X


# single qubit rotation gates

class _SingleQubitRotationGate(QOperation, abc.ABC):
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


class Ry(_SingleQubitRotationGate):
    def __init__(self, theta: ArrayLike):
        super().__init__(theta, name="Ry")


class Rz(_SingleQubitRotationGate):
    def __init__(self, theta: ArrayLike):
        super().__init__(theta, name="Rz")


# controlled gates

CX = Controlled(X)
CY = Controlled(Y)
CZ = Controlled(Z)
CNOT = CX

# measurements

M = ProjectiveMeasurement
D = DesiredMeasurement
