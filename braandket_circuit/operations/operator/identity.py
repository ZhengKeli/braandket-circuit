from braandket_circuit.basics import QOperation
from braandket_circuit.system import QSystem


class _IdentityOperation(QOperation):
    """ Operation that does nothing """

    def __call__(self, *args: QSystem, **kwargs: QSystem):
        pass


Identity = _IdentityOperation()
