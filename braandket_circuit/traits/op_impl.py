from typing import Any, Callable, TypeVar, overload

from braandket_circuit.basics import QOperation, QRuntime, QSystemStruct, R
from zkl_registries import SimpleRegistry
from zkl_registries.tagkeys.type import SupTypeTagKey

Rt = TypeVar('Rt', bound=QRuntime)
Op = TypeVar('Op', bound=QOperation)
BnkRuntimeOpImpl = Callable[[Rt, Op, QSystemStruct], R]

RtType = SupTypeTagKey[type[QRuntime], type[QRuntime]]('RuntimeType')
OpType = SupTypeTagKey[type[QOperation], type[QOperation]]('OperationType')
_op_impl_registry = SimpleRegistry[BnkRuntimeOpImpl, Any, Any](keys=[RtType, OpType])


@overload
def register_op_impl(
    rt_type: type[Rt] | None,
    op_type: type[Op] | None,
    impl: BnkRuntimeOpImpl
) -> BnkRuntimeOpImpl:
    pass


@overload
def register_op_impl(
    rt_type: type[Rt] | None,
    op_type: type[Op] | None,
) -> Callable[[BnkRuntimeOpImpl], BnkRuntimeOpImpl]:
    pass


def register_op_impl(
    rt_type: type[Rt] | None,
    op_type: type[Op] | None,
    impl: BnkRuntimeOpImpl | None = None
) -> BnkRuntimeOpImpl | Callable[[BnkRuntimeOpImpl], BnkRuntimeOpImpl]:
    if impl is None:
        def decorator(impl: BnkRuntimeOpImpl):
            register_op_impl(rt_type, op_type, impl)
            return impl

        return decorator

    _op_impl_registry.register(impl, {RtType: rt_type, OpType: op_type})
    return impl


def get_op_impls(
    rt_type: type[Rt] | None,
    op_type: type[Op] | None,
) -> tuple[BnkRuntimeOpImpl, ...]:
    return _op_impl_registry.match({RtType: rt_type, OpType: op_type})
