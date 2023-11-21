from braandket_circuit.basics import QOperation, QSystemStruct, R
from braandket_circuit.traits import QRuntime, register_apply_impl


@register_apply_impl(None, None)
def default_impl(_: QRuntime, op: QOperation, *args: QSystemStruct) -> R:
    custom_call = getattr(op, "_custom_call", None)
    if custom_call is None:
        raise NotImplementedError
    return custom_call(*args)
