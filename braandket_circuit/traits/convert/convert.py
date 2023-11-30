import traceback
from typing import Any, Callable, TypeVar, overload

from zkl_registries import ObjTagKey, SimpleRegistry, SupTypeTagKey

from braandket_circuit.basics import QOperation
from braandket_circuit.traits.utils import resolve_type_and_instance
from .conversion import Conversion, T

Cv = TypeVar('Cv', bound=Conversion)
Op = TypeVar('Op', bound=QOperation)
ConversionImpl = Callable[[Conversion[T], QOperation], T]

CvType = SupTypeTagKey[type[Conversion], type[Conversion]]('CompilePassType')
CvInst = ObjTagKey[Cv]('CompilePassInstance', strict=False, required=False)
OpType = SupTypeTagKey[type[QOperation], type[QOperation]]('OperationType')
OpInst = ObjTagKey[QOperation]('OperationInstance', strict=False, required=False)
_registry = SimpleRegistry[ConversionImpl, Any, Any](keys=[CvType, CvInst, OpType, OpInst])


@overload
def register_convert_impl(
    cv: type[Conversion] | Conversion[T] | None,
    op: type[QOperation] | QOperation | None,
    impl: ConversionImpl
) -> ConversionImpl:
    pass


@overload
def register_convert_impl(
    cv: type[Conversion] | Conversion[T] | None,
    op: type[QOperation] | QOperation | None,
) -> Callable[[ConversionImpl], ConversionImpl]:
    pass


def register_convert_impl(
    cv: type[Conversion] | Conversion[T] | None,
    op: type[QOperation] | QOperation | None,
    impl: ConversionImpl | None = None
) -> ConversionImpl | Callable[[ConversionImpl], ConversionImpl]:
    if impl is None:
        def decorator(impl: ConversionImpl):
            register_convert_impl(cv, op, impl)
            return impl

        return decorator

    ps_type, ps_inst = resolve_type_and_instance(cv, base_type=Conversion)
    op_type, op_inst = resolve_type_and_instance(op, base_type=QOperation)
    _registry.register(impl, {CvType: ps_type, CvInst: ps_inst, OpType: op_type, OpInst: op_inst})
    return impl


def match_convert_impls(
    cv: type[Conversion] | Conversion[T] | None,
    op: type[QOperation] | QOperation | None,
) -> tuple[ConversionImpl, ...]:
    ps_type, ps_inst = resolve_type_and_instance(cv, base_type=Conversion)
    op_type, op_inst = resolve_type_and_instance(op, base_type=QOperation)
    return _registry.match({CvType: ps_type, CvInst: ps_inst, OpType: op_type, OpInst: op_inst})


def convert(cv: Conversion[T], op: QOperation) -> T:
    impls = match_convert_impls(cv, op)
    impls_error = []
    for impl in reversed(impls):
        try:
            return impl(cv, op)
        except Exception as err:
            impls_error.append(err)
    if not impls_error:
        raise NotImplementedError(f"No implementation for conversion {cv} and operation {op}.")
    elif len(impls_error) == 1:
        raise impls_error[0]
    else:
        for impl_error in impls_error:
            traceback.print_exception(impl_error)
        raise NotImplementedError(f"No viable implementation for conversion {cv} and operation {op}.")
