import traceback
from typing import Any, Callable, TypeVar, overload

from braandket_circuit.basics import QOperation, QSystemStruct
from braandket_circuit.traits.utils import resolve_type_and_instance
from zkl_registries import ObjTagKey, SimpleRegistry, SupTypeTagKey

Op = TypeVar('Op', bound=QOperation)
SOp = TypeVar('SOp', bound=QOperation)
FreezeImpl = Callable[[Op, QSystemStruct], SOp]

OpType = SupTypeTagKey[type[QOperation], type[QOperation]]('OperationType')
OpInst = ObjTagKey[QOperation]('OperationInstance', strict=False, required=False)
_registry = SimpleRegistry[FreezeImpl, Any, Any](keys=[OpType, OpInst])


@overload
def register_freeze_impl(
    op: type[Op] | Op | None,
    impl: FreezeImpl
) -> FreezeImpl:
    pass


@overload
def register_freeze_impl(
    op: type[Op] | Op | None,
) -> Callable[[FreezeImpl], FreezeImpl]:
    pass


def register_freeze_impl(
    op: type[Op] | Op | None,
    impl: FreezeImpl | None = None
) -> FreezeImpl | Callable[[FreezeImpl], FreezeImpl]:
    if impl is None:
        def decorator(impl: FreezeImpl):
            register_freeze_impl(op, impl)
            return impl

        return decorator

    op_type, op_inst = resolve_type_and_instance(op, base_type=QOperation)
    _registry.register(impl, {OpType: op_type, OpInst: op_inst})
    return impl


def match_freeze_impls(
    op: type[Op] | Op | None,
) -> tuple[FreezeImpl, ...]:
    op_type, op_inst = resolve_type_and_instance(op, base_type=QOperation)
    return _registry.match({OpType: op_type, OpInst: op_inst})


def freeze(op: Op, *args: QSystemStruct) -> SOp:
    impls = match_freeze_impls(op)
    impls_error = []
    for impl in reversed(impls):
        try:
            return impl(op, *args)
        except Exception as err:
            impls_error.append(err)
    if not impls_error:
        raise NotImplementedError(f"No freeze implementation for operation {op}.")
    elif len(impls_error) == 1:
        raise impls_error[0]
    else:
        for impl_error in impls_error:
            traceback.print_exception(impl_error)
        raise NotImplementedError(f"Failed to freeze operation {op}.")
