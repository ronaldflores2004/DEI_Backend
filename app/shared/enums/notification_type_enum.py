from enum import Enum


class NotificationTypeEnum(str, Enum):
    SESSION = "SESSION"
    RISK_ALERT = "RISK_ALERT"
