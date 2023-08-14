import abc

from braandket import OperatorTensor
from braandket_circuit.basics import QOperation
from braandket_circuit.system import QComposed, QSystem


class OperatorOperation(QOperation, abc.ABC):
    """ Operation that can be fully described by an operator. """

    @abc.abstractmethod
    def make_operator_tensor(self, *args: QSystem, **kwargs: QSystem) -> OperatorTensor:
        pass

    def __call__(self, *args: QSystem, **kwargs: QSystem):
        state = QComposed(*(*args, *kwargs.values())).state
        operator = self.make_operator_tensor(*args, **kwargs)
        state.tensor = operator @ state.tensor
