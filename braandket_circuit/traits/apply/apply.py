import traceback
from typing import Any, Callable, TypeVar, overload

from braandket_circuit.basics import QOperation, QSystemStruct, R
from braandket_circuit.traits.utils import resolve_type_and_instance
from zkl_registries import ObjTagKey, SimpleRegistry, SupTypeTagKey
from .runtime import QRuntime

Rt = TypeVar('Rt', bound=QRuntime)
Op = TypeVar('Op', bound=QOperation)
ApplyImpl = Callable[[Rt, Op, QSystemStruct], R]

RtType = SupTypeTagKey[type[QRuntime], type[QRuntime]]('RuntimeType')
RtInst = ObjTagKey[QRuntime]('RuntimeInstance', strict=False, required=False)
OpType = SupTypeTagKey[type[QOperation], type[QOperation]]('OperationType')
OpInst = ObjTagKey[QOperation]('OperationInstance', strict=False, required=False)
_registry = SimpleRegistry[ApplyImpl, Any, Any](keys=[RtType, RtInst, OpType, OpInst])


@overload
def register_apply_impl(
    rt: type[Rt] | Rt | None,
    op: type[Op] | Op | None,
    impl: ApplyImpl
) -> ApplyImpl:
    pass


@overload
def register_apply_impl(
    rt: type[Rt] | Rt | None,
    op: type[Op] | Op | None,
) -> Callable[[ApplyImpl], ApplyImpl]:
    pass


def register_apply_impl(
    rt: type[Rt] | Rt | None,
    op: type[Op] | Op | None,
    impl: ApplyImpl | None = None
) -> ApplyImpl | Callable[[ApplyImpl], ApplyImpl]:
    if impl is None:
        def decorator(impl: ApplyImpl):
            register_apply_impl(rt, op, impl)
            return impl

        return decorator

    rt_type, rt_inst = resolve_type_and_instance(rt, base_type=QRuntime)
    op_type, op_inst = resolve_type_and_instance(op, base_type=QOperation)
    _registry.register(impl, {RtType: rt_type, RtInst: rt_inst, OpType: op_type, OpInst: op_inst})
    return impl


def match_apply_impls(
    rt: type[Rt] | Rt | None,
    op: type[Op] | Op | None,
) -> tuple[ApplyImpl, ...]:
    rt_type, rt_inst = resolve_type_and_instance(rt, base_type=QRuntime)
    op_type, op_inst = resolve_type_and_instance(op, base_type=QOperation)
    return _registry.match({RtType: rt_type, RtInst: rt_inst, OpType: op_type, OpInst: op_inst})


def apply(rt: Rt, op: Op, *args: QSystemStruct) -> R:
    impls = match_apply_impls(rt, op)
    impls_error = []
    for impl in reversed(impls):
        try:
            return impl(rt, op, *args)
        except NotImplementedError as err:
            impls_error.append(err)
    if not impls_error:
        raise NotImplementedError(f"No implementation for operation {op} on runtime {rt}.")
    elif len(impls_error) == 1:
        raise impls_error[0]
    else:
        for impl_error in impls_error:
            traceback.print_exception(impl_error)
        raise NotImplementedError(f"Failed to apply operation {op} on runtime {rt}")
