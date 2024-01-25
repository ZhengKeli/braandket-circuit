from braandket_circuit.operations import Controlled, Remapped, Sequential
from braandket_circuit.traits import CompilePass, compile, register_compile_impl


@register_compile_impl(None, None)
def default_compile_impl(_: CompilePass, op: Sequential):
    return op


@register_compile_impl(None, Sequential)
def sequential_compile_impl(ps: CompilePass, op: Sequential):
    return Sequential([compile(ps, step) for step in op], name=op.name)


@register_compile_impl(None, Controlled)
def controlled_compile_impl(ps: CompilePass, op: Controlled):
    return Controlled(compile(ps, op.op), name=op.name)


@register_compile_impl(None, Remapped)
def remapped_compile_impl(ps: CompilePass, op: Remapped):
    return Remapped(compile(ps, op.op), *op.indices, name=op.name)
