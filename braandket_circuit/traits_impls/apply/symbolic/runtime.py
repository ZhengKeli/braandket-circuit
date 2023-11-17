import importlib
from typing import Optional

from braandket_circuit.basics import QOperation, QParticle, QSystemStruct
from braandket_circuit.operations import AllocateParticle, MeasurementResult
from braandket_circuit.traits import QRuntime


class SymbolicCall:
    def __init__(self, op: QOperation, *args: QSystemStruct):
        self._op = op
        self._args = args

    @property
    def op(self) -> QOperation:
        return self._op

    @property
    def args(self) -> tuple[QSystemStruct, ...]:
        return self._args


class SymbolicRuntime(QRuntime):
    def __init__(self):
        self._calls = []

    def record_call(self, call: SymbolicCall):
        self._calls.append(call)

    @property
    def recorded_calls(self) -> tuple[SymbolicCall, ...]:
        return tuple(self._calls)


class SymbolicParticle(QParticle):
    def __init__(self, call: SymbolicCall):
        self._call = call

    @property
    def call(self):
        return self._call

    @property
    def name(self) -> Optional[str]:
        op = self.call.op
        assert isinstance(op, AllocateParticle)
        return op.name

    @property
    def ndim(self) -> int:
        op = self.call.op
        assert isinstance(op, AllocateParticle)
        return op.ndim


class SymbolicMeasurementResult(MeasurementResult):
    class SymbolicValue:
        pass

    class SymbolicProb:
        pass

    def __init__(self, call: SymbolicCall):
        value = SymbolicMeasurementResult.SymbolicValue()
        prob = SymbolicMeasurementResult.SymbolicProb()
        super().__init__(call.args, value, prob)
        self._call = call

    @property
    def call(self) -> SymbolicCall:
        return self._call


importlib.import_module(".impls", __package__)
