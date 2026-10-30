from datetime import datetime

from pydantic import BaseModel

from app.shared.enums.recommendation_status_enum import (
    RecommendationStatusEnum
)


class PatientRecommendationResponse(BaseModel):

    id: int

    patient_id: int

    title: str

    # None mientras espera la revisión del profesional.
    content: str | None

    source: str

    status: RecommendationStatusEnum

    created_at: datetime

    class Config:
        from_attributes = True


class RecommendationReviewResponse(PatientRecommendationResponse):

    analysis_id: int

    reviewed_at: datetime | None
