import inspect

from braandket_circuit.basics import QOperation, QSystemStruct
from braandket_circuit.operations import Sequential
from braandket_circuit.traits import freeze, match_apply_impls, register_freeze_impl


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
    return [SymbolicParticle(2, name=arg_name) for arg_name in spec.args[1:]]


@register_freeze_impl(QOperation)
def common_impl(op: QOperation, *args: QSystemStruct) -> QOperation:
    if len(args) == 0:
        try:
            args = args_from_signature(op)
        except (AttributeError, TypeError):
            pass

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
        call_op = freeze(call.op, *call.args)
        args_index = [args.index(arg) for arg in call.args]
        steps.append(call_op.on(*args_index))
    return Sequential(steps, name=op.name)


@register_freeze_impl(Sequential)
def sequential_impl(op: Sequential, *args: QSystemStruct) -> Sequential:
    return op
