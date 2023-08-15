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

    @abc.abstractmethod
    def __call__(self, *args: QSystemStruct) -> R:
        pass
