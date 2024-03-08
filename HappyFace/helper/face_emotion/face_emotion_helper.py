import cv2
import numpy as np
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.models import Sequential
from keras.optimizers import Adam
from keras.regularizers import l2

from helper.face_emotion.face_emotion_config_helper import FaceEmotionConfigHelper


class FaceEmotionHelper:
    fer_model = None

    @staticmethod
    def load_model() -> None:
        model = Sequential()

        model.add(Conv2D(64, (3, 3), activation='relu', padding='same', kernel_regularizer=l2(1e-7),
                         kernel_initializer='he_uniform', name='block1_conv1', input_shape=(48, 48, 1)))
        model.add(Conv2D(64, (3, 3), activation='relu', padding='same', kernel_regularizer=l2(1e-7),
                         kernel_initializer='he_uniform', name='block1_conv2'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='block1_maxpool'))

        model.add(Conv2D(128, (3, 3), activation='relu', padding='same', kernel_regularizer=l2(1e-7),
                         kernel_initializer='he_uniform', name='block2_conv1'))
        model.add(Conv2D(128, (3, 3), activation='relu', padding='same', kernel_regularizer=l2(1e-7),
                         kernel_initializer='he_uniform', name='block2_conv2'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='block2_maxpool'))

        model.add(Conv2D(256, (3, 3), activation='relu', padding='same', kernel_regularizer=l2(1e-7),
                         kernel_initializer='he_uniform', name='block3_conv1'))
        model.add(Conv2D(256, (3, 3), activation='relu', padding='same', kernel_regularizer=l2(1e-7),
                         kernel_initializer='he_uniform', name='block3_conv2'))
        model.add(Conv2D(256, (3, 3), activation='relu', padding='same', kernel_regularizer=l2(1e-7),
                         kernel_initializer='he_uniform', name='block3_conv3'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='block3_maxpool'))

        model.add(Conv2D(512, (3, 3), activation='relu', padding='same', kernel_regularizer=l2(1e-7),
                         kernel_initializer='he_uniform', name='block4_conv1'))
        model.add(Conv2D(512, (3, 3), activation='relu', padding='same', kernel_regularizer=l2(1e-7),
                         kernel_initializer='he_uniform', name='block4_conv2'))
        model.add(Conv2D(512, (3, 3), activation='relu', padding='same', kernel_regularizer=l2(1e-7),
                         kernel_initializer='he_uniform', name='block4_conv3'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='block4_maxpool'))

        model.add(Conv2D(512, (3, 3), activation='relu', padding='same', kernel_regularizer=l2(1e-7),
                         kernel_initializer='he_uniform', name='block5_conv1'))
        model.add(Conv2D(512, (3, 3), activation='relu', padding='same', kernel_regularizer=l2(1e-7),
                         kernel_initializer='he_uniform', name='block5_conv2'))
        model.add(Conv2D(512, (3, 3), activation='relu', padding='same', kernel_regularizer=l2(1e-7),
                         kernel_initializer='he_uniform', name='block5_conv3'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='block5_maxpool'))

        model.add(Flatten())
        model.add(Dense(4096, kernel_regularizer=l2(1e-7), activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(4096, kernel_regularizer=l2(1e-7), activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(8, activation='softmax'))

        model.compile(optimizer=Adam(learning_rate=0.0002), loss='categorical_crossentropy', metrics=['accuracy'])
        model.load_weights(FaceEmotionConfigHelper.MODEL_FILE_PATH)

        FaceEmotionHelper.fer_model = model

    @staticmethod
    def get_emotions(face: np.ndarray) -> tuple:
        if not FaceEmotionHelper.fer_model:
            FaceEmotionHelper.load_model()

        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        face = cv2.resize(face, FaceEmotionConfigHelper.RESIZE_DIM)
        face = face / 255.0
        face = np.reshape(face, (1, face.shape[0], face.shape[1], 1))
        probabilities = FaceEmotionHelper.fer_model.predict(face)
        emotions = []

        for index, probability in enumerate(probabilities[0]):
            probability = round(probability * 100, 2)
            emotion = dict(
                emotion=FaceEmotionConfigHelper.LABEL_CLASSES[index],
                probability=probability
            )
            emotions.append(emotion)
        return tuple(emotions)
