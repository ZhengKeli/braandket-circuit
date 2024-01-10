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
    sub_ops_matrix = (convert(cv, sub_op) for sub_op in op)

    matrix = 1
    for sub_op_matrix in sub_ops_matrix:
        if isinstance(sub_op_matrix, int) and sub_op_matrix == 1:
            continue
        if isinstance(matrix, int) and matrix == 1:
            matrix = sub_op_matrix
            continue
        matrix = matrix @ sub_op_matrix
    return matrix
