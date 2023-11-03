import importlib
import weakref
from typing import Optional, Union

from braandket import Backend, KetSpace, PureStateTensor, StateTensor, get_default_backend
from braandket_circuit.basics import QParticle, QRuntime, QSystem, QSystemStruct
from braandket_circuit.utils import iter_struct


class BnkRuntime(QRuntime):
    def __init__(self, backend: Backend | None = None):
        self._backend = backend or get_default_backend()

    @property
    def backend(self) -> Backend:
        return self._backend

    def allocate_particle(self, ndim: int, *, name: str | None = None) -> QSystem:
        return BnkParticle(KetSpace(ndim, name=name))

    def __enter__(self):
        self.backend.__enter__()
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self.backend.__exit__(exc_type, exc_val, exc_tb)


class BnkState:
    def __init__(self, tensor: StateTensor, systems: QSystemStruct = ()):
        self._tensor = tensor
        self._particles = weakref.WeakSet()
        self._register(*systems)

    def _register(self, *systems: QSystemStruct):
        for particle in iter_struct(systems, atom_typ=BnkParticle):
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

    def __matmul__(self, other: 'BnkState') -> 'BnkState':
        if other is self:
            return self
        new_tensor = self._tensor @ other._tensor
        new_particles = (*self._particles, *other._particles)
        return BnkState(new_tensor, new_particles)

    @classmethod
    def prod(cls, *states: 'BnkState') -> 'BnkState':
        if len(states) == 0:
            return BnkState(PureStateTensor.of((), ()))
        if len(states) == 1:
            return states[0]
        return cls.prod(states[0] @ states[1], *states[2:])


class BnkParticle(QParticle):
    def __init__(self, space: KetSpace, state: Union[BnkState, StateTensor, None] = None):
        self._space = space
        self._state: Optional[BnkState] = None

        if isinstance(state, BnkState):
            if space not in state.tensor.spaces:
                raise ValueError(f"Space {space} not included in the given state tensor!")
            state._register(self)
        elif isinstance(state, StateTensor):
            if space not in state.spaces:
                raise ValueError(f"Space {space} not included in the given state tensor!")
            BnkState(state, (self,))
        elif state is not None:
            raise TypeError(f"Expected BnkState or StateTensor, got {state}!")

    @property
    def space(self) -> KetSpace:
        return self._space

    @property
    def state(self) -> BnkState:
        if self._state is None:
            BnkState(self.space.eigenstate(0), (self,))
        return self._state

    # system

    @property
    def name(self) -> Optional[str]:
        return self.space.name

    @property
    def n(self) -> int:
        return self.space.n

    # hash & eq

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.space == other.space and self.state == other.state

    def __hash__(self):
        return hash((id(self.space), id(self.state)))


importlib.import_module(".apply_impls", __package__)
