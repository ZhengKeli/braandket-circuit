from typing import Generic, Iterable, Optional, TypeVar

from braandket_circuit.basics import QOperation, QSystem

Op = TypeVar('Op', bound=QOperation)


class Sequential(Generic[Op], QOperation[tuple]):
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

    def __call__(self, *args: QSystem) -> tuple:
        results = []
        for step in self.steps:
            results.append(step(*args))
        return tuple(results)
