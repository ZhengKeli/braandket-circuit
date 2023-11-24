from braandket_circuit import CompilePass, QSystemStruct


class FreezePass(CompilePass):
    def __init__(self, args: tuple[QSystemStruct, ...] | None = None):
        self.args = args
