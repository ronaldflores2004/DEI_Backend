from pydantic import BaseModel


class NotificationReadResponse(BaseModel):

    id: int

    is_read: bool

    class Config:
        from_attributes = True