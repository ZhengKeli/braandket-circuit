import dataclasses
from typing import Optional

from braandket import ArrayLike
from braandket_circuit.basics import QOperation, QSystemStruct


@dataclasses.dataclass
class MeasurementResult:
    target: QSystemStruct
    value: ArrayLike
    prob: ArrayLike


class ProjectiveMeasurement(QOperation):
    pass


class DesiredMeasurement(QOperation):
    def __init__(self, value: ArrayLike, *, name: Optional[str] = None):
        super().__init__(name=name)
        self._value = value

    @property
    def value(self) -> ArrayLike:
        return self._value
