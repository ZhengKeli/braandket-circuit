import abc
from typing import Generic, Iterable, Optional, TypeVar, Union


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
    def ndim(self) -> int:
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
