from helper.datetime.datetime_helper import DateTimeHelper


class WorkEmotion:
    def __init__(self, emotion: str = None, probability: float = None, aro_val: tuple = ()) -> None:
        self.__emotion: str = emotion
        self.__probability: float = probability
        self.__aro_val: tuple[float, float] = aro_val
        self.__recorded_on: str = DateTimeHelper.get_formatted_datetime()

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

    @property
    def recorded_on(self) -> str:
        return self.__recorded_on

    @recorded_on.setter
    def recorded_on(self, recorded_on: str) -> None:
        self.__recorded_on = recorded_on

    @staticmethod
    def generate_alias(field: str):
        if field == "aroVal":
            return "aro_val"
        if field == "recordedOn":
            return "recorded_on"
        return field

    def cast_from_dict(self, work_emotion_dict: dict) -> None:
        for key, value in work_emotion_dict.items():
            setattr(self, WorkEmotion.generate_alias(key), value)

    def cast_to_dict(self) -> dict:
        return {
            "emotion": self.emotion,
            "probability": self.probability,
            "aroVal": (float(self.aro_val[0]), float(self.aro_val[1])),
            "recordedOn": self.recorded_on
        }
