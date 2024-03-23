import contextlib
import os

import cv2

from helper.api_call.api_call_helper import ApiCallHelper
from helper.capture_record.capture_record_helper import CaptureRecordHelper
from helper.config.app_config_helper import AppConfigHelper
from helper.face_detect.face_detector_helper import FaceDetectorHelper
from helper.face_emotion.face_emotion_helper import FaceEmotionHelper
from helper.face_match.face_match_helper import FaceMatchHelper
from helper.log.default.log_helper import LogHelper
from helper.ui.message_box_helper import MessageBoxHelper
from helper.ui.validation_helper import ValidationHelper
from service.capture_record.capture_record_service import CaptureRecordService
from service.data_visualize.data_visualize_service import DataVisualizeService
from service.data_visualize.data_visualize_service_config import DataVisualizeServiceConfig
from service.fd_fm_fer.fd_fm_fer_service import FdFmFerService
from service.model.entry_service import EntryService
from service.snap.snap_service import SnapService


class DashboardService:
    @staticmethod
    def validate_entries(**kwargs) -> bool:
        save_dir_id = kwargs["save_dir_id"]

        if ValidationHelper.is_empty(save_dir_id):
            MessageBoxHelper.show_warning_message_box("Empty Entry", "Please enter a valid save directory ID")
            return False
        return True

    @staticmethod
    def get_snap_dir_path(save_dir_id: str) -> str:
        basic_configs = AppConfigHelper.get_basic_app_config()
        subject_snap_save_parent_dir_path = basic_configs["subject_snap_save_dir"]
        path = os.path.join(subject_snap_save_parent_dir_path, save_dir_id)
        return path

    @staticmethod
    def create_snap_dir(path: str) -> None:
        with contextlib.suppress(FileExistsError):
            os.mkdir(path)

    @staticmethod
    def collect_and_save_snaps(
            camera_id: int | str,
            snap_count_per_iter: int,
            save_dir_id: str
    ) -> None:
        snap_dir_path = DashboardService.get_snap_dir_path(save_dir_id)
        snap_service = SnapService(camera_id, snap_count_per_iter, snap_dir_path)
        collected_face_files = snap_service.collect()

        if MessageBoxHelper.show_ok_cancel_message_box("Snap Save Confirmation",
                                                       "Are you confirming the new snap collection?"):
            DashboardService.create_snap_dir(snap_dir_path)
            snap_service.save_face_files(collected_face_files)
            MessageBoxHelper.show_info_message_box("Successful Snap Collection", "Snaps collected successfully")

    @staticmethod
    def start_capture_with_record(
            camera_id: int | str,
            subject_snap_save_dir: str,
            face_detector_helper: FaceDetectorHelper,
            face_match_helper: FaceMatchHelper,
            face_emotion_helper: FaceEmotionHelper,
            entry_service: EntryService
    ):
        fd_fm_fer_service = FdFmFerService(
            camera_id,
            subject_snap_save_dir,
            face_detector_helper,
            face_match_helper,
            face_emotion_helper,
            entry_service
        )
        fd_fm_fer_service.run()

    @staticmethod
    def process_entries_manually(
            entry_service: EntryService,
            capture_record_helper: CaptureRecordHelper,
            api_call_helper: ApiCallHelper,
            capture_record_save_dir: str,
            log_helper: LogHelper,
            waiting_time_secs: int
    ):
        capture_record_service = CaptureRecordService(
            entry_service,
            capture_record_helper,
            capture_record_save_dir,
            log_helper,
            api_call_helper
        )

        capture_record_service.waiting_time_secs = waiting_time_secs
        capture_record_service.process_entries_manually()

    @staticmethod
    def visualize_overall_emotion_distribution_summary(data_visualize_service: DataVisualizeService):
        overall_emotion_distribution_summary = data_visualize_service.generate_overall_emotion_distribution_summary()

        if overall_emotion_distribution_summary is not None:
            cv2.imshow(DataVisualizeServiceConfig.FACE_EMOTION_DIST_WINDOW_TITLE, overall_emotion_distribution_summary)
        else:
            MessageBoxHelper.show_info_message_box(
                "Unavailability of Data for Visualization",
                "No available data to visualize overall emotion distribution statistics"
            )

    @staticmethod
    def visualize_emotion_distribution_based_on_positivity(data_visualize_service: DataVisualizeService):
        emotion_distribution_based_on_positivity = (data_visualize_service.
                                                    generate_emotion_distribution_summary_based_on_positivity())

        if emotion_distribution_based_on_positivity is not None:
            cv2.imshow(
                DataVisualizeServiceConfig.FACE_EMOTION_POS_DIST_WINDOW_TITLE,
                emotion_distribution_based_on_positivity
            )
        else:
            MessageBoxHelper.show_info_message_box(
                "Unavailability of Data for Visualization",
                "No available data to visualize emotion distribution based on positivity statistics"
            )
