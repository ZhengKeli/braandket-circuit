import abc

from braandket import OperatorTensor
from braandket_circuit.basics import QComposed, QOperation, QSystem


class OperatorOperation(QOperation, abc.ABC):
    """ Operation that can be fully described by an operator. """

    @abc.abstractmethod
    def make_operator_tensor(self, *args: QSystem) -> OperatorTensor:
        pass

    def __call__(self, *args: QSystem):
        state = QComposed(*args).state
        operator = self.make_operator_tensor(*args)
        state.tensor = operator @ state.tensor
