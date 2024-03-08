from helper.database.mysql.db_helper import DbHelper
from helper.database.mysql.query import Query
from helper.log.default.log_helper import LogHelper
from model.entry import Entry
from model.entry_work_emotion import EntryWorkEmotion
from model.work_emotion import WorkEmotion


class EntryService:
    def __init__(self, db_helper: DbHelper, log_helper: LogHelper):
        self.__db_helper = db_helper
        self.__log_helper = log_helper

    @property
    def db_helper(self) -> DbHelper:
        return self.__db_helper

    @db_helper.setter
    def db_helper(self, db_helper: DbHelper) -> None:
        self.__db_helper = db_helper

    @property
    def log_helper(self) -> LogHelper:
        return self.__log_helper

    @log_helper.setter
    def log_helper(self, log_helper: LogHelper) -> None:
        self.__log_helper = log_helper

    def insert_entry(self, entry: Entry) -> bool:
        query_params = entry.repo_id,
        affected_rows = self.db_helper.insert(Query.ENTRY_INSERT.value, query_params, self.log_helper)
        return affected_rows > 0

    def insert_entry_work_emotions(self, entry: Entry):
        affected_rows = 0

        for entry_work_emotion in entry.work_emotions:
            query_params = (
                entry_work_emotion.repo_id,
                entry_work_emotion.emotion,
                str(entry_work_emotion.emotion_prob)
            )
            affected_rows += self.db_helper.insert(Query.ENTRY_WORK_EMOTION_INSERT.value, query_params, self.log_helper)
        return affected_rows > 0

    def read_entries(self) -> tuple[Entry]:
        entries = []
        if entry_rows := self.db_helper.read_all(Query.ENTRY_READ_ALL.value, (), self.log_helper):
            for entry_row in entry_rows:
                entry = Entry()

                entry.to_entry(entry_row)
                entries.append(entry)

            for entry in entries:
                entry_work_emotion_rows = self.db_helper.read_all(
                    Query.ENTRY_WORK_EMOTION_READ_ALL.value,
                    (entry.repo_id,),
                    self.log_helper
                )
                for entry_work_emotion_row in entry_work_emotion_rows:
                    work_emotion_row = self.db_helper.read_one(
                        Query.WORK_EMOTION_READ_ONE.value,
                        (entry_work_emotion_row[1].decode(),),
                        self.log_helper
                    )
                    entry_work_emotion = EntryWorkEmotion()
                    work_emotion = WorkEmotion()

                    work_emotion.to_work_emotion(work_emotion_row)
                    entry_work_emotion.to_entry_work_emotion(
                        (
                            entry_work_emotion_row[0],
                            work_emotion,
                            entry_work_emotion_row[2],
                            entry_work_emotion_row[3]
                        )
                    )
                    entry.work_emotions.append(entry_work_emotion)
            return tuple(entries)

    def update_entry(self, old_entry: Entry, new_entry: Entry) -> bool:
        pass

    def delete_entry(self, entry: Entry) -> bool:
        pass

    def reset_db(self):
        affected_rows = self.db_helper.delete(Query.ENTRY_WORK_EMOTION_DELETE.value, (), self.log_helper)
        return affected_rows > 0
