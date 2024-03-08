import hashlib


class HashHelper:
    @staticmethod
    def hash(content: str):
        sha256 = hashlib.sha256()
        sha256.update(content.encode("utf-8"))
        return sha256.hexdigest()
