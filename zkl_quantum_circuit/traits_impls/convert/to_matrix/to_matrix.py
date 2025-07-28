from braandket import ArrayLike

from zkl_quantum_circuit.basics import QSystemStruct
from zkl_quantum_circuit.traits import Conversion


class ToMatrix(Conversion[ArrayLike]):
    def __init__(self, args: tuple[QSystemStruct, ...] | None = None):
        self.args = args
