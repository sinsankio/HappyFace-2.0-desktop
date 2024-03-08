class WorkEmotion:
    def __init__(self):
        self.__emotion = None
        self.__positivity = None

    @property
    def emotion(self):
        return self.__emotion

    @emotion.setter
    def emotion(self, emotion: str):
        self.__emotion = emotion

    @property
    def positivity(self):
        return self.__positivity

    @positivity.setter
    def positivity(self, positivity: int):
        self.__positivity = bool(positivity)

    def to_work_emotion(self, work_emotion_result: tuple):
        self.emotion = work_emotion_result[0].decode()
        self.positivity = work_emotion_result[1]
