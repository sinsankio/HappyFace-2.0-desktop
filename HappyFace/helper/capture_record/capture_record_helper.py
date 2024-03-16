import json
import os

from helper.datetime.datetime_helper import DateTimeHelper


class CaptureRecordHelper:
    @staticmethod
    def write_json(entries_dict: dict, capture_record_save_dir: str) -> None:
        formatted_datetime = DateTimeHelper.get_formatted_datetime(dt_format="%Y-%m-%d %H-%M-%S")
        capture_record_file_save_path = os.path.join(capture_record_save_dir, f"crf-{formatted_datetime}.json")

        with open(capture_record_file_save_path, 'w') as capture_record_file:
            json.dump(entries_dict, capture_record_file)
