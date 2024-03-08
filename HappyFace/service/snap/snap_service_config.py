import cv2


class SnapServiceConfig:
    WINDOW_RESOLUTION = (600, 600)
    TEXT_ORG = (10, 20)
    TEXT_COLOR = (0, 255, 0)
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.6
    LINE_THICKNESS = 2
    WINDOW_TITLE = "[LIVE] Subject Snap Collection"
