from datetime import datetime

from pydantic import BaseModel


class PatientRecommendationResponse(BaseModel):

    id: int

    patient_id: int

    title: str

    content: str

    source: str

    created_at: datetime

    class Config:
        from_attributes = True