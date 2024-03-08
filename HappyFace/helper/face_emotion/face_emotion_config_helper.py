from helper.face_emotion.face_emotion import FaceEmotion


class FaceEmotionConfigHelper:
    MODEL_FILE_PATH = "utility-models/fer"
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
