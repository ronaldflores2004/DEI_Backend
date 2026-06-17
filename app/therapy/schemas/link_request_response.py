from datetime import datetime

from pydantic import BaseModel


class LinkRequestResponse(BaseModel):

    id: int

    patient_id: int
    professional_id: int

    status: str

    created_at: datetime

    class Config:
        from_attributes = True