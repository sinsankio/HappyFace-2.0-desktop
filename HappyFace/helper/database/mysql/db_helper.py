from typing import Any

from mysql.connector import connect, Error

from helper.database.abstract_db_helper import AbstractDbHelper
from helper.log.default.log_helper import LogHelper


class DbHelper(AbstractDbHelper):
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        self.__connection = None
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__database = database

    @property
    def connection(self) -> Any:
        return self.__connection

    @connection.setter
    def connection(self, connection: Any) -> None:
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
    def user(self) -> str:
        return self.__user

    @user.setter
    def user(self, user: str) -> None:
        self.__user = user

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, password: str) -> None:
        self.__password = password

    @property
    def database(self) -> str:
        return self.__database

    @database.setter
    def database(self, database: str) -> None:
        self.__database = database

    def establish_connection(self, logger: LogHelper) -> bool:
        if not self.connection:
            try:
                self.connection = connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    passwd=self.password,
                    database=self.database
                )
                logger.log_info_message("[MysqlDbHelper] Connected to the DB successfully")
            except Error as e:
                logger.log_error_message(f"[MysqlDbHelper] Not connected to the DB successfully {e}")
                return False
        return True

    def close_connection(self, logger: LogHelper):
        if self.connection.cursor():
            self.connection.cursor().close()
            self.connection.close()
        logger.log_info_message("[MysqlDbHelper] Closed DB connection successfully")

    def insert(
            self,
            query: str,
            query_params: tuple,
            logger: LogHelper
    ) -> int:
        try:
            if self.connection:
                cursor = self.connection.cursor(prepared=True)

                if query_params:
                    cursor.execute(query, query_params)
                else:
                    cursor.execute(query)

                self.connection.commit()
                return cursor.rowcount
        except Error as e:
            logger.log_error_message(f"[MysqlDbHelper] Data insertion failed: {e}")
        return 0

    def update(
            self,
            query: str,
            query_params: tuple,
            logger: LogHelper
    ) -> int:
        try:
            if self.connection:
                cursor = self.connection.cursor(prepared=True)

                if query_params:
                    cursor.execute(query, query_params)
                else:
                    cursor.execute(query)

                self.connection.commit()
                return cursor.rowcount
        except Error as e:
            logger.log_error_message(f"[MysqlDbHelper] Data modification failed: {e}")
        return 0

    def read_all(
            self,
            query: str,
            query_params: tuple,
            logger: LogHelper
    ) -> tuple[Any | None] | None:
        try:
            if self.connection:
                cursor = self.connection.cursor(prepared=True)

                if query_params:
                    cursor.execute(query, query_params)
                else:
                    cursor.execute(query)

                return cursor.fetchall()
        except Error as e:
            logger.log_error_message(f"[MysqlDbHelper] Data fetching failed: {e}")

    def read_one(
            self,
            query: str,
            query_params: tuple,
            logger: LogHelper
    ) -> tuple[Any | None] | None:
        try:
            if self.connection:
                cursor = self.connection.cursor(prepared=True)

                if query_params:
                    cursor.execute(query, query_params)
                else:
                    cursor.execute(query)

                return cursor.fetchone()
        except Error as e:
            logger.log_error_message(f"[MysqlDbHelper] Data fetching failed: {e}")

    def delete(
            self,
            query: str,
            query_params: tuple,
            logger: LogHelper
    ) -> int:
        try:
            if self.connection:
                cursor = self.connection.cursor(prepared=True)

                if query_params:
                    cursor.execute(query, query_params)
                else:
                    cursor.execute(query)

                self.connection.commit()
                return cursor.rowcount
        except Error as e:
            logger.log_error_message(f"[MysqlDbHelper] Data deletion failed: {e}")
        return 0
