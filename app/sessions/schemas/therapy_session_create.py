from datetime import datetime

from pydantic import BaseModel, Field


class TherapySessionCreate(BaseModel):

    patient_id: int = Field(gt=0)

    session_date: datetime