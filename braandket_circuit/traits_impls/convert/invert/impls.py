from typing import Iterable

from braandket_circuit.operations import Controlled, H, I, Phase, Remapped, Rx, Ry, Rz, Sequential, X, Y, Z
from braandket_circuit.traits import convert, register_convert_impl
from .invert import Invert


@register_convert_impl(Invert, I)
def identity_impl(_: Invert, __: I) -> I:
    return I


@register_convert_impl(Invert, X)
def x_gate_impl(_: Invert, __: X) -> X:
    return X


@register_convert_impl(Invert, Y)
def y_gate_impl(_: Invert, __: Y) -> Y:
    return Y


@register_convert_impl(Invert, Z)
def z_gate_impl(_: Invert, __: Z) -> Z:
    return Z


# TODO S,T

@register_convert_impl(Invert, H)
def h_gate_impl(_: Invert, __: H) -> H:
    return H


@register_convert_impl(Invert, Phase)
def phase_gate_impl(_: Invert, op: Phase) -> Phase:
    return Phase(theta=-op.theta)


@register_convert_impl(Invert, Rx)
def rx_gate_impl(_: Invert, op: Rx) -> Rx:
    return Rx(theta=-op.theta)


@register_convert_impl(Invert, Ry)
def ry_gate_impl(_: Invert, op: Ry) -> Ry:
    return Ry(theta=-op.theta)


@register_convert_impl(Invert, Rz)
def rz_gate_impl(_: Invert, op: Rz) -> Rz:
    return Rz(theta=-op.theta)


@register_convert_impl(Invert, Sequential)
def sequential_impl(cv: Invert, op: Sequential) -> Sequential:
    return Sequential(reversed([convert(cv, step) for step in op]))


@register_convert_impl(Invert, Controlled)
def controlled_impl(cv: Invert, op: Controlled) -> Controlled:
    if cv.args is None:
        return Controlled(convert(cv, op.op))
    else:
        c, t = cv.args
        t = (t,) if not isinstance(t, Iterable) else tuple(t)
        return Controlled(convert(Invert(t), op.op))


@register_convert_impl(Invert, Remapped)
def remapped_impl(cv: Invert, op: Remapped) -> Remapped:
    if cv.args is None:
        return Remapped(convert(cv, op.op), *op.indices)
    else:
        remapped_args = op.remap(*cv.args)
        return Remapped(convert(Invert(remapped_args), op.op), *op.indices)
