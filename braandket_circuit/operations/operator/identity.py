import numpy as np

import braandket as bnk
from braandket import BackendValue, OperatorTensor
from braandket_circuit.basics import QSystem, QSystemStruct
from .matrix import MatrixOperation


class _IdentityOperation(MatrixOperation):
    """ Operation that does nothing """

    def make_matrix(self, *args: QSystemStruct) -> BackendValue:
        system = QSystem.of(args)
        N = int(np.prod([space.n for space in system.spaces]))
        return system.backend.eye(N)

    def make_operator_tensor(self, *args: QSystemStruct) -> OperatorTensor:
        system = QSystem.of(args)
        spaces_identity = [space.identity(backend=system.backend) for space in system.spaces]
        return OperatorTensor.of(bnk.prod(*spaces_identity, backend=system.backend))

    def __call__(self, *args: QSystemStruct):
        pass


Identity = _IdentityOperation()
