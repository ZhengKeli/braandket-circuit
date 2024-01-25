from typing import Generic, Iterable, Optional, ParamSpec, TypeVar, Union

from braandket_circuit.basics import QOperation, QSystemStruct, R
from braandket_circuit.utils import freeze_struct, map_struct

Op = TypeVar('Op', bound=QOperation)
QSystemSpec = ParamSpec('QSystemSpec', bound=QSystemStruct)
IndexStruct = Union[int, Iterable['IndexStruct']]


class Remapped(QOperation, Generic[Op]):
    def __init__(self, op: Op, *indices: IndexStruct, name: Optional[str] = None):
        super().__init__(name=name)
        self._op = op
        self._indices = freeze_struct(indices, atom_typ=int)

    @property
    def op(self) -> Op:
        return self._op

    @property
    def indices(self) -> IndexStruct:
        return self._indices

    def remap(self, *args: QSystemStruct) -> tuple[QSystemStruct, ...]:
        return map_struct(lambda i: args[i], self._indices, atom_typ=int)

    def __call__(self, *args: QSystemStruct) -> R:
        return self.op(*self.remap(*args))

    def __repr__(self) -> str:
        return f"Remapped({self.op!r}, {', '.join(map(repr, self._indices))})"
