import itertools

import numpy as np

import braandket as bnk
from braandket import MixedStateTensor, OperatorTensor, PureStateTensor
from braandket_circuit.basics import QOperation, QParticle, QSystemStruct
from braandket_circuit.operations import Controlled, H, MeasurementResult, ProjectiveMeasurement, Rx, Ry, Rz, S, T, X, \
    Y, Z
from braandket_circuit.traits import register_apply_impl
from braandket_circuit.utils.struct import iter_struct
from .runtime import BnkParticle, BnkRuntime, BnkState


@register_apply_impl(BnkRuntime, X)
def x_gate_impl(rt: BnkRuntime, _: QOperation, qubit: BnkParticle):
    matrix = np.asarray([[0, 1], [1, 0]])
    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_apply_impl(BnkRuntime, Y)
def y_gate_impl(rt: BnkRuntime, _: QOperation, qubit: BnkParticle):
    matrix = np.asarray([[0, -1j], [+1j, 0]])
    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_apply_impl(BnkRuntime, Z)
def z_gate_impl(rt: BnkRuntime, _: QOperation, qubit: BnkParticle):
    matrix = np.asarray([[1, 0], [0, -1]])
    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_apply_impl(BnkRuntime, S)
def s_gate_impl(rt: BnkRuntime, _: QOperation, qubit: BnkParticle):
    matrix = np.asarray([[1, 0], [0, 1j]])
    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_apply_impl(BnkRuntime, T)
def t_gate_impl(rt: BnkRuntime, _: QOperation, qubit: BnkParticle):
    matrix = np.asarray([[1, 0], [0, np.exp(1j * np.pi / 4)]])
    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_apply_impl(BnkRuntime, H)
def h_gate_impl(rt: BnkRuntime, _: QOperation, qubit: BnkParticle):
    matrix = np.asarray([[1, 1], [1, -1]]) / np.sqrt(2)
    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_apply_impl(BnkRuntime, Rx)
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


@register_apply_impl(BnkRuntime, Ry)
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


@register_apply_impl(BnkRuntime, Rz)
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


@register_apply_impl(BnkRuntime, Controlled)
def controlled_impl(_: BnkRuntime, op: Controlled, control: QSystemStruct, target: QSystemStruct):
    control_spaces = set(particle.space for particle in iter_struct(control, atom_typ=BnkParticle))
    control_identity = bnk.prod(*(sp.identity() for sp in control_spaces))
    control_projector_on = bnk.prod(*(sp.projector(1) for sp in control_spaces))
    control_projector_off = control_identity - control_projector_on

    total_state = BnkState.prod(
        *(particle.state for particle in iter_struct(control, atom_typ=BnkParticle)),
        *(particle.state for particle in iter_struct(target, atom_typ=BnkParticle)))
    total_state_off = total_state.tensor

    if isinstance(target, QParticle):
        op.op(target)
    else:
        op.op(*target)
    total_state_on = total_state.tensor

    if isinstance(total_state_off, PureStateTensor) and isinstance(total_state_on, PureStateTensor):
        total_state.tensor = PureStateTensor.of(bnk.sum(
            control_projector_on @ total_state_on,
            control_projector_off @ total_state_off))
    else:
        total_state_on = MixedStateTensor.of(total_state_on)
        total_state_off = MixedStateTensor.of(total_state_off)
        total_state.tensor = MixedStateTensor.of(bnk.sum(
            control_projector_on @ total_state_on @ control_projector_on,
            control_projector_off @ total_state_off @ control_projector_off))


@register_apply_impl(BnkRuntime, ProjectiveMeasurement)
def projective_measurement_impl(_: BnkRuntime, __: ProjectiveMeasurement, *args: QSystemStruct) -> MeasurementResult:
    particles = tuple(particle for particle in iter_struct(args, atom_typ=BnkParticle))
    spaces = tuple(particle.space for particle in particles)
    state = BnkState.prod(*(particle.state for particle in particles))
    state_tensor = state.tensor
    backend = state_tensor.backend

    cases_value = tuple(itertools.product(*(range(space.n) for space in spaces)))
    cases_component = tuple(state_tensor.component(zip(spaces, case_values)) for case_values in cases_value)
    cases_prob = tuple(component.norm().values() for component in cases_component)
    cases_component = tuple(component.normalize() for component in cases_component)

    choice = backend.choose(cases_prob)
    value = cases_value[choice]
    prob = backend.take(cases_prob, choice)
    component = backend.take(cases_component, choice)

    ket_tensor = PureStateTensor.of(bnk.prod(*(
        space.eigenstate(value, backend=backend)
        for space, value in zip(spaces, value))))
    if isinstance(state_tensor, PureStateTensor):
        state_tensor = PureStateTensor.of(ket_tensor @ component)
    elif isinstance(state_tensor, MixedStateTensor):
        state_tensor = MixedStateTensor.of((ket_tensor @ ket_tensor.ct) @ component)
    else:
        raise TypeError(f"Unexpected type of state tensor: {type(state_tensor)}")
    state.tensor = state_tensor

    return MeasurementResult(args, value, prob)
