from zkl_quantum_circuit.basics import QSystemStruct
from zkl_quantum_circuit.traits import CompilePass


class FreezePass(CompilePass):
    def __init__(self, args: tuple[QSystemStruct, ...] | None = None):
        self.args = args
