class ImageProcessingHelper:
    @staticmethod
    def calculate_fps(pre_frame_time: float, new_frame_time: float) -> int:
        return int(1 / (new_frame_time - pre_frame_time))
