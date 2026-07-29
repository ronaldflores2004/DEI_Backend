from pydantic import BaseModel, Field

from app.shared.enums.emotion_intensity_enum import (
    EmotionIntensityEnum
)

from app.shared.enums.risk_level_enum import (
    RiskLevelEnum
)

class EmotionalAnalysisCreate(BaseModel):

    primary_emotion: str = Field(
        min_length=1,
        max_length=100
    )

    emotion_intensity: EmotionIntensityEnum

    risk_level: RiskLevelEnum

    analysis_json: dict