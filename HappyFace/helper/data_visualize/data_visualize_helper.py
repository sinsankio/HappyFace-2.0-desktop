import io

import cv2
import matplotlib.pyplot as plt
import numpy as np

from helper.data_visualize.data_visualize_config_helper import DataVisualizeConfigHelper
from helper.face_emotion.face_emotion_config_helper import FaceEmotionConfigHelper
from service.fd_fm_fer.fd_fm_fer_service_config import FdFmFerServiceConfig
from service.model.entry_service import EntryService


class DataVisualizeHelper:

    @staticmethod
    def plt_to_opencv_img(plot) -> np.ndarray:
        buffer = io.BytesIO()

        plot.savefig(buffer, format="png", bbox_inches='tight', pad_inches=0.01)
        buffer.seek(0)

        plt_image = np.asarray(bytearray(buffer.read()), dtype=np.uint8)
        plt_opencv_image = cv2.imdecode(plt_image, cv2.IMREAD_COLOR)
        return cv2.resize(plt_opencv_image, DataVisualizeConfigHelper.IMAGE_RESOLUTION)

    @staticmethod
    def get_overall_emotion_distribution(entry_service: EntryService) -> np.ndarray:
        entries = entry_service.read_entries()
        available_emotions = tuple(FaceEmotionConfigHelper.LABEL_CLASSES.values())
        emotion_distribution_count = {emotion: 0 for emotion in available_emotions}

        for entry in entries:
            work_emotion = entry.work_emotion

            if work_emotion.probability >= FdFmFerServiceConfig.MIN_FACE_EMOTION_CONF:
                emotion_distribution_count[work_emotion.emotion] += 1

        figure, axis = plt.subplots()

        axis.bar(
            available_emotions,
            tuple(emotion_distribution_count.values()),
            color=DataVisualizeConfigHelper.BAR_COLOR
        )
        plt.title(DataVisualizeConfigHelper.BAR_CHART_TITLE)
        plt.xlabel(DataVisualizeConfigHelper.BAR_CHART_X_AXIS_NAME)
        plt.ylabel(DataVisualizeConfigHelper.BAR_CHART_Y_AXIS_NAME)
        return DataVisualizeHelper.plt_to_opencv_img(plt)

    @staticmethod
    def get_emotion_distribution_based_on_positivity(entry_service: EntryService) -> np.ndarray:
        entries = entry_service.read_entries()
        emotions_based_on_positivity = DataVisualizeConfigHelper.EMOTIONS_BASED_ON_POSITIVITY
        pos_neg_emotion_distribution_count = dict(positive=0, negative=0)

        for entry in entries:
            work_emotion = entry.work_emotion

            if work_emotion.probability >= FdFmFerServiceConfig.MIN_FACE_EMOTION_CONF:
                if work_emotion.emotion in emotions_based_on_positivity["positive"]:
                    pos_neg_emotion_distribution_count["positive"] += 1
                else:
                    pos_neg_emotion_distribution_count["negative"] += 1

        values = [pos_neg_emotion_distribution_count["positive"], pos_neg_emotion_distribution_count["negative"]]

        if values[0] > 0 or values[1] > 0:
            figure, axis = plt.subplots()
            labels = ["positive", "negative"]

            axis.pie(
                values,
                colors=[
                    DataVisualizeConfigHelper.PIE_CHART_POS_SEGMENT_COLOR,
                    DataVisualizeConfigHelper.PIE_CHART_NEG_SEGMENT_COLOR
                ],
                labels=labels,
                autopct='%1.1f%%',
                startangle=90,
                textprops={'fontsize': DataVisualizeConfigHelper.PIE_CHART_FONT_SIZE}
            )
            axis.axis("equal")
            plt.tight_layout()
            plt.title(DataVisualizeConfigHelper.PIE_CHART_TITLE)
            return DataVisualizeHelper.plt_to_opencv_img(plt)
