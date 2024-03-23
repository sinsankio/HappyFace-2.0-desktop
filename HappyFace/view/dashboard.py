import os

import pygubu

from helper.api_call.api_call_helper import ApiCallHelper
from helper.capture_record.capture_record_helper import CaptureRecordHelper
from helper.config.app_config_helper import AppConfigHelper
from helper.datetime.datetime_helper import DateTimeHelper
from helper.face_detect.face_detector_helper import FaceDetectorHelper
from helper.face_emotion.face_emotion_helper import FaceEmotionHelper
from helper.face_match.face_match_helper import FaceMatchHelper
from helper.log.default.log_helper import LogHelper
from service.dashboard_service import DashboardService
from service.data_visualize.data_visualize_service import DataVisualizeService
from service.model.entry_service import EntryService
from service.setting_service import SettingService
from view.settings import SettingsApp

PROJECT_PATH = "ui"
PROJECT_UI = os.path.join(PROJECT_PATH, "dashboard.ui")


class DashboardApp:
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
            api_call_helper: ApiCallHelper,
            master=None
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
        self.builder = builder = pygubu.Builder()

        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        self.main_window = builder.get_object("toplevel", master)
        builder.connect_callbacks(self)

        self.save_dir_id_entry = builder.get_object("save_dir_id_entry")

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
    def dashboard_service(self, dashboard_service: DashboardService):
        self.__dashboard_service = dashboard_service

    @property
    def setting_service(self) -> SettingService:
        return self.__setting_service

    @setting_service.setter
    def setting_service(self, setting_service: SettingService):
        self.__setting_service = setting_service

    @property
    def entry_service(self):
        return self.__entry_service

    @entry_service.setter
    def entry_service(self, entry_service: EntryService):
        self.__entry_service = entry_service

    @property
    def data_visualize_service(self) -> DataVisualizeService:
        return self.__data_visualize_service

    @data_visualize_service.setter
    def data_visualize_service(self, data_visualize_service: DataVisualizeService) -> None:
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

    def run(self):
        self.main_window.mainloop()

    def on_settings_button_clicked(self):
        settings_app = SettingsApp(self.log_helper, self.setting_service)
        settings_app.run()

    def on_clear_button_clicked(self):
        self.save_dir_id_entry.delete(0, "end")

    def on_collect_button_clicked(self):
        save_dir_id = self.save_dir_id_entry.get()

        if self.dashboard_service.validate_entries(save_dir_id=save_dir_id):
            basic_config = AppConfigHelper.get_basic_app_config()
            camera_src = basic_config["camera_src"]

            if camera_src.isdigit():
                camera_src = int(camera_src)

            self.dashboard_service.collect_and_save_snaps(
                camera_src,
                int(basic_config["snap_count_per_iter"]),
                save_dir_id
            )
            self.on_clear_button_clicked()

    def on_start_button_clicked(self):
        basic_config = AppConfigHelper.get_basic_app_config()
        camera_src = basic_config["camera_src"]

        if camera_src.isdigit():
            camera_src = int(camera_src)

        self.dashboard_service.start_capture_with_record(
            camera_src,
            basic_config["subject_snap_save_dir"],
            self.face_detector_helper,
            self.face_match_helper,
            self.face_emotion_helper,
            self.entry_service
        )

    def on_generate_capture_record_button_clicked(self):
        basic_config = AppConfigHelper.get_basic_app_config()
        capture_record_save_dir = basic_config["capture_record_save_dir"]
        waiting_time_secs = DateTimeHelper.to_secs(
            int(basic_config["work_duration_hours"]),
            int(basic_config["work_duration_minutes"]),
            int(basic_config["work_duration_seconds"])
        )

        self.dashboard_service.process_entries_manually(
            self.entry_service,
            self.capture_record_helper,
            self.api_call_helper,
            capture_record_save_dir,
            self.log_helper,
            waiting_time_secs
        )

    def on_overall_emotion_dist_button_clicked(self):
        self.dashboard_service.visualize_overall_emotion_distribution_summary(self.data_visualize_service)

    def on_positivity_emotion_dist_button_clicked(self):
        self.dashboard_service.visualize_emotion_distribution_based_on_positivity(self.data_visualize_service)
