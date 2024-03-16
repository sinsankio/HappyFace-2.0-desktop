from typing import Any

import pymongo

from helper.database.abstract_db_helper import AbstractDbHelper
from helper.log.default.log_helper import LogHelper
from model.entry import Entry


class DbHelper(AbstractDbHelper):
    def __init__(self, host: str, port: int, database: str):
        self.__connection = None
        self.__host = host
        self.__port = port
        self.__database = database

    @property
    def connection(self) -> pymongo.MongoClient:
        return self.__connection

    @connection.setter
    def connection(self, connection: pymongo.MongoClient) -> None:
        self.__connection = connection

    @property
    def host(self) -> str:
        return self.__host

    @host.setter
    def host(self, host: str) -> None:
        self.__host = host

    @property
    def port(self) -> int:
        return self.__port

    @port.setter
    def port(self, port: int) -> None:
        self.__port = port

    @property
    def database(self) -> Any:
        return self.__database

    @database.setter
    def database(self, database: str) -> None:
        self.__database = self.connection[database]

    def establish_connection(self, logger: LogHelper) -> None:
        if not self.connection:
            try:
                self.connection = pymongo.MongoClient(f"mongodb://{self.host}:{self.port}/")
                self.database = self.connection[f"{self.database}"]
                logger.log_info_message("[MongoDbHelper] Connected to the DB successfully")
            except Exception as e:
                logger.log_error_message(f"[MongoDbHelper] Not connected to the DB successfully {e}")

    def close_connection(self, logger: LogHelper) -> None:
        self.connection.close()
        logger.log_info_message("[MongoDbHelper] Closed DB connection successfully")

    def insert(self, entry: dict, logger: LogHelper, collection: str = "entries") -> int:
        collection = self.database[collection]
        result = collection.insert_many([entry])
        return len(result.inserted_ids)

    def update(self, query: dict, values: dict, logger: LogHelper, collection: str = "entries"):
        pass

    def read_all(self, condition: dict, logger: LogHelper, collection: str = "entries") -> tuple[Entry]:
        collection = self.database[collection]
        records = []

        for record in collection.find({}, condition):
            records.append(record)
        records = tuple(records)
        return records

    def delete(self, condition: dict, logger: LogHelper, collection: str = "entries"):
        collection = self.database[collection]
        collection.delete_many(condition)
