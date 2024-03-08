import json
import os

from helper.datetime.datetime_helper import DateTimeHelper
from model.entry import Entry


class CaptureRecordHelper:
    def convert_entries(self, entries: tuple[Entry]) -> dict:
        entries_dict = dict(entries=[])

        for entry in entries:
            entry_dict = dict(
                faceSnapDirURI=entry.repo_id,
                createdOn=entry.created_on,
                workEmotions=[]
            )
            for entry_work_emotion in entry.work_emotions:
                work_emotion_dict = dict(
                    emotion=entry_work_emotion.emotion.emotion,
                    probability=entry_work_emotion.emotion_prob,
                    recordedOn=entry_work_emotion.recorded_on
                )
                entry_dict["workEmotions"].append(work_emotion_dict)
            entries_dict["entries"].append(entry_dict)
        return entries_dict

    def write_json(self, entries_dict: dict, capture_record_save_dir: str) -> None:
        formatted_datetime = DateTimeHelper.get_formatted_datetime(dt_format="%Y-%m-%d %H-%M-%S")
        capture_record_file_save_path = os.path.join(capture_record_save_dir, f"crf-{formatted_datetime}.json")

        with open(capture_record_file_save_path, 'w') as capture_record_file:
            json.dump(entries_dict, capture_record_file)
