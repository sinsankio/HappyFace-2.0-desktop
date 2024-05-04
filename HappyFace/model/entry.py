from helper.datetime.datetime_helper import DateTimeHelper
from model.work_emotion import WorkEmotion


class Entry:
    def __init__(self, repo_id: str = None, work_emotions: list[WorkEmotion] = []):
        self.__repo_id: str = repo_id
        self.__created_on: str = DateTimeHelper.get_formatted_datetime()
        self.__work_emotions: list[WorkEmotion] = work_emotions

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
    def created_on(self, created_on: str) -> None:
        self.__created_on = created_on

    @property
    def work_emotions(self) -> list[WorkEmotion]:
        return self.__work_emotions

    @work_emotions.setter
    def work_emotions(self, work_emotions: list[WorkEmotion]) -> None:
        self.__work_emotions = work_emotions

    @staticmethod
    def generate_alias(field: str):
        if field == "faceSnapDirURI":
            return "repo_id"
        if field == "createdOn":
            return "created_on"
        if field == "workEmotions":
            return "work_emotions"
        return field

    def cast_from_dict(self, entry_dict: dict) -> None:
        work_emotions: list[WorkEmotion] = []

        for key, value in entry_dict.items():
            if key == "workEmotions":
                for we in value:
                    if isinstance(we, WorkEmotion):
                        work_emotions.append(we)
                    else:
                        work_emotion = WorkEmotion(
                            emotion=we["expression"],
                            probability=we["accuracy"],
                            aro_val=(we["arousal"], we["valence"]),
                            recorded_on=we["recordedOn"]
                        )
                        work_emotion.cast_from_dict(we)
                        work_emotions.append(work_emotion)
                value = work_emotions
            setattr(self, Entry.generate_alias(key), value)

    def cast_to_dict(self) -> dict:
        work_emotions = [work_emotion.cast_to_dict() if isinstance(work_emotion, WorkEmotion) else work_emotion for
                         work_emotion
                         in self.work_emotions]
        return {
            "faceSnapDirURI": self.repo_id,
            "createdOn": self.created_on,
            "workEmotions": work_emotions
        }
