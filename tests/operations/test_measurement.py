import math

import tensorflow as tf

from braandket import tensorflow_backend
from braandket_circuit import BnkRuntime, CX, DM, H, M, Rx, X, allocate_qubit, allocate_qubits


def test_measure_0():
    qubit = allocate_qubit()
    result, prob = M(qubit)
    assert result == 0
    assert prob == 1.0


def test_measure_h():
    qubit = allocate_qubit()
    H(qubit)
    result, prob = M(qubit)
    assert abs(prob - 0.5) < 1e-6
    return result


def test_measure_h_statistics(n: int = 1000):
    def measure_h():
        qubit = allocate_qubit()
        H(qubit)
        result, prob = M(qubit)
        return result

    results = [measure_h() for _ in range(n)]
    result_mean = sum(results) / n
    assert abs(result_mean - 0.5) < 1e-1


def test_measure_rx():
    qubit = allocate_qubit()
    Rx(math.pi / 3)(qubit)
    result, prob = M(qubit)
    assert result == 0 or result == 1
    if result == 0:
        assert abs(prob - 3 / 4) < 1e-6
    elif result == 1:
        assert abs(prob - 1 / 4) < 1e-6
    return result


def test_measure_rx_statistics(n: int = 1000):
    def measure_rx():
        qubit = allocate_qubit()
        Rx(math.pi / 3)(qubit)
        result, prob = M(qubit)
        return result

    results = [measure_rx() for _ in range(n)]
    result_mean = sum(results) / n
    assert abs(result_mean - 1 / 4) < 1e-1


def test_desired_0_measure_0():
    qubit = allocate_qubit()
    result, prob = DM(0)(qubit)
    assert result == 0
    assert prob == 1.0


def test_desired_1_measure_0():
    qubit = allocate_qubit()
    result, prob = DM(1)(qubit)
    assert result == 1
    assert prob == 0.0


def test_desired_0_measure_h():
    qubit = allocate_qubit()
    H(qubit)
    result, prob = DM(0)(qubit)
    assert result == 0
    assert abs(prob - 0.5) < 1e-6
    return result


def test_desired_1_measure_h():
    qubit = allocate_qubit()
    H(qubit)
    result, prob = DM(1)(qubit)
    assert result == 1
    assert abs(prob - 0.5) < 1e-6
    return result


def test_measure_00():
    qubit0, qubit1 = allocate_qubits(2)
    result, prob = M(qubit0, qubit1)
    assert result[0] == 0
    assert result[1] == 0
    assert prob == 1.0


def test_measure_10():
    qubit0, qubit1 = allocate_qubits(2)
    X(qubit0)
    result, prob = M(qubit0, qubit1)
    assert result[0] == 1
    assert result[1] == 0
    assert prob == 1.0


def test_measure_01():
    qubit0, qubit1 = allocate_qubits(2)
    X(qubit1)
    result, prob = M(qubit0, qubit1)
    assert result[0] == 0
    assert result[1] == 1
    assert prob == 1.0


def test_measure_bell_state():
    qubit0, qubit1 = allocate_qubits(2)
    H(qubit0)
    CX(qubit0, qubit1)
    result, prob = M(qubit0, qubit1)
    assert result[0] == result[1]
    assert abs(prob - 0.5) < 1e-6


def test_measure_000():
    qubit0, qubit1, qubit2 = allocate_qubits(3)
    result, prob = M(qubit0, qubit1, qubit2)
    assert result[0] == 0
    assert result[1] == 0
    assert result[2] == 0
    assert prob == 1.0


def test_measure_twice_with_tf_function():
    @tf.function
    def circuit():
        qubit = allocate_qubit()
        H(qubit)
        result1, prob1 = M(qubit)
        result2, prob2 = M(qubit)
        return result1, prob1, result2, prob2

    with BnkRuntime(tensorflow_backend):
        result1, prob1, result2, prob2 = circuit()
        assert result1 == result2
        assert abs(prob1 - 0.5) < 1e-6
        assert abs(prob2 - 1.0) < 1e-6


def test_measure_then_desired_with_tf_function():
    @tf.function
    def circuit():
        qubit = allocate_qubit()
        H(qubit)
        result1, prob1 = M(qubit)
        result2, prob2 = DM(result1)(qubit)
        return result1, prob1, result2, prob2

    with BnkRuntime(tensorflow_backend):
        result1, prob1, result2, prob2 = circuit()
        assert result1 == result2
        assert abs(prob1 - 0.5) < 1e-6
        assert abs(prob2 - 1.0) < 1e-6
