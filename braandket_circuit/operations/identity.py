from braandket_circuit.basics import QOperation, QSystemStruct


class _Identity(QOperation):
    """ Operation that does nothing """

    def __call__(self, *args: QSystemStruct):
        pass  # do nothing


Identity = _Identity()