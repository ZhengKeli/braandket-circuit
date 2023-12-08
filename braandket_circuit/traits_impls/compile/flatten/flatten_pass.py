from braandket_circuit.basics import QSystemStruct
from braandket_circuit.traits import CompilePass


class FlattenPass(CompilePass):
    def __init__(self, args: tuple[QSystemStruct, ...] | None = None):
        self.args = args
