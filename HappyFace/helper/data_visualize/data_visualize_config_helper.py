from helper.face_emotion.face_emotion import FaceEmotion


class DataVisualizeConfigHelper:
    EMOTIONS_BASED_ON_POSITIVITY = dict(
        positive=[
            FaceEmotion.HAPPY.value,
            FaceEmotion.NEUTRAL.value,
            FaceEmotion.SURPRISE.value
        ],
        negative=[
            FaceEmotion.ANGER.value,
            FaceEmotion.CONTEMPT.value,
            FaceEmotion.DISGUST.value,
            FaceEmotion.FEAR.value,
            FaceEmotion.SAD.value
        ]
    )
    BAR_COLOR = "blue"
    PIE_CHART_POS_SEGMENT_COLOR = "#3732c2"
    PIE_CHART_NEG_SEGMENT_COLOR = "#c23239"
    PIE_CHART_FONT_SIZE = 12
    BAR_CHART_TITLE = "Overall Face Emotion Distribution"
    BAR_CHART_X_AXIS_NAME = "emotion"
    BAR_CHART_Y_AXIS_NAME = "frequency"
    PIE_CHART_TITLE = "Face Emotion Distribution based on Positivity"
    IMAGE_RESOLUTION = (450, 360)
