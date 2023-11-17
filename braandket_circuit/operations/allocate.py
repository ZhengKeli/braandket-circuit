from typing import Callable, Iterable

from braandket_circuit.basics import QComposed, QOperation, QParticle


class AllocateParticle(QOperation[QParticle]):
    def __init__(self, ndim: int, *, name: str | None = None):
        super().__init__(name=name)
        self._ndim = ndim
        self._name = name

    @property
    def ndim(self) -> int:
        return self._ndim


def allocate_particle(ndim: int, *, name: str | None = None) -> QParticle:
    return AllocateParticle(ndim, name=name)()


def allocate_qubit(*, name: str | None = None) -> QParticle:
    return allocate_particle(2, name=name)


def allocate_qubits(n: int, *, name: str | Iterable[str] | Callable[[int], str] | None = None) -> QComposed:
    if isinstance(name, str):
        name_func = lambda i: f"{name}_{i}"
    elif isinstance(name, Iterable):
        names = tuple(nm for _, nm in zip(range(n), name))
        name_func = lambda i: f"{names[i]}"
        name = None
    elif callable(name):
        name_func = name
        name = None
    elif name is None:
        name_func = lambda i: None
    else:
        raise TypeError(f"Unexpected type for name: {type(name)}")

    return QComposed((allocate_qubit(name=name_func(i)) for i in range(n)), name=name)
