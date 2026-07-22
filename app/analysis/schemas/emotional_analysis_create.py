from pydantic import BaseModel

from app.shared.enums.emotion_intensity_enum import (
    EmotionIntensityEnum
)

from app.shared.enums.risk_level_enum import (
    RiskLevelEnum
)

class EmotionalAnalysisCreate(BaseModel):

    primary_emotion: str

    emotion_intensity: EmotionIntensityEnum

    risk_level: RiskLevelEnum

    analysis_json: dict