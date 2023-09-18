import dataclasses

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
