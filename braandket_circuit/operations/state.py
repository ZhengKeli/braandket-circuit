from braandket import ArrayLike
from braandket_circuit import QOperation


class PureStatePreparation(QOperation[None]):
    def __init__(self, state: ArrayLike):
        super().__init__()
        self._state = state

    @property
    def state(self) -> ArrayLike:
        return self._state
