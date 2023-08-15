from typing import Generic, Iterable, Optional, TypeVar, Union

import braandket as bnk
from braandket import MixedStateTensor, PureStateTensor
from braandket_circuit.basics import QOperation, QSystem, QSystemStruct, compose
from .remapped import Remapped

Op = TypeVar("Op", bound=QOperation)


class Controlled(Generic[Op], QOperation[None]):
    def __init__(self, op: Op, *, name: Optional[str] = None):
        super().__init__(name=name)
        self._op = op

    @property
    def op(self) -> Op:
        return self._op

    def __call__(self, control: QSystemStruct, target: QSystemStruct):
        control_system = compose(control)
        control_identity = bnk.prod(*(sp.identity() for sp in control_system.spaces))
        control_projector_on = bnk.prod(*(sp.projector(1) for sp in control_system.spaces))
        control_projector_off = control_identity - control_projector_on

        total_system = compose(control, target)
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


def control_by_indices(
    op: Op,
    control: Union[int, Iterable[int]],
    target: Union[int, Iterable[int]],
) -> Remapped[Controlled[Op]]:
    def mapper(*args: QSystemStruct):
        control_arg = args[control] if isinstance(control, int) \
            else tuple(args[i] for i in control)
        target_arg = args[target] if isinstance(target, int) \
            else tuple(args[i] for i in target)
        return control_arg, target_arg

    return Remapped(Controlled(op), mapper)
