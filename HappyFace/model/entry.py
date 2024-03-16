from datetime import datetime

from helper.datetime.datetime_helper import DateTimeHelper
from model.work_emotion import WorkEmotion


class Entry:
    def __init__(self, repo_id: str, work_emotion: WorkEmotion):
        self.__repo_id: str = repo_id
        self.__created_on: str = DateTimeHelper.get_formatted_datetime()
        self.__work_emotion: WorkEmotion = work_emotion

    @property
    def repo_id(self) -> str:
        return self.__repo_id

    @repo_id.setter
    def repo_id(self, repo_id: str) -> None:
        self.__repo_id = repo_id

    @property
    def created_on(self) -> str:
        return self.__created_on

    @created_on.setter
    def created_on(self, created_on: datetime) -> None:
        created_on = DateTimeHelper.get_formatted_datetime(created_on)
        self.__created_on = created_on

    @property
    def work_emotion(self) -> WorkEmotion:
        return self.__work_emotion

    @work_emotion.setter
    def work_emotion(self, work_emotion: WorkEmotion) -> None:
        self.__work_emotion = work_emotion
