import abc
from typing import Optional

from braandket import ArrayLike
from braandket_circuit.basics import QOperation, QParticle


class _SingleQubitGate(QOperation, abc.ABC):
    def __call__(self, qubit: QParticle):
        return super().__call__(qubit)


# constant gates

class _SingleQubitConstantGate(_SingleQubitGate, abc.ABC):
    def __repr__(self):
        name_str = f"name={self.name!r}" if self.name else ""
        return f"{type(self).__name__}({name_str})"


class PauliXGate(_SingleQubitConstantGate):
    pass


class PauliYGate(_SingleQubitConstantGate):
    pass


class PauliZGate(_SingleQubitConstantGate):
    pass


class HalfPiPhaseGate(_SingleQubitConstantGate):
    pass


class QuarterPiPhaseGate(_SingleQubitConstantGate):
    pass


class HadamardGate(_SingleQubitConstantGate):
    pass


# rotation gates

class _SingleQubitRotationGate(_SingleQubitGate, abc.ABC):
    def __init__(self, theta: ArrayLike, *, name: Optional[str] = None):
        super().__init__(name=name)
        self._theta = theta

    @property
    def theta(self) -> ArrayLike:
        return self._theta

    def __repr__(self):
        name_str = f", name={self.name!r}" if self.name else ""
        return f"{type(self).__name__}({self.theta!r}{name_str})"


class RotationXGate(_SingleQubitRotationGate):
    pass


class RotationYGate(_SingleQubitRotationGate):
    pass


class RotationZGate(_SingleQubitRotationGate):
    pass


class GlobalPhaseGate(_SingleQubitRotationGate):
    pass
