import numpy as np

from braandket import tensorflow_backend
from braandket_circuit import BnkRuntime, DM, M, PureStatePreparation, allocate_qubit


def test_prepare_0():
    qubit = allocate_qubit()
    state_value = np.asarray([1, 0], dtype=np.float32)
    PureStatePreparation(state_value)(qubit)
    result, prob = M(qubit)
    assert result == 0
    assert abs(prob - 1) < 1e-6


def test_prepare_h():
    qubit = allocate_qubit()
    state_value = np.asarray([1, 1], dtype=np.float32) / np.sqrt(2)
    PureStatePreparation(state_value)(qubit)
    result, prob = DM(0)(qubit)
    assert abs(prob - 0.5) < 1e-6


def test_prepare_h_complex():
    qubit = allocate_qubit()
    state_value = np.asarray([1, 1j]) / np.sqrt(2)
    PureStatePreparation(state_value)(qubit)
    result, prob = DM(0)(qubit)
    assert abs(prob - 0.5) < 1e-6


def test_prepare_rx_statistics(n: int = 1000):
    def circuit():
        qubit = allocate_qubit()
        state_value = np.sqrt(np.asarray([1 / 3, 2 / 3], dtype=np.float32))
        PureStatePreparation(state_value)(qubit)
        result, prob = M(qubit)
        return result

    results = [circuit() for _ in range(n)]
    result_mean = sum(results) / n
    assert abs(result_mean - 2 / 3) < 1e-1


def test_prepare_0_tensorflow():
    with BnkRuntime(backend=tensorflow_backend):
        test_prepare_0()
