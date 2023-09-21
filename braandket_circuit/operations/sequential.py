from copy import copy
from typing import Generic, Iterable, Iterator, Optional, TypeVar, Union, overload

from braandket_circuit.basics import QOperation, QSystemStruct, R

Op = TypeVar('Op', bound=QOperation)


class Sequential(QOperation[tuple], Generic[Op]):
    @overload
    def __init__(self, *steps: Op, name: Optional[str] = None):
        pass

    @overload
    def __init__(self, steps: Iterable[Op], *, name: Optional[str] = None):
        pass

    def __init__(self, *args: Iterable[Op] | Op, name: Optional[str] = None):
        super().__init__(name=name)
        if len(args) == 1:
            args0 = args[0]
            if isinstance(args0, QOperation):
                self._steps = args0,
            elif isinstance(args0, Iterable):
                self._steps = tuple(args0)
            else:
                raise TypeError(f"Unexpected type {type(args0)}!")
        else:
            self._steps = args

    def __len__(self):
        return len(self._steps)

    def __iter__(self) -> Iterator[Op]:
        return iter(self._steps)

    @overload
    def __getitem__(self, item: int) -> Op:
        pass

    @overload
    def __getitem__(self, item: slice) -> 'Sequential[Op]':
        pass

    def __getitem__(self, item: int | slice) -> Union[Op, 'Sequential[Op]']:
        if isinstance(item, slice):
            new = copy(self)
            new._steps = new._steps[item]
            return new
        return self._steps[item]

    def __add__(self, other: Op) -> 'Sequential[Op]':
        if isinstance(other, Sequential) and other.name is None:
            return Sequential((*self, *other), name=self.name)
        else:
            return Sequential((*self, other), name=self.name)

    def __radd__(self, other: Op) -> 'Sequential[Op]':
        return Sequential((other, *self), name=self.name)

    def __mul__(self, other: int) -> 'Sequential[Op]':
        return Sequential([self] * other, name=self.name)

    def __call__(self, *args: QSystemStruct) -> R:
        results = []
        for step in self:
            results.append(step(*args))
        return tuple(results)

    def __repr__(self) -> str:
        s = f"{type(self).__name__}(["
        for step in self:
            s += f"\n\t" + repr(step).replace("\n", "\n\t") + ","
        return s + "\n])"
