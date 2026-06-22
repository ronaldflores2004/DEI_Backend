from datetime import datetime

from pydantic import BaseModel


class TherapySessionCreate(BaseModel):

    patient_id: int

    session_date: datetime