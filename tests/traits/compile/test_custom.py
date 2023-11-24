from braandket_circuit import CompilePass, QOperation, Sequential, compile, register_compile_impl


class GateA(QOperation):
    pass


class GateB(QOperation):
    pass


class GateC(QOperation):
    pass


class GateAToGateB(CompilePass):
    pass


@register_compile_impl(GateAToGateB, GateA)
def a_to_b(op: GateA, pr: object):
    return GateB()


def test_custom_compile_pass():
    circuit1 = Sequential(GateA(), GateB(), GateA(), GateC())
    circuit2 = compile(GateAToGateB(), circuit1)

    assert isinstance(circuit2, Sequential)
    assert isinstance(circuit2[0], GateB)
    assert isinstance(circuit2[1], GateB)
    assert isinstance(circuit2[2], GateB)
    assert isinstance(circuit2[3], GateC)
