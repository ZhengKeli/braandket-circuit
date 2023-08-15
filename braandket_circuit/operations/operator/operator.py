import abc

from braandket import OperatorTensor
from braandket_circuit.basics import QOperation, QSystemStruct, compose


class OperatorOperation(QOperation[None], abc.ABC):
    """ Operation that can be fully described by an operator. """

    @abc.abstractmethod
    def make_operator_tensor(self, *args: QSystemStruct) -> OperatorTensor:
        pass

    def __call__(self, *args: QSystemStruct):
        state = compose(*args).state
        operator = self.make_operator_tensor(*args)
        state.tensor = operator @ state.tensor
