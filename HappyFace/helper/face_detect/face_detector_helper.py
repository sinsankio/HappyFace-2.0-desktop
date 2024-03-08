import cv2
import mediapipe as mp
import numpy as np

from helper.face_detect.face_detector_config_helper import FaceDetectorConfigHelper


class FaceDetectorHelper:
    face_detector_model = None

    @staticmethod
    def load_model():
        FaceDetectorHelper.face_detector_model = mp.solutions.face_detection.FaceDetection(
            min_detection_confidence=FaceDetectorConfigHelper.MIN_FACE_DETECT_CONF
        )

    @staticmethod
    def detect_face(
            frame: np.ndarray,
            face_draw: bool = False,
            bound_rect: bool = False
    ) -> tuple[np.ndarray, dict] | np.ndarray | None:
        if not FaceDetectorHelper.face_detector_model:
            FaceDetectorHelper.load_model()

        height, width, _ = frame.shape
        rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_detect_results = FaceDetectorHelper.face_detector_model.process(rgb_img)

        if face_detect_results.detections:
            face = face_detect_results.detections[0]
            rel_bound_rect = face.location_data.relative_bounding_box
            face_x, face_w, face_y, face_h = \
                int(rel_bound_rect.xmin * width), \
                int(rel_bound_rect.width * width), \
                int(rel_bound_rect.ymin * height), \
                int(rel_bound_rect.height * height)
            face = frame[face_y: face_y + face_h, face_x: face_x + face_w]
            face = cv2.resize(face, FaceDetectorConfigHelper.FACE_RESIZE)

            if face_draw:
                cv2.rectangle(
                    frame,
                    (face_x, face_y),
                    (face_x + face_w, face_y + face_h),
                    FaceDetectorConfigHelper.FACE_DRAW_COLOR,
                    2
                )
            if bound_rect:
                bound_rect_points = dict(
                    x=face_x,
                    y=face_y,
                    w=face_w,
                    h=face_h
                )
                return face, bound_rect_points
            return face
        return None

    @staticmethod
    def detect_faces(frame: np.ndarray, face_draw: bool = False, bound_rect: bool = False) -> tuple:
        if not FaceDetectorHelper.face_detector_model:
            FaceDetectorHelper.load_model()

        detected_face_records = []
        height, width, _ = frame.shape
        rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_detect_results = FaceDetectorHelper.face_detector_model.process(rgb_img)

        if face_detect_results.detections:
            for face in face_detect_results.detections:
                rel_bound_rect = face.location_data.relative_bounding_box
                face_x, face_w, face_y, face_h = \
                    int(rel_bound_rect.xmin * width), \
                    int(rel_bound_rect.width * width), \
                    int(rel_bound_rect.ymin * height), \
                    int(rel_bound_rect.height * height)
                face = frame[face_y: face_y + face_h, face_x: face_x + face_w]
                face = cv2.resize(face, FaceDetectorConfigHelper.FACE_RESIZE)
                face_record = [face]

                if face_draw:
                    cv2.rectangle(
                        frame,
                        (face_x, face_y),
                        (face_x + face_w, face_y + face_h),
                        FaceDetectorConfigHelper.FACE_DRAW_COLOR,
                        2
                    )
                if bound_rect:
                    face_record.append(
                        dict(
                            x=face_x,
                            y=face_y,
                            w=face_w,
                            h=face_h
                        )
                    )
                detected_face_records.append(tuple(face_record))
        return tuple(detected_face_records)
