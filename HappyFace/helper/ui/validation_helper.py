import os


class ValidationHelper:
    @staticmethod
    def is_empty(entry: str) -> bool:
        return not entry or len(entry) <= 0 or entry.isspace()

    @staticmethod
    def is_numeric(entry: str) -> bool:
        return entry.isnumeric()

    @staticmethod
    def is_valid_file_path(entry: str) -> bool:
        return os.path.isfile(entry)

    @staticmethod
    def is_valid_dir_path(entry: str) -> bool:
        return os.path.isdir(entry)
