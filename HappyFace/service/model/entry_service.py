from helper.database.mongodb.db_helper import DbHelper
from helper.log.default.log_helper import LogHelper
from model.entry import Entry


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
        affected_rows = self.db_helper.insert(entry, self.log_helper)
        return affected_rows > 0

    def read_entries(self) -> tuple[Entry]:
        return self.db_helper.read_all({}, self.log_helper)

    def update_entry(self, old_entry: Entry, new_entry: Entry) -> bool:
        pass

    def delete_entry(self, entry: Entry) -> bool:
        pass

    def reset_db(self) -> None:
        affected_rows = self.db_helper.delete({}, self.log_helper)
        return affected_rows > 0
