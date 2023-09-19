from typing import Callable, Generic, Optional, ParamSpec, TypeVar, overload

from braandket_circuit.basics import QOperation, QSystemStruct
from .remapped import IndexStruct, remap

Op = TypeVar("Op", bound=QOperation)
QSystemSpec = ParamSpec('QSystemSpec', bound=QSystemStruct)


class Controlled(Generic[Op], QOperation[None]):
    def __init__(self, op: Op, *, name: Optional[str] = None):
        super().__init__(name=name)
        self._op = op

    @property
    def op(self) -> Op:
        return self._op

    def __repr__(self):
        name_str = f", name={self.name!r}" if self.name else ""
        return f"{type(self).__name__}({self._op!r}{name_str})"


@overload
def control(op: Op, control: Callable[QSystemSpec, QSystemStruct], target: Callable[QSystemSpec, QSystemStruct]):
    pass


@overload
def control(op: Op, control: IndexStruct, target: IndexStruct):
    pass


def control(op: Op, control, target):
    if callable(control) and callable(target):
        return remap(Controlled(op), lambda *args: (control(*args), target(*args)))
    else:
        return remap(Controlled(op), control, target)
