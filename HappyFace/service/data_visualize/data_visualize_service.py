import numpy as np

from helper.data_visualize.data_visualize_helper import DataVisualizeHelper
from service.model.entry_service import EntryService


class DataVisualizeService:
    def __init__(self, data_visualize_helper: DataVisualizeHelper, entry_service: EntryService):
        self.__data_visualize_helper = data_visualize_helper
        self.__entry_service = entry_service

    @property
    def data_visualize_helper(self) -> DataVisualizeHelper:
        return self.__data_visualize_helper

    @data_visualize_helper.setter
    def data_visualize_helper(self, data_visualize_helper: DataVisualizeHelper) -> None:
        self.__data_visualize_helper = data_visualize_helper

    @property
    def entry_service(self) -> EntryService:
        return self.__entry_service

    @entry_service.setter
    def entry_service(self, entry_service: EntryService) -> None:
        self.__entry_service = entry_service

    def generate_overall_emotion_distribution_summary(self) -> np.ndarray:
        return self.data_visualize_helper.get_overall_emotion_distribution(self.entry_service)

    def generate_emotion_distribution_summary_based_on_positivity(self) -> np.ndarray:
        return self.data_visualize_helper.get_emotion_distribution_based_on_positivity(
            self.entry_service
        )
