from contextlib import contextmanager
from contextvars import ContextVar
from typing import Optional

from braandket_circuit.basics import QOperation, QSystemStruct, R
from braandket_circuit.traits import QRuntime, register_apply_impl

_default_impl_context_var = ContextVar[tuple]('default_impl_stack', default=None)


@contextmanager
def default_impl_context_manager(op: QOperation, *args: QSystemStruct):
    token = _default_impl_context_var.set((op, *args))
    try:
        yield
    finally:
        _default_impl_context_var.reset(token)


def get_default_impl_context() -> Optional[tuple]:
    return _default_impl_context_var.get()


@register_apply_impl(None, None)
def default_impl(_: QRuntime, op: QOperation, *args: QSystemStruct) -> R:
    custom_call = getattr(op, "_custom_call", None)
    if custom_call is None:
        raise NotImplementedError
    if get_default_impl_context() == (op, *args):
        raise NotImplementedError
    with default_impl_context_manager(op, *args):
        return custom_call(*args)
