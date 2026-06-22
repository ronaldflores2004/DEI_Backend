from pydantic import BaseModel


class NotificationSummaryResponse(BaseModel):

    total: int

    unread: int