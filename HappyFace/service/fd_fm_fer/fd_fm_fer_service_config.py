import cv2


class FdFmFerServiceConfig:
    MIN_FACE_EMOTION_CONF = 80
    MIN_FACE_MATCH_CONF = 50
    MIN_DB_ENTRY_DELAY_SECS = 5
    WINDOW_RESOLUTION = (750, 600)
    TEXT_ORG = (645, 32)
    TEXT_COLOR = (0, 0, 255)
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.6
    LINE_THICKNESS = 2
    PAUSE_KEY_COMPOSITION = {ord('p'), ord('p')}
    EXIT_KEY_COMPOSITION = {ord('q'), ord('Q')}
    WINDOW_TITLE = "[LIVE] Subject Face Analysis"
