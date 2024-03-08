from abc import ABC, abstractmethod


class AbstractDbHelper(ABC):
    @abstractmethod
    def establish_connection(self, logger):
        pass

    @abstractmethod
    def close_connection(self, logger):
        pass

    @abstractmethod
    def insert(self, query, query_params, logger):
        pass

    @abstractmethod
    def update(self, query, query_params, logger):
        pass

    @abstractmethod
    def read_all(self, query, query_params, logger):
        pass

    @abstractmethod
    def read_one(self, query, query_params, logger):
        pass

    @abstractmethod
    def delete(self, query, query_params, logger):
        pass
