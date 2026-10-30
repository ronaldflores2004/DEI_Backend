from enum import Enum


class RiskAlertStatusEnum(str, Enum):
    NEW = "NEW"
    SEEN = "SEEN"
    RESOLVED = "RESOLVED"
