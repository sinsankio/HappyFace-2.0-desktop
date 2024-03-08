from datetime import datetime

from helper.datetime.datetime_helper import DateTimeHelper
from model.entry_work_emotion import EntryWorkEmotion


class Entry:
    def __init__(self):
        self.__repo_id = None
        self.__created_on = None
        self.__work_emotions = []

    @property
    def repo_id(self) -> str:
        return self.__repo_id

    @repo_id.setter
    def repo_id(self, repo_id: str) -> None:
        self.__repo_id = repo_id

    @property
    def created_on(self) -> datetime:
        return self.__created_on

    @created_on.setter
    def created_on(self, created_on: datetime) -> None:
        created_on = DateTimeHelper.get_formatted_datetime(created_on)
        self.__created_on = created_on

    @property
    def work_emotions(self) -> list[EntryWorkEmotion]:
        return self.__work_emotions

    @work_emotions.setter
    def work_emotions(self, work_emotions: list[EntryWorkEmotion]) -> None:
        self.__work_emotions = work_emotions

    def to_entry(self, entry_result: tuple) -> None:
        self.repo_id = entry_result[0]
        self.created_on = entry_result[1]

    def generate_entry(self, repo_id: str, best_face_emotion_record: dict) -> "Entry":
        entry = Entry()

        entry.repo_id = repo_id
        emotion, probability = best_face_emotion_record["emotion"], best_face_emotion_record["probability"]

        entry_work_emotion = EntryWorkEmotion()
        entry_work_emotion.repo_id = repo_id
        entry_work_emotion.emotion = emotion
        entry_work_emotion.emotion_prob = probability

        entry.work_emotions.append(entry_work_emotion)
        return entry
