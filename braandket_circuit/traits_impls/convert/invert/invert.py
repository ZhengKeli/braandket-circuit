from braandket_circuit import QOperation

from braandket_circuit.basics import QSystemStruct
from braandket_circuit.traits import Conversion


class Invert(Conversion[QOperation]):
    def __init__(self, args: tuple[QSystemStruct, ...] | None = None):
        self.args = args
