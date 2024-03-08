import os

import cv2
import numpy as np
import face_recognition


class FaceMatchHelper:
    @staticmethod
    def get_face_encodings(face: np.ndarray) -> np.ndarray | None:
        if face_encodings := face_recognition.face_encodings(face):
            return face_encodings[0]

    @staticmethod
    def match(subject_snap_save_dir: str, face: np.ndarray) -> dict[str: str | int] | None:
        subject_dirs = os.listdir(subject_snap_save_dir)
        subject_dir_avg_accuracies = {sub_dir: 0 for sub_dir in subject_dirs}

        for directory in subject_dirs:
            subject_dir_path = os.path.join(subject_snap_save_dir, directory)
            subject_dir_img_files = os.listdir(subject_dir_path)
            subject_dir_total_img_file_count = 0
            subject_dir_total_match_accuracy = 0

            for img_file in subject_dir_img_files:
                subject_dir_img_file_path = os.path.join(subject_dir_path, img_file)
                face_to_be_compared = cv2.imread(subject_dir_img_file_path)
                face_to_compare_enc = FaceMatchHelper.get_face_encodings(face)
                face_to_be_compared_enc = FaceMatchHelper.get_face_encodings(face_to_be_compared)

                if (face_to_compare_enc is not None and face_to_be_compared_enc is not None and
                        face_recognition.compare_faces([face_to_compare_enc], face_to_be_compared_enc)[0]):
                    face_distance = face_recognition.face_distance([face_to_compare_enc], face_to_be_compared_enc)
                    face_distance = round(face_distance[0] * 100, 2)
                    match_accuracy = round(100 - face_distance, 2)
                    subject_dir_total_match_accuracy += match_accuracy
                    subject_dir_total_img_file_count += 1

            if subject_dir_total_img_file_count > 0:
                subject_dir_avg_accuracies[directory] = round(
                    subject_dir_total_match_accuracy / subject_dir_total_img_file_count,
                    2
                )

        best_matching_dir_id = max(subject_dir_avg_accuracies, key=subject_dir_avg_accuracies.get)
        best_matching_prob = subject_dir_avg_accuracies[best_matching_dir_id]

        if best_matching_prob <= 0:
            best_matching_dir_id = "[NO_MATCH]"

        return dict(
            directory_id=best_matching_dir_id,
            probability=best_matching_prob
        )
