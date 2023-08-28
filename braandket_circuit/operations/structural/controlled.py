from typing import Callable, Generic, Optional, ParamSpec, TypeVar, overload

import braandket as bnk
from braandket import MixedStateTensor, PureStateTensor
from braandket_circuit.basics import QOperation, QSystem, QSystemStruct
from .remapped import IndexStruct, remap

Op = TypeVar("Op", bound=QOperation)
QSystemSpec = ParamSpec('QSystemSpec', bound=QSystemStruct)


class Controlled(Generic[Op], QOperation[None]):
    def __init__(self, op: Op, *, name: Optional[str] = None):
        super().__init__(name=name)
        self._op = op

    @property
    def op(self) -> Op:
        return self._op

    def __call__(self, control: QSystemStruct, target: QSystemStruct):
        control_system = QSystem.of(control)
        control_identity = bnk.prod(*(sp.identity() for sp in control_system.spaces))
        control_projector_on = bnk.prod(*(sp.projector(1) for sp in control_system.spaces))
        control_projector_off = control_identity - control_projector_on

        total_system = QSystem.of([control, target])
        total_state_off = total_system.state.tensor
        target = (target,) if isinstance(target, QSystem) else target
        self.op(*target)
        total_state_on = total_system.state.tensor

        if isinstance(total_state_off, PureStateTensor) and isinstance(total_state_on, PureStateTensor):
            total_system.state.tensor = PureStateTensor.of(bnk.sum(
                control_projector_on @ total_state_on,
                control_projector_off @ total_state_off
            ))
        else:
            total_state_on = MixedStateTensor.of(total_state_on)
            total_state_off = MixedStateTensor.of(total_state_off)
            total_system.state.tensor = MixedStateTensor.of(bnk.sum(
                control_projector_on @ total_state_on @ control_projector_on,
                control_projector_off @ total_state_off @ control_projector_off
            ))


@overload
def control(op: Op, control: Callable[QSystemSpec, QSystemStruct], target: Callable[QSystemSpec, QSystemStruct]):
    pass


@overload
def control(op: Op, control: IndexStruct, target: IndexStruct):
    pass


def control(op: Op, control, target):
    if callable(control) and callable(target):
        return remap(Controlled(op), lambda *args: (control(*args), target(*args)))
    else:
        return remap(Controlled(op), control, target)
