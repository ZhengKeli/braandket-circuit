from braandket_circuit.basics import QOperation, QSystemStruct


class Identity(QOperation[None]):
    """ Operation that does nothing """

    def __call__(self, *args: QSystemStruct):
        pass  # do nothing

    def __repr__(self):
        name_str = f"name={self.name!r}" if self.name else ""
        return f"{type(self).__name__}({name_str})"
