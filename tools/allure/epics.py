from enum import Enum


class AllureEpic(str, Enum):
    LMS = 'LMS'
    STUDENT = 'Student service'
    ADMINISTRATOR = 'Administrator service'