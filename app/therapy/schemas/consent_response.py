from datetime import datetime

from pydantic import BaseModel


class ConsentResponse(BaseModel):

    id: int

    patient_id: int
    professional_id: int

    granted: bool

    granted_at: datetime

    class Config:
        from_attributes = True