import abc
from typing import Callable, Generic, Iterable, Optional, ParamSpec, TypeVar, Union

from braandket_circuit.basics import QOperation, QParticle, QSystemStruct, R
from braandket_circuit.utils import freeze_struct, map_struct

Op = TypeVar('Op', bound=QOperation)
QSystemSpec = ParamSpec('QSystemSpec', bound=QSystemStruct)
IndexStruct = Union[int, Iterable['IndexStruct']]


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

    @abc.abstractmethod
    def spawn(self, op: Op) -> 'Remapped':
        pass

    def __call__(self, *args: QSystemStruct) -> R:
        mapped_args = self.remap(*args)
        if isinstance(mapped_args, QParticle):
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

    def spawn(self, op: Op) -> 'RemappedByLambda':
        return RemappedByLambda(op, self.func, name=self.name)

    def __repr__(self) -> str:
        return f"RemappedByLambda({self.op!r}, {self.func!r})"


class RemappedByIndices(Remapped[Op]):
    def __init__(self, op: Op, *indices: IndexStruct, name: Optional[str] = None):
        super().__init__(op, name=name)
        self._indices = freeze_struct(indices, atom_typ=int)

    @property
    def indices(self) -> IndexStruct:
        return self._indices

    def remap(self, *args: QSystemStruct) -> QSystemStruct:
        return map_struct(lambda i: args[i], self._indices, atom_typ=int)

    def spawn(self, op: Op) -> 'RemappedByIndices':
        return RemappedByIndices(op, *self.indices, name=self.name)

    def __repr__(self) -> str:
        return f"RemappedByIndices({self.op!r}, {', '.join(map(repr, self._indices))})"
