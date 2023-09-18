from typing import Any, Callable, TypeVar, overload

from braandket_circuit.basics import QOperation, QRuntime, QSystemStruct, R
from zkl_registries import ObjTagKey, SimpleRegistry, SupTypeTagKey

Rt = TypeVar('Rt', bound=QRuntime)
Op = TypeVar('Op', bound=QOperation)
BnkRuntimeOpImpl = Callable[[Rt, Op, QSystemStruct], R]

RtType = SupTypeTagKey[type[QRuntime], type[QRuntime]]('RuntimeType')
OpType = SupTypeTagKey[type[QOperation], type[QOperation]]('OperationType')
OpInst = ObjTagKey[QOperation]('OperationInstance', strict=False, required=False)
_op_impl_registry = SimpleRegistry[BnkRuntimeOpImpl, Any, Any](keys=[RtType, OpType, OpInst])


@overload
def register_op_impl(
    rt: type[Rt] | Rt | None,
    op: type[Op] | Op | None,
    impl: BnkRuntimeOpImpl
) -> BnkRuntimeOpImpl:
    pass


@overload
def register_op_impl(
    rt: type[Rt] | Rt | None,
    op: type[Op] | Op | None,
) -> Callable[[BnkRuntimeOpImpl], BnkRuntimeOpImpl]:
    pass


def register_op_impl(
    rt: type[Rt] | Rt | None,
    op: type[Op] | Op | None,
    impl: BnkRuntimeOpImpl | None = None
) -> BnkRuntimeOpImpl | Callable[[BnkRuntimeOpImpl], BnkRuntimeOpImpl]:
    if impl is None:
        def decorator(impl: BnkRuntimeOpImpl):
            register_op_impl(rt, op, impl)
            return impl

        return decorator

    if not isinstance(rt, type):
        rt = type(rt)

    if not isinstance(op, type):
        op_type = type(op)
    else:
        op_type = op
        op = None

    _op_impl_registry.register(impl, {RtType: rt, OpType: op_type, OpInst: op})
    return impl


def get_op_impls(
    rt: type[Rt] | Rt | None,
    op: type[Op] | Op | None,
) -> tuple[BnkRuntimeOpImpl, ...]:
    if not isinstance(rt, type):
        rt = type(rt)
    if not isinstance(op, type):
        op_type = type(op)
    else:
        op_type = op
        op = None

    return _op_impl_registry.match({RtType: rt, OpType: op_type, OpInst: op})
