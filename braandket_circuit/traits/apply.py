from typing import Any, Callable, TypeVar, overload

from braandket_circuit.basics import QOperation, QRuntime, QSystemStruct, R
from zkl_registries import ObjTagKey, SimpleRegistry, SupTypeTagKey

Rt = TypeVar('Rt', bound=QRuntime)
Op = TypeVar('Op', bound=QOperation)
ApplyImpl = Callable[[Rt, Op, QSystemStruct], R]

RtType = SupTypeTagKey[type[QRuntime], type[QRuntime]]('RuntimeType')
OpType = SupTypeTagKey[type[QOperation], type[QOperation]]('OperationType')
OpInst = ObjTagKey[QOperation]('OperationInstance', strict=False, required=False)
_registry = SimpleRegistry[ApplyImpl, Any, Any](keys=[RtType, OpType, OpInst])


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

    if not isinstance(rt, type):
        rt = type(rt)

    if not isinstance(op, type):
        op_type = type(op)
    else:
        op_type = op
        op = None

    _registry.register(impl, {RtType: rt, OpType: op_type, OpInst: op})
    return impl


def get_apply_impls(
    rt: type[Rt] | Rt | None,
    op: type[Op] | Op | None,
) -> tuple[ApplyImpl, ...]:
    if not isinstance(rt, type):
        rt = type(rt)
    if not isinstance(op, type):
        op_type = type(op)
    else:
        op_type = op
        op = None

    return _registry.match({RtType: rt, OpType: op_type, OpInst: op})


def apply(rt: Rt, op: Op, *args: QSystemStruct) -> R:
    impls = get_apply_impls(rt, op)
    for impl in reversed(impls):
        try:
            return impl(rt, op, *args)
        except NotImplementedError:
            pass
    raise NotImplementedError
