import importlib
import weakref
from typing import Optional, Union

from braandket import Backend, KetSpace, StateTensor, get_default_backend
from braandket_circuit.basics import QParticle, QSystemStruct
from braandket_circuit.traits import QRuntime
from braandket_circuit.utils import iter_struct


class BnkRuntime(QRuntime):
    def __init__(self, backend: Backend | None = None):
        self._backend = backend or get_default_backend()

    @property
    def backend(self) -> Backend:
        return self._backend

    def __enter__(self):
        self.backend.__enter__()
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self.backend.__exit__(exc_type, exc_val, exc_tb)


class BnkState:
    def __init__(self, runtime: BnkRuntime, tensor: StateTensor, systems: QSystemStruct = ()):
        self._runtime = runtime
        self._tensor = tensor
        self._particles = weakref.WeakSet()
        self._register(*systems)

        if tensor.backend is not self.backend:
            raise ValueError(f"The backend of given state does not match the of backend runtime!")

    def _register(self, *systems: QSystemStruct):
        for particle in iter_struct(systems, atom_typ=BnkParticle):
            particle._state = self
            self._particles.add(particle)

    @property
    def runtime(self) -> BnkRuntime:
        return self._runtime

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
        if self.runtime is not other.runtime:
            raise ValueError(f"The runtimes of two states are not matched!")
        new_tensor = self._tensor @ other._tensor
        new_particles = (*self._particles, *other._particles)
        return BnkState(self.runtime, new_tensor, new_particles)

    @classmethod
    def prod(cls, *states: 'BnkState') -> 'BnkState':
        if len(states) == 0:
            raise ValueError("No states to compose!")
        if len(states) == 1:
            return states[0]
        return cls.prod(states[0] @ states[1], *states[2:])


class BnkParticle(QParticle):
    def __init__(self, runtime: BnkRuntime, space: KetSpace, state: Union[BnkState, StateTensor, None] = None):
        self._runtime = runtime
        self._space = space
        self._state: Optional[BnkState] = None

        if isinstance(state, BnkState):
            if state.runtime is not self.runtime:
                raise ValueError(f"The runtime of given state does not match!")
            if space not in state.tensor.spaces:
                raise ValueError(f"Space {space} not included in the given state tensor!")
            state._register(self)
        elif isinstance(state, StateTensor):
            if state.backend is not self.backend:
                raise ValueError(f"The backend of given state does not match!")
            if space not in state.spaces:
                raise ValueError(f"Space {space} not included in the given state tensor!")
            BnkState(self.runtime, state, (self,))
        elif state is not None:
            raise TypeError(f"Expected BnkState or StateTensor, got {state}!")

    @property
    def runtime(self) -> BnkRuntime:
        return self._runtime

    @property
    def backend(self) -> Backend:
        return self.runtime.backend

    @property
    def space(self) -> KetSpace:
        return self._space

    @property
    def state(self) -> BnkState:
        if self._state is None:
            BnkState(self.runtime, self.space.eigenstate(0, backend=self.backend), (self,))
        return self._state

    # system

    @property
    def name(self) -> Optional[str]:
        return self.space.name

    @property
    def ndim(self) -> int:
        return self.space.n

    # hash & eq

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.space == other.space and self.state == other.state

    def __hash__(self):
        return hash((id(self.space), id(self.state)))


importlib.import_module(".impls", __package__)
