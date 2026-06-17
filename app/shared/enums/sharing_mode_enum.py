from enum import Enum


class SharingModeEnum(str, Enum):
    FULL_HISTORY = "FULL_HISTORY"
    FROM_DATE = "FROM_DATE"
    NEW_ONLY = "NEW_ONLY"