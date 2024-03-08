from helper.config.app_config_helper import AppConfigHelper
from helper.ui.message_box_helper import MessageBoxHelper
from helper.ui.validation_helper import ValidationHelper


class SettingService:
    def validate_entries(self, **kwargs) -> bool:
        camera_src = kwargs["camera_src"]
        subject_snap_save_dir = kwargs["subject_snap_save_dir"]
        capture_record_save_dir = kwargs["capture_record_save_dir"]
        work_duration_hours = kwargs["work_duration_hours"]
        work_duration_minutes = kwargs["work_duration_minutes"]
        work_duration_seconds = kwargs["work_duration_seconds"]
        snap_count_per_iter = kwargs["snap_count_per_iter"]

        if ValidationHelper.is_empty(camera_src):
            MessageBoxHelper.show_warning_message_box("Empty Entry", "Please enter a valid camera source")
            return False

        if ValidationHelper.is_empty(subject_snap_save_dir):
            MessageBoxHelper.show_warning_message_box("Empty Entry", "Please enter a valid Subject Snap Save Dir Path")
            return False

        if ValidationHelper.is_empty(capture_record_save_dir):
            MessageBoxHelper.show_warning_message_box("Empty Entry",
                                                      "Please enter a valid Capture Record Save Dir Path")
            return False

        if ValidationHelper.is_empty(work_duration_hours):
            MessageBoxHelper.show_warning_message_box("Empty Entry", "Please enter a valid Work Duration Hours")
            return False

        if ValidationHelper.is_empty(work_duration_minutes):
            MessageBoxHelper.show_warning_message_box("Empty Entry", "Please enter a valid Work Duration Minutes")
            return False

        if ValidationHelper.is_empty(work_duration_seconds):
            MessageBoxHelper.show_warning_message_box("Empty Entry", "Please enter a valid Work Duration Seconds")
            return False

        if ValidationHelper.is_empty(snap_count_per_iter):
            MessageBoxHelper.show_warning_message_box("Empty Entry", "Please enter a valid Snap Count Per Iteration")
            return False

        if not ValidationHelper.is_valid_dir_path(subject_snap_save_dir):
            MessageBoxHelper.show_warning_message_box("Invalid Entry",
                                                      "Please enter a valid file path for Subject Snap Save Dir Path")
            return False

        if not ValidationHelper.is_valid_dir_path(capture_record_save_dir):
            MessageBoxHelper.show_warning_message_box("Invalid Entry",
                                                      "Please enter a valid file path for Capture Record Save Dir Path")
            return False

        if not ValidationHelper.is_numeric(work_duration_hours):
            MessageBoxHelper.show_warning_message_box("Invalid Entry",
                                                      "Please enter a valid numeric for Work Duration Hours")
            return False

        if not ValidationHelper.is_numeric(work_duration_minutes):
            MessageBoxHelper.show_warning_message_box("Invalid Entry",
                                                      "Please enter a valid numeric for Work Duration Minutes")
            return False

        if not ValidationHelper.is_numeric(work_duration_seconds):
            MessageBoxHelper.show_warning_message_box("Invalid Entry",
                                                      "Please enter a valid numeric for Work Duration Seconds")
            return False

        if not ValidationHelper.is_numeric(snap_count_per_iter):
            MessageBoxHelper.show_warning_message_box("Invalid Entry",
                                                      "Please enter a valid numeric for Snap Count Per Iteration")
            return False
        return True

    def save_settings(self, **kwargs) -> bool:
        camera_src = kwargs["camera_src"]
        subject_snap_save_dir = kwargs["subject_snap_save_dir"]
        capture_record_save_dir = kwargs["capture_record_save_dir"]
        work_duration_hours = kwargs["work_duration_hours"]
        work_duration_minutes = kwargs["work_duration_minutes"]
        work_duration_seconds = kwargs["work_duration_seconds"]
        snap_count_per_iter = kwargs["snap_count_per_iter"]

        if validated := self.validate_entries(
                camera_src=camera_src,
                subject_snap_save_dir=subject_snap_save_dir,
                capture_record_save_dir=capture_record_save_dir,
                work_duration_hours=work_duration_hours,
                work_duration_minutes=work_duration_minutes,
                work_duration_seconds=work_duration_seconds,
                snap_count_per_iter=snap_count_per_iter
        ):
            if confirmation := MessageBoxHelper.show_ok_cancel_message_box("Settings Update Confirmation",
                                                                           "Are you confirming new changes to settings?"):
                AppConfigHelper.set_basic_app_config(
                    dict(
                        camera_src=camera_src,
                        subject_snap_save_dir=subject_snap_save_dir,
                        capture_record_save_dir=capture_record_save_dir,
                        work_duration_hours=work_duration_hours,
                        work_duration_minutes=work_duration_minutes,
                        work_duration_seconds=work_duration_seconds,
                        snap_count_per_iter=snap_count_per_iter
                    )
                )
                MessageBoxHelper.show_info_message_box("Successful Setting Update",
                                                       "Settings updated with new changes successfully")
            return confirmation
        return validated
