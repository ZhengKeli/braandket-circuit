from zkl_quantum_circuit import QOperation

from zkl_quantum_circuit.basics import QSystemStruct
from zkl_quantum_circuit.traits import Conversion


class Invert(Conversion[QOperation]):
    def __init__(self, args: tuple[QSystemStruct, ...] | None = None):
        self.args = args
