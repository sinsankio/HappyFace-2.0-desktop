import cv2
import dlib
import numpy as np
from imutils import face_utils
from tensorflow.keras import models

from helper.face_emotion.face_emotion_config_helper import FaceEmotionConfigHelper


class FaceEmotionHelper:
    fer_model = None
    aro_val_model = None
    lm_predictor: dlib.shape_predictor = None

    @staticmethod
    def load_fer_model() -> None:
        FaceEmotionHelper.fer_model = models.load_model(FaceEmotionConfigHelper.FER_MODEL_FILE_PATH)

    @staticmethod
    def load_aro_val_model() -> None:
        FaceEmotionHelper.aro_val_model = models.load_model(FaceEmotionConfigHelper.ARO_VAL_MODEL_FILE_PATH)

    @staticmethod
    def load_lm_predictor() -> None:
        FaceEmotionHelper.lm_predictor = dlib.shape_predictor(FaceEmotionConfigHelper.LM_MODEL_FILE_PATH)

    @staticmethod
    def preprocess_face(image: np.ndarray, face_bound_rect: dict, res: tuple[int] = (48, 48)) -> np.ndarray:
        face_bound = dlib.rectangle(
            left=face_bound_rect["face_x"],
            top=face_bound_rect["face_y"],
            right=face_bound_rect["face_x"] + face_bound_rect["face_w"],
            bottom=face_bound_rect["face_y"] + face_bound_rect["face_h"]
        )
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        landmarks = FaceEmotionHelper.lm_predictor(image, face_bound)
        landmarks = face_utils.shape_to_np(landmarks).astype(np.int32)
        mask = np.zeros(res, dtype=np.uint8)
        bound_landmarks = []

        for pt in FaceEmotionConfigHelper.FACE_BOUND_PTS:
            bound_landmarks.append(landmarks[pt - 1])
        bound_landmarks = np.array([bound_landmarks], dtype=np.int32)

        cv2.fillPoly(mask, bound_landmarks, 255)
        masked_img = cv2.bitwise_and(image, image, mask=mask)

        x, y, w, h = face_bound.left(), face_bound.top(), face_bound.width(), face_bound.height()
        masked_face_img = masked_img[y: y + h, x: x + w]
        masked_face_img = cv2.resize(masked_face_img, res)
        masked_face_rescaled = masked_face_img / 255
        masked_face_reshaped = np.reshape(masked_face_rescaled, (1, res[0], res[1], 1))

        return masked_face_reshaped

    @staticmethod
    def get_emotions(image: np.ndarray, face_bound_rect: dict) -> tuple:
        if not (FaceEmotionHelper.fer_model and FaceEmotionHelper.aro_val_model and FaceEmotionHelper.lm_predictor):
            FaceEmotionHelper.load_fer_model()
            FaceEmotionHelper.load_aro_val_model()
            FaceEmotionHelper.load_lm_predictor()

            image = FaceEmotionHelper.preprocess_face(image, face_bound_rect)
            probabilities = FaceEmotionHelper.fer_model.predict(image)[0]
            aro_val = FaceEmotionHelper.aro_val_model.predict(probabilities)[0]
            emotions = dict(emotions=[])

            for index, probability in enumerate(probabilities):
                probability = round(probability * 100, 2)
                emotion = dict(
                    emotion=FaceEmotionConfigHelper.LABEL_CLASSES[index],
                    probability=probability
                )
                emotions["emotions"].append(emotion)
            emotions["aro_val"] = (aro_val[0], aro_val[1])
            return tuple(emotions)
