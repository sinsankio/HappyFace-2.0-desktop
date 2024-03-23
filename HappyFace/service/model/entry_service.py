from helper.database.mongodb.db_helper import DbHelper
from helper.log.default.log_helper import LogHelper
from model.entry import Entry


class EntryService:
    def __init__(self, log_helper: LogHelper):
        self.__db_helper: DbHelper = None
        self.__log_helper: LogHelper = log_helper

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

    def read_entries(self) -> tuple[Entry]:
        if entry_dicts := self.db_helper.read_all({}, {"_id": False}, self.log_helper):
            entries = []

            for entry_dict in entry_dicts:
                entry = Entry()

                entry.cast_from_dict(entry_dict)
                entries.append(entry)
            return entries
        return tuple()

    def insert_update_entry(self, entry: Entry) -> bool:
        if entry_dict := self.db_helper.read_one({"faceSnapDirURI": entry.repo_id}, {"_id": False},
                                                 self.log_helper):
            entry.created_on = entry_dict["createdOn"]
            for work_emotion in entry_dict["workEmotions"]:
                entry.work_emotions.append(work_emotion)
            return self.db_helper.update({"faceSnapDirURI": entry.repo_id},
                                         {"$set": entry.cast_to_dict()}, self.log_helper)
        result = self.db_helper.insert(entry.cast_to_dict(), self.log_helper)
        self.add_unique_index_on("faceSnapDirURI")
        return result

    def delete_entry(self, entry: Entry) -> bool:
        pass

    def reset_db(self) -> None:
        affected_rows = self.db_helper.delete({}, self.log_helper)
        return affected_rows > 0

    def add_unique_index_on(self, field: str) -> None:
        self.db_helper.unique(field, self.log_helper)
