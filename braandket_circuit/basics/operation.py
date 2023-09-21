import abc
from typing import Callable, Generic, Iterable, Optional, ParamSpec, TypeVar, Union, overload

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
    def on(self, func: Callable[QSystemSpec, QSystemStruct]) -> 'QOperation':
        pass

    @overload
    def on(self, *indices: IndexStruct) -> 'QOperation':
        pass

    def on(self, *args: Callable[QSystemSpec, QSystemStruct] | IndexStruct) -> 'QOperation':
        if len(args) == 1 and callable(args[0]):
            from braandket_circuit import RemappedByLambda
            op = RemappedByLambda(self, args[0])
        else:
            from braandket_circuit import RemappedByIndices
            op = RemappedByIndices(self, *args)
        return op
