import abc
from contextvars import ContextVar
from typing import Optional

from braandket_circuit.basics import QOperation, QSystemStruct, R


class QRuntime(abc.ABC):
    def apply_operation(self, op: QOperation[R], *args: QSystemStruct) -> R:
        from braandket_circuit.traits import apply
        return apply(self, op, *args)

    def __enter__(self):
        token = _current_runtime_context_var.set(self)
        setattr(self, '_org_default_runtime_token_', token)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        token = getattr(self, '_org_default_runtime_token_')
        _current_runtime_context_var.reset(token)


# current runtime context

_current_runtime_context_var = ContextVar[Optional[QRuntime]]('runtime', default=None)


def _default_runtime() -> QRuntime:
    from braandket_circuit import BnkRuntime
    return BnkRuntime()


def get_current_runtime() -> QRuntime:
    runtime = _current_runtime_context_var.get()
    if runtime is None:
        runtime = _default_runtime()
        _current_runtime_context_var.set(runtime)
    return runtime


def set_current_runtime(runtime: QRuntime):
    _current_runtime_context_var.set(runtime)
