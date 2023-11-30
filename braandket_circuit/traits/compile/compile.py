import traceback
from typing import Any, Callable, TypeVar, overload

from zkl_registries import ObjTagKey, SimpleRegistry, SupTypeTagKey

from braandket_circuit.basics import QOperation
from braandket_circuit.traits.utils import resolve_type_and_instance
from .compile_pass import CompilePass

Ps = TypeVar('Ps', bound=CompilePass)
Op = TypeVar('Op', bound=QOperation)
CompilePassImpl = Callable[[Ps, Op], QOperation]

PsType = SupTypeTagKey[type[CompilePass], type[CompilePass]]('CompilePassType')
PsInst = ObjTagKey[Ps]('CompilePassInstance', strict=False, required=False)
OpType = SupTypeTagKey[type[QOperation], type[QOperation]]('OperationType')
OpInst = ObjTagKey[QOperation]('OperationInstance', strict=False, required=False)
_registry = SimpleRegistry[CompilePassImpl, Any, Any](keys=[PsType, PsInst, OpType, OpInst])


@overload
def register_compile_impl(
    ps: type[Ps] | Ps | None,
    op: type[Op] | Op | None,
    impl: CompilePassImpl
) -> CompilePassImpl:
    pass


@overload
def register_compile_impl(
    ps: type[Ps] | Ps | None,
    op: type[Op] | Op | None,
) -> Callable[[CompilePassImpl], CompilePassImpl]:
    pass


def register_compile_impl(
    ps: type[Ps] | Ps | None,
    op: type[Op] | Op | None,
    impl: CompilePassImpl | None = None
) -> CompilePassImpl | Callable[[CompilePassImpl], CompilePassImpl]:
    if impl is None:
        def decorator(impl: CompilePassImpl):
            register_compile_impl(ps, op, impl)
            return impl

        return decorator

    ps_type, ps_inst = resolve_type_and_instance(ps, base_type=CompilePass)
    op_type, op_inst = resolve_type_and_instance(op, base_type=QOperation)
    _registry.register(impl, {PsType: ps_type, PsInst: ps_inst, OpType: op_type, OpInst: op_inst})
    return impl


def match_compile_impls(
    ps: type[Ps] | Ps | None,
    op: type[Op] | Op | None,
) -> tuple[CompilePassImpl, ...]:
    ps_type, ps_inst = resolve_type_and_instance(ps, base_type=CompilePass)
    op_type, op_inst = resolve_type_and_instance(op, base_type=QOperation)
    return _registry.match({PsType: ps_type, PsInst: ps_inst, OpType: op_type, OpInst: op_inst})


def compile(ps: Ps, op: Op) -> QOperation:
    impls = match_compile_impls(ps, op)
    impls_error = []
    for impl in reversed(impls):
        try:
            return impl(ps, op)
        except Exception as err:
            impls_error.append(err)
    if not impls_error:
        raise NotImplementedError(f"No implementation for compile pass {ps} and operation {op}.")
    elif len(impls_error) == 1:
        raise impls_error[0]
    else:
        for impl_error in impls_error:
            traceback.print_exception(impl_error)
        raise NotImplementedError(f"No viable implementation for compile pass {ps} and operation {op}.")
