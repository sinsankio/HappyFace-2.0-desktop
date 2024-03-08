from datetime import datetime

from helper.datetime.datetime_helper import DateTimeHelper
from model.work_emotion import WorkEmotion


class EntryWorkEmotion:
    def __init__(self):
        self.__repo_id = None
        self.__emotion = None
        self.__emotion_prob = None
        self.__recorded_on = None

    @property
    def repo_id(self) -> str:
        return self.__repo_id

    @repo_id.setter
    def repo_id(self, repo_id: str) -> None:
        self.__repo_id = repo_id

    @property
    def emotion(self) -> WorkEmotion:
        return self.__emotion

    @emotion.setter
    def emotion(self, emotion: WorkEmotion) -> None:
        self.__emotion = emotion

    @property
    def emotion_prob(self) -> float:
        return self.__emotion_prob

    @emotion_prob.setter
    def emotion_prob(self, emotion_prob: float) -> None:
        self.__emotion_prob = emotion_prob

    @property
    def recorded_on(self) -> datetime:
        return self.__recorded_on

    @recorded_on.setter
    def recorded_on(self, recorded_on: datetime) -> None:
        recorded_on = DateTimeHelper.get_formatted_datetime(recorded_on, dt_format="%Y-%m-%dT%H:%M:%S.%f")
        self.__recorded_on = recorded_on

    def to_entry_work_emotion(self, entry_work_emotion_result: tuple):
        self.repo_id = entry_work_emotion_result[0].decode()
        self.emotion = entry_work_emotion_result[1]
        self.emotion_prob = entry_work_emotion_result[2]
        self.recorded_on = entry_work_emotion_result[3]
