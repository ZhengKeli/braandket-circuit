import abc
from typing import Generic, Optional, TypeVar

from .system import QSystemStruct

R = TypeVar('R')


class QOperation(Generic[R], abc.ABC):
    def __init__(self, *, name: Optional[str] = None):
        self._name = name

    @property
    def name(self) -> Optional[str]:
        return self._name

    def __call__(self, *args: QSystemStruct) -> R:
        from .runtime import get_default_runtime
        return get_default_runtime().operate(self, *args)

    def __repr__(self):
        name_str = f" name={self.name}" if self.name else ""
        return f"<{type(self).__name__}{name_str}>"
