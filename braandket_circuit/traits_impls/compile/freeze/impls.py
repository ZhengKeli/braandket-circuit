import inspect

from braandket_circuit.basics import QOperation, QSystemStruct
from braandket_circuit.operations import Remapped, Sequential
from braandket_circuit.traits import compile, match_apply_impls, register_compile_impl
from .freeze_pass import FreezePass


def args_from_signature(op: QOperation) -> QSystemStruct:
    # noinspection PyProtectedMember
    org_call = op._custom_call

    spec = inspect.getfullargspec(org_call)
    if spec.varargs is not None:
        raise TypeError("varargs is not supported in compiling!")
    if spec.varkw is not None:
        raise TypeError("varkw is not supported in compiling!")
    if spec.kwonlyargs:
        raise TypeError("kwonlyargs is not supported in compiling!")

    from braandket_circuit.traits_impls import SymbolicParticle
    return tuple(SymbolicParticle(2, name=arg_name) for arg_name in spec.args[1:])


@register_compile_impl(FreezePass, None)
def common_impl(ps: FreezePass, op: QOperation) -> QOperation:
    args = ps.args
    if args is None:
        args = args_from_signature(op)

    impls = match_apply_impls(None, op)
    if len(impls) == 0:
        return op

    calls = None
    from braandket_circuit.traits_impls import SymbolicRuntime
    for impl in reversed(impls):
        try:
            with SymbolicRuntime() as rt:
                impl(rt, op, *args)
            calls = rt.recorded_calls
            break
        except NotImplementedError:
            calls = None

    if calls is None:
        return op
    if len(calls) == 1 and calls[0].op is op and calls[0].args == args:
        return op

    steps = []
    for call in calls:
        call_op = compile(FreezePass(call.args), call.op)
        args_index = [args.index(arg) for arg in call.args]
        steps.append(call_op.on(*args_index))
    return Sequential(steps, name=op.name)


@register_compile_impl(FreezePass, Sequential)
def sequential_impl(ps: FreezePass, op: Sequential, *args: QSystemStruct) -> Sequential:
    return op


@register_compile_impl(FreezePass, Remapped)
def remapped_impl(ps: FreezePass, op: Remapped, *args: QSystemStruct) -> Remapped:
    return op
