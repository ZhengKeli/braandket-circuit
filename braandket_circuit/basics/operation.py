import abc
from typing import Callable, Generic, Iterable, Optional, ParamSpec, TypeVar, Union, overload

from braandket_circuit.utils import map_struct
from .system import QSystemStruct

R = TypeVar('R')

QSystemSpec = ParamSpec('QSystemSpec', bound=QSystemStruct)
IndexStruct = Union[int, Iterable['IndexStruct']]


class QOperation(Generic[R], abc.ABC):
    def __init__(self, *, name: Optional[str] = None):
        self._name = name

    @property
    def name(self) -> Optional[str]:
        return self._name

    def __call__(self, *args: QSystemStruct) -> R:
        from .runtime import get_runtime
        return get_runtime().operate(self, *args)

    def __repr__(self):
        name_str = f" name={self.name}" if self.name else ""
        return f"<{type(self).__name__}{name_str}>"

    # remap

    @overload
    def on(self,
        func: Callable[QSystemSpec, QSystemStruct], *,
        ctrl: Callable[QSystemSpec, QSystemStruct] | IndexStruct | None = None,
    ) -> 'QOperation':
        pass

    @overload
    def on(self,
        *indices: IndexStruct,
        ctrl: Callable[QSystemSpec, QSystemStruct] | IndexStruct | None = None,
    ) -> 'QOperation':
        pass

    def on(self,
        *target: Callable[QSystemSpec, QSystemStruct] | IndexStruct,
        ctrl: Callable[QSystemSpec, QSystemStruct] | IndexStruct | None = None,
    ) -> 'QOperation':
        target_is_lambda = len(target) == 1 and callable(target[0])
        if target_is_lambda:
            target = target[0]

        if ctrl is None:
            if target_is_lambda:
                from braandket_circuit import RemappedByLambda
                return RemappedByLambda(self, target)
            else:
                from braandket_circuit import RemappedByIndices
                return RemappedByIndices(self, *target)

        from braandket_circuit import Controlled
        controlled = Controlled(self)

        control_is_lambda = callable(ctrl)
        if target_is_lambda or control_is_lambda:
            if not target_is_lambda:
                target = lambda *args: map_struct(lambda i: args[i], target, atom_typ=int)
            if not control_is_lambda:
                ctrl = lambda *args: map_struct(lambda i: args[i], ctrl, atom_typ=int)

            from braandket_circuit import RemappedByLambda
            return RemappedByLambda(controlled, lambda *args: (ctrl(*args), target(*args)))
        else:
            from braandket_circuit import RemappedByIndices
            return RemappedByIndices(controlled, ctrl, target)
