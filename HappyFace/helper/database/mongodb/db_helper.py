from typing import Any

import pymongo

from helper.database.abstract_db_helper import AbstractDbHelper
from helper.log.default.log_helper import LogHelper


class DbHelper(AbstractDbHelper):
    def __init__(self, db_uri: str):
        self.__connection = None
        self.__db_uri = db_uri
        self.__database = None

    @property
    def connection(self) -> pymongo.MongoClient:
        return self.__connection

    @connection.setter
    def connection(self, connection: pymongo.MongoClient) -> None:
        self.__connection = connection

    @property
    def db_uri(self) -> str:
        return self.__db_uri

    @db_uri.setter
    def db_uri(self, db_uri: str) -> None:
        self.__db_uri = db_uri

    @property
    def database(self) -> Any:
        return self.__database

    @database.setter
    def database(self, database: Any) -> None:
        self.__database = database

    def establish_connection(self, db_name: str, logger: LogHelper) -> None:
        if not self.connection:
            try:
                self.connection = pymongo.MongoClient(self.db_uri)
                self.database = self.connection[db_name]
                logger.log_info_message("[MongoDbHelper] Connected to the DB successfully")
            except Exception as e:
                logger.log_error_message(f"[MongoDbHelper] Not connected to the DB successfully {e}")

    def close_connection(self, logger: LogHelper) -> None:
        self.connection.close()
        logger.log_info_message("[MongoDbHelper] Closed DB connection successfully")

    def insert(self, entry: dict, logger: LogHelper, collection: str = "entries") -> int:
        collection = self.database[collection]
        result = collection.insert_many([entry])

        logger.log_info_message(f"[MongoDbHelper] {len(result.inserted_ids)} records inserted to {collection.name}")
        return len(result.inserted_ids)

    def update(self, query: dict, values: dict, logger: LogHelper, collection: str = "entries") -> int:
        collection = self.database[collection]
        result = collection.update_one(query, values)

        logger.log_info_message(f"[MongoDbHelper] {result.modified_count} records updated from {collection.name}")
        return result.modified_count

    def read_all(self, condition: dict, projection: dict, logger: LogHelper, collection: str = "entries") -> (
            tuple)[dict]:
        collection = self.database[collection]
        records = []

        for record in collection.find(condition, projection):
            records.append(record)
        records = tuple(records)

        logger.log_info_message(f"[MongoDbHelper] {len(records)} records read from {collection.name}")
        return records

    def read_one(self, condition: dict, projection: dict, logger: LogHelper, collection: str = "entries") \
            -> dict:
        collection = self.database[collection]
        record = collection.find_one(condition, projection)

        logger.log_info_message(f"[MongoDbHelper] 1 record read from {collection.name}")
        return record

    def delete(self, condition: dict, logger: LogHelper, collection: str = "entries") -> int:
        collection = self.database[collection]
        result = collection.delete_many(condition)

        logger.log_info_message(f"[MongoDbHelper] {result.deleted_count} record(s) deleted from {collection.name}")
        return result.deleted_count

    def unique(self, field: str, logger: LogHelper, collection: str = "entries") -> None:
        self.database[collection].create_index(field, unique=True)
