import pytest

from braandket_circuit import QOperation, QParticle, allocate_qubit


class CustomGate(QOperation):
    def __call__(self, q: QParticle):
        return super().__call__(q)


def test_custom_gate_no_recursion():
    q = allocate_qubit()
    gate = CustomGate()
    with pytest.raises(NotImplementedError):
        gate(q)
