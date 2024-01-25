from braandket_circuit import CNOT, Controlled, H, Remapped, Rx, Sequential, X, convert
from braandket_circuit.traits_impls.convert.invert import Invert


def test_invert_sequential():
    sequential = Sequential([
        H.on(0),
        CNOT.on(0, 1),
        Rx(theta=0.5).on(0),
        X.on(1),
    ])

    inverted = convert(Invert(), sequential)
    print(inverted)

    assert isinstance(inverted, Sequential)
    assert len(inverted) == 4

    assert isinstance(inverted[0], Remapped)
    assert inverted[0].indices == (1,)
    assert inverted[0].op is X

    assert isinstance(inverted[1], Remapped)
    assert inverted[1].indices == (0,)
    assert isinstance(inverted[1].op, Rx)
    assert inverted[1].op.theta == -0.5

    assert isinstance(inverted[2], Remapped)
    assert inverted[2].indices == (0, 1)
    assert isinstance(inverted[2].op, Controlled)
    assert inverted[2].op.op is X

    assert isinstance(inverted[3], Remapped)
    assert inverted[3].indices == (0,)
    assert inverted[3].op is H
