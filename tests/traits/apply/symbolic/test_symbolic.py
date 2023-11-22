from braandket_circuit import AllocateParticle, CNOT, H, M, SymbolicRuntime, allocate_qubits


def test_symbolic_runtime():
    with SymbolicRuntime() as rt:
        q0, q1 = allocate_qubits(2, name="q")
        H(q0)
        CNOT(q0, q1)
        M(q0)
    assert len(rt.recorded_calls) == 5
    assert isinstance(rt.recorded_calls[0].op, AllocateParticle)
    assert isinstance(rt.recorded_calls[1].op, AllocateParticle)
    assert rt.recorded_calls[2].op is H
    assert rt.recorded_calls[3].op is CNOT
    assert rt.recorded_calls[4].op is M
