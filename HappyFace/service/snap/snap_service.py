import os
import time

import cv2
import numpy as np

from helper.face_detect.face_detector_helper import FaceDetectorHelper
from helper.image_processing.image_processing_helper import ImageProcessingHelper
from service.snap.snap_service_config import SnapServiceConfig


class SnapService:
    def __init__(self, camera_id: int | str, snap_count_per_iter: int, snap_dir_path: str):
        self.__camera_id = camera_id
        self.__snap_count_per_iter = snap_count_per_iter
        self.__snap_dir_path = snap_dir_path

    @property
    def camera_id(self):
        return self.__camera_id

    @camera_id.setter
    def camera_id(self, camera_id: str) -> None:
        self.__camera_id = camera_id

    @property
    def snap_count_per_iter(self) -> int:
        return self.__snap_count_per_iter

    @snap_count_per_iter.setter
    def snap_count_per_iter(self, snap_count_per_id: int) -> None:
        self.__snap_count_per_iter = snap_count_per_id

    @property
    def snap_dir_path(self):
        return self.__snap_dir_path

    @snap_dir_path.setter
    def snap_dir_path(self, snap_dir_path: str) -> None:
        self.__snap_dir_path = snap_dir_path

    def collect(self) -> dict[int, np.ndarray]:
        iter_snap_collection = {
            0: [],
            1: [],
            2: [],
        }
        fps, pre_frame_time, new_frame_time = 0, 0, 0
        camera_src = cv2.VideoCapture(self.camera_id)
        window_closed = False
        frame_cpy = None

        for i in range(len(iter_snap_collection)):
            if window_closed:
                break

            snap_collecting = False

            while camera_src.isOpened():
                ret, frame = camera_src.read()
                frame_cpy = frame.copy()

                if ret:
                    new_frame_time = time.time()
                    fps = ImageProcessingHelper.calculate_fps(pre_frame_time, new_frame_time)
                    pre_frame_time = new_frame_time

                    cv2.resize(frame, SnapServiceConfig.WINDOW_RESOLUTION)

                    if not snap_collecting:
                        cv2.putText(
                            frame, f"ITERATION: {i} [Press Space to Continue]",
                            SnapServiceConfig.TEXT_ORG,
                            cv2.FONT_HERSHEY_SIMPLEX,
                            SnapServiceConfig.FONT_SCALE,
                            SnapServiceConfig.TEXT_COLOR,
                            SnapServiceConfig.LINE_THICKNESS
                        )

                        iteration = cv2.waitKey(1)

                        if iteration == ord(' '):
                            snap_collecting = True
                    elif len(iter_snap_collection[i]) < self.snap_count_per_iter:
                        cv2.putText(
                                frame,
                                f"NUM. SNAPS COMPLETED: {len(iter_snap_collection[i])}",
                                SnapServiceConfig.TEXT_ORG,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                SnapServiceConfig.FONT_SCALE,
                                SnapServiceConfig.TEXT_COLOR,
                                SnapServiceConfig.LINE_THICKNESS
                        )

                        face = FaceDetectorHelper.detect_face(frame, face_draw=True)
                        if face is not None:
                            iter_snap_collection[i].append(face)
                    else:
                        snap_collecting = False
                        break

                    iteration = cv2.waitKey(1)

                    if iteration in {ord('q'), ord('Q')}:
                        window_closed = True
                        break

                    cv2.putText(
                        frame, f"FPS: {fps}",
                        (555, 20),
                        SnapServiceConfig.FONT,
                        SnapServiceConfig.FONT_SCALE,
                        (0, 0, 255),
                        SnapServiceConfig.LINE_THICKNESS
                    )
                    cv2.imshow(SnapServiceConfig.WINDOW_TITLE, frame)

        if frame_cpy is not None:
            cv2.putText(
                frame_cpy,
                "Snap Collection is Completed",
                SnapServiceConfig.TEXT_ORG,
                SnapServiceConfig.FONT,
                SnapServiceConfig.FONT_SCALE,
                (255, 0, 0),
                SnapServiceConfig.LINE_THICKNESS
            )
            cv2.imshow(SnapServiceConfig.WINDOW_TITLE, frame_cpy)
            cv2.waitKey(3000)

        camera_src.release()
        cv2.destroyAllWindows()

        for iteration, collection in iter_snap_collection.items():
            iter_snap_collection[iteration] = np.array(collection)
        return iter_snap_collection

    def save_face_files(self, iter_snap_collection: dict[int, np.ndarray]) -> None:
        for iteration, collection in iter_snap_collection.items():
            for img_id in range(collection.shape[0]):
                img_file_path = os.path.join(self.snap_dir_path, f"iter={iteration}-{img_id}.jpg")
                cv2.imwrite(img_file_path, collection[img_id])
