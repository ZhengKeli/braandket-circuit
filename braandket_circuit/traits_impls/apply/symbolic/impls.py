from braandket_circuit.basics import QOperation, QSystemStruct
from braandket_circuit.operations import AllocateParticle, DesiredMeasurement, ProjectiveMeasurement
from braandket_circuit.traits import register_apply_impl
from .runtime import SymbolicCall, SymbolicMeasurementResult, SymbolicParticle, SymbolicRuntime


@register_apply_impl(SymbolicRuntime, None)
def common_impl(rt: SymbolicRuntime, op: QOperation, *args: QSystemStruct):
    call = SymbolicCall(op, *args)
    rt.record_call(call)


@register_apply_impl(SymbolicRuntime, AllocateParticle)
def allocate_particle_impl(rt: SymbolicRuntime, op: AllocateParticle):
    call = SymbolicCall(op)
    rt.record_call(call)
    return SymbolicParticle(call)


@register_apply_impl(SymbolicRuntime, ProjectiveMeasurement)
def projective_measurement_impl(rt: SymbolicRuntime, op: ProjectiveMeasurement, *args: QSystemStruct):
    call = SymbolicCall(op, *args)
    rt.record_call(call)
    return SymbolicMeasurementResult(call)


@register_apply_impl(SymbolicRuntime, DesiredMeasurement)
def projective_measurement_impl(rt: SymbolicRuntime, op: ProjectiveMeasurement, *args: QSystemStruct):
    call = SymbolicCall(op, *args)
    rt.record_call(call)
    return SymbolicMeasurementResult(call)
