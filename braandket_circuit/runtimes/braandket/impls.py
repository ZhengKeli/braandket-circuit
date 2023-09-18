import numpy as np

from braandket import OperatorTensor
from braandket_circuit.basics import QOperation
from braandket_circuit.operations import H, Rx, Ry, Rz, S, T, X, Y, Z
from braandket_circuit.traits import register_op_impl
from .runtime import BnkParticle, BnkRuntime


@register_op_impl(BnkRuntime, X)
def x_gate_impl(rt: BnkRuntime, _: QOperation, qubit: BnkParticle):
    matrix = np.asarray([[0, 1], [1, 0]])
    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_op_impl(BnkRuntime, Y)
def y_gate_impl(rt: BnkRuntime, _: QOperation, qubit: BnkParticle):
    matrix = np.asarray([[0, -1j], [+1j, 0]])
    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_op_impl(BnkRuntime, Z)
def z_gate_impl(rt: BnkRuntime, _: QOperation, qubit: BnkParticle):
    matrix = np.asarray([[1, 0], [0, -1]])
    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_op_impl(BnkRuntime, S)
def s_gate_impl(rt: BnkRuntime, _: QOperation, qubit: BnkParticle):
    matrix = np.asarray([[1, 0], [0, 1j]])
    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_op_impl(BnkRuntime, T)
def t_gate_impl(rt: BnkRuntime, _: QOperation, qubit: BnkParticle):
    matrix = np.asarray([[1, 0], [0, np.exp(1j * np.pi / 4)]])
    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_op_impl(BnkRuntime, H)
def h_gate_impl(rt: BnkRuntime, _: QOperation, qubit: BnkParticle):
    matrix = np.asarray([[1, 1], [1, -1]]) / np.sqrt(2)
    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_op_impl(BnkRuntime, Rx)
def rx_gate_impl(rt: BnkRuntime, op: Rx, qubit: BnkParticle):
    backend = rt.backend
    theta = backend.convert(op.theta)
    half_theta = backend.div(theta, 2.0)
    cos_half_theta = backend.cos(half_theta)
    sin_half_theta = backend.sin(half_theta)
    m1j_sin_half_theta = backend.mul(sin_half_theta, -1.0j)

    cos_half_theta, m1j_sin_half_theta = backend.compact(cos_half_theta, m1j_sin_half_theta)
    matrix = backend.convert([[cos_half_theta, m1j_sin_half_theta], [m1j_sin_half_theta, cos_half_theta]])

    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_op_impl(BnkRuntime, Ry)
def ry_gate_impl(rt: BnkRuntime, op: Ry, qubit: BnkParticle):
    backend = rt.backend
    theta = backend.convert(op.theta)
    half_theta = backend.div(theta, 2.0)
    cos_half_theta = backend.cos(half_theta)
    sin_half_theta = backend.sin(half_theta)

    cos_half_theta, sin_half_theta = backend.compact(cos_half_theta, sin_half_theta)
    matrix = backend.convert([[cos_half_theta, -sin_half_theta], [sin_half_theta, cos_half_theta]])

    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_op_impl(BnkRuntime, Rz)
def rz_gate_impl(rt: BnkRuntime, op: Rz, qubit: BnkParticle):
    backend = rt.backend
    theta = backend.convert(op.theta)
    half_theta = backend.div(theta, 2.0)
    p1j_half_theta = backend.mul(half_theta, 1.0j)
    exp_p1j_half_theta = backend.exp(p1j_half_theta)
    m1j_half_theta = -p1j_half_theta
    exp_m1j_half_theta = backend.exp(m1j_half_theta)

    exp_p1j_half_theta, exp_m1j_half_theta, zero \
        = backend.compact(exp_p1j_half_theta, exp_m1j_half_theta, 0)
    matrix = backend.convert([[exp_m1j_half_theta, zero], [zero, exp_p1j_half_theta]])

    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor
