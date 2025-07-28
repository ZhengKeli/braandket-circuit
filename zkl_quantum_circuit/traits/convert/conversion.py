import abc
from typing import Generic, TypeVar

T = TypeVar('T')


class Conversion(Generic[T], abc.ABC):
    pass
