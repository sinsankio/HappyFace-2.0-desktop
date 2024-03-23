from datetime import datetime


class DateTimeHelper:
    @staticmethod
    def get_formatted_datetime(
            current_datetime: datetime = datetime.now(),
            dt_format: str = "%Y-%m-%dT%H:%M:%S.%f"
    ) -> str:
        return current_datetime.strftime(dt_format)

    @staticmethod
    def to_secs(hours: int = 0, minutes: int = 0, secs: int = 0) -> int:
        secs += (hours * 60 * 60) + (minutes * 60)
        return secs
