import numpy as np

import braandket as bnk
from braandket import MixedStateTensor, OperatorTensor, PureStateTensor
from braandket_circuit.basics import QParticle, QSystemStruct
from braandket_circuit.operations import Controlled, DesiredMeasurement, GlobalPhaseGate, HadamardGate, HalfPiPhaseGate, \
    MeasurementResult, PauliXGate, PauliYGate, PauliZGate, ProjectiveMeasurement, PureStatePreparation, \
    QuarterPiPhaseGate, RotationXGate, RotationYGate, RotationZGate
from braandket_circuit.traits.apply.apply import register_apply_impl
from braandket_circuit.utils import iter_struct
from .runtime import BnkParticle, BnkRuntime, BnkState


@register_apply_impl(BnkRuntime, PauliXGate)
def x_gate_impl(rt: BnkRuntime, _: PauliXGate, qubit: BnkParticle):
    matrix = np.asarray([[0, 1], [1, 0]])
    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_apply_impl(BnkRuntime, PauliYGate)
def y_gate_impl(rt: BnkRuntime, _: PauliYGate, qubit: BnkParticle):
    matrix = np.asarray([[0, -1j], [+1j, 0]])
    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_apply_impl(BnkRuntime, PauliZGate)
def z_gate_impl(rt: BnkRuntime, _: PauliZGate, qubit: BnkParticle):
    matrix = np.asarray([[1, 0], [0, -1]])
    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_apply_impl(BnkRuntime, HalfPiPhaseGate)
def s_gate_impl(rt: BnkRuntime, _: HalfPiPhaseGate, qubit: BnkParticle):
    matrix = np.asarray([[1, 0], [0, 1j]])
    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_apply_impl(BnkRuntime, QuarterPiPhaseGate)
def t_gate_impl(rt: BnkRuntime, _: QuarterPiPhaseGate, qubit: BnkParticle):
    matrix = np.asarray([[1, 0], [0, np.exp(1j * np.pi / 4)]])
    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_apply_impl(BnkRuntime, HadamardGate)
def h_gate_impl(rt: BnkRuntime, _: HadamardGate, qubit: BnkParticle):
    matrix = np.asarray([[1, 1], [1, -1]]) / np.sqrt(2)
    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_apply_impl(BnkRuntime, GlobalPhaseGate)
def phase_gate_impl(rt: BnkRuntime, op: GlobalPhaseGate, qubit: BnkParticle):
    matrix = np.asarray([[np.exp(1j * op.theta), 0], [0, np.exp(1j * op.theta)]])
    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_apply_impl(BnkRuntime, RotationXGate)
def rx_gate_impl(rt: BnkRuntime, op: RotationXGate, qubit: BnkParticle):
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


@register_apply_impl(BnkRuntime, RotationYGate)
def ry_gate_impl(rt: BnkRuntime, op: RotationYGate, qubit: BnkParticle):
    backend = rt.backend
    theta = backend.convert(op.theta)
    half_theta = backend.div(theta, 2.0)
    cos_half_theta = backend.cos(half_theta)
    sin_half_theta = backend.sin(half_theta)

    cos_half_theta, sin_half_theta = backend.compact(cos_half_theta, sin_half_theta)
    matrix = backend.convert([[cos_half_theta, -sin_half_theta], [sin_half_theta, cos_half_theta]])

    operator = OperatorTensor.from_matrix(matrix, [qubit.space], backend=rt.backend)
    qubit.state.tensor = operator @ qubit.state.tensor


@register_apply_impl(BnkRuntime, RotationZGate)
def rz_gate_impl(rt: BnkRuntime, op: RotationZGate, qubit: BnkParticle):
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
    state = BnkState.prod(*(particle.state for particle in particles))
    spaces = tuple(particle.space for particle in particles)
    results, prob, state.tensor = state.tensor.measure(spaces)
    if len(args) == 1:
        args = args[0]
        results = results[0]
    return MeasurementResult(args, results, prob)


@register_apply_impl(BnkRuntime, DesiredMeasurement)
def desired_measurement_impl(_: BnkRuntime, op: DesiredMeasurement, *args: QSystemStruct) -> MeasurementResult:
    particles = tuple(particle for particle in iter_struct(args, atom_typ=BnkParticle))
    state = BnkState.prod(*(particle.state for particle in particles))
    spaces = tuple(particle.space for particle in particles)
    results = tuple(iter_struct(op.value))
    results, prob, state.tensor = state.tensor.measure(zip(spaces, results))
    if len(args) == 1:
        args = args[0]
        results = results[0]
    return MeasurementResult(args, results, prob)


@register_apply_impl(BnkRuntime, PureStatePreparation)
def pure_state_preparation_impl(rt: BnkRuntime, op: PureStatePreparation, *args: QSystemStruct):
    state_tensor_value = rt.backend.convert(op.state)

    particles = tuple(particle for particle in iter_struct(args, atom_typ=BnkParticle))
    state_spaces = tuple(particle.space for particle in particles)
    state_tensor_shape = tuple(space.n for space in state_spaces)
    state_tensor_value = rt.backend.reshape(state_tensor_value, state_tensor_shape)
    state_tensor = PureStateTensor.of(state_tensor_value, state_spaces, backend=rt.backend)

    state = BnkState.prod(*(particle.state for particle in particles))
    state.tensor = state_tensor
