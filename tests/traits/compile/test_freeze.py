from braandket_circuit import CNOT, Controlled, FreezePass, H, QOperation, QParticle, RemappedByIndices, Sequential, X, \
    apply, compile


class CustomGate(QOperation[None]):
    def __call__(self, q0: QParticle, q1: QParticle):
        H(q0)
        CNOT(q0, q1)


def test_freeze_custom_gate():
    print(apply)
    gate = CustomGate()
    frozen = compile(FreezePass(), gate)
    assert isinstance(frozen, Sequential)
    assert len(frozen) == 2
    assert isinstance(frozen[0], RemappedByIndices)
    assert frozen[0].op is H
    assert isinstance(frozen[1], RemappedByIndices)
    assert isinstance(frozen[1].op, Controlled)
    assert frozen[1].op.op is X
