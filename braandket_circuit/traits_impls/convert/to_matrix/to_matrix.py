from braandket import ArrayLike

from braandket_circuit.basics import QSystemStruct
from braandket_circuit.traits import Conversion


class ToMatrix(Conversion[ArrayLike]):
    def __init__(self, args: tuple[QSystemStruct, ...] | None = None):
        self.args = args
