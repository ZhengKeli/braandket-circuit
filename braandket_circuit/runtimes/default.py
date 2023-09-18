from braandket_circuit.basics import QRuntime
from braandket_circuit.runtimes import BnkRuntime


def make_default_runtime() -> QRuntime:
    return BnkRuntime()
