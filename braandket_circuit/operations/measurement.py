import dataclasses
from typing import Optional

from braandket import ArrayLike
from braandket_circuit.basics import QOperation, QSystemStruct


# result

@dataclasses.dataclass
class MeasurementResult:
    target: QSystemStruct
    value: ArrayLike
    prob: ArrayLike


# projective

class _ProjectiveMeasurement(QOperation):
    pass


ProjectiveMeasurement = _ProjectiveMeasurement()


# desired

class DesiredMeasurement(QOperation):
    def __init__(self, value: ArrayLike, *, name: Optional[str] = None):
        super().__init__(name=name)
        self._value = value

    @property
    def value(self) -> ArrayLike:
        return self._value
