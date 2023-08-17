import abc
from typing import Callable, Generic, Optional, ParamSpec, TypeVar

from braandket_circuit.basics import QOperation, QSystem, QSystemStruct

Op = TypeVar('Op', bound=QOperation)
QSystemSpec = ParamSpec('QSystemSpec', bound=QSystemStruct)


class Remapped(QOperation, Generic[Op], abc.ABC):
    def __init__(self, op: Op, *, name: Optional[str] = None):
        super().__init__(name=name)
        self._op = op

    @property
    def op(self) -> Op:
        return self._op

    @abc.abstractmethod
    def remap(self, *args: QSystemStruct) -> QSystemStruct:
        pass

    def __call__(self, *args: QSystemStruct):
        mapped_args = self.remap(*args)
        if isinstance(mapped_args, QSystem):
            mapped_args = (mapped_args,)
        return self.op(*mapped_args)


class RemappedByLambda(Remapped[Op]):
    def __init__(self, op: Op, func: Callable[QSystemSpec, QSystemStruct], *, name: Optional[str] = None):
        super().__init__(op, name=name)
        self._func = func

    @property
    def op(self) -> Op:
        return self._op

    @property
    def func(self) -> Callable[QSystemSpec, QSystemStruct]:
        return self._func

    def remap(self, *args: QSystemStruct) -> QSystemStruct:
        return self.func(*args)

    def __repr__(self) -> str:
        return f"RemappedByLambda({self.op}, {self.func})"


class RemappedByIndices(Remapped[Op]):
    def __init__(self, op: Op, *indices: int, name: Optional[str] = None):
        super().__init__(op, name=name)
        self._indices = indices

    @property
    def indices(self) -> tuple[int, ...]:
        return self._indices

    def remap(self, *args: QSystemStruct) -> QSystemStruct:
        return tuple(args[i] for i in self._indices)

    def __repr__(self) -> str:
        return f"RemappedByIndices({self.op}, {', '.join(map(str, self._indices))})"
