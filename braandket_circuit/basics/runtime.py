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
        from braandket_circuit.traits import get_op_impls
        impls = get_op_impls(type(self), type(op))
        for impl in reversed(impls):
            try:
                return impl(self, op, *args)
            except NotImplementedError:
                pass
        raise NotImplementedError

    def __enter__(self):
        token = _default_runtime.set(self)
        setattr(self, '_org_default_runtime_token_', token)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        token = getattr(self, '_org_default_runtime_token_')
        _default_runtime.reset(token)


_default_runtime = ContextVar[Optional[QRuntime]]('default_runtime', default=None)


def get_default_runtime() -> QRuntime:
    runtime = _default_runtime.get()
    if runtime is None:
        raise NotImplementedError  # TODO init default runtime
    return runtime
