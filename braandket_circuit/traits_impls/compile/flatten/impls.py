from braandket_circuit.basics import QOperation
from braandket_circuit.operations import Controlled, Remapped, RemappedByIndices, Sequential
from braandket_circuit.traits import compile, register_compile_impl
from braandket_circuit.traits_impls.compile.freeze import FreezePass
from braandket_circuit.utils import iter_struct
from .flatten_pass import FlattenPass


@register_compile_impl(FlattenPass, None)
def common_impl(ps: FlattenPass, op: QOperation):
    op = compile(FreezePass(ps.args), op)
    return compile(ps, op)


@register_compile_impl(FlattenPass, Sequential)
def sequential_impl(ps: FlattenPass, op: Sequential):
    flattened_steps = []
    for step in op:
        flattened_step = compile(ps, step)
        if isinstance(flattened_step, Sequential):
            flattened_steps.extend(flattened_step)
        else:
            flattened_steps.append(flattened_step)
    return Sequential(flattened_steps, name=op.name)


@register_compile_impl(FlattenPass, Remapped)
def remapped_impl(ps: FlattenPass, op: Remapped):
    flattened_op_op = compile(ps, op.op)
    if isinstance(flattened_op_op, Sequential):
        return Sequential([op.spawn(step) for step in flattened_op_op], name=op.name)
    else:
        return op


@register_compile_impl(FlattenPass, RemappedByIndices)
def remapped_by_indices_impl(ps: FlattenPass, op: RemappedByIndices):
    flattened_op_op = compile(ps, op.op)
    if isinstance(flattened_op_op, Sequential):
        return Sequential([compile(ps, op.spawn(step)) for step in flattened_op_op], name=op.name)
    elif isinstance(flattened_op_op, RemappedByIndices):
        op_indices = tuple(iter_struct(op.indices))
        op_op_indices = iter_struct(flattened_op_op.indices)
        merged_indices = tuple(op_indices[i] for i in op_op_indices)
        merged_op = RemappedByIndices(flattened_op_op.op, *merged_indices, name=op.name)
        return compile(ps, merged_op)
    else:
        return op


@register_compile_impl(FlattenPass, Controlled)
def controlled_impl(ps: FlattenPass, op: Controlled):
    flattened_op_op = compile(ps, op.op)
    if isinstance(flattened_op_op, Sequential):
        return Sequential([op.spawn(step) for step in flattened_op_op], name=op.name)
    else:
        return op
