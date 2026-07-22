from datetime import datetime

from pydantic import BaseModel

from app.shared.enums.emotion_intensity_enum import (
    EmotionIntensityEnum
)

from app.shared.enums.risk_level_enum import (
    RiskLevelEnum
)

class EmotionalAnalysisResponse(BaseModel):

    id: int

    entry_id: int

    primary_emotion: str | None

    emotion_intensity: EmotionIntensityEnum | None

    risk_level: RiskLevelEnum | None

    provider: str

    model: str

    analysis_json: dict

    analyzed_at: datetime

    class Config:
        from_attributes = True