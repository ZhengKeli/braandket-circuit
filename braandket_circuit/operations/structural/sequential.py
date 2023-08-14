from typing import Generic, Iterable, Optional, TypeVar

from braandket_circuit.basics import QOperation
from braandket_circuit.system import QSystem

Op = TypeVar('Op', bound=QOperation)


class Sequential(QOperation, Generic[Op]):
    def __init__(self, steps: Iterable[Op], *, name: Optional[str] = None):
        super().__init__(name=name)

        # check
        steps = tuple(steps)
        for i, step in enumerate(steps):
            if not isinstance(step, QOperation):
                raise TypeError(f"steps[{i}]={step} is not a QOperation!")

        self._steps = steps

    @property
    def steps(self) -> tuple[Op, ...]:
        return self._steps

    def __call__(self, *args: QSystem, **kwargs: QSystem):
        for step in self.steps:
            step(*args, **kwargs)
