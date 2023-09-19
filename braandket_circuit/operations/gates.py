import abc

from braandket import ArrayLike
from braandket_circuit.basics import QOperation, QParticle


# single qubit constant gates

class _SingleQubitConstantGate(QOperation):
    def __call__(self, qubit: QParticle):
        return super().__call__(qubit)

    def __repr__(self):
        return f"{self.name}"


class PauliXGate(_SingleQubitConstantGate):
    def __init__(self):
        super().__init__(name="X")


class PauliYGate(_SingleQubitConstantGate):
    def __init__(self):
        super().__init__(name="Y")


class PauliZGate(_SingleQubitConstantGate):
    def __init__(self):
        super().__init__(name="Z")


class HalfPiPhaseGate(_SingleQubitConstantGate):
    def __init__(self):
        super().__init__(name="S")


class QuarterPiPhaseGate(_SingleQubitConstantGate):
    def __init__(self):
        super().__init__(name="T")


class HadamardGate(_SingleQubitConstantGate):
    def __init__(self):
        super().__init__(name="H")


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


class RotationXGate(_SingleQubitRotationGate):
    def __init__(self, theta: ArrayLike):
        super().__init__(theta, name="Rx")


class RotationYGate(_SingleQubitRotationGate):
    def __init__(self, theta: ArrayLike):
        super().__init__(theta, name="Ry")


class RotationZGate(_SingleQubitRotationGate):
    def __init__(self, theta: ArrayLike):
        super().__init__(theta, name="Rz")
