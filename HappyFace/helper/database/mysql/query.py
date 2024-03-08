from enum import Enum


class Query(Enum):
    ENTRY_INSERT = "INSERT INTO `entry` (`repo_id`) VALUES (%s);"
    ENTRY_READ_ONE = "SELECT * FROM `entry` WHERE `repo_id`=%s;"
    ENTRY_READ_ALL = "SELECT * FROM `entry`;"
    ENTRY_UPDATE = "UPDATE `entry` SET `repo_id`=%s WHERE `repo_id`=%s;"
    ENTRY_DELETE = "DELETE FROM `entry` WHERE 1;"

    ENTRY_WORK_EMOTION_INSERT = "INSERT INTO `entry_work_emotion` (`repo_id`, `emotion`, `emotion_prob`) VALUES (%s, %s, %s);"
    ENTRY_WORK_EMOTION_READ_ALL = "SELECT * FROM `entry_work_emotion` WHERE `repo_id`=%s;"
    ENTRY_WORK_EMOTION_UPDATE = "UPDATE `entry_work_emotion` SET `repo_id`=%s,`emotion`=%s,`emotion_prob`=%s," \
                                "`recorded_on`=%s WHERE `repo_id`=%s;"
    ENTRY_WORK_EMOTION_DELETE = "DELETE FROM `entry_work_emotion` WHERE 1;"

    WORK_EMOTION_INSERT = "INSERT INTO `work_emotion` VALUES (%s, %s);"
    WORK_EMOTION_READ_ONE = "SELECT * FROM `work_emotion` WHERE `emotion`=%s;"
    WORK_EMOTION_READ_ALL = "SELECT * FROM `work_emotion`;"
    WORK_EMOTION_UPDATE = "UPDATE `work_emotion` SET `emotion`=%s,`positivity`=%s WHERE `emotion`=%s;"
    WORK_EMOTION_DELETE = "DELETE FROM `work_emotion` WHERE 1;"

