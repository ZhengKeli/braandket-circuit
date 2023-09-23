import dataclasses
from typing import Optional

from braandket import ArrayLike
from braandket_circuit.basics import QOperation, QSystemStruct


@dataclasses.dataclass
class MeasurementResult:
    target: QSystemStruct
    value: ArrayLike
    prob: ArrayLike


class ProjectiveMeasurement(QOperation[MeasurementResult]):
    def __repr__(self):
        name_str = f"name={self.name!r}" if self.name else ""
        return f"{type(self).__name__}({name_str})"


class DesiredMeasurement(QOperation[MeasurementResult]):
    def __init__(self, value: ArrayLike, *, name: Optional[str] = None):
        super().__init__(name=name)
        self._value = value

    @property
    def value(self) -> ArrayLike:
        return self._value

    def __repr__(self):
        name_str = f", name={self.name!r}" if self.name else ""
        return f"{type(self).__name__}({self.value!r}{name_str})"
