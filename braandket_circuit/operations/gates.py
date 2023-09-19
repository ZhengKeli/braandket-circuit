import abc
from typing import Optional

from braandket import ArrayLike
from braandket_circuit.basics import QOperation, QParticle


class _SingleQubitGate(QOperation, abc.ABC):
    def __call__(self, qubit: QParticle):
        return super().__call__(qubit)


# constant gates

class PauliXGate(_SingleQubitGate):
    def __init__(self):
        super().__init__(name="X")


class PauliYGate(_SingleQubitGate):
    def __init__(self):
        super().__init__(name="Y")


class PauliZGate(_SingleQubitGate):
    def __init__(self):
        super().__init__(name="Z")


class HalfPiPhaseGate(_SingleQubitGate):
    def __init__(self):
        super().__init__(name="S")


class QuarterPiPhaseGate(_SingleQubitGate):
    def __init__(self):
        super().__init__(name="T")


class HadamardGate(_SingleQubitGate):
    def __init__(self):
        super().__init__(name="H")


# rotation gates

class _SingleQubitRotationGate(_SingleQubitGate, abc.ABC):
    def __init__(self, theta: ArrayLike, *, name: Optional[str] = None):
        super().__init__(name=name)
        self._theta = theta

    @property
    def theta(self) -> ArrayLike:
        return self._theta

    def __str__(self):
        return f'{self.name}({self.theta})'

    def __repr__(self):
        return f'{type(self).__name__}({self.theta})'


class RotationXGate(_SingleQubitRotationGate):
    def __init__(self, theta: ArrayLike):
        super().__init__(theta, name="Rx")


class RotationYGate(_SingleQubitRotationGate):
    def __init__(self, theta: ArrayLike):
        super().__init__(theta, name="Ry")


class RotationZGate(_SingleQubitRotationGate):
    def __init__(self, theta: ArrayLike):
        super().__init__(theta, name="Rz")
