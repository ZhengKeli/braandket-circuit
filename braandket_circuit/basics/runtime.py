import abc

from .operation import QOperation, R
from .system import QSystem, QSystemStruct


class QRuntime(abc.ABC):
    @abc.abstractmethod
    def allocate(self, n: int, name: str | None = None) -> QSystem:
        pass

    @abc.abstractmethod
    def operate(self, op: QOperation[R], *args: QSystemStruct) -> R:
        pass
