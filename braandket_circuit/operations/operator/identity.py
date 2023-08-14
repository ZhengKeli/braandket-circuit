import numpy as np

import braandket as bnk
from braandket import BackendValue, OperatorTensor
from braandket_circuit.system import QComposed, QSystem
from .matrix import MatrixOperation


class _IdentityOperation(MatrixOperation):
    """ Operation that does nothing """

    def make_matrix(self, *systems: QSystem) -> BackendValue:
        system = QComposed(*systems)
        N = int(np.prod([space.n for space in system.spaces]))
        return system.backend.eye(N)

    def make_operator_tensor(self, *systems: QSystem) -> OperatorTensor:
        system = QComposed(*systems)
        spaces_identity = [space.identity(backend=system.backend) for space in system.spaces]
        return OperatorTensor.of(bnk.prod(*spaces_identity, backend=system.backend))

    def __call__(self, *args: QSystem, **kwargs: QSystem):
        pass


Identity = _IdentityOperation()
