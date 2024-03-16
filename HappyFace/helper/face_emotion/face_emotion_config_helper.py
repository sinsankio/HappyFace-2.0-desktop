from helper.face_emotion.face_emotion import FaceEmotion


class FaceEmotionConfigHelper:
    FER_MODEL_FILE_PATH = "../../../../../utility-models/fer"
    ARO_VAL_MODEL_FILE_PATH = "../../../../../utility-models/aro_val"
    LM_MODEL_FILE_PATH = "lm-model/shape_predictor_68_face_landmarks.dat"
    LABEL_CLASSES = {
        0: FaceEmotion.ANGER.value,
        1: FaceEmotion.CONTEMPT.value,
        2: FaceEmotion.DISGUST.value,
        3: FaceEmotion.FEAR.value,
        4: FaceEmotion.HAPPY.value,
        5: FaceEmotion.NEUTRAL.value,
        6: FaceEmotion.SAD.value,
        7: FaceEmotion.SURPRISE.value
    }
    RESIZE_DIM = (48, 48)
    FACE_BOUND_PTS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18]
