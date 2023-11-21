from braandket_circuit import CNOT, DM, H, Sequential, allocate_qubits


def test_sequential_bell_pair():
    circuit = Sequential([
        H.on(0),
        CNOT.on(0, 1),
    ])

    q0, q1 = allocate_qubits(2)
    circuit(q0, q1)
    result, prob = DM([0, 0])(q0, q1)
    assert abs(prob - 0.5) < 1e-6


def test_sequential_bell_pair_measure():
    circuit = Sequential([
        H.on(0),
        CNOT.on(0, 1),
        DM(0).on(0, 1),
    ])

    q0, q1 = allocate_qubits(2)
    result, prob = circuit(q0, q1)[-1]
    assert abs(prob - 0.5) < 1e-6
