import abc
from typing import Callable, Generic, Iterable, Optional, TypeVar, Union


class QSystem(abc.ABC):
    @property
    @abc.abstractmethod
    def name(self) -> Optional[str]:
        pass

    @property
    @abc.abstractmethod
    def particles(self) -> tuple['QParticle', ...]:
        pass

    # compose

    def __matmul__(self, other: 'QSystem'):
        components = []

        if isinstance(self, QComposed) and self.name is None:
            components.extend(self)
        else:
            components.append(self)

        if isinstance(other, QComposed) and other.name is None:
            components.extend(other)
        else:
            components.append(other)

        return QComposed(components)

    @classmethod
    def prod(cls, *systems: 'QSystem') -> 'QSystem':
        if len(systems) == 0:
            raise ValueError("No systems to compose!")
        if len(systems) == 1:
            return systems[0]
        return cls.prod(systems[0] @ systems[1], *systems[2:])

    # str & repr

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{type(self).__name__} name={self.name}>"


QSystemStruct = Union[QSystem, Iterable['QSystemStruct']]


# particle

class QParticle(QSystem, abc.ABC):
    @property
    @abc.abstractmethod
    def name(self) -> Optional[str]:
        pass

    @property
    @abc.abstractmethod
    def n(self) -> int:
        pass

    @property
    def particles(self) -> tuple['QParticle', ...]:
        return self,


# composed

S = TypeVar('S', bound=QSystem)


class QComposed(QSystem, Generic[S], Iterable[S]):
    def __init__(self, components: Iterable[S], *, name: Optional[str] = None):
        self._components = tuple(components)
        self._name = name

    # system

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def particles(self) -> tuple['QParticle', ...]:
        return tuple(particle for component in self for particle in component.particles)

    # components

    def __iter__(self):
        return iter(self._components)

    def __len__(self):
        return len(self._components)

    def __getitem__(self, item):
        return self._components[item]

    # str & repr

    def __str__(self):
        if self.name:
            return self.name
        return f"({', '.join(str(component) for component in self._components)})"

    def __repr__(self):
        name_str = f", name={self.name}" if self.name else ""
        components_str = ", ".join(repr(component) for component in self._components)
        return f"{type(self).__name__}([{components_str}]{name_str})"


# allocation

def allocate_particle(ndim: int, *, name: str | None = None) -> QParticle:
    from .runtime import get_runtime
    return get_runtime().allocate_particle(ndim, name=name)


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
