import abc
from typing import Callable, Generic, Iterable, Optional, ParamSpec, TypeVar, Union, overload

from braandket_circuit.basics import QOperation, QSystem, QSystemStruct
from braandket_circuit.utils.struct import freeze_struct, map_struct

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
    def __init__(self, op: Op, *indices: IndexStruct, name: Optional[str] = None):
        super().__init__(op, name=name)
        self._indices = freeze_struct(indices, atom_typ=int)

    @property
    def indices(self) -> IndexStruct:
        return self._indices

    def remap(self, *args: QSystemStruct) -> QSystemStruct:
        return map_struct(lambda i: args[i], self._indices, atom_typ=int)

    def __repr__(self) -> str:
        return f"RemappedByIndices({self.op}, {', '.join(map(str, self._indices))})"


@overload
def remap(op: Op, func: Callable[QSystemSpec, QSystemStruct], *, name: Optional[str] = None) -> RemappedByLambda[Op]:
    return RemappedByLambda(op, func, name=name)


@overload
def remap(op: Op, *indices: IndexStruct, name: Optional[str] = None) -> RemappedByIndices[Op]:
    return RemappedByIndices(op, *indices, name=name)


def remap(op: Op, *args, name: Optional[str] = None) -> Remapped[Op]:
    if len(args) == 1 and callable(args[0]):
        return RemappedByLambda(op, args[0], name=name)
    else:
        return RemappedByIndices(op, *args, name=name)
