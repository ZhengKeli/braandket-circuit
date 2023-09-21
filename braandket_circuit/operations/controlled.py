from typing import Generic, Optional, TypeVar

from braandket_circuit.basics import QOperation

Op = TypeVar("Op", bound=QOperation)


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
