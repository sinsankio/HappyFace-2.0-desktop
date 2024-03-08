import time

import cv2
import numpy as np

from helper.face_detect.face_detector_helper import FaceDetectorHelper
from helper.face_emotion.face_emotion_helper import FaceEmotionHelper
from helper.face_match.face_match_helper import FaceMatchHelper
from helper.image_processing.image_processing_helper import ImageProcessingHelper
from model.entry import Entry
from service.fd_fm_fer.fd_fm_fer_service_config import FdFmFerServiceConfig
from service.model.entry_service import EntryService


class FdFmFerService:
    def __init__(
            self,
            camera_id: int | str,
            subject_snap_save_dir: str,
            face_detector_helper: FaceDetectorHelper,
            face_match_helper: FaceMatchHelper,
            face_emotion_helper: FaceEmotionHelper,
            entry_service: EntryService
    ):
        self.__camera_id = camera_id
        self.__subject_snap_save_dir = subject_snap_save_dir
        self.__face_detector_helper = face_detector_helper
        self.__face_match_helper = face_match_helper
        self.__face_emotion_helper = face_emotion_helper
        self.__entry_service = entry_service

    @property
    def camera_id(self) -> int | str:
        return self.__camera_id

    @camera_id.setter
    def camera_id(self, camera_id: str | int) -> None:
        self.__camera_id = camera_id

    @property
    def subject_snap_save_dir(self) -> str:
        return self.__subject_snap_save_dir

    @subject_snap_save_dir.setter
    def subject_snap_save_dir(self, subject_snap_save_dir: str) -> None:
        self.__subject_snap_save_dir = subject_snap_save_dir

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
    def entry_service(self) -> EntryService:
        return self.__entry_service

    @entry_service.setter
    def entry_service(self, entry_service: EntryService) -> None:
        self.__entry_service = entry_service

    def detect_faces(self, frame: np.ndarray, face_draw: bool = False, bound_rect: bool = False) -> tuple:
        return self.face_detector_helper.detect_faces(frame, face_draw, bound_rect)

    def match_face(self, face: np.ndarray) -> dict[str, str | int] | None:
        return self.face_match_helper.match(self.subject_snap_save_dir, face)

    def get_face_emotions(self, face: np.ndarray) -> tuple:
        emotion_result = self.face_emotion_helper.get_emotions(face)
        return tuple(
            sorted(
                emotion_result,
                key=lambda x: x["probability"],
                reverse=True
            )
        )

    def run(self):
        camera_src = cv2.VideoCapture(self.camera_id)
        fps, pre_frame_time, new_frame_time = 0, 0, 0
        last_record_saved_time = None

        while camera_src.isOpened():
            ret, frame = camera_src.read()

            if ret:
                new_frame_time = time.time()
                fps = ImageProcessingHelper.calculate_fps(pre_frame_time, new_frame_time)
                pre_frame_time = new_frame_time
                frame = cv2.resize(frame, FdFmFerServiceConfig.WINDOW_RESOLUTION)

                if face_records := self.detect_faces(frame, face_draw=True, bound_rect=True):
                    for face_record in face_records:
                        face, face_bound_rect = face_record[0], face_record[1]
                        face_match_result = self.match_face(face)
                        face_emotion_result = self.get_face_emotions(face)
                        best_face_emotion_record = face_emotion_result[0]
                        face_match_result_dir_id, face_match_result_prob = face_match_result["directory_id"], \
                            face_match_result["probability"]
                        best_face_emotion, best_face_emotion_prob = best_face_emotion_record["emotion"], \
                            best_face_emotion_record["probability"]

                        if last_record_saved_time is None or \
                                (time.time() - last_record_saved_time) >= FdFmFerServiceConfig.MIN_DB_ENTRY_DELAY_SECS:
                            if face_match_result_prob >= FdFmFerServiceConfig.MIN_FACE_MATCH_CONF and \
                                    best_face_emotion_prob >= FdFmFerServiceConfig.MIN_FACE_EMOTION_CONF:
                                entry = Entry()
                                entry = entry.generate_entry(face_match_result_dir_id, best_face_emotion_record)

                                self.entry_service.insert_entry_work_emotions(entry)

                                last_record_saved_time = time.time()

                        face_x, face_y, face_w, face_h = face_bound_rect['x'], face_bound_rect['y'], \
                            face_bound_rect['w'], face_bound_rect['h']
                        cv2.putText(
                            frame,
                            f"{face_match_result_dir_id}: {str(face_match_result_prob)}%",
                            (face_x, face_y - 30),
                            FdFmFerServiceConfig.FONT,
                            FdFmFerServiceConfig.FONT_SCALE,
                            (255, 0, 0),
                            FdFmFerServiceConfig.LINE_THICKNESS
                        )
                        cv2.putText(
                            frame,
                            f"{best_face_emotion}: {str(best_face_emotion_prob)}%",
                            (face_x, face_y - 10),
                            FdFmFerServiceConfig.FONT,
                            FdFmFerServiceConfig.FONT_SCALE,
                            (0, 255, 0),
                            FdFmFerServiceConfig.LINE_THICKNESS
                        )
                cv2.putText(
                    frame,
                    f"FPS: {fps}",
                    FdFmFerServiceConfig.TEXT_ORG,
                    FdFmFerServiceConfig.FONT,
                    FdFmFerServiceConfig.FONT_SCALE,
                    FdFmFerServiceConfig.TEXT_COLOR,
                    FdFmFerServiceConfig.LINE_THICKNESS
                )
                cv2.imshow(FdFmFerServiceConfig.WINDOW_TITLE, frame)

            k = cv2.waitKey(1)

            if k in FdFmFerServiceConfig.EXIT_KEY_COMPOSITION:
                break
            if k in FdFmFerServiceConfig.PAUSE_KEY_COMPOSITION:
                k = cv2.waitKey(-1)
                while k not in FdFmFerServiceConfig.PAUSE_KEY_COMPOSITION:
                    k = cv2.waitKey(-1)

        camera_src.release()
        cv2.destroyAllWindows()