import abc
from typing import Callable, Generic, Optional, ParamSpec, TypeVar

from braandket_circuit.basics import QOperation, QSystem, QSystemStruct

Op = TypeVar('Op', bound=QOperation)
QSystemsArgs = QSystemStruct
QSystemSpec = ParamSpec('QSystemSpec', bound=QSystemStruct)


class Remapped(QOperation, Generic[Op], abc.ABC):
    def __init__(self, op: Op, mapper: Callable[QSystemSpec, QSystemsArgs], *, name: Optional[str] = None):
        super().__init__(name=name)

        # check
        if not isinstance(op, QOperation):
            raise TypeError(f"op={op} is not a QOperation!")

        self._op = op
        self._mapper = mapper

    @property
    def op(self) -> Op:
        return self._op

    @property
    def mapper(self) -> Callable[QSystemSpec, QSystemsArgs]:
        return self._mapper

    def __call__(self, *args: QSystemStruct):
        mapped_args = self.mapper(*args)
        if isinstance(mapped_args, QSystem):
            mapped_args = (mapped_args,)
        return self.op(*mapped_args)


def remap_by_indices(op: Op, *indices: int) -> Remapped:
    return Remapped(op, lambda *args: tuple(args[i] for i in indices))
