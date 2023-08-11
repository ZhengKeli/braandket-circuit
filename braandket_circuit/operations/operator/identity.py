from braandket import QSystem
from braandket_circuit import QOperation


class _IdentityOperation(QOperation):
    """ Operation that does nothing """

    def __call__(self, *args: QSystem, **kwargs: QSystem):
        pass


Identity = _IdentityOperation()
