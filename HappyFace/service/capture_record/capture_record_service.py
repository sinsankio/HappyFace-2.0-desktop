import contextlib
import time

from helper.api_call.api_call_config_helper import ApiCallConfigHelper
from helper.api_call.api_call_helper import ApiCallHelper
from helper.capture_record.capture_record_helper import CaptureRecordHelper
from helper.config.app_config_helper import AppConfigHelper
from helper.datetime.datetime_helper import DateTimeHelper
from helper.hash.hash_helper import HashHelper
from helper.log.default.log_helper import LogHelper
from service.model.entry_service import EntryService


class CaptureRecordService:
    def __init__(
            self,
            entry_service: EntryService,
            capture_record_helper: CaptureRecordHelper,
            capture_record_save_dir: str,
            log_helper: LogHelper,
            api_call_helper: ApiCallHelper
    ):
        self.__entry_service = entry_service
        self.__capture_record_helper = capture_record_helper
        self.__capture_record_save_dir = capture_record_save_dir
        self.__log_helper = log_helper
        self.__api_call_helper = api_call_helper

    @property
    def entry_service(self) -> EntryService:
        return self.__entry_service

    @entry_service.setter
    def entry_service(self, entry_service: EntryService) -> None:
        self.__entry_service = entry_service

    @property
    def capture_record_helper(self) -> CaptureRecordHelper:
        return self.__capture_record_helper

    @capture_record_helper.setter
    def capture_record_helper(self, capture_record_helper: CaptureRecordHelper) -> None:
        self.__capture_record_helper = capture_record_helper

    @property
    def capture_record_save_dir(self):
        return self.__capture_record_save_dir

    @capture_record_save_dir.setter
    def capture_record_save_dir(self, capture_record_save_dir: str) -> None:
        self.__capture_record_save_dir = capture_record_save_dir

    @property
    def log_helper(self) -> LogHelper:
        return self.__log_helper

    @log_helper.setter
    def log_helper(self, log_helper: LogHelper) -> None:
        self.__log_helper = log_helper

    @property
    def api_call_helper(self) -> ApiCallHelper:
        return self.__api_call_helper

    @api_call_helper.setter
    def api_call_helper(self, api_call_helper: ApiCallHelper) -> None:
        self.__api_call_helper = api_call_helper

    def process_entries_in_background(self) -> None:
        with contextlib.suppress(Exception):
            while True:
                basic_config = AppConfigHelper.get_basic_app_config()
                waiting_time_secs = DateTimeHelper.to_secs(
                    int(basic_config["work_duration_hours"]),
                    int(basic_config["work_duration_minutes"]),
                    int(basic_config["work_duration_seconds"])
                )

                time.sleep(waiting_time_secs)

                entries_for_upload = [entry.cast_to_dict() for entry in self.entry_service.read_entries()]
                org_config = AppConfigHelper.get_org_config()
                org_key = org_config["key"]
                org_key = HashHelper.hash(org_key)
                work_emotion_entry_upload_endpoint = ApiCallConfigHelper.WORK_EMOTION_ENTRY_UPLOAD_ENDPOINT % org_key
                work_emotion_consultancy_setup_endpoint = ApiCallConfigHelper.WORK_EMOTION_CONSULTANCY_SETUP_ENDPOINT \
                                                          % org_key
                try:
                    self.capture_record_helper.write_json(entries_for_upload, self.capture_record_save_dir)
                    self.api_call_helper.put(work_emotion_entry_upload_endpoint, entries_for_upload)
                    self.api_call_helper.post(work_emotion_consultancy_setup_endpoint)
                    self.entry_service.reset_db()
                    self.log_helper.log_info_message(
                        "[CaptureRecordService: Background] Latest capture record entries are processed successfully")
                except Exception:
                    self.log_helper.log_info_message(
                        "[CaptureRecordService: Background] Latest capture record entries are not processed "
                        "successfully")

    def process_entries_manually(self) -> None:
        entries_for_upload = [entry.cast_to_dict() for entry in self.entry_service.read_entries()]
        org_config = AppConfigHelper.get_org_config()
        org_key = org_config["key"]
        org_key = HashHelper.hash(org_key)
        work_emotion_entry_upload_endpoint = ApiCallConfigHelper.WORK_EMOTION_ENTRY_UPLOAD_ENDPOINT % org_key
        work_emotion_consultancy_setup_endpoint = ApiCallConfigHelper.WORK_EMOTION_CONSULTANCY_SETUP_ENDPOINT \
                                                  % org_key
        try:
            self.capture_record_helper.write_json(entries_for_upload, self.capture_record_save_dir)
            self.api_call_helper.put(work_emotion_entry_upload_endpoint, entries_for_upload)
            self.api_call_helper.post(work_emotion_consultancy_setup_endpoint)
            self.entry_service.reset_db()
            self.log_helper.log_info_message(
                "[CaptureRecordService: Manual] Latest capture record entries are processed successfully")
        except Exception:
            self.log_helper.log_info_message(
                "[CaptureRecordService: Manual] Latest capture record entries are not processed successfully")
