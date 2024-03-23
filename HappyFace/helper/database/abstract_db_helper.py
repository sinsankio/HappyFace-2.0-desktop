from abc import ABC, abstractmethod


class AbstractDbHelper(ABC):
    @abstractmethod
    def establish_connection(self, db_name, logger):
        pass

    @abstractmethod
    def close_connection(self, logger):
        pass

    @abstractmethod
    def insert(self, entry, logger, collection):
        pass

    @abstractmethod
    def update(self, query, values, logger, collection):
        pass

    @abstractmethod
    def read_all(self, condition, projection, logger, collection):
        pass

    @abstractmethod
    def read_one(self, condition, projection, logger, collection):
        pass

    @abstractmethod
    def delete(self, condition, logger, collection):
        pass

    @abstractmethod
    def unique(self, field, logger, collection):
        pass
