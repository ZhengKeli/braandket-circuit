from braandket_circuit import CNOT, FlattenPass, RemappedByIndices, Sequential, X, Y, compile


def test_flatten_elementary_gate():
    flattened = compile(FlattenPass(), X)
    assert flattened is X


def test_flatten_sequential():
    circuit = Sequential(X, Y)
    flattened = compile(FlattenPass(), circuit)
    assert isinstance(flattened, Sequential)
    assert len(flattened) == 2
    assert flattened[0] is X
    assert flattened[1] is Y


def test_flatten_sequential_remapped():
    circuit = Sequential(X.on(0), Y.on(1))
    flattened = compile(FlattenPass(), circuit)
    assert isinstance(flattened, Sequential)
    assert len(flattened) == 2
    assert isinstance(flattened[0], RemappedByIndices)
    assert flattened[0].indices == (0,)
    assert flattened[0].op is X
    assert isinstance(flattened[1], RemappedByIndices)
    assert flattened[1].indices == (1,)
    assert flattened[1].op is Y


def test_flatten_nested_sequential():
    circuit = Sequential(
        Sequential(
            X.on(0),
            X.on(1)
        ),
        X.on(2),
        Sequential(
            X.on(3),
            X.on(4)
        ),
    )
    flattened = compile(FlattenPass(), circuit)
    assert isinstance(flattened, Sequential)
    assert len(flattened) == 5
    for step_i, step in enumerate(flattened):
        assert isinstance(step, RemappedByIndices)
        assert step.indices == (step_i,)
        assert step.op is X


def test_flatten_nested_remapped():
    circuit = CNOT.on(0, 1).on(2, 1, 0)
    flattened = compile(FlattenPass(), circuit)
    assert isinstance(flattened, RemappedByIndices)
    assert flattened.indices == (2, 1)
    assert flattened.op is CNOT
