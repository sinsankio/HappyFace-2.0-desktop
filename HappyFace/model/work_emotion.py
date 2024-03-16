class WorkEmotion:
    def __init__(self, emotion: str, probability: float, aro_val: tuple) -> None:
        self.__emotion: str = emotion
        self.__probability: float = probability
        self.__aro_val: tuple[float, float] = aro_val

    @property
    def emotion(self) -> str:
        return self.__emotion

    @emotion.setter
    def emotion(self, emotion: str) -> None:
        self.__emotion = emotion

    @property
    def probability(self) -> float:
        return self.__probability

    @probability.setter
    def probability(self, probability: float) -> None:
        self.__probability = probability

    @property
    def aro_val(self) -> tuple[float, float]:
        return self.__aro_val

    @aro_val.setter
    def aro_val(self, aro_val: tuple) -> None:
        self.__aro_val = aro_val
