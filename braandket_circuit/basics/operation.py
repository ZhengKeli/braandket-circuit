import abc
from typing import Generic, Iterable, Optional, ParamSpec, TypeVar, Union, overload

from .system import QSystemStruct

R = TypeVar('R')

QSystemSpec = ParamSpec('QSystemSpec', bound=QSystemStruct)
IndexStruct = Union[int, Iterable['IndexStruct']]


class QOperation(Generic[R], abc.ABC):
    def __init_subclass__(cls, **kwargs):
        if cls.__call__ != QOperation.__call__:
            cls._custom_call = cls.__call__
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
        *target: IndexStruct,
        control: IndexStruct | None = None,
    ) -> 'QOperation':
        pass

    @overload
    def on(self, *,
        target: IndexStruct,
        control: IndexStruct | None = None,
    ) -> 'QOperation':
        pass

    def on(self,
        *target_args: IndexStruct,
        target: IndexStruct | None = None,
        control: IndexStruct | None = None,
    ) -> 'QOperation':
        if len(target_args) == 0 and target is None:
            raise TypeError("No target specified.")
        if len(target_args) != 0 and target is not None:
            raise TypeError("Cannot specify 'target' both with varargs and kwargs.")
        target = target_args if target is None else target
        target = (target,) if not isinstance(target, Iterable) else target

        from braandket_circuit import Remapped
        if control is None:
            return Remapped(self, *target)

        from braandket_circuit import Controlled
        return Remapped(Controlled(self), control, target)
