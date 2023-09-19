from .controlled import Controlled
from .gates import HadamardGate, HalfPiPhaseGate, PauliXGate, PauliYGate, PauliZGate, QuarterPiPhaseGate, RotationXGate, \
    RotationYGate, RotationZGate
from .identity import Identity
from .measurement import DesiredMeasurement, ProjectiveMeasurement

I = Identity()

# single qubit constant gates

XGate = PauliXGate
YGate = PauliYGate
ZGate = PauliZGate
SGate = HalfPiPhaseGate
TGate = QuarterPiPhaseGate
HGate = HadamardGate
NOTGate = PauliXGate

X = PauliXGate()
Y = PauliYGate()
Z = PauliZGate()
S = HalfPiPhaseGate()
T = QuarterPiPhaseGate()
H = HadamardGate()
NOT = X

# single qubit rotation gates

Rx = RotationXGate
Ry = RotationYGate
Rz = RotationZGate

# controlled gates

C = Controlled
CX = C(X)
CY = C(Y)
CZ = C(Z)
CNOT = CX

# measurements

Measure = ProjectiveMeasurement
DesiredMeasure = DesiredMeasurement

M = ProjectiveMeasurement()
DM = DesiredMeasurement
