import abc
from typing import Optional

from braandket_circuit.system import QSystem


class QOperation(abc.ABC):
    def __init__(self, *, name: Optional[str] = None):
        self._name = name

    @property
    def name(self) -> Optional[str]:
        return self._name

    @abc.abstractmethod
    def __call__(self, *args: QSystem, **kwargs: QSystem):
        pass
