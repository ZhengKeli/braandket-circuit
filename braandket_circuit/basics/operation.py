import abc
import warnings
from typing import Callable, Generic, Iterable, Optional, ParamSpec, TypeVar, Union, overload

from braandket_circuit.utils import map_struct
from .system import QSystemStruct

R = TypeVar('R')

QSystemSpec = ParamSpec('QSystemSpec', bound=QSystemStruct)
IndexStruct = Union[int, Iterable['IndexStruct']]


class QOperation(Generic[R], abc.ABC):
    def __init_subclass__(cls, **kwargs):
        org_call = cls.__call__
        if org_call != QOperation.__call__:
            from braandket_circuit.traits import register_apply_impl
            register_apply_impl(None, cls, lambda _, op, *args: org_call(op, *args))
            del cls.__call__

    def __init__(self, *, name: Optional[str] = None):
        self._name = name

    @property
    def name(self) -> Optional[str]:
        return self._name

    def __call__(self, *args: QSystemStruct) -> R:
        from braandket_circuit.traits import apply, get_current_runtime
        return apply(get_current_runtime(), self, *args)

    def __repr__(self):
        name_str = f" name={self.name}" if self.name else ""
        return f"<{type(self).__name__}{name_str}>"

    # remap

    @overload
    def on(self,
        target: Callable[QSystemSpec, QSystemStruct], *,
        control: Callable[QSystemSpec, QSystemStruct] | IndexStruct | None = None,
    ) -> 'QOperation':
        pass

    @overload
    def on(self,
        *indices: IndexStruct,
        control: Callable[QSystemSpec, QSystemStruct] | IndexStruct | None = None,
    ) -> 'QOperation':
        pass

    @overload
    def on(self, *,
        target: Callable[QSystemSpec, QSystemStruct] | IndexStruct | None = None,
        control: Callable[QSystemSpec, QSystemStruct] | IndexStruct | None = None,
    ) -> 'QOperation':
        pass

    def on(self,
        *target_args: Callable[QSystemSpec, QSystemStruct] | IndexStruct,
        target: Callable[QSystemSpec, QSystemStruct] | IndexStruct | None = None,
        control: Callable[QSystemSpec, QSystemStruct] | IndexStruct | None = None,
    ) -> 'QOperation':
        if target is not None:
            target_is_lambda = isinstance(target, Callable)
            if len(target_args) != 0:
                warnings.warn("Ignored varargs when argument 'target' presents.")
        else:
            target_is_lambda = len(target_args) == 1 and isinstance(target_args[0], Callable)
            if target_is_lambda:
                target = target_args[0]
            else:
                target = target_args

        if control is None:
            if target_is_lambda:
                from braandket_circuit import RemappedByLambda
                return RemappedByLambda(self, target)
            else:
                from braandket_circuit import RemappedByIndices
                return RemappedByIndices(self, *target)

        from braandket_circuit import Controlled
        controlled = Controlled(self)

        control_is_lambda = callable(control)
        if target_is_lambda or control_is_lambda:
            if not target_is_lambda:
                target = lambda *args: map_struct(lambda i: args[i], target, atom_typ=int)
            if not control_is_lambda:
                control = lambda *args: map_struct(lambda i: args[i], control, atom_typ=int)

            from braandket_circuit import RemappedByLambda
            return RemappedByLambda(controlled, lambda *args: (control(*args), target(*args)))
        else:
            from braandket_circuit import RemappedByIndices
            return RemappedByIndices(controlled, control, target)
