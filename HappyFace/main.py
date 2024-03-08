import sys
import threading

from helper.api_call.api_call_helper import ApiCallHelper
from helper.capture_record.capture_record_helper import CaptureRecordHelper
from helper.config.app_config_helper import AppConfigHelper
from helper.data_visualize.data_visualize_helper import DataVisualizeHelper
from helper.database.mysql.db_helper import DbHelper
from helper.face_detect.face_detector_helper import FaceDetectorHelper
from helper.face_emotion.face_emotion_helper import FaceEmotionHelper
from helper.face_match.face_match_helper import FaceMatchHelper
from helper.log.default.log_helper import LogHelper
from service.capture_record.capture_record_service import CaptureRecordService
from service.dashboard_service import DashboardService
from service.data_visualize.data_visualize_service import DataVisualizeService
from service.model.entry_service import EntryService
from service.setting_service import SettingService
from view.dashboard import DashboardApp


class Main:
    def __init__(
            self,
            log_helper: LogHelper,
            dashboard_service: DashboardService,
            setting_service: SettingService,
            entry_service: EntryService,
            data_visualize_service: DataVisualizeService,
            face_detector_helper: FaceDetectorHelper,
            face_match_helper: FaceMatchHelper,
            face_emotion_helper: FaceEmotionHelper,
            capture_record_helper: CaptureRecordHelper,
            api_call_helper: ApiCallHelper
    ):
        self.__log_helper = log_helper
        self.__dashboard_service = dashboard_service
        self.__setting_service = setting_service
        self.__entry_service = entry_service
        self.__data_visualize_service = data_visualize_service
        self.__face_detector_helper = face_detector_helper
        self.__face_match_helper = face_match_helper
        self.__face_emotion_helper = face_emotion_helper
        self.__capture_record_helper = capture_record_helper
        self.__api_call_helper = api_call_helper

        self.__app = DashboardApp(
            self.log_helper,
            self.dashboard_service,
            self.setting_service,
            self.entry_service,
            self.data_visualize_service,
            self.face_detector_helper,
            self.face_match_helper,
            self.face_emotion_helper,
            self.capture_record_helper,
            self.api_call_helper
        )

    @property
    def log_helper(self) -> LogHelper:
        return self.__log_helper

    @log_helper.setter
    def log_helper(self, log_helper: LogHelper) -> None:
        self.__log_helper = log_helper

    @property
    def dashboard_service(self) -> DashboardService:
        return self.__dashboard_service

    @dashboard_service.setter
    def dashboard_service(self, dashboard_service: DashboardService) -> None:
        self.__dashboard_service = dashboard_service

    @property
    def setting_service(self) -> SettingService:
        return self.__setting_service

    @setting_service.setter
    def setting_service(self, setting_service: SettingService):
        self.__setting_service = setting_service

    @property
    def entry_service(self) -> EntryService:
        return self.__entry_service

    @entry_service.setter
    def entry_service(self, entry_service: EntryService) -> None:
        self.__entry_service = entry_service

    @property
    def data_visualize_service(self):
        return self.__data_visualize_service

    @data_visualize_service.setter
    def data_visualize_service(self, data_visualize_service: DataVisualizeService):
        self.__data_visualize_service = data_visualize_service

    @property
    def face_detector_helper(self) -> FaceDetectorHelper:
        return self.__face_detector_helper

    @face_detector_helper.setter
    def face_detector_helper(self, face_detector_helper: FaceDetectorHelper) -> None:
        self.__face_detector_helper = face_detector_helper

    @property
    def face_match_helper(self) -> FaceMatchHelper:
        return self.__face_match_helper

    @face_match_helper.setter
    def face_match_helper(self, face_match_helper: FaceMatchHelper) -> None:
        self.__face_match_helper = face_match_helper

    @property
    def face_emotion_helper(self) -> FaceEmotionHelper:
        return self.__face_emotion_helper

    @face_emotion_helper.setter
    def face_emotion_helper(self, face_emotion_helper: FaceEmotionHelper) -> None:
        self.__face_emotion_helper = face_emotion_helper

    @property
    def capture_record_helper(self) -> CaptureRecordHelper:
        return self.__capture_record_helper

    @capture_record_helper.setter
    def capture_record_helper(self, capture_record_helper: CaptureRecordHelper) -> None:
        self.__capture_record_helper = capture_record_helper

    @property
    def api_call_helper(self) -> ApiCallHelper:
        return self.__api_call_helper

    @api_call_helper.setter
    def api_call_helper(self, api_call_helper: ApiCallHelper) -> None:
        self.__api_call_helper = api_call_helper

    def run(self) -> None:
        self.__app.run()


if __name__ == '__main__':
    log_config = AppConfigHelper.get_log_config()
    db_config = AppConfigHelper.get_database_config()
    basic_config = AppConfigHelper.get_basic_app_config()

    log_helper = LogHelper(
        log_config["LOGGER_NAME"],
        log_config["LOG_FILE_NAME"],
        log_config["LOG_FORMAT_TEMPLATE"],
        log_config["LOG_FILE_OPEN_MODE"]
    )
    db_helper = DbHelper(
        db_config["host"],
        int(db_config["port"]),
        db_config["user"],
        db_config["password"],
        db_config["database"]
    )
    face_detector_helper = FaceDetectorHelper()
    face_match_helper = FaceMatchHelper()
    face_emotion_helper = FaceEmotionHelper()
    capture_record_helper = CaptureRecordHelper()
    data_visualize_helper = DataVisualizeHelper()
    api_call_helper = ApiCallHelper()

    dashboard_service = DashboardService()
    setting_service = SettingService()
    entry_service = EntryService(db_helper, log_helper)
    data_visualize_service = DataVisualizeService(data_visualize_helper, entry_service)
    capture_record_service = CaptureRecordService(
        entry_service,
        capture_record_helper,
        basic_config["capture_record_save_dir"],
        log_helper,
        api_call_helper
    )
    main = Main(
        log_helper,
        dashboard_service,
        setting_service,
        entry_service,
        data_visualize_service,
        face_detector_helper,
        face_match_helper,
        face_emotion_helper,
        capture_record_helper,
        api_call_helper
    )
    capture_record_process_thread = threading.Thread(target=capture_record_service.process_entries_in_background)
    capture_record_process_thread.daemon = True

    main.log_helper.log_info_message("[Main] App initialized successfully")
    db_helper.establish_connection(main.log_helper)
    capture_record_process_thread.start()
    main.run()
    db_helper.close_connection(main.log_helper)
    main.log_helper.log_info_message("[Main] App disabled successfully")

    sys.exit()
