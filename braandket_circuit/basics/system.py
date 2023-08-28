import abc
import weakref
from typing import Iterable, Optional, Union, overload

from braandket import Backend, KetSpace, PureStateTensor, StateTensor


# state

class QState:
    def __init__(self, tensor: StateTensor, systems: Iterable['QSystem'] = ()):
        self._tensor = tensor
        self._particles = weakref.WeakSet()
        self._register(*systems)

    def _register(self, *systems: 'QSystem'):
        for system in systems:
            for particle in system.particles:
                particle._state = self
                self._particles.add(particle)

    @property
    def tensor(self) -> StateTensor:
        return self._tensor

    @tensor.setter
    def tensor(self, tensor: StateTensor):
        self._tensor = tensor

    @property
    def backend(self) -> Backend:
        return self.tensor.backend

    def __matmul__(self, other: 'QState') -> 'QState':
        if other is self:
            return self
        new_tensor = self._tensor @ other._tensor
        new_particles = (*self._particles, *other._particles)
        return QState(new_tensor, new_particles)

    @classmethod
    def prod(cls, *states: 'QState') -> 'QState':
        if len(states) == 0:
            return QState(PureStateTensor.of((), ()))
        if len(states) == 1:
            return states[0]
        return cls.prod(states[0] @ states[1], *states[2:])


# system

QSystemStruct = Union['QSystem', Iterable['QSystemStruct']]


class QSystem(abc.ABC):
    @classmethod
    @overload
    def of(cls, systems: QSystemStruct) -> 'QSystem':
        pass

    @classmethod
    @overload
    def of(cls, state_tensor: StateTensor) -> 'QSystem':
        pass

    @classmethod
    def of(cls, arg: Union[QSystemStruct, StateTensor]) -> 'QSystem':
        if isinstance(arg, QSystem):
            return arg
        if isinstance(arg, StateTensor):
            return cls._from_state_tensor(arg)
        if isinstance(arg, Iterable):
            return QComposed(QSystem.of(item) for item in arg)
        raise TypeError(f"Expected QSystemStruct or StateTensor, got {arg}!")

    @classmethod
    def _from_state_tensor(cls, state_tensor: StateTensor) -> 'QSystem':
        state = QState(state_tensor)
        return QSystem.of([QParticle(space, state) for space in state_tensor.ket_spaces])

    @property
    @abc.abstractmethod
    def name(self) -> Optional[str]:
        pass

    @property
    @abc.abstractmethod
    def particles(self) -> tuple['QParticle', ...]:
        pass

    @property
    def spaces(self) -> tuple[KetSpace, ...]:
        return tuple(particle.space for particle in self.particles)

    @property
    @abc.abstractmethod
    def state(self) -> QState:
        pass

    @property
    def backend(self) -> Backend:
        return self.state.backend

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


class QParticle(QSystem):
    def __init__(self, space: KetSpace, state: Union[QState, StateTensor, None] = None):
        self._space = space
        self._state: Optional[QState] = None

        if isinstance(state, QState):
            if space not in state.tensor.spaces:
                raise ValueError(f"Space {space} not included in the given state tensor!")
            state._register(self)
        elif isinstance(state, StateTensor):
            if space not in state.spaces:
                raise ValueError(f"Space {space} not included in the given state tensor!")
            QState(state, (self,))
        elif state is not None:
            raise TypeError(f"Expected QState or StateTensor, got {state}!")

    @property
    def space(self) -> KetSpace:
        return self._space

    # system

    @property
    def name(self) -> Optional[str]:
        return self.space.name

    @property
    def particles(self) -> tuple['QParticle', ...]:
        return self,

    @property
    def state(self) -> QState:
        if self._state is None:
            QState(self.space.eigenstate(0), (self,))
        return self._state

    # hash & eq

    def __eq__(self, other):
        if not isinstance(other, QParticle):
            return False
        return self.space == other.space and self.state == other.state

    def __hash__(self):
        return hash((id(self.space), id(self.state)))


class QComposed(QSystem, Iterable[QSystem]):
    def __init__(self, components: Iterable[QSystem], *, name: Optional[str] = None):
        self._name = name
        self._components = tuple(components)
        self._composed = False

    # system

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def particles(self) -> tuple['QParticle', ...]:
        return tuple(particle for component in self for particle in component.particles)

    @property
    def state(self) -> QState:
        particles = self.particles
        if not particles:
            return QState(PureStateTensor.of((), ()))

        if not self._composed:
            self._composed = True
            QState.prod(*(component.state for component in self))

        return particles[0].state

    # components

    def __iter__(self):
        return iter(self._components)

    def __len__(self):
        return len(self._components)

    def __getitem__(self, item):
        return self._components[item]
