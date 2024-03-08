import os

import pygubu

from helper.config.app_config_helper import AppConfigHelper
from helper.log.default.log_helper import LogHelper
from service.setting_service import SettingService

PROJECT_PATH = "ui"
PROJECT_UI = os.path.join(PROJECT_PATH, "settings.ui")


class SettingsApp:
    def __init__(
            self,
            log_helper: LogHelper,
            setting_service: SettingService,
            master=None
    ):
        self.__log_helper = log_helper
        self.__setting_service = setting_service
        self.builder = builder = pygubu.Builder()

        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        self.main_window = builder.get_object("toplevel", master)
        builder.connect_callbacks(self)

        self.cam_id_ip_entry = builder.get_object("cam_id_ip_entry")
        self.subject_snap_dir_path_entry = builder.get_object("subject_snap_dir_path_entry")
        self.capture_record_dir_path_entry = builder.get_object("capture_record_dir_path_entry")
        self.hours_combo = builder.get_object("hours_combo")
        self.minutes_combo = builder.get_object("minutes_combo")
        self.seconds_combo = builder.get_object("seconds_combo")
        self.snap_counter_per_iter_combo = builder.get_object("snap_counter_per_iter_combo")

        basic_configs = AppConfigHelper.get_basic_app_config()

        self.cam_id_ip_entry.insert(0, basic_configs["camera_src"])
        self.subject_snap_dir_path_entry.insert(0, basic_configs["subject_snap_save_dir"])
        self.capture_record_dir_path_entry.insert(0, basic_configs["capture_record_save_dir"])
        self.hours_combo.insert(0, basic_configs["work_duration_hours"])
        self.minutes_combo.insert(0, basic_configs["work_duration_minutes"])
        self.seconds_combo.insert(0, basic_configs["work_duration_seconds"])
        self.snap_counter_per_iter_combo.insert(0, basic_configs["snap_count_per_iter"])

    @property
    def log_helper(self):
        return self.__log_helper

    @log_helper.setter
    def log_helper(self, log_helper: LogHelper):
        self.__log_helper = log_helper

    @property
    def setting_service(self):
        return self.__setting_service

    @setting_service.setter
    def setting_service(self, setting_service: SettingService):
        self.__setting_service = setting_service

    def run(self):
        self.main_window.mainloop()

    def on_save_button_clicked(self):
        camera_src = self.cam_id_ip_entry.get()
        subject_snap_save_dir = self.subject_snap_dir_path_entry.get()
        capture_record_save_dir = self.capture_record_dir_path_entry.get()
        work_duration_hours = self.hours_combo.get()
        work_duration_minutes = self.minutes_combo.get()
        work_duration_seconds = self.seconds_combo.get()
        snap_count_per_iter = self.snap_counter_per_iter_combo.get()

        if self.setting_service.save_settings(
            camera_src=camera_src,
            subject_snap_save_dir=subject_snap_save_dir,
            capture_record_save_dir=capture_record_save_dir,
            work_duration_hours=work_duration_hours,
            work_duration_minutes=work_duration_minutes,
            work_duration_seconds=work_duration_seconds,
            snap_count_per_iter=snap_count_per_iter
        ):
            self.main_window.destroy()
            self.log_helper.log_info_message("[SettingsApp] New settings saved successfully")
