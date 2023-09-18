import abc
from contextvars import ContextVar
from typing import Optional

from .operation import QOperation, R
from .system import QSystem, QSystemStruct


class QRuntime(abc.ABC):
    @abc.abstractmethod
    def allocate(self, n: int, name: str | None = None) -> QSystem:
        pass

    def operate(self, op: QOperation[R], *args: QSystemStruct) -> R:
        from braandket_circuit.traits import apply
        return apply(self, op, *args)

    def __enter__(self):
        token = _runtime_context_var.set(self)
        setattr(self, '_org_default_runtime_token_', token)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        token = getattr(self, '_org_default_runtime_token_')
        _runtime_context_var.reset(token)


_runtime_context_var = ContextVar[Optional[QRuntime]]('runtime', default=None)


def get_runtime() -> QRuntime:
    runtime = _runtime_context_var.get()
    if runtime is None:
        from braandket_circuit.runtimes import make_default_runtime
        runtime = make_default_runtime()
        _runtime_context_var.set(runtime)
    return runtime
