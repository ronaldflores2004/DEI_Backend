from datetime import datetime

from pydantic import BaseModel


class LinkRequestResponse(BaseModel):

    id: int

    patient_id: int
    professional_id: int

    status: str

    sharing_mode: str

    share_from: datetime | None

    created_at: datetime

    class Config:
        from_attributes = True