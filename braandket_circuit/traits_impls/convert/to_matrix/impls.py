from braandket import ArrayLike

from braandket_circuit.operations import MatrixOperation, Sequential
from braandket_circuit.traits import convert, register_convert_impl
from .to_matrix import ToMatrix


@register_convert_impl(ToMatrix, MatrixOperation)
def matrix_operation_matrix_impl(_: ToMatrix, op: MatrixOperation) -> ArrayLike:
    # TODO check args match
    return op.matrix


@register_convert_impl(ToMatrix, Sequential)
def sequential_matrix_impl(cv: ToMatrix, op: Sequential) -> ArrayLike:
    matrix = 1
    for sub_op in op:
        matrix = matrix @ convert(cv, sub_op)
    return matrix
