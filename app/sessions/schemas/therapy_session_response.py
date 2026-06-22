from datetime import datetime

from pydantic import BaseModel


class TherapySessionResponse(BaseModel):

    id: int

    patient_id: int

    professional_id: int

    session_date: datetime

    status: str

    class Config:
        from_attributes = True